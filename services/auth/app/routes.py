from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.settings import settings
from app.utils.jwt import create_access_token

router = APIRouter()

# Request body for login
class LoginRequest(BaseModel):
    username: str
    password: str

# Dummy user database (for now)
fake_users = {
    "admin": {"username": "admin", "password": "admin123"}
}

@router.post("/login")
def login(request: LoginRequest):
    user = fake_users.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub": request.username})
    return {"access_token": token, "token_type": "bearer"}
