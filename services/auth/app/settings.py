from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_algorithm: str

    class Config:
        env_file = ".env"  # This works since .env is in the same directory as settings.py

settings = Settings()

