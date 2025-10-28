from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "HyperLaunch - Backend"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./dev.db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
