from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Will come from Auth service
    status = Column(String, default="pending", nullable=False)
    total_price = Column(Float, nullable=False)

    # Relationship example (future: could link to OrderItems table)
