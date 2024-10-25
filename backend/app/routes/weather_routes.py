# app/routes/weather_routes.py
from fastapi import APIRouter, HTTPException
from app.services.weather_service import get_bulk_weather
from app.schemas.bulk_request import BulkWeatherRequest  # Ensure this matches your file structure
from app.services.alerts_service import get_weather_alerts
from app.services.future_weather_service import get_future_weather

router = APIRouter()

@router.get("/alerts")
async def weather_alerts(location: str):
    data = get_weather_alerts(location)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return data.get("alerts", {})

@router.post("/bulk")
async def bulk_weather(request: BulkWeatherRequest):
    locations = request.locations
    data = get_bulk_weather(locations)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return data.get("bulk", [])

@router.get("/future")
async def future_weather(location: str, date: str):
    data = get_future_weather(location, date)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return data