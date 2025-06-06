# Importing necessary classes
from langchain_ollama.llms import OllamaLLM
from fastapi import HTTPException
from src.conf.Configurations import OLLAMA_BASE_URL



class OllamaPipeline:
    def __init__(self, model: str):
        """
        This function initializes the OllamaPipeline class with the specified model path.
        :param model: The model to be used for the Ollama pipeline.
        """
        # Load the Ollama model
        try:
            self.model = OllamaLLM(base_url=OLLAMA_BASE_URL, model=model, stream=True)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while initializing the model: {e}")


    def get_model(self):
        """
        This function returns the Ollama model.
        :return: Ollama model
        """

        # Return the Ollama model
        return self.model
