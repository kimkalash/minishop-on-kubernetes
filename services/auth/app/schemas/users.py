from pydantic import BaseModel, EmailStr
from typing import Optional

# ✅ Schema for creating a user (input only)
class UserCreate(BaseModel):
    username: str
    password: str  # raw password
    email: EmailStr

# ✅ Schema for showing a user (response/output)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    email_verified: bool

    class Config:
        orm_mode = True  # allows SQLAlchemy model -> Pydantic conversion

# ✅ Schema for internal logic (optional: for DB-only fields)
class UserInDB(UserOut):
    hashed_password: str
