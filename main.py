from langchain.messages import HumanMessage
from langgraph.graph.state import RunnableConfig
import threading
from agents.supervisor_agent import build_supervisor_graph

from dotenv import load_dotenv

load_dotenv()

def main():
    """
    Main function to run the multi-agent supervisor system in a loop, allowing user interaction.
    """
    graph = build_supervisor_graph()
    config = RunnableConfig(configurable={"thread_id": threading.get_ident()})

    while True:
        user_input = input("Você: ")
        if user_input.lower() in ["q", "quit", "exit"]:
            break

        # Invoke the multi-agent graph
        result = graph.invoke(
            {"messages": [HumanMessage(user_input)]},
            config=config
        )

        # Message formatting for better readability
        last_msg = result["messages"][-1].content
        if isinstance(last_msg, list):
            text = last_msg[0].get("text", "")
            print("\nAssistente:", text) if text else print(f"\nAssistente: {last_msg}")
        else:
            print("\nAssistente:", last_msg)
    
    # Formating result['messages'] for better readability and learning
    print("\n\n--- Full Conversation ---")
    for i, message in enumerate(result["messages"]):
        print(f"\n--- Message {i+1} ---")
        print(f"Type: {type(message).__name__}")
        print(f"Content: {message.content}")
        if hasattr(message, "tool_calls"):
            print(f"Tool Calls: {message.tool_calls}")

if __name__ == "__main__":
    main()
