from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str | None = None  # Optional for now, not needed for catalog
    jwt_algorithm: str | None = None

    class Config:
        env_file = ".env"  # Load from .env file in this directory

settings = Settings()
