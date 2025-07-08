import re

def to_float(value: str) -> float:
    # Remove currency symbols and commas
    value = re.sub(r'[^\d.]', '', value.replace(',', ''))
    try:
        return float(value)
    except ValueError:
        return 0.0
