from typing import List, Dict, Any, Literal
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from utils.tools import get_tools

system_message = SystemMessage(content="""You are an AI assistant for a personal improvement app with access to a MongoDB database. 
Your primary goal is to help users with personal development, task management, and knowledge retrieval.

Always use the appropriate tools to store, retrieve, and update information in the database. Before responding to queries about projects, tasks, or schedules, 
always check the database first using the relevant tools. If information is missing or seems outdated, use the appropriate tool to update it. 
Confirm all updates and retrievals with the user.

Available tools include:
1. add_project, get_project_details, update_project: Manage projects in the database.
2. add_task, get_tasks: Manage tasks in the database.
3. add_schedule_entry, get_schedule, update_schedule_entry: Manage schedule entries in the database.

Ensure your responses are helpful, concise, and directly address the user's query or need. Always strive to provide accurate and up-to-date information from the database.""")


class Agent:
    def __init__(self, graph):
        self.graph = graph

    def run(self, user_input: str) -> str:
        state = {"messages": [system_message,
                              HumanMessage(content=user_input)]}
        result = self.graph.invoke(state)

        # Extract the final AI message
        for message in reversed(result["messages"]):
            if isinstance(message, AIMessage):
                return message.content

        return "An error occurred. Please try again."


def create_agent():
    tools = get_tools()
    model = ChatAnthropic(model="claude-3-haiku-20240307",
                          temperature=0).bind_tools(tools)
    tool_node = ToolNode(tools)

    def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
        messages = state["messages"]
        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tools"
        return "__end__"

    def call_model(state: MessagesState):
        messages = state["messages"]
        response = model.invoke(messages)
        return {"messages": messages + [response]}

    workflow = StateGraph(MessagesState)

    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge("__start__", "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "__end__": "__end__"
        }
    )
    workflow.add_edge("tools", "agent")

    app = workflow.compile()
    return Agent(app)
