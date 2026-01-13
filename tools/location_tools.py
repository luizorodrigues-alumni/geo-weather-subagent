import os
import requests
from langchain.tools import tool


@tool
def get_location_data(text: str) -> dict:
    """
    Fetches geolocation data for a given text input using the GeoApiFy service.
    Args:
        text (str): The location text to be geocoded.
    Returns:
        dict: A dictionary with parsed geolocation data including name, country, state, county, city, longitude, and latitude.
    """
    
    api_key = os.getenv("GEO_APIFY_API_KEY")

    # GeoApiFy URL
    geolocation_url = "https://api.geoapify.com/v1/geocode/search"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    params = {
        "apiKey": api_key,
        "text": text,
    }

    # Get Request
    response = requests.get(url=geolocation_url, headers=headers, params=params)
    data = response.json()
    
    # Parse the response
    try:
        props = data.get("features", [{}])[0].get("properties", {})
        parsed_data = {
            "name": props.get("name", text),
            "state": props.get("state", "Unknown"),
            "city": props.get("city", "Unknown"),
            "lon": props.get("lon", "Unknown"),
            "lat": props.get("lat", "Unknown"),
        }
    except (IndexError, KeyError) as e:
        parsed_data = {"error": "Location not found or invalid response from API."}
        
    return parsed_data

LOCATION_TOOLS = [get_location_data]