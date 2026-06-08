from functools import lru_cache
from pathlib import Path
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OpenVoC Radar"
    database_url: str = "sqlite:///./openvoc.db"
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    slack_webhook_url: str | None = None
    lark_webhook_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("LARK_WEBHOOK_URL", "FEISHU_WEBHOOK_URL"),
    )
    dedupe_window_hours: int = 24

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def sample_csv_path(self) -> Path:
        return Path(__file__).resolve().parents[2] / "sample-data" / "tickets.csv"


@lru_cache
def get_settings() -> Settings:
    return Settings()
