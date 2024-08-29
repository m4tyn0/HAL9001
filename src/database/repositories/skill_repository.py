# src/database/repositories/skill_repository.py

from bson import ObjectId
from database.models.skill import Skill


class SkillRepository:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.skills

    # ... (existing methods)

    def find_children(self, skill_id):
        children = self.collection.find({"parent": str(skill_id)})
        return [Skill(**child) for child in children]

    def update_hierarchy(self, skill_id, parent_id=None, child_ids=None):
        update = {}
        if parent_id is not None:
            update["parent"] = str(parent_id)
        if child_ids is not None:
            update["children"] = [str(child_id) for child_id in child_ids]

        self.collection.update_one(
            {"_id": ObjectId(skill_id)}, {"$set": update})
