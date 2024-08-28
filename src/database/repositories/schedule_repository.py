from bson import ObjectId
from database.models.schedule import Schedule


class ScheduleRepository:
    def __init__(self, database):
        self.db = database
        self.collection = self.db.schedules

    def create(self, schedule):
        result = self.collection.insert_one(schedule.to_dict())
        return str(result.inserted_id)

    def find_by_id(self, schedule_id):
        schedule_data = self.collection.find_one(
            {"_id": ObjectId(schedule_id)})
        return Schedule(**schedule_data) if schedule_data else None

    def find_by_user_and_date(self, user_id, date):
        schedule_data = self.collection.find_one(
            {"user_id": ObjectId(user_id), "date": date})
        return Schedule(**schedule_data) if schedule_data else None

    def update(self, schedule):
        self.collection.update_one({"_id": schedule._id}, {
                                   "$set": schedule.to_dict()})

    def delete(self, schedule_id):
        self.collection.delete_one({"_id": ObjectId(schedule_id)})
