# Importing required libraries
from src.conf.Configurations import logger
from src.conf.Configurations import embedding_model_path
from fastapi import HTTPException
from sentence_transformers import SentenceTransformer



class EmbeddingUtility:
    def __init__(self):
        """
        This function initializes the LateChunking class with the specified model path.
        """

        # Set the model name
        self.model_name = embedding_model_path

        try:
            # Load the model
            logger.info(f"Loading model from {embedding_model_path}...")
            self.model = SentenceTransformer(self.model_name)

        except Exception as e:
            # Log the error
            logger.error(f"Error during model loading: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during model loading: {e}")

    def get_model(self):
        """
        This function returns the model.
        :return: Model
        """

        # Return the model
        return self.model
