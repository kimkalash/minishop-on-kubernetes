# app/schemas.py

from pydantic import BaseModel, conint
from typing import List, Optional


class CartItemCreate(BaseModel):
    product_id: int
    quantity: conint(gt=0)  # quantity must be an integer greater than 0


class CartItemResponse(BaseModel):
    product_id: int
    quantity: int
    name: Optional[str] = None  # Optional product name for convenience in responses
    price: Optional[float] = None  # Optional product price for client display

    class Config:
        orm_mode = True  # Allows compatibility with ORM models or dicts


class CartResponse(BaseModel):
    items: List[CartItemResponse]  # List of cart items
    total_items: int  # Total count of items in cart
    total_price: float  # Total price of all items in cart
