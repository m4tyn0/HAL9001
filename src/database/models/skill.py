from bson import ObjectId


class Skill:
    def __init__(self, user_id, name, description, level, xp, projects=None, logs=None, tags=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.user_id = user_id
        self.name = name
        self.description = description
        self.level = level
        self.xp = xp
        self.projects = projects if projects else []
        self.logs = logs if logs else []
        self.tags = tags if tags else []

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "xp": self.xp,
            "projects": self.projects,
            "logs": self.logs,
            "tags": self.tags
        }
