from datetime import datetime
from bson import ObjectId


class Log:
    def __init__(self, user_id, entry, project_id=None, skill_id=None, tags=None, timestamp=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.user_id = user_id
        self.timestamp = timestamp if timestamp else datetime.utcnow()
        self.entry = entry
        self.project_id = project_id
        self.skill_id = skill_id
        self.tags = tags if tags else []

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "entry": self.entry,
            "project_id": self.project_id,
            "skill_id": self.skill_id,
            "tags": self.tags
        }
