"""Project settings."""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment or default values."""

    root_dir: Path = Path(__file__).parent.parent.parent.resolve()
    sales_data: Path = root_dir / "sales_data.csv"

    class Config:
        env_file = ".env"  # Optional: Load settings from a .env file
        env_file_encoding = "utf-8"


settings = Settings()