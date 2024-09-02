# main.py
import os
from dotenv import load_dotenv
from cli.cli import create_cli
from agents.chat_agent import create_agent
from engine.command_handler import CommandHandler 

# Load environment variables from .env file
load_dotenv()

# Ensure these environment variables are set in your .env file
required_env_vars = [
    "MONGODB_URI",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY"
]


def check_environment_variables():
    missing_vars = [var for var in required_env_vars if var not in os.environ]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


def create_app():
    check_environment_variables()
    agent = create_agent()
    command_handler = CommandHandler(agent)
    return create_cli(command_handler)


def main():
    try:
        cli = create_app()
        cli()
    except Exception as e:
        print(f"An error occurred while starting the application: {e}")
        exit(1)


if __name__ == '__main__':
    main()
