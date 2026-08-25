import os

import httpx

from app.services.pvwatts import pvwatts_service


SOLAR_RESOURCE_URL = "https://developer.nrel.gov/api/solar/solar_resource/v1.json"


class SolarService:
    """Coordinates solar resource retrieval and PVWatts calculations."""

    async def get_solar_resource(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        api_key = os.getenv("NREL_API_KEY", "DEMO_KEY")

        params = {
            "api_key": api_key,
            "lat": latitude,
            "lon": longitude,
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(
                    SOLAR_RESOURCE_URL,
                    params=params,
                )
                response.raise_for_status()
                data = response.json()

            if data.get("errors"):
                return {
                    "status": "error",
                    "error": "; ".join(data["errors"]),
                }

            outputs = data.get("outputs", {})

            return {
                "status": "success",
                "avg_ghi": outputs.get("avg_ghi"),
                "avg_dni": outputs.get("avg_dni"),
                "avg_lat_tilt": outputs.get("avg_lat_tilt"),
                "raw": outputs,
            }

        except httpx.HTTPError as exc:
            return {
                "status": "error",
                "error": f"Solar resource API request failed: {exc}",
            }

    async def get_solar_estimate(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        solar_resource = await self.get_solar_resource(
            latitude,
            longitude,
        )

        pvwatts = await pvwatts_service.calculate(
            latitude=latitude,
            longitude=longitude,
        )

        return {
            "latitude": latitude,
            "longitude": longitude,
            "solar_resource": solar_resource,
            "pvwatts": pvwatts,
        }


solar_service = SolarService()
