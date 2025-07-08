from fastapi import FastAPI
from pydantic import BaseModel
from pricecompass.orchestrator import fetch_prices

class Req(BaseModel):
    country: str
    query: str

app = FastAPI(title="2-hour Price API")

@app.post("/prices")
async def prices(body: Req):
    return await fetch_prices(body.country.upper(), body.query)
