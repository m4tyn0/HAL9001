# src/workflows/onboarding_workflow.py

from langgraph.graph import Graph
from langgraph.prebuilt import ToolExecutor
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models import ChatAnthropic
from utils.database_tool import DatabaseTool


def create_onboarding_workflow(db_handler):
    chat_model = ChatAnthropic(model="claude-3-haiku-20240307")
    database_tool = DatabaseTool(db_handler)
    tool_executor = ToolExecutor(tools=[database_tool])

    def extract_and_store_data(state):
        human_message = state['human_message']
        system_prompt = """You are an AI assistant helping with user onboarding. 
        Extract relevant information about the user, their skills, tasks, and preferences. 
        Use the DatabaseTool to store this information in the appropriate collections."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message)
        ]

        ai_message = chat_model.invoke(messages)

        # Here you would parse the AI's response and use the DatabaseTool to store the extracted information
        # This is a simplified example
        tool_executor.invoke({
            "action": "insert_one",
            "collection": "users",
            "data": {"message": ai_message.content}
        })

        return {"ai_message": ai_message.content}

    workflow = Graph()
    workflow.add_node("extract_and_store", extract_and_store_data)
    workflow.set_entry_point("extract_and_store")

    return workflow

# Usage
# workflow = create_onboarding_workflow(db_handler)
# result = workflow.invoke({"human_message": "Hello, I'm John and I'm good at programming."})
