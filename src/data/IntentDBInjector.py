import pandas as pd
from src.conf.Configurations import logger
from src.data.EmbeddingsGenerator import EmbeddingsGenerator
from src.utilities.IntentDatabaseUtility import IntentDatabaseUtility

class IntentDBInjector:
    """
    This class is responsible for injecting intents into the database.
    """

    def __init__(self):
        self._logger = logger

    def inject_intent_data(self, file_path):
        """
        Injects an intent into the database.

        :param file_path: Path to the CSV file containing intent data.
        """

        # Read the CSV file
        self._logger.info(f"Reading intent data from {file_path}...")
        df = pd.read_csv(file_path)

        # Extract columns as lists
        self._logger.info("Extracting queries and intents from the DataFrame...")
        queries = df["query"].tolist()
        intents = df["Intent"].tolist()

        # Generate embeddings for the queries
        self._logger.info("Generating embeddings for the queries...")
        embeddings = EmbeddingsGenerator().get_embeddings(queries)

        # Insert data into the database
        self._logger.info("Inserting data into the database...")
        IntentDatabaseUtility().insert_data(queries, intents, embeddings)

if __name__ == "__main__":
    file = "C:\Docs\sample_intent_queries.csv"

    intent_db_injector = IntentDBInjector()

    intent_db_injector.inject_intent_data(file)