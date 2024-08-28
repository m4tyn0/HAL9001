from bson import ObjectId
from database.models.checkin import CheckIn


class CheckInRepository:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.checkins

    def create(self, checkin):
        result = self.collection.insert_one(checkin.to_dict())
        return str(result.inserted_id)

    def find_by_id(self, checkin_id):
        checkin_data = self.collection.find_one({"_id": ObjectId(checkin_id)})
        return CheckIn(**checkin_data) if checkin_data else None

    def find_by_user(self, user_id):
        checkins = self.collection.find({"user_id": ObjectId(user_id)})
        return [CheckIn(**checkin) for checkin in checkins]

    def update(self, checkin):
        self.collection.update_one({"_id": checkin._id}, {
                                   "$set": checkin.to_dict()})

    def delete(self, checkin_id):
        self.collection.delete_one({"_id": ObjectId(checkin_id)})
