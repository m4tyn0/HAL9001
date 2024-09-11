# main.py
import os
from dotenv import load_dotenv
from cli.cli import create_cli
from engine.command_handler import CommandHandler
from database.handlers.neo4j import Neo4jDatabase

# Load environment variables from .env file
load_dotenv()

# Ensure these environment variables are set in your .env file
required_env_vars = [
    "NEO4J_URI",
    "NEO4J_USERNAME",
    "NEO4J_PASSWORD",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY"
]


def check_environment_variables():
    missing_vars = [var for var in required_env_vars if var not in os.environ]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {
                         ', '.join(missing_vars)}")


def create_app():
    load_dotenv()
    check_environment_variables()

    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    try:
        db = Neo4jDatabase(uri, user, password)
    except ConnectionError as e:
        print(f"Failed to connect to Neo4j database: {e}")
        exit(1)
    except ValueError as e:
        print(f"Authentication error: {e}")
        exit(1)
    try:
        command_handler = CommandHandler(db)
    except Exception as e:
        print(e)
    return create_cli(command_handler)


def main():
    try:
        cli = create_app()
        cli()
    except Exception as e:
        print(f"An error occurred while starting the application: {e}")


if __name__ == '__main__':
    main()
