# services/catalog/app/models.py
from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class Product(Base):
    __tablename__ = "products"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
