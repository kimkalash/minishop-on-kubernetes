from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Create new user
async def create_user(db: AsyncSession, username: str, password: str):
    hashed_pw = hash_password(password)
    user = User(username=username, hashed_password=hashed_pw)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# Get user by username
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()
