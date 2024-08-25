from langchain_core.messages import AIMessage
from ..agent_types import AgentState



def player_manager(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    messages = state["messages"]
    last_message = messages[-1].content.lower()

    if "view stats" in last_message:
        return view_player_stats(state)
    elif "add skill" in last_message:
        return add_skill(state)
    elif "level up" in last_message:
        return level_up(state)
    elif "gain xp" in last_message:
        return gain_xp(state)
    elif "view skills" in last_message:
        return view_skills(state)
    else:
        response = "I can help you manage your player profile. You can ask me to view stats, add a skill, level up, gain XP, or view skills. What would you like to do?"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def view_player_stats(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    player_data = data_manager.load_player_data()

    response = f"Player: {player_data['name']}\n"
    response += f"Overall Level: {player_data['overall_level']}\n"
    response += f"Total XP: {player_data['total_xp']}\n"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def add_skill(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    player_data = data_manager.load_player_data()

    skill_name = input("Enter the name of the new skill: ")

    if any(skill['name'] == skill_name for skill in player_data['skills']):
        response = f"The skill '{skill_name}' already exists."
    else:
        new_skill = {
            "name": skill_name,
            "level": 1,
            "xp": 0,
            "xp_to_next_level": 100
        }
        player_data['skills'].append(new_skill)
        data_manager.save_player_data(player_data)
        response = f"New skill '{skill_name}' has been added successfully."

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def level_up(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    player_data = data_manager.load_player_data()

    skill_name = input("Enter the name of the skill to level up: ")

    skill = next(
        (s for s in player_data['skills'] if s['name'] == skill_name), None)
    if skill:
        if skill['xp'] >= skill['xp_to_next_level']:
            skill['level'] += 1
            skill['xp'] -= skill['xp_to_next_level']
            # Increase XP needed for next level
            skill['xp_to_next_level'] = int(skill['xp_to_next_level'] * 1.5)
            data_manager.save_player_data(player_data)
            response = f"Congratulations! Your '{
                skill_name}' skill has leveled up to level {skill['level']}!"
        else:
            response = f"Not enough XP to level up '{skill_name}'. You need {
                skill['xp_to_next_level'] - skill['xp']} more XP."
    else:
        response = f"Skill '{skill_name}' not found."

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def gain_xp(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    player_data = data_manager.load_player_data()

    skill_name = input("Enter the name of the skill to gain XP: ")
    xp_gained = int(input("Enter the amount of XP gained: "))

    skill = next(
        (s for s in player_data['skills'] if s['name'] == skill_name), None)
    if skill:
        skill['xp'] += xp_gained
        player_data['total_xp'] += xp_gained
        data_manager.save_player_data(player_data)
        data_manager.log_xp_gain(
            player_data['name'], skill_name, xp_gained, "Manual Entry")
        response = f"Added {xp_gained} XP to '{skill_name}'. Current XP: {
            skill['xp']}/{skill['xp_to_next_level']}"
    else:
        response = f"Skill '{skill_name}' not found."

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state


def view_skills(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    player_data = data_manager.load_player_data()

    response = "Your skills:\n"
    for skill in player_data['skills']:
        response += f"- {skill['name']}: Level {skill['level']
                                                }, XP: {skill['xp']}/{skill['xp_to_next_level']}\n"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state
