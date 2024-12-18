"""Project settings."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment or default values."""

    root_dir: Path = Path(__file__).parent.parent.parent.resolve()
    sales_data: Path = root_dir / "sales_data.csv"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
