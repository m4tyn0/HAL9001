from datetime import date
from src.agent_types import AgentState


def scheduler(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    messages = state["messages"]
    last_message = messages[-1].content.lower()

    if "generate schedule" in last_message:
        today = date.today()
        data_manager.generate_daily_schedule(today)
        response = "I've generated today's schedule based on your project priorities and available time. Would you like to review it?"

    elif "view schedule" in last_message:
        today = date.today()
        schedule = data_manager.get_daily_schedule(today)
        response = "Here's your schedule for today:\n"
        for item in schedule:
            response += f"{item[3]}: {item[4]} - {item[5]} ({item[6]})\n"
        response += "\nWould you like to make any changes?"

    elif "update schedule" in last_message:
        # TODO: Implement logic to parse the update request and call update_schedule_item
        response = "I understand you want to update the schedule. Can you tell me which item you'd like to change and how?"

    elif "prioritize" in last_message:
        # TODO: Implement logic to adjust project or task priorities
        response = "I see you want to adjust priorities. Which project or task would you like to prioritize?"

    else:
        response = "I'm here to help with your schedule. You can ask me to generate a schedule, view your schedule, update a schedule item, or adjust priorities. What would you like to do?"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state
