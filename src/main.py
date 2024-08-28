# src/main.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from cli.cli import create_cli
from engine.command_handler import CommandHandler

# Load environment variables from .env file
load_dotenv()


def create_app():
    # Get MongoDB URI and database name from environment variables
    mongodb_uri = os.getenv('MONGODB_URI')
    db_name = os.getenv('MONGODB_DATABASE')

    if not mongodb_uri:
        raise ValueError("MONGODB_URI environment variable is not set")
    if not db_name:
        raise ValueError("MONGODB_DATABASE environment variable is not set")

    client = MongoClient(mongodb_uri)
    db = client[db_name]  # Explicitly select the database
    command_handler = CommandHandler(db)
    return create_cli(command_handler)


if __name__ == '__main__':
    cli = create_app()
    cli()  # This invokes the Click command group
