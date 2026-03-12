from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user
import httpx
import logging
from app.config import settings

router = APIRouter(prefix="/environment", tags=["environment"])
logger = logging.getLogger(__name__)


class EnvironmentRequest(BaseModel):
    pm25: float
    pm10: float
    aqi: float
    location: Optional[str] = None


@router.post("")
async def store_environment_data(data: EnvironmentRequest, user_id: str = Depends(get_current_user)):
    supabase = get_db()
    try:
        res = supabase.table("environment_data").insert({
            "user_id": user_id,
            "pm25": data.pm25,
            "pm10": data.pm10,
            "aqi": data.aqi,
            "location": data.location
        }).execute()
        return {"message": "Environment data saved", "data": res.data}
    except Exception as e:
        logger.error(f"Error saving environment data: {e}")
        raise HTTPException(status_code=500, detail="Failed to store environment data")


@router.get("/aqi")
async def get_aqi(lat: float = 0.0, lon: float = 0.0):
    """Fetch real AQI for a lat/lon coordinate via AQICN."""
    try:
        url = f"http://api.waqi.info/feed/geo:{lat};{lon}/?token={settings.aqicn_api_key}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            data = response.json()

            if data.get("status") == "ok":
                aqi_val = data["data"]["aqi"]
                iaqi = data["data"].get("iaqi", {})
                return {
                    "aqi": aqi_val,
                    "pm25": iaqi.get("pm25", {}).get("v", None),
                    "pm10": iaqi.get("pm10", {}).get("v", None),
                    "no2": iaqi.get("no2", {}).get("v", None),
                    "so2": iaqi.get("so2", {}).get("v", None),
                    "o3": iaqi.get("o3", {}).get("v", None),
                    "co": iaqi.get("co", {}).get("v", None),
                    "location_name": data["data"]["city"]["name"]
                }

            logger.error(f"AQICN returned non-ok status: {data}")
            raise HTTPException(status_code=503, detail="AQI service returned invalid response")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching AQI by coordinates: {e}")
        raise HTTPException(status_code=503, detail="AQI service unavailable")


@router.get("/aqi-by-city")
async def get_aqi_by_city(city: str):
    """Fetch real AQI for a city name via AQICN."""
    if not city or len(city.strip()) < 2:
        raise HTTPException(status_code=400, detail="City name must be at least 2 characters")
    try:
        url = f"http://api.waqi.info/feed/{city.strip()}/?token={settings.aqicn_api_key}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            data = response.json()

            if data.get("status") == "ok":
                aqi_val = data["data"]["aqi"]
                iaqi = data["data"].get("iaqi", {})
                return {
                    "aqi": aqi_val,
                    "pm25": iaqi.get("pm25", {}).get("v", None),
                    "pm10": iaqi.get("pm10", {}).get("v", None),
                    "no2": iaqi.get("no2", {}).get("v", None),
                    "so2": iaqi.get("so2", {}).get("v", None),
                    "o3": iaqi.get("o3", {}).get("v", None),
                    "co": iaqi.get("co", {}).get("v", None),
                    "location_name": data["data"]["city"]["name"]
                }

            logger.error(f"AQICN city search returned non-ok: {data}")
            raise HTTPException(status_code=503, detail=f"AQI data not available for city: {city}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching AQI by city '{city}': {e}")
        raise HTTPException(status_code=503, detail="AQI service unavailable")


@router.get("/weather")
async def get_weather(lat: float = 0.0, lon: float = 0.0):
    """Fetch real weather data for a lat/lon coordinate via OpenWeatherMap."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.openweather_api_key}&units=metric"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            data = response.json()

            if response.status_code == 200:
                return {
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"].get("feels_like"),
                    "humidity": data["main"].get("humidity"),
                    "description": data["weather"][0]["description"],
                    "wind_speed": data.get("wind", {}).get("speed")
                }

            logger.error(f"OpenWeather returned non-200: {response.status_code} - {data}")
            raise HTTPException(status_code=503, detail="Weather service returned invalid response")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        raise HTTPException(status_code=503, detail="Weather service unavailable")
