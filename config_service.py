import json
from functools import lru_cache
from pathlib import Path

from fastapi import Depends

from app.config.settings import Settings, settings
from app.models.site_config import SiteConfig


class ConfigService:
    """Loads and validates site configuration from a JSON file."""

    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path

    def load(self) -> SiteConfig:
        raw = json.loads(self._config_path.read_text(encoding="utf-8"))
        return SiteConfig.model_validate(raw)


@lru_cache
def _get_config_service(config_path: str) -> ConfigService:
    return ConfigService(Path(config_path))


def get_settings() -> Settings:
    return settings


def get_config_service(
    app_settings: Settings = Depends(get_settings),
) -> ConfigService:
    return _get_config_service(str(app_settings.site_config_path))
