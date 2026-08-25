from app.config.settings import Settings
from app.models.health import HealthResponse
from app.services.config_service import ConfigService


class HealthService:
    """Business logic for health checks."""

    def __init__(self, settings: Settings, config_service: ConfigService) -> None:
        self._settings = settings
        self._config_service = config_service

    def get_health(self) -> HealthResponse:
        site_config = self._config_service.load()
        return HealthResponse(
            status="ok",
            app_name=site_config.site_name,
            version=site_config.version,
        )
