import asyncio, httpx, re
from .utils import currency as cur
from .sources import serpapi, gemini_extractor

def filter_by_gemini(query, results):
    verdicts = gemini_extractor.validate_results(query, results)
    return [r for r, v in zip(results, verdicts) if v]

async def fetch_prices(country: str, query: str):
    # Tier-A – SerpAPI Google Shopping 
    results = await serpapi.search(country, query)
    # Validate with Gemini
    results = filter_by_gemini(query, results)
    if len(results) >= 5:
        return sorted(results, key=lambda x: x["price"])[:20]

    # Tier-B – scrape top 3 organic product pages and let Gemini parse
    async with httpx.AsyncClient() as cli:
        goog = await cli.get("https://duckduckgo.com/html/",
                             params={"q": query, "kl": f"{country}-en"})
    links = re.findall(r'https?://[^"]+', goog.text)[:3]

    async def scrape(url):
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as cli:
                html = (await cli.get(url)).text
        except Exception:
            return None
        soup = BeautifulSoup(html, "lxml")
        # take first div / li containing a currency symbol
        for n in soup.find_all(["div","li","span"], limit=60):
            if re.search(r"[₹$€£]\s?\d", n.get_text()):
                parsed = gemini_extractor.extract(str(n))
                if parsed:
                    parsed["source"] = re.sub(r"^www\.","",
                                    re.sub(r"/.*","", parsed["link"]))
                    return parsed
        return None

    tasks = [scrape(u) for u in links]
    gem_results = [r for r in await asyncio.gather(*tasks) if r]

    # simple MiniLM filter for accuracy
    final = [r for r in (results + gem_results)
             if score(query, r["productName"]) > 0.80]

    return sorted(final, key=lambda x: x["price"])[:20]
