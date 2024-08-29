# src/database/repositories/routine_repository.py

from bson import ObjectId
from database.models.routine import Routine


class RoutineRepository:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.routines

    def create(self, routine):
        result = self.collection.insert_one(routine.to_dict())
        return str(result.inserted_id)

    def find_by_id(self, routine_id):
        routine_data = self.collection.find_one({"_id": ObjectId(routine_id)})
        return Routine(**routine_data) if routine_data else None

    def find_by_user(self, user_id):
        routines = self.collection.find({"user_id": ObjectId(user_id)})
        return [Routine(**routine) for routine in routines]

    def update(self, routine):
        self.collection.update_one({"_id": routine._id}, {
                                   "$set": routine.to_dict()})

    def delete(self, routine_id):
        self.collection.delete_one({"_id": ObjectId(routine_id)})

    def add_task_to_routine(self, routine_id, task_id):
        self.collection.update_one(
            {"_id": ObjectId(routine_id)},
            {"$addToSet": {"task_ids": str(task_id)}}
        )

    def remove_task_from_routine(self, routine_id, task_id):
        self.collection.update_one(
            {"_id": ObjectId(routine_id)},
            {"$pull": {"task_ids": str(task_id)}}
        )
