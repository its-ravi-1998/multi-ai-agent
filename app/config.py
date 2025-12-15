import os
from dotenv import load_dotenv

load_dotenv()
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # Fallback for development only - should be set in production
    SECRET_KEY = "dev-secret-key-change-in-production"
    import warnings
    warnings.warn("SECRET_KEY not set in environment. Using default dev key. This is insecure for production!")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Token expiration times
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

class Settings(BaseSettings):
    """Application settings loaded from .env with sensible defaults.

    Note: Database configuration is handled directly in `app.db` to preserve
    the existing behavior of using env vars with fallbacks.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # JWT / auth
    secret_key: str | None = Field(default=None, env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    # External services
    HF_TOKEN: str | None = Field(default=None, env="HF_TOKEN")