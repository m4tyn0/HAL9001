from typing import TypedDict, List, Any
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: List[BaseMessage]
    data_manager: Any
