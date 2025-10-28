from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True   # correct field name
    MAIL_SSL_TLS: bool = False   # correct field name

    class Config:
        env_file = ".env"
        extra = "ignore"
        
settings = Settings()
