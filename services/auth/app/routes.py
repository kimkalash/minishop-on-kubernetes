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

    from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import settings
from app.utils.jwt import create_access_token
from app.models import User
from app.db import get_db  # you'll create this function next
from app.crud import create_user, get_user_by_username

router = APIRouter()

# --- SCHEMAS --- #
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

# --- DUMMY LOGIN (already existing) --- #
fake_users = {
    "admin": {"username": "admin", "password": "admin123"}
}

@router.post("/login")
async def login(request: LoginRequest):
    user = fake_users.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub": request.username})
    return {"access_token": token, "token_type": "bearer"}

# --- NEW: Register endpoint --- #
@router.post("/register", status_code=201)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check if username already exists
    existing_user = await get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create the user
    user = await create_user(db, request.username, request.password)
    return {"message": "User created", "user_id": user.id}

