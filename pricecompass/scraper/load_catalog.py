import os, yaml

CATALOG_DIR = os.path.join(os.path.dirname(__file__), "site_catalog")

def load_sites(country: str) -> list:
    path = os.path.join(CATALOG_DIR, f"{country.upper()}.yml")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or [] 