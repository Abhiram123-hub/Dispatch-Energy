import json
from functools import lru_cache
from pathlib import Path

from fastapi import Depends

from app.config.settings import Settings, settings
from app.models.site import Site, SiteRecord, SitesFile
from app.services.config_service import get_settings
from app.services.geocoding_service import GeocodingService, _get_geocoding_service


class SiteService:
    """Loads sites from configuration and enriches them with geocoding data."""

    def __init__(
        self,
        sites_path: Path,
        geocoding_service: GeocodingService,
    ) -> None:
        self._sites_path = sites_path
        self._geocoding_service = geocoding_service

    def get_all_sites(self) -> list[Site]:
        records = self._load_site_records()
        return [self._build_site(record) for record in records]

    def _load_site_records(self) -> list[SiteRecord]:
        raw = json.loads(self._sites_path.read_text(encoding="utf-8"))
        return SitesFile.model_validate(raw).sites

    def _build_site(self, record: SiteRecord) -> Site:
        geocode = self._geocoding_service.geocode(record.address)
        return Site(
            id=record.id,
            name=record.name,
            address=record.address,
            latitude=geocode.latitude,
            longitude=geocode.longitude,
            geocode_status=geocode.status,
            geocode_error=geocode.error,
        )


@lru_cache
def _get_site_service(sites_path: str) -> SiteService:
    return SiteService(Path(sites_path), _get_geocoding_service())


def get_geocoding_service(
    app_settings: Settings = Depends(get_settings),
) -> GeocodingService:
    del app_settings
    return _get_geocoding_service()


def get_site_service(
    app_settings: Settings = Depends(get_settings),
) -> SiteService:
    return _get_site_service(str(app_settings.sites_config_path))
