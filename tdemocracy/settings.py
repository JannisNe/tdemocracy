from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for tdemocracy. Per default, the values are being read from the environment as `TDEMOCRACY_<key>`, or the `tdemocracy.env` file."""

    username: str
    """Username for the Hopskotch stream"""
    password: str
    """Password for the Hopskotch stream"""
    topic: str = "Ampel-TDEmocracy.nucelar-stream-dev"
    """Hopskotch topic"""
    group_id: Any | None = None
    """Group ID when listening to the kafka stream. If None (default) a new value will be assigned with each call (good for testing). Set to a persistent <username>-<key> value to keep track of the stream position between calls (good for production)."""
    model_config = SettingsConfigDict(env_prefix="TDEMOCRACY_", env_file="tdemocracy.env")
