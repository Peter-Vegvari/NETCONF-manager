from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NETCONF-manager"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    FRONTEND_HOST: str = "http://localhost:3000"
    DOWNLOADED_MODULES_PATH: Path = Path("../resources/downloaded-modules")

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TEST_",
        env_ignore_empty=True,
        extra="ignore",
    )

    NOTCONF_HOST: str = "notconf"
    NOTCONF_PORT: int = 830
    NOTCONF_USER: str = "admin"
    NOTCONF_PASSWORD: str = "admin"


settings = Settings()  # type: ignore
settings.DOWNLOADED_MODULES_PATH.mkdir(parents=True, exist_ok=True)
test_settings = TestSettings()  # type: ignore
