import logging
from typing import Dict, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import Graph
from utils.database_tool import create_database_tool, DatabaseTool
from langgraph.prebuilt import ToolExecutor
import os


class CommandHandler:
    def __init__(self, db_handler):
        self.logger = logging.getLogger(__name__)
        self.db_handler = db_handler

        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is not set")

        self.llm = ChatAnthropic(
            model="claude-3-opus-20240229", anthropic_api_key=anthropic_api_key)
        self.db_tool: DatabaseTool = create_database_tool(db_handler)
        self.tool_executor = ToolExecutor([self.db_tool])

        # Initialize the graph
        self.graph = self.create_graph()

    def create_graph(self) -> Graph:
        workflow = Graph()

        # Define nodes
        workflow.add_node("process_input", self.process_input)
        workflow.add_node("database", self.tool_executor)
        workflow.add_node("generate_response", self.generate_response)

        # Define edges
        workflow.add_edge("process_input", "database")
        workflow.add_edge("database", "generate_response")

        # Set entry point
        workflow.set_entry_point("process_input")

        return workflow.compile()

    def process_input(self, state: Dict[str, Any]) -> Dict[str, Any]:
        user_input = state.get("input", "")
        return {
            "tool_input": {
                "name": "database_tool",
                "arguments": {
                    "action": "find_one",
                    "collection": "users",
                    "data": {}
                }
            }
        }

    def generate_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        db_result = state.get("database", {})
        user_input = state.get("input", "")

        system_prompt = "You are HAL-9001, an AI assistant. Respond to the user based on their input and the database information provided."
        human_message = f"User input: {user_input}\nDatabase info: {db_result}"

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message)
        ]

        response = self.llm.invoke(messages)
        return {"response": response.content}

    def handle_command(self, command: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            result = self.graph.invoke({"input": data.get("input", "")})
            return {"status": "success", "data": result.get("response", "No response generated.")}
        except Exception as e:
            self.logger.error(f"Error in handling command: {str(e)}")
            return {"status": "error", "data": f"An error occurred while processing your request: {str(e)}"}

    # You can add more specific command handlers here if needed
    def handle_chat(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.handle_command("chat", data)

    def handle_onboarding(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement onboarding logic here
        pass

    def handle_schedule(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement schedule generation logic here
        pass
