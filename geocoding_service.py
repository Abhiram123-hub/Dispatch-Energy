import logging
from functools import lru_cache

import httpx

from app.config.settings import Settings, settings
from app.models.geocode import GeocodeStatus
from app.models.site import GeocodeResult

logger = logging.getLogger(__name__)


class GeocodingService:
    """Geocodes addresses via the OpenStreetMap Nominatim API."""

    def __init__(self, app_settings: Settings) -> None:
        self._settings = app_settings

    def geocode(self, address: str) -> GeocodeResult:
        return _geocode_address(
            self._settings.nominatim_base_url,
            self._settings.nominatim_user_agent,
            self._settings.geocoding_timeout_seconds,
            address,
        )


@lru_cache(maxsize=128)
def _geocode_address(
    base_url: str,
    user_agent: str,
    timeout_seconds: float,
    address: str,
) -> GeocodeResult:
    try:
        response = httpx.get(
            f"{base_url}/search",
            params={
                "q": address,
                "format": "json",
                "limit": 1,
                "countrycodes": "us",
            },
            headers={"User-Agent": user_agent},
            timeout=timeout_seconds,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.warning("Nominatim HTTP error for address %r: %s", address, exc)
        return GeocodeResult(
            status=GeocodeStatus.ERROR,
            error=f"Geocoding service returned HTTP {exc.response.status_code}",
        )
    except httpx.RequestError as exc:
        logger.warning("Nominatim request failed for address %r: %s", address, exc)
        return GeocodeResult(
            status=GeocodeStatus.ERROR,
            error="Unable to reach geocoding service",
        )

    results = response.json()
    if not results:
        return GeocodeResult(
            status=GeocodeStatus.UNRESOLVED,
            error="No matching location found for address",
        )

    match = results[0]
    try:
        latitude = float(match["lat"])
        longitude = float(match["lon"])
    except (KeyError, TypeError, ValueError):
        logger.warning("Unexpected Nominatim response for address %r", address)
        return GeocodeResult(
            status=GeocodeStatus.ERROR,
            error="Geocoding service returned an invalid response",
        )

    return GeocodeResult(
        latitude=latitude,
        longitude=longitude,
        status=GeocodeStatus.RESOLVED,
    )


@lru_cache
def _get_geocoding_service() -> GeocodingService:
    return GeocodingService(settings)
