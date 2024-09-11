from typing import List, Dict, Any
from agents.general_agent import GeneralAgent
from agents.onboarding_agent import OnboardingAgent
from database.handlers.neo4j import Neo4jDatabase
from pygments import highlight, lexers, formatters
import json


class CommandHandler:
    def __init__(self, db: Neo4jDatabase):
        self.db = db
        self.conversation_history: List[Dict[str, str]] = []

    def _get_agent(self, agent_type: str):
        if agent_type == "general":
            return GeneralAgent(self.db)
        elif agent_type == "onboarding":
            return OnboardingAgent(self.db)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")

    def handle_chat(self, user_input: str) -> str:
        agent = self._get_agent("general")
        self.conversation_history.append({"user": user_input})
        result = agent.run(user_input)
        self.conversation_history.append({"assistant": result})
        return result

    def handle_onboarding(self, user_input: str) -> str:
        agent = self._get_agent("onboarding")
        self.conversation_history.append({"user": user_input})
        try:
            result = agent.run(user_input, user_id=1, thread_id=1)
            self.conversation_history.append({"assistant": result})
            return result
        except RecursionError:
            error_message = "The onboarding process encountered an recursion limit. Please try again or contact support."
            self.conversation_history.append({"assistant": error_message})
            return error_message

    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.conversation_history

    def clear_conversation_history(self) -> None:
        self.conversation_history.clear()

    def handle_command(self, command: str, **kwargs: Any) -> str:
        if command == "history":
            return self._format_history()
        elif command == "clear":
            self.clear_conversation_history()
            return "Conversation history cleared."
        elif command == "help":
            return self._get_help_message()
        elif command == "add_skill":
            result = self.db.create_skill(**kwargs)
            return f"Skill added: {result['name']} (ID: {result['id']})"
        elif command == "add_project":
            result = self.db.create_project(**kwargs)
            return f"Project added: {result['name']} (ID: {result['id']})"
        elif command == "add_task":
            result = self.db.create_task(**kwargs)
            return f"Task added: {result['name']} (ID: {result['id']})"
        elif command == "list_skills":
            skills = self.db.list_skills()
            return self._format_list("Skills", skills)
        elif command == "list_projects":
            projects = self.db.list_projects()
            return self._format_list("Projects", projects)
        elif command == "list_tasks":
            tasks = self.db.list_tasks()
            return self._format_list("Tasks", tasks)
        elif command == "add_skill_to_project":
            result = self.db.add_skill_to_project(**kwargs)
            return result
        elif command == "add_task_to_project":
            result = self.db.add_task_to_project(**kwargs)
            return result
        elif command == "update_skill_xp":
            result = self.db.update_skill_xp(**kwargs)
            if "error" in result:
                return f"Error: {result['error']}"
            return f"Skill '{result['name']}' updated. New XP: {result['new_xp']}, New Level: {result['new_level']}"
        elif command == "update_project_status":
            result = self.db.update_project_status(**kwargs)
            if "error" in result:
                return f"Error: {result['error']}"
            return f"Project '{result['name']}' updated. New Status: {result['new_status']}, Completion: {result['completion_percentage']}%"
        else:
            return f"Unknown command: {command}"

    def _format_history(self) -> str:
        formatted_history = []
        for entry in self.conversation_history:
            for role, content in entry.items():
                formatted_history.append(f"{role.capitalize()}: {content}")
        return "\n\n".join(formatted_history)

    def _format_list(self, title: str, items: List[Dict[str, Any]]) -> str:
        formatted = {title: items}
        json_formatted = json.dumps(formatted, indent=2)
        colorful_json = highlight(
            json_formatted, lexers.JsonLexer(), formatters.TerminalFormatter())
        return colorful_json

    def _get_help_message(self) -> str:
        return """
Available commands:
- history: Show conversation history
- clear: Clear conversation history
- help: Show this help message
- add_skill: Add a new skill
- add_project: Add a new project
- add_task: Add a new task
- list_skills: List all skills
- list_projects: List all projects
- list_tasks: List all tasks
- add_skill_to_project: Associate a skill with a project
- add_task_to_project: Add a task to a project
- update_skill_xp: Update a skill's XP
- update_project_status: Update a project's status
        """
