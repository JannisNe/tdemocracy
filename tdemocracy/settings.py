from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    username: str
    password: str
    topic: str = "Ampel-TDEmocracy.nucelar-stream-dev"
    group_id: Any | None = None
    model_config = SettingsConfigDict(env_prefix="TDEMOCRACY_", env_file="tdemocracy.env")
