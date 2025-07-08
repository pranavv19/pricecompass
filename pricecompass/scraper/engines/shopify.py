from bs4 import BeautifulSoup
from pricecompass.utils.currency import to_float
from . import register

@register("shopify")
def parse(html: str, base: str):
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select("[data-product-id]")[:40] or soup.select(".grid-product")[:40]
    out = []
    for c in cards:
        title = c.get_text(" ", strip=True)
        price_tag = c.select_one(".money,.price")
        if not price_tag:
            continue
        price = to_float(price_tag.text)
        link_tag = c.select_one("a[href]")
        out.append(dict(productName=title, price=price, currency="USD",
                        link=base + link_tag["href"].split("?")[0]))
    return out 