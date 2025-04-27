from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    FB_APP_ID: str
    FB_APP_SECRET: str
    FRONTEND_ORIGIN: str = "https://thecove.boatable.app"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    class Config(SettingsConfigDict):
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
