from pydantic import BaseModel

# User input when registering
class UserCreate(BaseModel):
    username: str
    password: str

# User data returned in responses (safe to expose)
class UserOut(BaseModel):
    id: int
    username: str
    email_verified: bool

    class Config:
        orm_mode = True

# Internal use (includes hashed password)
class UserInDB(UserOut):
    hashed_password: str
