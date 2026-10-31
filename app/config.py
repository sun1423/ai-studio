from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Studio"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    app_username: str = "admin"
    app_password: str = ""
    data_dir: Path = Path("./data")
    max_upload_mb: int = 250
    min_free_disk_gb: int = 5
    comfyui_url: str = "http://127.0.0.1:8188"
    text_model_url: str = "http://127.0.0.1:11434"
    chatterbox_command: str = ""
    openvoice_command: str = ""
    telegram_bot_token: str = ""
    telegram_allowed_user_ids: str = ""
    playcon_base_url: str = ""
    playcon_api_token: str = ""


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    (settings.data_dir / "uploads").mkdir(parents=True, exist_ok=True)
    (settings.data_dir / "outputs").mkdir(parents=True, exist_ok=True)
    return settings
