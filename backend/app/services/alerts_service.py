# app/services/alerts_service.py
import requests
from app.config import API_KEY, BASE_URL

def get_weather_alerts(location):
    """
    Calls the WeatherAPI alerts endpoint.
    
    Parameters:
    - location (str): Location query parameter (e.g., city name, coordinates)

    Returns:
    - dict: JSON response with alerts data or an error message
    """
    endpoint = f"{BASE_URL}/alerts.json"
    params = {
        "key": API_KEY,
        "q": location
    }
    
    response = requests.get(endpoint, params=params)
    return response.json() if response.status_code == 200 else {"error": "Could not retrieve alerts"}