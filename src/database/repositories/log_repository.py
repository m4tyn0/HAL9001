from bson import ObjectId
from database.models.log import Log


class LogRepository:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.logs

    def create(self, log):
        result = self.collection.insert_one(log.to_dict())
        return str(result.inserted_id)

    def find_by_id(self, log_id):
        log_data = self.collection.find_one({"_id": ObjectId(log_id)})
        return Log(**log_data) if log_data else None

    def find_by_user(self, user_id):
        logs = self.collection.find({"user_id": ObjectId(user_id)})
        return [Log(**log) for log in logs]

    def find_by_project(self, project_id):
        logs = self.collection.find({"project_id": ObjectId(project_id)})
        return [Log(**log) for log in logs]

    def update(self, log):
        self.collection.update_one({"_id": log._id}, {"$set": log.to_dict()})

    def delete(self, log_id):
        self.collection.delete_one({"_id": ObjectId(log_id)})
