from datetime import datetime
from bson import ObjectId


class Project:
    def __init__(self, user_id, name, description, status, start_date, end_date, tasks=None, skills=None, logs=None, xp_gain=0, tags=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.user_id = user_id
        self.name = name
        self.description = description
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.tasks = tasks if tasks else []
        self.skills = skills if skills else []
        self.logs = logs if logs else []
        self.xp_gain = xp_gain
        self.tags = tags if tags else []

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "tasks": self.tasks,
            "skills": self.skills,
            "logs": self.logs,
            "xp_gain": self.xp_gain,
            "tags": self.tags
        }
