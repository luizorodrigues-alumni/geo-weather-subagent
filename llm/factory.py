

from typing import Sequence
from langchain_core.tools import BaseTool
from langchain.chat_models import init_chat_model, BaseChatModel
from.settings import DEFAULT_MODEL
from dotenv import load_dotenv

load_dotenv()

def get_llm(model: str | None=None, tools : Sequence[BaseTool] | None=None) -> BaseChatModel:
    """
    Initializes and returns a chat model with optional tool bindings.
    Args:
        model (str | None): The model identifier to use. If None, uses the default model.
        tools (Sequence[BaseTool] | None): A sequence of tools to bind to the chat model. If None, no tools are bound.
    Returns:
        BaseChatModel: An instance of a chat model, optionally with tools bound.
    """
    model_name = model or DEFAULT_MODEL

    if tools:
        return init_chat_model(model=model_name).bind_tools(tools=tools)

    return init_chat_model(model=model_name)
