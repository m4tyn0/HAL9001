import os
from typing import Dict, Any
from langchain.llms import OpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor

# Update imports to reflect new structure
from app.cli import parse_cli_arguments
from app.data_manager import load_data, save_data
from tools.skill_tool import SkillTool
from tools.project_tool import ProjectTool
from tools.routine_tool import RoutineTool
from tools.schedule_tool import ScheduleTool
from config.config import Config

# Initialize OpenAI LLM
llm = OpenAI(api_key=Config.OPENAI_API_KEY)

# Initialize tools
skill_tool = SkillTool()
project_tool = ProjectTool(llm)
routine_tool = RoutineTool()
schedule_tool = ScheduleTool(llm)

# Combine all tools
tools = [skill_tool, project_tool, routine_tool, schedule_tool]
tool_executor = ToolExecutor(tools)

def cli_interface(state: Dict[str, Any]) -> Dict[str, Any]:
    """Parse CLI arguments and load user data."""
    state["command"] = parse_cli_arguments()
    state["data"] = load_data()
    return state

def brain(state: Dict[str, Any]) -> Dict[str, Any]:
    """Main logic for processing commands and executing tools."""
    command = state["command"]
    data = state["data"]

    if command["action"] == "onboard":
        data["user"]["name"] = input("Enter your name: ")
        state["output"] = f"Welcome, {data['user']['name']}!"
    else:
        # Execute the appropriate tool based on the command
        tool_input = {"data": data, "command": command}
        result = tool_executor.execute(command["action"], tool_input)
        state.update(result)

    save_data(data)
    return state

def user_output(state: Dict[str, Any]) -> Dict[str, Any]:
    """Display output to the user."""
    print(state.get("output", "Operation completed."))
    return state

# Create the LangGraph
workflow = StateGraph()

# Add nodes
workflow.add_node("CLI", cli_interface)
workflow.add_node("Brain", brain)
workflow.add_node("Output", user_output)

# Add edges
workflow.add_edge("CLI", "Brain")
workflow.add_edge("Brain", "Output")
workflow.add_edge("Output", END)

# Set entry point
workflow.set_entry_point("CLI")

# Compile the graph
app = workflow.compile()

if __name__ == "__main__":
    for output in app.stream({}, {"recursion_limit": 10}):
        pass