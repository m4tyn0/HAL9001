from typing import TypedDict, Annotated
from langchain_anthropic import ChatAnthropic
from langchain.tools import BaseTool
from langgraph.graph import Graph, END
from langgraph.prebuilt import ToolExecutor
from langgraph.prebuilt.tool_node import tools_condition
from langgraph.graph.message import add_messages
import os


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


def create_chat_workflow(db_handler):
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    chat_model = ChatAnthropic(
        model="claude-3-haiku-20240307", anthropic_api_key=anthropic_api_key)

    # Assuming DatabaseTool is a subclass of BaseTool
    database_tool = DatabaseTool(db_handler)
    tools = [database_tool]

    tool_executor = ToolExecutor(tools)

    def agent(state: AgentState):
        messages = state['messages']
        response = chat_model.invoke(messages)
        return {"messages": [response]}

    workflow = Graph()

    workflow.add_node("agent", agent)
    workflow.add_node("tools", tool_executor)

    workflow.add_edge("agent", tools_condition)
    workflow.add_edge("tools", "agent")
    workflow.set_entry_point("agent")

    return workflow.compile()

# Usage
# workflow = create_chat_workflow(db_handler)
# result = workflow.invoke({"messages": [HumanMessage(content="Hello, can you help me?")]})
