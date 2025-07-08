
import os, httpx, asyncio, urllib.parse as up
from dotenv import load_dotenv
from pricecompass.utils.currency import to_float, detect_currency

load_dotenv()

KEY = os.getenv("SERPAPI_KEY")
URL = "https://serpapi.com/search.json"

async def search(country: str, query: str):
    params = {
        "engine":   "google_shopping",
        "q":        query,
        "gl":       country.lower(),   # "us", "in", etc.
        "hl":       "en",
        "num":      100,
        "api_key":  KEY
    }
    async with httpx.AsyncClient() as cli:
        r = await cli.get(URL, params=params, timeout=15)
    if r.status_code != 200:
        print("SerpAPI error:", r.text)
        return []

    out = []
    for it in r.json().get("shopping_results", []):
        raw_price = it.get("price") or it.get("extracted_price")
        if not raw_price:
            continue
        price_val = to_float(str(raw_price))
        if not price_val:
            continue

        # ---- grab the best available link ----
        link = (it.get("link") or
                it.get("product_link") or
                it.get("shopping_url") or
                it.get("serpapi_product_api") or
                None)

        source = it.get("source") or (up.urlparse(link).netloc if link else "")

        # currency
        currency = detect_currency(str(raw_price), it.get("currency") or "USD")

        out.append({
            "productName": it.get("title"),
            "price":       price_val,
            "currency":    currency,
            "link":        link,
            "source":      source,
        })
    return out
