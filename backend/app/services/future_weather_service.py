# app/services/future_weather_service.py
import requests
from app.config import API_KEY, BASE_URL

def get_future_weather(location, future_date):
    """
    Calls the WeatherAPI future endpoint for a specified date.

    Parameters:
    - location (str): Location query parameter (e.g., city name, coordinates)
    - future_date (str): Date in the format YYYY-MM-DD between 14 and 300 days from today

    Returns:
    - dict: JSON response with future weather data or an error message
    """
    endpoint = f"{BASE_URL}/future.json"
    params = {
        "key": API_KEY,
        "q": location,
        "dt": future_date
    }
    
    response = requests.get(endpoint, params=params)
    return response.json() if response.status_code == 200 else {"error": "Could not retrieve future weather data"}