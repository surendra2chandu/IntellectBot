# Import necessary libraries
from fastapi import HTTPException
from src.utilities.OllamaPipeline import OllamaPipeline
from src.conf.Configurations import DEFAULT_LLAMA_MODEL , logger
from typing import Optional
from src.conf.Prompts import prompt1

class IntentClassifier:
    def __init__(self, llama_model: Optional[str] = DEFAULT_LLAMA_MODEL):
        """
        Initialize the IntentClassifier with the specified Ollama model.
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

        # Invoke the model with the chat structure
        try:
            # Directly invoke the model with the formatted prompt
            self.logger.info("invoking the model with input message")
            response = self.llm.invoke(input=prompt1.format(query=query))
            self.logger.info("response received from the model")
            self.logger.info(f"response: {response}")

            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during invocation: {e}")

if __name__ == "__main__":
    # Example usage of the IntentClassifier
    sample_query = "Hello , good morning "

    classifier = IntentClassifier()
    # intent = classifier.classify(sample_query)
    # print(sample_query)
    # print(f"Predicted intent: {intent}")
    #
    # sample_query = "What is  the status of my order?"
    # intent = classifier.classify(sample_query)
    # print(sample_query)
    # print(f"Predicted intent: {intent}")
    #
    # sample_query = "Who was surgeon general in 2019?"
    # intent = classifier.classify(sample_query)
    # print(sample_query)
    # print(f"Predicted intent: {intent}")

    sample_query = "Hi how are you?"
    intent = classifier.classify(sample_query)
    print(sample_query)
    print(f"Predicted intent: {intent}")