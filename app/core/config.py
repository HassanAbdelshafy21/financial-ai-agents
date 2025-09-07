from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

# 👇 Force load .env first, overriding system env
load_dotenv(override=True)


class Settings(BaseSettings):
    APP_ENV: str = "dev"
    SECRET_KEY: str = "change_me"
    JWT_EXPIRES_MIN: int = 60
    DB_URI: str = "mysql+aiomysql://user:pass@mysql:3306/finai"
    REDIS_URL: str = "redis://redis:6379/0"
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    FROM_EMAIL: str = ""

    # OpenAI / LangChain settings
    OPENAI_API_KEY: str | None = None
    LANGCHAIN_TRACING_V2: bool = False  # 👈 stays as a bool

    # overwrite DB_URI for docker/local dev
    DB_URI: str = "mysql+aiomysql://root:pickles@mysql:3306/finai"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# 👇 Always force .env OPENAI_API_KEY into os.environ
if settings.OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
