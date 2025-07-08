# pricecompass/sources/gemini_extractor.py

import os, google.generativeai as genai, json, re, pricecompass.utils.currency as cur
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

SYS = ("You are an HTML product parser. "
       "Return JSON with keys productName, price, currency, link. "
       "Respond ONLY with the JSON object.")

def extract(html_snippet: str):
    resp = model.generate_content(SYS + "\nHTML:\n" + html_snippet[:7000],
                                  generation_config={"temperature":0.2})
    m = re.search(r"\{.*\}", resp.text, re.S)
    if not m: return None
    try:
        d = json.loads(m.group(0))
        d["price"] = cur.to_float(str(d.get("price", "")))
        return d if d["price"] else None
    except json.JSONDecodeError:
        return None 

def validate_results(query: str, results: list) -> list:
    """
    Send the query and all SerpAPI results to Gemini, asking if each result matches the query.
    Returns a list of booleans (or filtered results).
    """
    if not results:
        return []
    prompt = (
        "You are a product search validator. "
        "Given a user query and a list of product results (with name, price, currency, link), "
        "for each result, answer YES if it matches the query, NO if not. "
        "Respond with a JSON list of 'YES' or 'NO' for each result, in order.\n"
        f"Query: {query}\n"
        f"Results: {json.dumps([{'productName': r.get('productName'), 'price': r.get('price'), 'currency': r.get('currency'), 'link': r.get('link')} for r in results])}"
    )
    resp = model.generate_content(prompt, generation_config={"temperature":0.1})
    m = re.search(r"\[.*\]", resp.text, re.S)
    if not m:
        return [True] * len(results)  # fallback: allow all
    try:
        verdicts = json.loads(m.group(0))
        return [v.strip().upper() == "YES" for v in verdicts]
    except Exception:
        return [True] * len(results) 