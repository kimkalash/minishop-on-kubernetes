from fastapi import FastAPI
from app.routes import router as order_router

app = FastAPI()

app.include_router(order_router, prefix="/orders", tags=["orders"])

@app.get("/")
def root():
    return {"message": "Orders Service Running"}
