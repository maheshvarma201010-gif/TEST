import os
import sys
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Credentials
    API_ID: int
    API_HASH: str
    BOT_TOKEN: str

    # Database
    MONGO_URI: str = "mongodb://localhost:27017/scraper_bot"
    DB_NAME: str = "scraper_bot"

    # Access Control
    ADMIN_IDS: List[int] = Field(default_factory=list)

    # Server Configuration
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # Bot Session
    SESSION_NAME: str = "scraper_bot"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @classmethod
    def from_env(cls):
        # Handle comma separated ADMIN_IDS in env
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        if admin_ids_str:
            try:
                admin_ids = [int(i.strip()) for i in admin_ids_str.split(",") if i.strip()]
                return cls(ADMIN_IDS=admin_ids)
            except ValueError:
                # Fallback to defaults if list parsing fails
                return cls()
        return cls()

try:
    settings = Settings.from_env()
except Exception as e:
    print(f"CRITICAL: Failed to load configuration: {e}")
    print("Please check your .env file and environment variables.")
    sys.exit(1)
