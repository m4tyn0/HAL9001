from bson import ObjectId
from database.models.project import Project


class ProjectRepository:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.projects

    def create(self, project):
        result = self.collection.insert_one(project.to_dict())
        return str(result.inserted_id)

    def find_by_id(self, project_id):
        project_data = self.collection.find_one({"_id": ObjectId(project_id)})
        return Project(**project_data) if project_data else None

    def find_by_user(self, user_id):
        projects = self.collection.find({"user_id": ObjectId(user_id)})
        return [Project(**project) for project in projects]

    def update(self, project):
        self.collection.update_one({"_id": project._id}, {
                                   "$set": project.to_dict()})

    def delete(self, project_id):
        self.collection.delete_one({"_id": ObjectId(project_id)})
