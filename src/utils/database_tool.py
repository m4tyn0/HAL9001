# src/utils/database_tool.py

from typing import Dict, Any, Type
from langchain.tools import StructuredTool
from langchain.pydantic_v1 import BaseModel, Field, PrivateAttr
from database.handlers.database_handler import DatabaseHandler


class DatabaseInput(BaseModel):
    action: str = Field(
        ..., description="The database action to perform (e.g., 'insert_one', 'find_one', etc.)")
    collection: str = Field(...,
                            description="The name of the collection to operate on")
    data: Dict[str, Any] = Field(
        ..., description="The data for the operation (e.g., document to insert, query to find)")
    limit: int = Field(
        default=0, description="Limit for find_many operation")


class DatabaseTool(StructuredTool):
    name: str = "database_tool"
    description: str = "Use this tool to interact with the database. Available actions: insert_one, insert_many, find_one, find_many, update_one, update_many, delete_one, delete_many, count_documents"
    args_schema: Type[BaseModel] = DatabaseInput
    _db_handler: DatabaseHandler = PrivateAttr()

    def __init__(self, db_handler: DatabaseHandler):
        super().__init__(
            name=self.name,
            description=self.description,
            args_schema=self.args_schema,
            func=self._run
        )
        self._db_handler = db_handler

    def _run(self, action: str, collection: str, data: Dict[str, Any], limit: int = 0) -> Dict[str, Any]:
        try:
            method = getattr(self._db_handler, action, None)
            if method is None:
                return {"status": "error", "message": f"Unsupported database action: {action}"}

            if action == 'find_many':
                result = method(collection, data, limit)
            elif action in ['insert_many', 'update_many', 'delete_many']:
                result = method(collection, data)
            else:
                result = method(collection, data)

            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def _arun(self, action: str, collection: str, data: Dict[str, Any], limit: int = 0) -> Dict[str, Any]:
        # If you need async support, implement it here
        # For now, we'll just call the sync version
        return self._run(action, collection, data, limit)


def create_database_tool(database):
    db_handler = DatabaseHandler(database)
    return DatabaseTool(db_handler=db_handler)
