import re

# Unicode symbol  → ISO-4217 code
SYM2CUR = {
    "$": "USD",        # or many others; resolved later
    "₹": "INR",
    "€": "EUR",
    "£": "GBP",
    "¥": "JPY",  "￥": "JPY",
    "₩": "KRW",
    "₽": "RUB",
    "₴": "UAH",
    "₦": "NGN",
    "₫": "VND",
    "₪": "ILS",
    "฿": "THB",
    "₱": "PHP",
    "₲": "PYG",
    "₵": "GHS",
    "₡": "CRC",
    "₭": "LAK",
    "₮": "MNT",
    "₺": "TRY",
    "₸": "KZT",
    "₼": "AZN",
    "₾": "GEL",
    "₸": "KZT",
    "R": "ZAR",
    "د.إ": "AED",      # Arabic symbols
    "د.ك": "KWD",
    "ر.س": "SAR",
    "ر.ع.": "OMR",
    "ر.ق": "QAR",
    "лв": "BGN",
    "zł": "PLN",
    "kr": "SEK",       # will refine below
    "Kč": "CZK",
    "Ft": "HUF",
    "₺": "TRY",
    "ƒ": "ANG",
    "RM": "MYR",
    "S/": "PEN",
    "R$": "BRL",
    "A$": "AUD",
    "C$": "CAD",
    "NZ$": "NZD",
    "HK$": "HKD",
    "SG$": "SGD",
    "MX$": "MXN",
    "CA$": "CAD",
}

# Extra patterns like “USD 1,299.99”
ISO3 = r"([A-Z]{3})\s?"

def to_float(txt: str) -> float:
    """'₹ 89,999' → 89999.0  |  'USD 1,299.99' → 1299.99"""
    num = re.sub(r"[^\d.,]", "", txt).replace(",", "")
    try:
        return float(num)
    except ValueError:
        return 0.0

def detect_currency(txt: str, fallback="USD"):
    """
    >>> detect_currency("₹ 89,999")   → 'INR'
    >>> detect_currency("USD 1299")   → 'USD'
    >>> detect_currency("kr 999")     → 'SEK'  (defaults, see map below)
    """
    # 1) ISO-4217 prefix
    m = re.match(ISO3, txt)
    if m:
        return m.group(1)

    # 2) Symbol lookup (longest first for “HK$”, “NZ$”, …)
    for sym in sorted(SYM2CUR, key=len, reverse=True):
        if txt.strip().startswith(sym):
            code = SYM2CUR[sym]
            # ambiguous “$”, “kr”
            if code == "USD" and "MX$" in txt: return "MXN"
            if code == "USD" and "CA$" in txt: return "CAD"
            if code == "USD" and "A$"  in txt: return "AUD"
            if code == "SEK" and "DKK" in txt: return "DKK"
            return code
    return fallback
