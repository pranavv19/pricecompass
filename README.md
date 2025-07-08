# PriceCompass

## Setup

1. Copy `.env.example` to `.env` and fill in your API keys (AWS, eBay, MELI, CJ, etc).
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the ETL

Run the nightly ETL script to download affiliate feeds and build the index:
```sh
python scripts/nightly_etl.py
```

## Running the API

Start the FastAPI server:
```sh
uvicorn pricecompass.main:app --reload
```

## Querying Prices

POST to `/prices` with a JSON body:
```json
{
  "country": "IN",
  "query": "iPhone 15 Pro"
}
```

## Data
- Affiliate feeds and the index are stored in `data/feeds/` (ignored by git).
