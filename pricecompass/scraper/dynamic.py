from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time

_CHROME_OPTS = uc.ChromeOptions()
_CHROME_OPTS.add_argument("--headless=new")
_CHROME_OPTS.add_argument("--no-sandbox")
_CHROME_OPTS.add_argument("--disable-gpu")

def get_html(url: str, wait: float = 5) -> str:
    """Return fully-rendered HTML for JS-heavy pages."""
    drv = uc.Chrome(options=_CHROME_OPTS)
    try:
        drv.get(url)
        time.sleep(wait)                 # give SPA time to paint prices
        return drv.page_source
    finally:
        drv.quit()

def soup(url: str, wait: float = 5):
    return BeautifulSoup(get_html(url, wait), "lxml") 