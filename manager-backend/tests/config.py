from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="TEST_",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"

    NOTCONF_HOST: str = "notconf"
    NOTCONF_PORT: int = 830
    NOTCONF_USER: str = "admin"
    NOTCONF_PASSWORD: str = "admin"


settings = Settings()
