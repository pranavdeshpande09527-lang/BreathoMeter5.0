import httpx
from fastapi import HTTPException
from app.config import settings

class AQIService:
    def __init__(self):
        self.api_key = settings.aqicn_api_key
        self.base_url = "https://api.waqi.info/feed"

    def _get_pollution_category(self, aqi: int) -> str:
        if aqi <= 50: return "Good"
        elif aqi <= 100: return "Moderate"
        elif aqi <= 150: return "Unhealthy for Sensitive Groups"
        elif aqi <= 200: return "Unhealthy"
        elif aqi <= 300: return "Very Unhealthy"
        else: return "Hazardous"

    async def get_aqi(self, location: str = "here") -> dict:
        """Fetch AQI data for a specific location or based on IP ('here')."""
        # AQICN supports /feed/here/ for IP-based or /feed/{city}/
        url = f"{self.base_url}/{location}/?token={self.api_key}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            
            if response.status_code != 200:
                raise HTTPException(status_code=502, detail="Error fetching data from AQI API")
            
            data = response.json()
            if data["status"] != "ok":
                raise HTTPException(status_code=400, detail=f"AQI API Error: {data.get('data', 'Unknown')}")
            
            aqi_value = data["data"]["aqi"]
            iaqi = data["data"]["iaqi"]
            
            # Format response for real-time frontend dashboard
            result = {
                "location_name": data["data"]["city"]["name"],
                "latitude": data["data"]["city"]["geo"][0],
                "longitude": data["data"]["city"]["geo"][1],
                "aqi": aqi_value,
                "pollution_category": self._get_pollution_category(aqi_value),
                "pm25": iaqi.get("pm25", {}).get("v") if "pm25" in iaqi else None,
                "pm10": iaqi.get("pm10", {}).get("v") if "pm10" in iaqi else None,
                "timestamp": data["data"]["time"]["s"]
            }
            return result

aqi_service = AQIService()
