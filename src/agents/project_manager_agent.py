from datetime import datetime, timedelta
from langchain_core.messages import AIMessage
from ..agent_types import AgentState


def project_manager(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    messages = state["messages"]
    last_message = messages[-1].content.lower()

    if "add project" in last_message:
        return add_project(state)
    elif "view projects" in last_message:
        return view_projects(state)
    elif "update project" in last_message:
        return update_project(state)
    elif "add task" in last_message:
        return add_task(state)
    elif "view tasks" in last_message:
        return view_tasks(state)
    elif "update task" in last_message:
        return update_task(state)
    else:
        response = "I can help you manage your projects. You can ask me to add a project, view projects, update a project, add a task, view tasks, or update a task. What would you like to do?"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state

def add_project(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    
    # Collect project details
    name = input("Project name: ")
    description = input("Project description: ")
    priority = int(input("Priority (1-5, 5 being highest): "))
    due_date_str = input("Due date (YYYY-MM-DD): ")
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    estimated_time = int(input("Estimated time (in hours): "))
    xp_reward = int(input("XP reward: "))

    # Add project to database
    project_id = data_manager.add_project(name, description, priority, due_date, estimated_time, xp_reward)

    response = f"Project '{name}' has been added successfully with ID {project_id}."
    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state

def view_projects(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    projects = data_manager.get_projects_and_tasks()

    response = "Here are your current projects:\n"
    for project in projects:
        project_id, name, description, status, priority, due_date, estimated_time, xp_reward = project[:8]
        response += f"- ID: {project_id}, Name: {name}\n"
        response += f"  Status: {status}, Priority: {priority}, Due: {due_date}\n"
        response += f"  Estimated Time: {estimated_time} hours, XP Reward: {xp_reward}\n\n"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state

def update_project(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    
    project_id = int(input("Enter the ID of the project you want to update: "))
    
    # TODO: Implement logic to update project details
    # For now, we'll just update the status as an example
    new_status = input("Enter the new status for the project: ")
    
    # Assume we have a method to update project status
    data_manager.update_project_status(project_id, new_status)

    response = f"Project with ID {project_id} has been updated. New status: {new_status}"
    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state

def add_task(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    
    project_id = int(input("Enter the ID of the project this task belongs to: "))
    name = input("Task name: ")
    description = input("Task description: ")
    priority = int(input("Priority (1-5, 5 being highest): "))
    estimated_time = int(input("Estimated time (in hours): "))
    xp_reward = int(input("XP reward: "))

    task_id = data_manager.add_task(project_id, name, description, priority, estimated_time, xp_reward)

    response = f"Task '{name}' has been added successfully to project {project_id} with ID {task_id}."
    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state

def view_tasks(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    projects_and_tasks = data_manager.get_projects_and_tasks()

    response = "Here are your current tasks grouped by project:\n"
    current_project_id = None
    for item in projects_and_tasks:
        project_id, project_name = item[0], item[1]
        task_id, task_name, task_description, task_status, task_priority, task_estimated_time, task_xp_reward = item[8:]
        
        if project_id != current_project_id:
            response += f"\nProject: {project_name} (ID: {project_id})\n"
            current_project_id = project_id
        
        if task_id:
            response += f"- Task ID: {task_id}, Name: {task_name}\n"
            response += f"  Status: {task_status}, Priority: {task_priority}\n"
            response += f"  Estimated Time: {task_estimated_time} hours, XP Reward: {task_xp_reward}\n"

    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state

def update_task(state: AgentState) -> AgentState:
    data_manager = state["data_manager"]
    
    task_id = int(input("Enter the ID of the task you want to update: "))
    
    # TODO: Implement logic to update task details
    # For now, we'll just update the status as an example
    new_status = input("Enter the new status for the task: ")
    
    # Assume we have a method to update task status
    data_manager.update_task_status(task_id, new_status)

    response = f"Task with ID {task_id} has been updated. New status: {new_status}"
    state["messages"].append(AIMessage(content=response))
    print(f"Assistant: {response}")
    return state