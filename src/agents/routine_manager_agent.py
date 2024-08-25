from langchain_core.messages import AIMessage
import os
from ..agent_types import AgentState



def routine_manager(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    messages = state["messages"]
    last_message = messages[-1].content.lower()

    if "create routine" in last_message:
        return create_routine(state)
    elif "view routines" in last_message:
        return view_routines(state)
    elif "update routine" in last_message:
        return update_routine(state)
    elif "execute routine" in last_message:
        return execute_routine(state)
    elif "add habit" in last_message:
        return add_habit(state)
    else:
        response = "I can help you manage your routines and habits. You can ask me to create a routine, view routines, update a routine, execute a routine, or add a habit. What would you like to do?"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def create_routine(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]

    routine_name = input("Enter the name for the new routine: ")
    routine_description = input("Enter a brief description of the routine: ")

    habits = []
    while True:
        habit = input(
            "Enter a habit for this routine (or press Enter to finish): ")
        if not habit:
            break
        habits.append(habit)

    routine_content = f"# {routine_name}\n\n{
        routine_description}\n\n## Habits:\n"
    for i, habit in enumerate(habits, 1):
        routine_content += f"{i}. [ ] {habit}\n"

    routine_path = os.path.join(
        data_manager.data_dir, 'routines', f'{routine_name}.md')
    with open(routine_path, 'w') as f:
        f.write(routine_content)

    response = f"Routine '{routine_name}' has been created successfully with {
        len(habits)} habits."
    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def view_routines(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]

    routines_dir = os.path.join(data_manager.data_dir, 'routines')
    routine_files = [f for f in os.listdir(routines_dir) if f.endswith('.md')]

    if not routine_files:
        response = "You don't have any routines set up yet."
    else:
        response = "Here are your current routines:\n"
        for routine_file in routine_files:
            routine_name = routine_file[:-3]  # Remove .md extension
            routine_content = data_manager.get_routine(routine_name)
            habit_count = routine_content.count('[ ]')
            response += f"- {routine_name} ({habit_count} habits)\n"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def update_routine(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]

    routine_name = input("Enter the name of the routine you want to update: ")
    routine_content = data_manager.get_routine(routine_name)

    if routine_content is None:
        response = f"Routine '{routine_name}' not found."
    else:
        print(f"Current routine content:\n{routine_content}\n")
        updated_content = input(
            "Enter the updated routine content (or press Enter to keep current):\n")
        if updated_content:
            routine_path = os.path.join(
                data_manager.data_dir, 'routines', f'{routine_name}.md')
            with open(routine_path, 'w') as f:
                f.write(updated_content)
            response = f"Routine '{
                routine_name}' has been updated successfully."
        else:
            response = "No changes were made to the routine."

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def execute_routine(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]

    routine_name = input("Enter the name of the routine you want to execute: ")
    routine_content = data_manager.get_routine(routine_name)

    if routine_content is None:
        response = f"Routine '{routine_name}' not found."
    else:
        print(f"Executing routine '{routine_name}':")
        habits = [line.strip()[4:] for line in routine_content.split(
            '\n') if line.strip().startswith('[ ]')]

        completed_habits = []
        for habit in habits:
            completion = input(f"Did you complete: {habit}? (yes/no): ")
            if completion.lower() == 'yes':
                completed_habits.append(habit)

        completion_rate = len(completed_habits) / len(habits) if habits else 0
        # Award up to 100 XP for completing the routine
        xp_gained = int(100 * completion_rate)

        # TODO: Implement XP gain in player_manager
        # For now, we'll just log the XP gain
        data_manager.log_xp_gain(data_manager.load_player_data(
        )['name'], 'Routine Execution', xp_gained, routine_name)

        response = f"Routine '{routine_name}' executed. You completed {
            len(completed_habits)} out of {len(habits)} habits and gained {xp_gained} XP."

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def add_habit(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]

    routine_name = input(
        "Enter the name of the routine you want to add a habit to: ")
    routine_content = data_manager.get_routine(routine_name)

    if routine_content is None:
        response = f"Routine '{routine_name}' not found."
    else:
        new_habit = input("Enter the new habit: ")
        routine_lines = routine_content.split('\n')
        habits_index = routine_lines.index(
            "## Habits:") if "## Habits:" in routine_lines else -1

        if habits_index != -1:
            habit_number = sum(
                1 for line in routine_lines[habits_index+1:] if line.strip().startswith('[ ]')) + 1
            routine_lines.insert(habits_index + habit_number,
                                 f"{habit_number}. [ ] {new_habit}")
        else:
            routine_lines.append("\n## Habits:")
            routine_lines.append(f"1. [ ] {new_habit}")

        updated_content = '\n'.join(routine_lines)
        routine_path = os.path.join(
            data_manager.data_dir, 'routines', f'{routine_name}.md')
        with open(routine_path, 'w') as f:
            f.write(updated_content)

        response = f"Habit '{new_habit}' has been added to routine '{
            routine_name}' successfully."

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state
