from bson import ObjectId
from database.models.task import Task


class TaskRepository:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.tasks

    def create(self, task):
        result = self.collection.insert_one(task.to_dict())
        return str(result.inserted_id)

    def find_by_id(self, task_id):
        task_data = self.collection.find_one({"_id": ObjectId(task_id)})
        return Task(**task_data) if task_data else None

    def find_by_user(self, user_id):
        tasks = self.collection.find({"user_id": ObjectId(user_id)})
        return [Task(**task) for task in tasks]

    def find_by_project(self, project_id):
        tasks = self.collection.find({"project_id": ObjectId(project_id)})
        return [Task(**task) for task in tasks]

    def update(self, task):
        self.collection.update_one({"_id": task._id}, {"$set": task.to_dict()})

    def delete(self, task_id):
        self.collection.delete_one({"_id": ObjectId(task_id)})
