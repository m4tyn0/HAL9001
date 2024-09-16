from typing import List, Dict, Any
from database.handlers.markdown_db import MarkdownDatabase
from tools.tool_registry import ToolRegistry
from agents.general_agent import GeneralAgent
import logging
import os
from dotenv import load_dotenv
import json
from database.models.model import ENTITY_TYPES

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CommandHandler:
    def __init__(self):
        load_dotenv()
        base_path = os.getenv("MARKDOWN_DB_PATH")
        if not base_path:
            raise ValueError(
                "MARKDOWN_DB_PATH environment variable is not set")
        self.db = MarkdownDatabase(base_path)
        self.conversation_history: List[Dict[str, str]] = []
        self.tool_registry = ToolRegistry(self.db)
        self.agent = GeneralAgent(self.db)

    def handle_command(self, command: str, **kwargs: Any) -> str:
        parts = command.split('_', 1)
        if len(parts) < 2:
            return self._handle_special_command(command, **kwargs)

        operation, entity_type = parts
        if entity_type not in ENTITY_TYPES:
            return f"Unknown entity type: {entity_type}"

        tool = self.tool_registry.get_tool(f"{operation}_{entity_type}")
        if tool:
            try:
                result = tool(**kwargs)
                return self._format_result(result, operation)
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return f"Unknown operation: {operation} for entity type: {entity_type}"

    def _handle_special_command(self, command: str, **kwargs: Any) -> str:
        if command == 'chat':
            return self.handle_chat(**kwargs)
        elif command == 'history':
            return self._format_history()
        elif command == 'clear':
            self.conversation_history.clear()
            return "Conversation history cleared."
        elif command == 'help':
            return self._get_help_message()
        else:
            return f"Unknown command: {command}"

    def handle_chat(self, user_input: str):
        result = self.agent.run(user_input)
        self.conversation_history.append({"user": user_input})
        self.conversation_history.append({"assistant": result})
        return result

    def _format_result(self, result: Any, operation: str) -> str:
        if operation == 'list':
            return self._format_list_result(result)
        elif operation in ['create', 'get', 'update']:
            return json.dumps(result, indent=2, default=str)
        elif operation == 'delete':
            return "Deleted successfully." if result else "Delete operation failed."
        else:
            return str(result)

    def _format_list_result(self, items: List[Any]) -> str:
        if not items:
            return "No items found."

        formatted_items = []
        for item in items:
            formatted_item = "\n".join(f"  {k}: {v}" for k, v in item.items())
            formatted_items.append(formatted_item)

        return "Items:\n" + "\n\n".join(formatted_items)

    def _format_history(self) -> str:
        formatted_history = []
        for entry in self.conversation_history:
            for role, content in entry.items():
                formatted_history.append(f"{role.capitalize()}: {content}")
        return "\n\n".join(formatted_history)

    def _get_help_message(self) -> str:
        entities = ', '.join(ENTITY_TYPES.keys())
        return f"""
            Available commands:
            - <entity> create, <entity> get, <entity> update, <entity> delete, <entity> list
              where <entity> can be one of: {entities}
            - chat: Start or continue a chat session
            - history: Show conversation history
            - clear: Clear conversation history
            - help: Show this help message
        """
