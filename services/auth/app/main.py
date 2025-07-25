from fastapi import FastAPI
from app.routes import router as auth_router

app = FastAPI()

# ✅ Attach your routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return {"message": "Auth Service Running"}
