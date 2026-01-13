
from typing import Literal
from graph.supervisor_state import  SupervisorState
from langchain.messages import SystemMessage
from langgraph.graph.state import StateGraph, CompiledStateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver

from prompts.supervisor_prompt import SUPERVISOR_PROMPT
from tools.supervisor_tools import SUPERVISOR_TOOLS
from llm.factory import get_llm


def supervisor(state: SupervisorState) -> SupervisorState:
    """
    Supervisor agent node function.
    Processes the current state and returns an updated SupervisorState.
    Args:
        state (SupervisorState): The current state containing messages.
    Returns:
        SupervisorState: The updated state with the LLM response message.
    """

    # LLM
    llm = get_llm(tools=SUPERVISOR_TOOLS)

    # System Message
    system_message = SystemMessage(SUPERVISOR_PROMPT)

    # Invoke LLM
    response = llm.invoke([system_message, *state.messages])

    return {"messages": [response]}

def supervisor_router(state: SupervisorState) -> Literal["tools", "END"]:
    """
    Router function to determine the next node in the supervisor agent graph.
    Decides whether to call tools or end the graph based on the last message.
    Args:
        state (SupervisorState): The current state containing messages.
    Returns:
        Literal["tools", "END"]: The next node to transition to ("tools" or "END").
    """
    
    if state.messages[-1].tool_calls:
        return "tools"
    return "END"
   
def build_supervisor_graph() -> CompiledStateGraph[SupervisorState, None, SupervisorState, SupervisorState]:
    """
    Builds and compiles the supervisor agent state graph.
    Returns:
        CompiledStateGraph[SupervisorState, None, SupervisorState, SupervisorState]: The compiled supervisor agent graph.
    """
    # Builder
    builder = StateGraph(SupervisorState)

    # Nodes
    builder.add_node("supervisor", supervisor)
    tool_node = ToolNode(SUPERVISOR_TOOLS)
    builder.add_node("tools", tool_node)

    # Edges
    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        supervisor_router,
        {"tools": "tools", "END": END}
    )
    builder.add_edge("tools", "supervisor")
    
    return builder.compile(checkpointer=InMemorySaver())