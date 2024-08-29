from datetime import datetime
from bson import ObjectId


class Task:
    def __init__(self, user_id, name, description, status, priority, due_date, project_id=None, estimated_time=0, actual_time=0, tags=None, created_at=None, completed_at=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.user_id = user_id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.created_at = created_at if created_at else datetime.utcnow()
        self.completed_at = completed_at
        self.estimated_time = estimated_time
        self.actual_time = actual_time
        self.tags = tags if tags else []


    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "estimated_time": self.estimated_time,
            "actual_time": self.actual_time,
            "tags": self.tags
        }
