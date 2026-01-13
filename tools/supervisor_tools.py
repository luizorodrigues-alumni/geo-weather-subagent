from langchain.messages import HumanMessage
from langchain.tools import tool
from agents.weather_agent import build_weather_graph
from agents.location_agent import build_location_graph


@tool
def fetch_location_data(request: str) -> str:
    """
    Fetches location data.
    Use this when the user is requesting location information (e.g., "Where is Paris?") or
    needs to convert a place name into coordinates.
    """
    result = build_location_graph().invoke(
        {"messages": [HumanMessage(content=request)]}
    )
    return result["messages"][-1].text

@tool
def fetch_weather_data(lat: float, lon: float) -> str:
    """
    Fetches weather data.
    Use this when the user is requesting weather information for specific coordinates (e.g., "What's the weather in Paris?").
    """

    result = build_weather_graph().invoke(
        {"messages": [HumanMessage(content=f"Get weather for coordinates: {lat}, {lon}")]}
    )
    return result["messages"][-1].text

SUPERVISOR_TOOLS = [fetch_location_data, fetch_weather_data]