# src/database/models/protocol.py
from datetime import datetime
from bson import ObjectId


class Protocol:
    def __init__(self, user_id, time_blocks=None, recurring_events=None, preferences=None, _id=None):
        self._id = _id if _id else ObjectId()
        self.user_id = user_id
        self.time_blocks = time_blocks if time_blocks else []
        self.recurring_events = recurring_events if recurring_events else []
        self.preferences = preferences if preferences else {}
        self.last_updated = datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "time_blocks": self.time_blocks,
            "recurring_events": self.recurring_events,
            "preferences": self.preferences,
            "last_updated": self.last_updated
        }

    @classmethod
    def from_dict(cls, data):
        protocol = cls(
            user_id=data['user_id'],
            time_blocks=data.get('time_blocks', []),
            recurring_events=data.get('recurring_events', []),
            preferences=data.get('preferences', {}),
            _id=data.get('_id')
        )
        protocol.last_updated = data.get('last_updated', datetime.utcnow())
        return protocol
