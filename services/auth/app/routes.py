from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.utils.jwt import create_access_token
from app.db import get_db
from app.crud import create_user, get_user_by_username
from app.dependencies import get_current_user
from app.schemas.users import UserCreate, LoginRequest, UserResponse

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", status_code=201)
async def register(request: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = await create_user(db, request.username, request.password)
    return {"message": "User created", "user_id": user.id}


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, request.username)
    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_me(current_user=Depends(get_current_user)):
    return current_user 
