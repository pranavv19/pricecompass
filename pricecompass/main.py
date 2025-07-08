from fastapi import FastAPI, HTTPException
from pricecompass.models import PriceReq, PriceResp
from pricecompass.orchestrator import fetch_prices

app = FastAPI(title="PriceCompass")

@app.post("/prices", response_model=list[PriceResp])
async def prices(body: PriceReq):
    try:
        return await fetch_prices(body.country.upper(), body.query)
    except ValueError as e:
        raise HTTPException(400, str(e))
