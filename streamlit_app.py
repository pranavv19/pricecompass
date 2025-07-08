import streamlit as st
import requests

st.set_page_config(page_title="PriceCompass", layout="wide")
st.title("🧭 PriceCompass: Global Price Comparison")

COUNTRIES = [
    ("US", "United States"), ("IN", "India"), ("JP", "Japan"), ("DE", "Germany"), ("GB", "United Kingdom"),
    ("FR", "France"), ("IT", "Italy"), ("CA", "Canada"), ("KR", "South Korea"), ("RU", "Russia"),
    ("BR", "Brazil"), ("AU", "Australia"), ("ES", "Spain"), ("MX", "Mexico"), ("CN", "China")
]

st.sidebar.header("Search Settings")
country = st.sidebar.selectbox("Country", options=[c[0] for c in COUNTRIES], format_func=lambda x: dict(COUNTRIES)[x])
query = st.sidebar.text_input("Product Query", "")

if st.sidebar.button("Search"):
    with st.spinner("Searching prices..."):
        try:
            resp = requests.post(
                "http://localhost:8000/prices",
                json={"country": country, "query": query},
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            if not data:
                st.warning("No results found.")
            else:
                st.success(f"Found {len(data)} offers.")
                st.dataframe([
                    {
                        "Product": d["productName"],
                        "Price": d["price"],
                        "Currency": d["currency"],
                        "Source": d["source"],
                        "Link": d["link"]
                    } for d in data
                ], use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Enter a product and click Search.") 