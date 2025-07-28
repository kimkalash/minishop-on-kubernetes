from fastapi import FastAPI
from app.routes import router as catalog_router

app = FastAPI()

# Attach catalog routes
app.include_router(catalog_router, prefix="/catalog", tags=["catalog"])

@app.get("/")
def root():
    return {"message": "Catalog Service Running"}
