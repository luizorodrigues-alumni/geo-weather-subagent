from typing import Literal
from graph.location_state import LocationState
from tools.location_tools import LOCATION_TOOLS
from llm.factory import get_llm
from langchain.messages import SystemMessage
from prompts.location_prompt import LOCATION_PROMPT
from langgraph.prebuilt import ToolNode
from langgraph.graph.state import StateGraph, CompiledStateGraph, START, END


def location(state: LocationState) -> LocationState:
    """
    Location agent node function.
    Processes the current state and returns an updated LocationState.
    Args:
        state (LocationState): The current state containing messages.
    Returns:
        LocationState: The updated state with the LLM response message.
    """

    # LLM
    llm = get_llm(tools=LOCATION_TOOLS)

    # System Prompt
    system_message = SystemMessage(LOCATION_PROMPT)

    # Invoke LLM
    response = llm.invoke([system_message, *state.messages])

    return {"messages": [response]}

def location_router(state: LocationState) -> Literal["tools", "END"]:
    """
    Router function to determine the next node in the location agent graph.
    Decides whether to call tools or end the graph based on the last message.
    Args:
        state (LocationState): The current state containing messages.
    Returns:
        Literal["tools", "END"]: The next node to transition to ("tools" or "END").
    """
    if state.messages[-1].tool_calls:
        return "tools"
    return "END"

def build_location_graph() -> CompiledStateGraph[LocationState, None, LocationState, LocationState]:
    """
    Builds and compiles the location agent state graph.
    Returns:
        CompiledStateGraph[LocationState, None, LocationState, LocationState]: The compiled location agent graph.
    """
    # Builder
    builder = StateGraph(LocationState)

    # Nodes
    tool_node = ToolNode(LOCATION_TOOLS)
    builder.add_node("location", location)
    builder.add_node("tools", tool_node)

    # Edges
    builder.add_edge(START, "location")
    builder.add_conditional_edges(
        "location",
        location_router,
        {"tools":"tools", "END": END}
    )
    builder.add_edge("tools", "location")
    
    return builder.compile()
