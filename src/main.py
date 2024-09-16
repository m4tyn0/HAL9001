# main.py
import os
from dotenv import load_dotenv
from cli.cli import create_cli
import logging

# Load environment variables from .env file
load_dotenv()

# Ensure these environment variables are set in your .env file
required_env_vars = [
    "NEO4J_URI",
    "NEO4J_USERNAME",
    "NEO4J_PASSWORD",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "SQLITE_PATH"
]


def check_environment_variables():
    missing_vars = [var for var in required_env_vars if var not in os.environ]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {
                         ', '.join(missing_vars)}")


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        check_environment_variables()

        # Create and run the CLI
        cli = create_cli()
        cli()
    except Exception as e:
        logging.error(f"An error occurred while running the application: {
                      e}", exc_info=True)


if __name__ == '__main__':
    main()
