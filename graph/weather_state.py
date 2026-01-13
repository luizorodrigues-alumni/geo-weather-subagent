from pydantic import BaseModel
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class WeatherState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], add_messages]
