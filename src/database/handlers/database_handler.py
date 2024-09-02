from typing import Dict, List, Any, Optional
from bson import ObjectId


class DatabaseHandler:
    def __init__(self, database):
        self.db = database

    def insert_one(self, collection: str, document: Dict[str, Any]) -> str:
        result = self.db[collection].insert_one(document)
        return str(result.inserted_id)

    def insert_many(self, collection: str, documents: List[Dict[str, Any]]) -> List[str]:
        result = self.db[collection].insert_many(documents)
        return [str(id) for id in result.inserted_ids]

    def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = self.db[collection].find_one(query)
        if result:
            result['_id'] = str(result['_id'])  # Convert ObjectId to string
        return result

    def find_many(self, collection: str, query: Dict[str, Any], limit: int = 0) -> List[Dict[str, Any]]:
        cursor = self.db[collection].find(query)
        if limit > 0:
            cursor = cursor.limit(limit)
        results = list(cursor)
        for result in results:
            result['_id'] = str(result['_id'])  # Convert ObjectId to string
        return results

    def update_one(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        result = self.db[collection].update_one(query, {"$set": update})
        return result.modified_count

    def update_many(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        result = self.db[collection].update_many(query, {"$set": update})
        return result.modified_count

    def delete_one(self, collection: str, query: Dict[str, Any]) -> int:
        result = self.db[collection].delete_one(query)
        return result.deleted_count

    def delete_many(self, collection: str, query: Dict[str, Any]) -> int:
        result = self.db[collection].delete_many(query)
        return result.deleted_count

    def count_documents(self, collection: str, query: Dict[str, Any]) -> int:
        return self.db[collection].count_documents(query)
