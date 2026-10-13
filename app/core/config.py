import os
import warnings
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Locate .env in the ecommerce project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")


def _csv(name: str, default: str) -> list[str]:
    return [
        item.strip()
        for item in os.getenv(name, default).split(",")
        if item.strip()
    ]


@dataclass(frozen=True)
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "ShopSphere API")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./ecommerce.db"
    )

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "CHANGE_THIS_IN_PRODUCTION"
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    CORS_ORIGINS: list[str] | None = None


settings = Settings(
    CORS_ORIGINS=_csv(
        "CORS_ORIGINS",
        "http://localhost:8000"
    )
)

if settings.SECRET_KEY == "CHANGE_THIS_IN_PRODUCTION":
    warnings.warn(
        "Using development SECRET_KEY. "
        "Set SECRET_KEY in your environment before deployment."
    )