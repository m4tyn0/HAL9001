# src/database/repositories/protocol_repository.py

from bson import ObjectId
from database.models.protocol import Protocol


class ProtocolRepository:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.protocols

    def create(self, protocol):
        result = self.collection.insert_one(protocol.to_dict())
        return str(result.inserted_id)

    def find_by_id(self, protocol_id):
        protocol_data = self.collection.find_one(
            {"_id": ObjectId(protocol_id)})
        return Protocol.from_dict(protocol_data) if protocol_data else None

    def find_by_user(self, user_id):
        protocol_data = self.collection.find_one(
            {"user_id": ObjectId(user_id)})
        return Protocol.from_dict(protocol_data) if protocol_data else None

    def update(self, protocol):
        self.collection.update_one(
            {"_id": protocol._id},
            {"$set": protocol.to_dict()}
        )

    def delete(self, protocol_id):
        self.collection.delete_one({"_id": ObjectId(protocol_id)})

    def get_active_projects(self, user_id):
        return self.db.projects.aggregate([
            {"$match": {"user_id": ObjectId(user_id), "status": "active"}},
            {"$project": {"_id": 1, "name": 1, "description": 1}}
        ])

    def get_upcoming_tasks(self, user_id):
        return self.db.tasks.aggregate([
            {"$match": {
                "user_id": ObjectId(user_id),
                "due_date": {"$gte": datetime.utcnow()},
                "status": {"$ne": "completed"}
            }},
            {"$project": {"_id": 1, "name": 1, "description": 1, "due_date": 1}},
            {"$sort": {"due_date": 1}},
            {"$limit": 10}  # Adjust as needed
        ])
