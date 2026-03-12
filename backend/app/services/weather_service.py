import httpx
from fastapi import HTTPException
from app.config import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.openweather_api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, lat: float, lon: float) -> dict:
        url = f"{self.base_url}?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            
            if response.status_code != 200:
                raise HTTPException(status_code=502, detail="Error fetching data from OpenWeather API")
            
            data = response.json()
            
            result = {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "atmospheric_pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"],
                "location_name": data.get("name")
            }
            return result
            
weather_service = WeatherService()
