# Geo Weather Subagent 🌍🌦️

A hierarchical multi-agent system built with **LangGraph** that orchestrates location resolution and weather data retrieval using a **Supervisor-Subgraph** architecture.

## 🏗️ Architecture

The system uses a Supervisor node to delegate tasks to specialized subgraphs based on user input.

```mermaid
graph TD
    User[User Input] --> Supervisor
    Supervisor -. "Fetch Location".-> LocationTool[Location Subgraph]
    Supervisor -. "Fetch Weather".-> WeatherTool[Weather Subgraph]
    WeatherTool[Weather Subgraph] --> Supervisor
     LocationTool[Location Subgraph] --> Supervisor
```

## ⚡ Tech Stack & APIs
- Orchestration: LangGraph & LangChain
- Geolocation: Geoapify API (Geocoding)
- Weather: wttr.in (JSON format)
