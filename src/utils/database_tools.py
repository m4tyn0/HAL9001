from langchain_core.tools import tool
from database.handlers.database_handler import DatabaseHandler


class DatabaseTools:
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

    @tool
    def query_database(self, action: str, collection: str, query: dict) -> str:
        """Query the database with the given parameters."""
        method = getattr(self.db_handler, action, None)
        if method is None:
            return f"Error: Unsupported database action: {action}"
        result = method(collection, query)
        return f"Database {action} result: {result}"

    @tool
    def insert_document(self, collection: str, document: dict) -> str:
        """Insert a document into the specified collection."""
        result = self.db_handler.insert_one(collection, document)
        return f"Document inserted with ID: {result}"

    @tool
    def update_document(self, collection: str, query: dict, update: dict) -> str:
        """Update a document in the specified collection."""
        result = self.db_handler.update_one(collection, query, update)
        return f"Updated {result} document(s)"

    @tool
    def delete_document(self, collection: str, query: dict) -> str:
        """Delete a document from the specified collection."""
        result = self.db_handler.delete_one(collection, query)
        return f"Deleted {result} document(s)"
