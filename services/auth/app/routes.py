from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.settings import settings
from app.utils.jwt import create_access_token
from app.models import User
from app.db import get_db
from app.crud import create_user, get_user_by_username
from app.dependencies import get_current_user


router = APIRouter()

# --- PASSWORD CONTEXT --- #
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- SCHEMAS --- #
class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# --- REGISTER --- #
@router.post("/register", status_code=201)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = await create_user(db, request.username, request.password)
    return {"message": "User created", "user_id": user.id}

# --- LOGIN --- #
@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, request.username)
    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
@router.get("/me")
async def read_current_user(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email_verified": current_user.email_verified
    }
