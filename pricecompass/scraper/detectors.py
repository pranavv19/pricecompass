def detect_cms(html: str, headers: dict):
    if "shopify" in html or any("shopify" in h.lower() for h in headers):
        return "shopify"
    if "woocommerce" in html or "wp-content" in html:
        return "woocommerce"
    return None 