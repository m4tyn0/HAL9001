from bson import ObjectId
from database.models.user import User


class UserRepository:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.users

    def create(self, user):
        result = self.collection.insert_one(user.to_dict())
        return str(result.inserted_id)

    def find_by_id(self, user_id):
        user_data = self.collection.find_one({"_id": ObjectId(user_id)})
        return User(**user_data) if user_data else None

    def find_by_username(self, username):
        user_data = self.collection.find_one({"username": username})
        return User(**user_data) if user_data else None

    def update(self, user):
        self.collection.update_one({"_id": user._id}, {"$set": user.to_dict()})

    def delete(self, user_id):
        self.collection.delete_one({"_id": ObjectId(user_id)})
