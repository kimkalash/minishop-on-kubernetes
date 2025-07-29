from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    user_id: int
    total_price: float
    status: Optional[str] = "pending"

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    total_price: Optional[float] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total_price: float

    class Config:
        from_attributes = True
