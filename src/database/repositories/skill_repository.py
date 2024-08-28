from bson import ObjectId
from database.models.skill import Skill


class SkillRepository:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.skills

    def create(self, skill):
        result = self.collection.insert_one(skill.to_dict())
        return str(result.inserted_id)

    def find_by_id(self, skill_id):
        skill_data = self.collection.find_one({"_id": ObjectId(skill_id)})
        return Skill(**skill_data) if skill_data else None

    def find_by_user(self, user_id):
        skills = self.collection.find({"user_id": ObjectId(user_id)})
        return [Skill(**skill) for skill in skills]

    def update(self, skill):
        self.collection.update_one(
            {"_id": skill._id}, {"$set": skill.to_dict()})

    def delete(self, skill_id):
        self.collection.delete_one({"_id": ObjectId(skill_id)})
