import requests
from langchain.tools import tool

@tool
def get_weather_data(lat: float, lon: float) -> dict:
    """
    Fetches weather data for given latitude and longitude using the wttr.in service.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
    Returns:
        dict: A dictionary with parsed weather data including current conditions and daily forecasts.
    """
    
    #wttr.in URL
    weather_url = f"https://wttr.in/{lat},{lon}?format=j1"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    # Get Request
    response = requests.get(url=weather_url, headers=headers)
    data = response.json()

    parsed_data = {
        "current_condition": data.get("current_condition", []),
        "weather": data.get("weather", [])
    }

    # Remove "hourly" data to reduce size
    for day in parsed_data["weather"]:
        if "hourly" in day:
            del day["hourly"]

    return parsed_data

WEATHER_TOOLS = [get_weather_data]