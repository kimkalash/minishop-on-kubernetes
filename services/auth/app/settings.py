from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./test.db"
    jwt_secret: str = "dummy-secret"
    
settings = Settings()
