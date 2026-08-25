import os
import httpx


PVWATTS_URL = "https://developer.nrel.gov/api/pvwatts/v8.json"


class PVWattsService:
    """Calls NREL PVWatts to estimate solar production."""

    async def calculate(
        self,
        latitude: float,
        longitude: float,
        system_capacity_kw: float = 10.0,
    ) -> dict:
        api_key = os.getenv("NREL_API_KEY", "DEMO_KEY")

        params = {
            "api_key": api_key,
            "azimuth": 180,
            "dataset": "nsrdb",
            "dc_ac_ratio": 1.2,
            "gcr": 0.4,
            "inv_eff": 96,
            "radius": 0,
            "system_capacity": system_capacity_kw,
            "tilt": abs(latitude),
            "array_type": 1,
            "module_type": 0,
            "losses": 14,
            "lat": latitude,
            "lon": longitude,
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(PVWATTS_URL, params=params)
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
                "annual_energy_kwh": outputs.get("ac_annual"),
                "capacity_factor": outputs.get("capacity_factor"),
                "monthly_energy_kwh": outputs.get("ac_monthly"),
                "inputs": data.get("inputs", {}),
            }

        except httpx.HTTPError as exc:
            return {
                "status": "error",
                "error": f"PVWatts API request failed: {exc}",
            }


pvwatts_service = PVWattsService()