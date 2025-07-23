from fastapi import FastAPI
from app.routes import router as auth_router
from app.settings import settings

app = FastAPI(
    title="Auth Service",
    version="1.0.0",
    description="Handles user authentication and JWT token issuance."
)

# Include auth routes (login, register, etc.)
app.include_router(auth_router, prefix="/auth")
@app.get("/")
def health_check():
    return {"status": "auth-service is running", "env": settings.database_url}

