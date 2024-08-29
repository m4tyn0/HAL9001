# src/database/models/routine.py

from bson import ObjectId
from datetime import timedelta


class Routine:
    def __init__(self, user_id, name, task_ids, description="", _id=None):
        self._id = _id if _id else ObjectId()
        self.user_id = user_id
        self.name = name
        self.task_ids = task_ids  # List of Task ObjectIds
        self.description = description

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "name": self.name,
            "task_ids": [str(task_id) for task_id in self.task_ids],
            "description": self.description
        }
