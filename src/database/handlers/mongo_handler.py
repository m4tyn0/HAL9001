# src/database/mongodb_handler.py

from pymongo import MongoClient
from tools.database_tool import DatabaseHandler
from typing import Any, Dict, List, Optional


class MongoDBHandler(DatabaseHandler):
    def __init__(self, connection_string: str, database_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]

    def insert_one(self, collection: str, document: Dict[str, Any]) -> str:
        result = self.db[collection].insert_one(document)
        return str(result.inserted_id)

    def insert_many(self, collection: str, documents: List[Dict[str, Any]]) -> List[str]:
        result = self.db[collection].insert_many(documents)
        return [str(id) for id in result.inserted_ids]

    def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.db[collection].find_one(query)

    def find_many(self, collection: str, query: Dict[str, Any], limit: int = 0) -> List[Dict[str, Any]]:
        cursor = self.db[collection].find(query)
        if limit > 0:
            cursor = cursor.limit(limit)
        return list(cursor)

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
