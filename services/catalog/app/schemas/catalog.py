# services/catalog/app/schemas/catalog.py

from pydantic import BaseModel
from typing import Optional

# Schema for creating a new product
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: Optional[int] = 0


# Schema for updating an existing product
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


# Schema for returning product data to clients
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int

    class Config:
        from_attributes = True  # Allows ORM objects to be converted to this schema
