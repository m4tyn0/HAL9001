

import threading
import logging
from src.generate_graph import generate_graph_image
from dotenv import load_dotenv
import os
from src.agents import *
from src.data_manager import DataManager
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from typing import TypedDict, List, Annotated


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("ANTHROPIC_API_KEY")
_set_env("LANGSMITH_API_KEY")
_set_env("TAVILY_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "HAL3000"

# File: src/main.py


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ... (keep your existing environment setup code)


class AgentState(TypedDict):
    messages: List[BaseMessage]
    data_manager: DataManager
    next_step: str


def user_input(state: AgentState) -> AgentState:
    # This function is now just a passthrough
    return state


def process_input(state: AgentState) -> AgentState:
    messages = state["messages"]
    last_message = messages[-1].content.lower() if messages else ""

    if "schedule" in last_message:
        state["next_step"] = "scheduler"
    elif "project" in last_message:
        state["next_step"] = "project_manager"
    elif "player" in last_message or "skill" in last_message or "xp" in last_message:
        state["next_step"] = "player_manager"
    elif "goal" in last_message:
        state["next_step"] = "goal_tracker"
    elif "routine" in last_message or "habit" in last_message:
        state["next_step"] = "routine_manager"
    else:
        state["next_step"] = "general_response"

    return state


def general_response(state: AgentState) -> AgentState:
    llm = ChatAnthropic(model="claude-3-opus-20240229",
                        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"))
    # Only pass the last user message to avoid multiple assistant messages
    last_user_message = next((msg for msg in reversed(
        state["messages"]) if isinstance(msg, HumanMessage)), None)
    if last_user_message:
        response = llm.invoke([last_user_message])
        state["messages"].append(AIMessage(content=response.content))
    state["next_step"] = "user_input"  # Change this to go back to user input
    return state


def check_end(state: AgentState) -> AgentState:
    last_message = state["messages"][-1].content if state["messages"] else ""
    if isinstance(last_message, str) and last_message.lower() == "quit":
        state["next_step"] = END
    else:
        state["next_step"] = "user_input"
    return state


def run_planner():
    # Initialize DataManager
    data_manager = DataManager("data/")

    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("user_input", user_input)
    workflow.add_node("process_input", process_input)
    workflow.add_node("general_response", general_response)
    workflow.add_node("scheduler", scheduler)
    workflow.add_node("project_manager", project_manager)
    workflow.add_node("player_manager", player_manager)
    workflow.add_node("goal_tracker", goal_tracker)
    workflow.add_node("routine_manager", routine_manager)
    workflow.add_node("check_end", check_end)

    # Add edges
    workflow.add_edge("user_input", "process_input")
    workflow.add_conditional_edges(
        "process_input",
        lambda x: x["next_step"],
        {
            "scheduler": "scheduler",
            "project_manager": "project_manager",
            "player_manager": "player_manager",
            "goal_tracker": "goal_tracker",
            "routine_manager": "routine_manager",
            "general_response": "general_response",
        }
    )
    workflow.add_edge("scheduler", "check_end")
    workflow.add_edge("project_manager", "check_end")
    workflow.add_edge("player_manager", "check_end")
    workflow.add_edge("goal_tracker", "check_end")
    workflow.add_edge("routine_manager", "check_end")
    workflow.add_edge("general_response", "check_end")
    workflow.add_edge("check_end", "user_input")

    # Set entrypoint
    workflow.set_entry_point("user_input")

    # Compile the graph
    app = workflow.compile()

    # Initialize the state
    state = AgentState(
        messages=[],
        data_manager=data_manager,
        next_step="user_input"
    )

    try:
        while True:
            user_input_text = input("You: ")
            if user_input_text.lower() == "quit":
                print("Thank you for using the Gamified Day Planner. Goodbye!")
                break

            state["messages"].append(HumanMessage(content=user_input_text))
            state["next_step"] = "process_input"

            for output in app.stream(state):
                state = output
                if "next_step" in state and state["next_step"] == END:
                    print("Thank you for using the Gamified Day Planner. Goodbye!")
                    return
                if "messages" in state and state["messages"]:
                    last_message = state["messages"][-1]
                    if isinstance(last_message, AIMessage):
                        print(f"Assistant: {last_message.content}")
                        break  # Exit the loop after processing one response

            # Clear messages to avoid memory issues in long conversations
            if "messages" in state:
                state["messages"] = state["messages"][-2:]

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

    finally:
        print("Exiting the Gamified Day Planner. Thank you for using our service!")
        if 'data_manager' in locals():
            data_manager.close_connection()


if __name__ == "__main__":
    run_planner()
