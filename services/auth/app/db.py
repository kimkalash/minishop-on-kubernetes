from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.settings import settings

# Create async engine using database URL from .env
engine = create_async_engine(settings.database_url, echo=True)

# Create session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models to inherit from
Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session
