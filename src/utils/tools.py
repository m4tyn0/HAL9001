from langchain_core.tools import tool
from database.handlers.mongodb_store import mongodb_store
from langchain_core.documents import Document


@tool
def add_project(name: str, description: str, status: str = "New"):
    """Add a new project to the database."""
    project = Document(page_content=description, metadata={
                       "name": name, "status": status, "type": "project"})
    mongodb_store.add_documents([project])
    return f"Project '{name}' added successfully."


@tool
def get_project_details(name: str):
    """Get details of a specific project."""
    results = mongodb_store.similarity_search(f"project {name}", k=1)
    if results:
        project = results[0]
        return f"Project: {project.metadata['name']}\nDescription: {project.page_content}\nStatus: {project.metadata['status']}"
    return f"No project found with name '{name}'."


@tool
def update_project(name: str, description: str = "", status: str = ""):
    """Update an existing project in the database."""
    results = mongodb_store.similarity_search(f"project {name}", k=1)
    if results:
        project = results[0]
        if description:
            project.page_content = description
        if status:
            project.metadata['status'] = status
        # This will update the existing document
        mongodb_store.add_documents([project])
        return f"Project '{name}' updated successfully."
    return f"No project found with name '{name}'. Update failed."


@tool
def add_task(title: str, description: str, status: str = "New", deadline: str = ""):
    """Add a new task to the database."""
    task = Document(page_content=description, metadata={
                    "title": title, "status": status, "deadline": deadline, "type": "task"})
    mongodb_store.add_documents([task])
    return f"Task '{title}' added successfully."


@tool
def get_tasks(status: str = ""):
    """Get all tasks, optionally filtered by status."""
    query = "task"
    if status:
        query += f" status:{status}"
    results = mongodb_store.similarity_search(
        query, k=10)  # Adjust k as needed
    if results:
        tasks = [f"Task: {task.metadata['title']}, Status: { task.metadata['status']}, Deadline: {task.metadata['deadline']}" for task in results]
        return "\n".join(tasks)
    return "No tasks found."


@tool
def add_schedule_entry(date: str, title: str, start_time: str, end_time: str):
    """Add a new schedule entry to the database."""
    entry = Document(page_content=title, metadata={
                     "date": date, "start_time": start_time, "end_time": end_time, "type": "schedule_entry"})
    mongodb_store.add_documents([entry])
    return f"Schedule entry '{title}' for {date} added successfully."


@tool
def get_schedule(date: str):
    """Get schedule entries for a specific date."""
    results = mongodb_store.similarity_search(
        f"schedule_entry date:{date}", k=10)  # Adjust k as needed
    if results:
        entries = [f"{entry.page_content}: {entry.metadata['start_time']} - {entry.metadata['end_time']}" for entry in results]
        return f"Schedule for {date}:\n" + "\n".join(entries)
    return f"No schedule entries found for {date}."


@tool
def update_schedule_entry(date: str, title: str, start_time: str = "", end_time: str = ""):
    """Update an existing schedule entry in the database."""
    results = mongodb_store.similarity_search(
        f"schedule_entry date:{date} {title}", k=1)
    if results:
        entry = results[0]
        if start_time:
            entry.metadata['start_time'] = start_time
        if end_time:
            entry.metadata['end_time'] = end_time
        # This will update the existing document
        mongodb_store.add_documents([entry])
        return f"Schedule entry '{title}' for {date} updated successfully."
    return f"No schedule entry found for '{title}' on {date}. Update failed."


def get_tools():
    return [
        add_project,
        get_project_details,
        update_project,
        add_task,
        get_tasks,
        add_schedule_entry,
        get_schedule,
        update_schedule_entry
    ]
