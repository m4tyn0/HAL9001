from typing import List, Dict, Any
from agents.chat_agent import Agent


class CommandHandler:
    def __init__(self, agent: Agent ):
        self.agent = agent
        self.conversation_history: List[Dict[str, str]] = []

    def handle_chat(self, user_input: str) -> str:
        self.conversation_history.append({"user": user_input})
        result = self.agent.run(user_input)
        self.conversation_history.append({"assistant": result})
        return result

    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.conversation_history

    def clear_conversation_history(self) -> None:
        self.conversation_history.clear()

    def handle_command(self, command: str, *args: Any) -> str:
        if command == "history":
            return self._format_history()
        elif command == "clear":
            self.clear_conversation_history()
            return "Conversation history cleared."
        elif command == "help":
            return self._get_help_message()
        else:
            return f"Unknown command: {command}"

    def _format_history(self) -> str:
        formatted_history = []
        for entry in self.conversation_history:
            for role, content in entry.items():
                formatted_history.append(f"{role.capitalize()}: {content}")
        return "\n\n".join(formatted_history)
   


    def _get_help_message(self) -> str:
        return """
    
Available commands:
- history: Show conversation history
- clear: Clear conversation history
- help: Show this help message
        """
