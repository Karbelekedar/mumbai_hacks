# app/services/weather_service.py
import requests
from app.config import API_KEY, BASE_URL

def get_weather_alerts(location):
    """
    Calls the WeatherAPI endpoint for weather alerts.
    
    Parameters:
    - location (str): Location query parameter (e.g., city name, coordinates)

    Returns:
    - dict: JSON response with alerts data or an error message
    """
    endpoint = f"{BASE_URL}/forecast.json"
    params = {
        "key": API_KEY,
        "q": location,
        "alerts": "yes"
    }
    response = requests.get(endpoint, params=params)
    return response.json() if response.status_code == 200 else {"error": "Could not retrieve alerts"}

def get_bulk_weather(locations):
    """
    Calls the WeatherAPI bulk endpoint to get weather data for multiple locations.
    
    Parameters:
    - locations (list): List of LocationQuery objects (Pydantic models)

    Returns:
    - dict: JSON response with weather data for each location or an error message
    """
    # Convert Pydantic objects to dictionaries
    location_dicts = [location.dict() for location in locations]

    endpoint = f"{BASE_URL}/current.json?q=bulk"
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}
    data = {"locations": location_dicts}
    
    response = requests.post(endpoint, params=params, headers=headers, json=data)
    return response.json() if response.status_code == 200 else {"error": "Could not retrieve bulk weather data"}