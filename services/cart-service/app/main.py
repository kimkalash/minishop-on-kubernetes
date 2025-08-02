# app/main.py

from fastapi import FastAPI
from app.routes import router as cart_router  # Import the router from routes.py

app = FastAPI()

# Include the cart router with prefix and tags for grouping
app.include_router(cart_router, prefix="/api", tags=["cart"])

@app.get("/")
async def root():
    return {"message": "Cart Service Running"}
