from pydantic import BaseModel, Field

class PriceReq(BaseModel):
    country: str = Field(..., min_length=2, max_length=2)
    query: str

class PriceResp(BaseModel):
    link: str
    price: float
    currency: str
    productName: str
    source: str
