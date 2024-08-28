from datetime import datetime
from bson import ObjectId


class CheckIn:
    def __init__(self, user_id, mood, notes, projects=None, skills=None, tags=None, timestamp=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.user_id = user_id
        self.timestamp = timestamp if timestamp else datetime.utcnow()
        self.mood = mood
        self.notes = notes
        self.projects = projects if projects else []
        self.skills = skills if skills else []
        self.tags = tags if tags else []

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "mood": self.mood,
            "notes": self.notes,
            "projects": self.projects,
            "skills": self.skills,
            "tags": self.tags
        }
