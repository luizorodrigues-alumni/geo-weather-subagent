from tools.weather_tools import WEATHER_TOOLS
from llm.factory import get_llm
from langchain.messages import SystemMessage
from prompts.weather_prompt import WEATHER_PROMPT
from langgraph.prebuilt import ToolNode
from langgraph.graph.state import CompiledStateGraph, StateGraph, START, END
from graph.weather_state import WeatherState
from typing import Literal

def weather(state: WeatherState) -> WeatherState:
    """
    Weather agent node function.
    Processes the current state and returns an updated WeatherState.
    Args:
        state (WeatherState): The current state containing messages.
    Returns:
        WeatherState: The updated state with the LLM response message.
    """

    # LLM
    llm = get_llm(tools=WEATHER_TOOLS)

    # System Message
    system_message = SystemMessage(WEATHER_PROMPT)
    
    # Invoke LLM
    response = llm.invoke([system_message, *state.messages])

    return {"messages": [response]}


def weather_router(state: WeatherState) -> Literal["tools", "END"]:
    """
    Router function to determine the next node in the weather agent graph.
    Decides whether to call tools or end the graph based on the last message.
    Args:
        state (WeatherState): The current state containing messages.
    Returns:
        Literal["tools", "END"]: The next node to transition to ("tools" or "END").
    """

    if state.messages[-1].tool_calls:
        return "tools"
    return "END"


def build_weather_graph() -> CompiledStateGraph[WeatherState, None, WeatherState, WeatherState]:
    """
    Builds and compiles the weather agent state graph.
    Returns:
        CompiledStateGraph[WeatherState, None, WeatherState, WeatherState]: The compiled weather agent graph.
    """
    # Builder
    builder = StateGraph(WeatherState)

    # Nodes
    tool_node = ToolNode(WEATHER_TOOLS)
    builder.add_node("weather", weather)
    builder.add_node("tools", tool_node)

    # Edges
    builder.add_edge(START, "weather")
    builder.add_conditional_edges(
        "weather",
        weather_router,
        {"tools": "tools", "END": END}
    )
    builder.add_edge("tools", "weather")

    return builder.compile()