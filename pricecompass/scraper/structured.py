import json, re
from bs4 import BeautifulSoup
from pricecompass.utils.currency import to_float

def parse(html: str, base: str):
    soup = BeautifulSoup(html, "lxml")
    out = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            blob = json.loads(tag.string)
        except:
            continue
        nodes = blob if isinstance(blob, list) else [blob]
        for n in nodes:
            if n.get("@type") != "Product":
                continue
            offers = n.get("offers") or {}
            if not offers.get("price"):
                continue
            out.append(dict(
                productName=n.get("name"),
                price=float(offers["price"]),
                currency=offers.get("priceCurrency", "USD"),
                link=offers.get("url", base)
            ))
    return out[:40] 