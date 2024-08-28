from datetime import date, time
from bson import ObjectId


class Schedule:
    def __init__(self, user_id, date, tasks=None, tags=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.user_id = user_id
        self.date = date
        self.tasks = tasks if tasks else []
        self.tags = tags if tags else []

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "date": self.date,
            "tasks": [
                {
                    "task_id": task["task_id"],
                    "start_time": task["start_time"],
                    "end_time": task["end_time"]
                } for task in self.tasks
            ],
            "tags": self.tags
        }
