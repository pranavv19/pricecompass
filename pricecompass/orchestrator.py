# pricecompass/orchestrator.py
import os, json, asyncio, redis.asyncio as redis
from pricecompass.scraper.load_catalog import load_sites
from pricecompass.scraper.fetcher import scrape_site
from pricecompass.embeddings import embed
from pricecompass.utils.similarity import cosine

CACHE_TTL = 60 * 60 * 12
rds = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

async def fetch_prices(country: str, query: str):
    sites = load_sites(country)
    if not sites:
        raise ValueError("Unsupported country")
    cache_key = f"{country}:{query}"
    if (cached := await rds.get(cache_key)):
        return json.loads(cached)

    tasks = [scrape_site(s, query) for s in sites]
    raw = [item for sub in await asyncio.gather(*tasks) for item in sub]
    print(f"RAW SCRAPED: {len(raw)} items: {[r.get('productName') for r in raw]}")
    qvec = embed(query)
    out = [
        {k: v for k, v in r.items() if k != "embedding"}
        for r in raw if cosine(qvec, r["embedding"]) > 0.50
    ]
    out.sort(key=lambda x: x["price"])
    await rds.set(cache_key, json.dumps(out), ex=CACHE_TTL)
    return out



