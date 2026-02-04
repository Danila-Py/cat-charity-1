from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import (
    DEFAULT_APP_TITLE,
    DEFAULT_DESCRIPTION,
    DEFAULT_DB_URL
)


class Settings(BaseSettings):
    app_title: str = DEFAULT_APP_TITLE
    description: str = DEFAULT_DESCRIPTION
    database_url: str = DEFAULT_DB_URL
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )


settings = Settings()