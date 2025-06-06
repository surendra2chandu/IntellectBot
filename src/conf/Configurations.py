# from src.logger.Logger import Logger
import os
from pathlib import Path
import logging
import os

# Set up logging configuration(Set the logging level to INFO)
logging.basicConfig(level=logging.INFO)

# Get the logger
logger = logging.getLogger()

# Define base url for invoking the llama3 model through ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")


# Define the default LLM model to be used
DEFAULT_LLAMA_MODEL = os.getenv("DEFAULT_LLAMA_MODEL", "llama3.2:1b")

# Define verbose mode
VERBOSE = os.getenv("VERBOSE", False)


# Define the database configuration
db_config = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": 5432,
    }
