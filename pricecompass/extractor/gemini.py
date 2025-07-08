import os, json, re, google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_model = genai.GenerativeModel(os.getenv("MODEL_ID", "gemini-2.5-pro-exp-03-25"))

SYS = ("You are an HTML product parser. "
       "Return JSON with keys: productName, price, currency, link. "
       "If price missing, respond with null.")

def extract_listing(html: str) -> dict | None:
    try:
        resp = _model.generate_content(
            SYS + "\nHTML:\n" + html[:10_000],
            generation_config={"temperature": 0.2}
        )
    except Exception as e:
        # Optionally log e
        return None
    m = re.search(r"{.*}", resp.text, re.S)
    if not m:
        return None
    try:
        data = json.loads(m.group(0))
        return data if data.get("price") else None
    except json.JSONDecodeError:
        return None
