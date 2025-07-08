import asyncio, httpx, re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from pricecompass.embeddings import embed
from pricecompass.utils.currency import to_float        # simple ₹1,299 → 1299.0
from pricecompass.utils.similarity import cosine        # already in utils
from pricecompass.scraper.detectors import detect_cms
from pricecompass.scraper.engines import get_engine     # registry dict
from pricecompass.scraper.structured import parse as parse_struct
from pricecompass.extractor.gemini import extract_listing  # LLM
# ---------------------------------------------------------------------

UA = UserAgent()

async def _get_html(url: str) -> tuple[str, dict]:
    """Single HTTP GET with timeout & fake UA; returns (html, headers)."""
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as cli:
        r = await cli.get(url, headers={"User-Agent": UA.random})
        r.raise_for_status()
        print(f"Fetched HTML from {url}:\n", r.text[:1000])  # Print first 1000 chars
        return r.text, r.headers

def _enrich(records: list[dict], site: dict) -> list[dict]:
    """Add source & embedding; clean prices to float."""
    out=[]
    for rec in records:
        try:
            rec["price"] = float(rec["price"]) if isinstance(rec["price"], (int, float)) \
                           else to_float(rec["price"])
        except Exception:
            continue
        rec["source"] = site["domain"]
        rec["embedding"] = embed(rec["productName"])
        out.append(rec)
    return out

# ------------  PUBLIC ENTRY  -------------------------------------------------
async def scrape_site(site: dict, query: str, max_nodes: int = 40) -> list[dict]:
    """
    3-tier scraper:
        1) platform engine   (Shopify, Woo…)
        2) JSON-LD Product   (structured data)
        3) Gemini LLM        (HTML → JSON)
    Returns list[dict] (may be empty).
    """
    url = site["search_url"].format(q=query)
    try:
        html, headers = await _get_html(url)
    except Exception:
        return []

    # --- Tier-1 · CMS template ---------------------------------------------
    cms = detect_cms(html, headers)
    if cms and (engine := get_engine(cms)):
        data = engine(html, base=f"https://{site['domain']}")
        if data:
            return _enrich(data, site)

    # --- Tier-2 · Structured data ------------------------------------------
    data = parse_struct(html, base=f"https://{site['domain']}")
    if data:
        return _enrich(data, site)

    # --- Tier-3 · Gemini LLM extractor -------------------------------------
    soup = BeautifulSoup(html, "lxml")
    # pick first N nodes containing a currency symbol
    candidates = [n for n in soup.find_all(["a", "div", "li"], limit=max_nodes)
                  if re.search(r"[₹$€£¥]\s?\d", n.get_text())]

    tasks = [asyncio.to_thread(extract_listing, str(n)) for n in candidates]
    llm_records = [r for r in await asyncio.gather(*tasks) if r]
    return _enrich(llm_records, site)
