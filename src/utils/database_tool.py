# src/tools/database_tool.py

from langgraph.prebuilt import Tool
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class DatabaseHandler(ABC):
    @abstractmethod
    async def insert_one(self, collection: str, document: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    async def insert_many(self, collection: str, documents: List[Dict[str, Any]]) -> List[str]:
        pass

    @abstractmethod
    async def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def find_many(self, collection: str, query: Dict[str, Any], limit: int = 0) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def update_one(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    async def update_many(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    async def delete_one(self, collection: str, query: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    async def delete_many(self, collection: str, query: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    async def count_documents(self, collection: str, query: Dict[str, Any]) -> int:
        pass


class DatabaseTool(Tool):
    def __init__(self, db_handler: DatabaseHandler):
        super().__init__(
            name="DatabaseTool",
            description="Tool for interacting with the database",
            function=self.execute
        )
        self.db = db_handler
        self.actions = {
            "insert_one": self._insert_one,
            "insert_many": self._insert_many,
            "find_one": self._find_one,
            "find_many": self._find_many,
            "update_one": self._update_one,
            "update_many": self._update_many,
            "delete_one": self._delete_one,
            "delete_many": self._delete_many,
            "count_documents": self._count_documents
        }

    async def execute(self, action: str, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if action not in self.actions:
                return {"status": "error", "message": f"Unsupported database action: {action}"}

            result = await self.actions[action](collection, data)
            return {"status": "success", **result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _insert_one(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.db.insert_one(collection, data)
        return {"inserted_id": result}

    async def _insert_many(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.db.insert_many(collection, data)
        return {"inserted_ids": result}

    async def _find_one(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.db.find_one(collection, data)
        return {"result": result}

    async def _find_many(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        limit = data.pop("limit", 0)
        result = await self.db.find_many(collection, data, limit)
        return {"results": result}

    async def _update_one(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        query = data["query"]
        update = data["update"]
        result = await self.db.update_one(collection, query, update)
        return {"modified_count": result}

    async def _update_many(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        query = data["query"]
        update = data["update"]
        result = await self.db.update_many(collection, query, update)
        return {"modified_count": result}

    async def _delete_one(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.db.delete_one(collection, data)
        return {"deleted_count": result}

    async def _delete_many(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.db.delete_many(collection, data)
        return {"deleted_count": result}

    async def _count_documents(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.db.count_documents(collection, data)
        return {"count": result}
