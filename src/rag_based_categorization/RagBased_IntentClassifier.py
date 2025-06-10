# Import necessary libraries
from fastapi import HTTPException
from src.utilities.OllamaPipeline import OllamaPipeline
from src.conf.Configurations import DEFAULT_LLAMA_MODEL , logger
from typing import Optional
from src.conf.Prompts import RAG_PROMPT1
from src.utilities.IntentDatabaseUtility import IntentDatabaseUtility
from src.data.EmbeddingsGenerator import EmbeddingsGenerator


class RagBasedIntentClassifier:
    def __init__(self, llama_model: Optional[str] = DEFAULT_LLAMA_MODEL):
        """
        Initialize the RagBasedIntentClassifier with the specified Ollama model.
        This class is designed to classify intents based on RAG (Retrieval-Augmented Generation) techniques.
        :param llama_model: The model to be used for intent classification. Defaults to DEFAULT_LLAMA_MODEL.
        """

        # Initialize the logger
        self.logger = logger

        try:
            # Initialize the OllamaPipeline model
            self.llm = OllamaPipeline(llama_model).get_model()
            self.logger.info("Ollama model initialized successfully")

        except Exception as e:
            self.logger.info(f"Error initializing the OllamaPipeline model: {str(e)}")
            raise HTTPException(status_code=500, detail="Error initializing the OllamaPipeline model")

    def classify(self, query: str) -> str:
        """
        Classify the intent of the given text using the provided model.

        Args:
            query (str): The text to classify.

        Returns:
            str: The predicted intent.
        """

        # Generate the embedding for the query
        self.logger.info("Generating embedding for the query...")
        embedding = EmbeddingsGenerator().get_embeddings([query])[0]

        # Get relevant intents from the database
        try:
            self.logger.info("Retrieving relevant intents from the database...")
            intent_res = IntentDatabaseUtility().get_relevant_intents(embedding)
            self.logger.info(f"Retrieved {len(intent_res)} relevant intents from the database.")
        except Exception as e:
            self.logger.error(f"Error retrieving intents from the database: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving intents from the database")

        if len(intent_res) < 2:
            self.logger.info("Insufficient intents found in the database for classification.")
            return "No sufficient intents found"

        # Invoke the model with the chat structure
        try:

            query1 = intent_res[0][0]
            intent1 = intent_res[0][1]
            query2 = intent_res[1][0]
            intent2 = intent_res[1][1]

            prompt = RAG_PROMPT1.format(query1=query1,intent1=intent1, query2=query2, intent2=intent2, query=query)

            print(prompt)
            print("--------------------------------------------------")

            # Directly invoke the model with the formatted prompt
            self.logger.info("invoking the model with input message")
            response = self.llm.invoke(input=prompt)
            self.logger.info("response received from the model")

            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during invocation: {e}")

if __name__ == "__main__":
    # Example usage of the IntentClassifier
    classifier = RagBasedIntentClassifier()
    # sample_query = "Hi how are you?"
    sample_query = "hi, buddy?"

    intent = classifier.classify(sample_query)
    print(sample_query)

    print(f"Predicted intent: {intent}")
