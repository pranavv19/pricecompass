import streamlit as st
import requests, os

# Safely get BACKEND_URL from st.secrets, then env, then fallback
if "BACKEND_URL" in st.secrets:
    BACKEND = st.secrets["BACKEND_URL"]
elif os.getenv("BACKEND_URL"):
    BACKEND = os.getenv("BACKEND_URL")
else:
    BACKEND = "https://pricecompass.onrender.com"

st.set_page_config(page_title="PriceCompass", layout="wide")
st.title("🧭 PriceCompass: Global Price Comparison")

COUNTRIES = [
    ("US", "United States"), ("IN", "India"), ("JP", "Japan"), ("DE", "Germany"), ("GB", "United Kingdom"),
    ("FR", "France"), ("IT", "Italy"), ("CA", "Canada"), ("KR", "South Korea"), ("RU", "Russia"),
    ("BR", "Brazil"), ("AU", "Australia"), ("ES", "Spain"), ("MX", "Mexico"), ("CN", "China"),
    ("TR", "Turkey"), ("ID", "Indonesia"), ("SA", "Saudi Arabia"), ("CH", "Switzerland"), ("NL", "Netherlands"),
    ("AR", "Argentina"), ("SE", "Sweden"), ("PL", "Poland"), ("BE", "Belgium"), ("TH", "Thailand"),
    ("NG", "Nigeria"), ("EG", "Egypt"), ("PK", "Pakistan"), ("VN", "Vietnam"), ("ZA", "South Africa")
]

st.sidebar.header("Search Settings")
country = st.sidebar.selectbox("Country", options=[c[0] for c in COUNTRIES], format_func=lambda x: dict(COUNTRIES)[x])
query = st.sidebar.text_input("Product Query", "")

if st.sidebar.button("Search"):
    if not query.strip():
        st.warning("Enter a product name.")
    else:
        with st.spinner("Searching…"):
            try:
                r = requests.post(
                    f"{BACKEND}/prices",
                    json={"country": country, "query": query},
                    timeout=40,
                )
                r.raise_for_status()
                rows = r.json()
                if not rows:
                    st.info("No exact-match offers found.")
                else:
                    st.success(f"{len(rows)} offers found")
                    st.dataframe(
                        [{
                            "Product":  x["productName"],
                            "Price":    x["price"],
                            "Currency": x["currency"],
                            "Source":   x["source"],
                            "Link":     x["link"],
                        } for x in rows],
                        use_container_width=True,
                    )
            except Exception as e:
                st.error(f"API error: {e}")
else:
    st.info("Fill in a query and click **Search**.") 