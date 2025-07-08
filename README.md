# PriceCompass

## Hosted API (Render)

**Test the API live:**

- [https://pricecompass.onrender.com/docs#/default/prices_prices_post](https://pricecompass.onrender.com/docs#/default/prices_prices_post)
- Endpoint: `https://pricecompass.onrender.com/prices`

## Example cURL Request

```
curl -X POST https://pricecompass.onrender.com/prices \
     -H "Content-Type: application/json" \
     -d '{"country": "US", "query": "iPhone 16 Pro, 128GB"}'
```

## Proof of Working

- ![Proof screenshot](docs/proof_screenshot.png)
- (Or attach a short video/gif of the above query returning results)

## Local Development (Docker Recommended)

1. **Clone the repo:**
   ```sh
   git clone <your-github-repo-url>
   cd pricecompass
   ```
2. **Copy `.env.example` to `.env` and fill in your API keys:**
   ```sh
   cp .env.example .env
   # Edit .env and add your SERPAPI_KEY, GEMINI_API_KEY
   ```
3. **Build and run with Docker:**
   ```sh
   docker build -t pricecompass .
   docker run --env-file .env -p 8000:8000 pricecompass
   ```
   The API will be available at `http://localhost:8000/prices`.

4. **Or run locally (Python 3.11 recommended):**
   ```sh
   pip install -r requirements.txt
   uvicorn pricecompass.main:app --reload
   ```

## Frontend (Optional)

- A Streamlit frontend is available in the `streamlit/` subfolder.
- To run locally:
  ```sh
  cd streamlit
  streamlit run streamlit_app.py
  ```
- Or deploy to Streamlit Community Cloud and set `BACKEND_URL` to your Render API.

## Testing Instructions

- Use the cURL command above or the `/docs` Swagger UI to test.
- The API must return valid results for:
  ```json
  {"country": "US", "query": "iPhone 16 Pro, 128GB"}
  ```

## Dependencies

- All dependencies are listed in `requirements.txt`.
- Dockerfile provided for reproducible builds.

---

**For any issues, please open an issue or contact the maintainer.**
