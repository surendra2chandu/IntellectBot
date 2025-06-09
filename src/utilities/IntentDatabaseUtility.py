from psycopg2.extras import execute_values
from fastapi import HTTPException
from src.conf.Configurations import logger, db_config, ALLOWED_INTENTS  # ALLOWED_INTENTS imported here
import psycopg2


class IntentDatabaseUtility:
    def __init__(self):
        """
        Initializes the database connection.
        """
        try:
            # Set the database configuration
            self.db_config = db_config

            # Connect to the database
            logger.info("Connecting to the database...")
            self.conn = psycopg2.connect(**db_config)
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise HTTPException(status_code=500, detail=f"DB connection error: {e}")

    def __create_table(self):
        """
        Creates the intent_data table if it doesn't exist.
        """
        try:
            # Build the CHECK constraint dynamically from ALLOWED_INTENTS constant
            intents_check = "', '".join(ALLOWED_INTENTS)
            self.cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS intent_data (
                    id SERIAL PRIMARY KEY,
                    query TEXT NOT NULL,
                    intent TEXT CHECK (intent IN ('{intents_check}')),
                    embedding VECTOR
                );
            """)
            self.conn.commit()
            logger.info("intent_data table created successfully.")
        except Exception as e:
            logger.error(f"Error creating table: {e}")
            raise HTTPException(status_code=500, detail=f"Error creating table: {e}")

    def insert_data(self, queries, intents, embeddings):
        """
        Inserts data into the intent_data table after filtering valid intents.

        :param queries: List of query strings.
        :param intents: List of intent labels.
        :param embeddings: List of embedding vectors.
        :return: None
        """
        # Drop the table if it exists
        logger.info("Dropping the table if it exists...")
        self.cursor.execute("DROP TABLE IF EXISTS intent_data;")

        # Create the table if it doesn't exist
        self.__create_table()

        try:
            values = []
            for i, (query, intent, emb) in enumerate(zip(queries, intents, embeddings)):
                if intent not in ALLOWED_INTENTS:
                    logger.info(f"Row {i + 1}: Skipping invalid intent '{intent}' for query: '{query}'")
                    continue
                values.append((query, intent, emb.tolist()))

            if not values:
                logger.error("No valid rows found with allowed intents to insert.")
                raise HTTPException(status_code=400, detail="No valid intent rows to insert.")

            query = "INSERT INTO intent_data (query, intent, embedding) VALUES %s"
            execute_values(self.cursor, query, values)
            self.conn.commit()
            logger.info(f"Successfully inserted {len(values)} valid rows into intent_data.")
        except Exception as e:
            logger.error(f"Error inserting data: {e}")
            raise HTTPException(status_code=422, detail=f"Insertion failed: {e}")

    def get_relevant_intents(self, query_embedding):
        """
        Retrieves the top 1 matching record from each intent categorization (excluding 'Unknown')
        based on embedding similarity.

        :param query_embedding: The embedding of the query.
        :return: Dictionary with top match for each intent.
        """
        results = {}
        try:
            # Fetch for all intents except 'Unknown' (if you want, can adjust here)
            intents_to_fetch = [intent for intent in ALLOWED_INTENTS if intent != 'Unknown']
            for intent in intents_to_fetch:
                self.cursor.execute(
                    """
                    SELECT query, intent, 1 - (embedding <=> %s::vector) AS similarity
                    FROM intent_data
                    WHERE intent = %s
                    ORDER BY similarity DESC
                    LIMIT 1;
                    """,
                    (query_embedding.tolist(), intent)
                )
                match = self.cursor.fetchone()
                if match:
                    results[intent] = {
                        "query": match[0],
                        "intent": match[1],
                        "similarity": match[2]
                    }
        except Exception as e:
            logger.error(f"Error fetching top match: {e}")
            raise HTTPException(status_code=500, detail=f"Fetch error: {e}")
        return results

    def close(self):
        """
        Closes DB resources.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
