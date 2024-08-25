from langchain_core.messages import AIMessage
from datetime import datetime, timedelta
from ..agent_types import AgentState



def goal_tracker(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    messages = state["messages"]
    last_message = messages[-1].content.lower()

    if "add goal" in last_message:
        return add_goal(state)
    elif "view goals" in last_message:
        return view_goals(state)
    elif "update goal" in last_message:
        return update_goal(state)
    elif "complete goal" in last_message:
        return complete_goal(state)
    else:
        response = "I can help you track your goals. You can ask me to add a goal, view goals, update a goal, or complete a goal. What would you like to do?"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def add_goal(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]

    description = input("Enter your goal description: ")
    start_date = datetime.now().date()
    end_date_str = input("Enter the target completion date (YYYY-MM-DD): ")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    goal_id = data_manager.add_goal(description, start_date, end_date)

    response = f"Goal added successfully with ID {
        goal_id}. Good luck achieving it!"
    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def view_goals(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]

    goals = data_manager.get_goals()

    if not goals:
        response = "You don't have any goals set at the moment."
    else:
        response = "Here are your current goals:\n"
        for goal in goals:
            goal_id, description, start_date, end_date, status = goal
            response += f"- ID: {goal_id}, Status: {status}\n"
            response += f"  Description: {description}\n"
            response += f"  Start Date: {start_date}, Target Completion: {end_date}\n\n"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def update_goal(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]

    goal_id = int(input("Enter the ID of the goal you want to update: "))
    new_description = input(
        "Enter the new description (press Enter to keep current): ")
    new_end_date_str = input(
        "Enter the new target completion date (YYYY-MM-DD, press Enter to keep current): ")

    # TODO: Implement logic to update goal details in data_manager
    # For now, we'll just update the status as an example
    new_status = input("Enter the new status for the goal: ")
    data_manager.update_goal_status(goal_id, new_status)

    response = f"Goal with ID {
        goal_id} has been updated. New status: {new_status}"
    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def complete_goal(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]

    goal_id = int(input("Enter the ID of the goal you've completed: "))

    # TODO: Implement logic to mark goal as completed and possibly award XP
    data_manager.update_goal_status(goal_id, "Completed")

    response = f"Congratulations! Goal with ID {
        goal_id} has been marked as completed."
    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state
