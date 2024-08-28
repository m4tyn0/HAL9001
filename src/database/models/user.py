from datetime import datetime
from bson import ObjectId


class User:
    def __init__(self, username, email, password_hash, created_at=None, last_login=None, settings=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at if created_at else datetime.utcnow()
        self.last_login = last_login
        self.settings = settings if settings else {
            "theme": "default",
            "notification_preferences": {}
        }

    def to_dict(self):
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "settings": self.settings
        }
