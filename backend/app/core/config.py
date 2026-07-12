from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./transitops.db"
    SECRET_KEY: str = "change_this_secret_key"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()