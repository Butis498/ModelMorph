from modelmorph.chatbot.domain import Llm
from dotenv import load_dotenv
import os
from openai import AzureOpenAI
import json

class OpenAILlm(Llm):

    def __init__(self, api_key: str, api_url: str, api_version: str, model_name: str):
        """
        Initializes an instance of OpenAILlm with Azure OpenAI configuration.

        Input:
            - api_key (str): API key for Azure OpenAI.
            - api_url (str): URL endpoint for the API.
            - api_version (str): API version to be used.
            - model_name (str): Name of the language model.

        Output:
            - None; sets up the AzureOpenAI client.
        """
        self.client = AzureOpenAI(
            azure_endpoint=api_url,
            api_key=api_key,
            api_version=api_version
        )
        self.model_name = model_name

    def get_response_message(self, message: str, system_message: str, max_tokens: int = 400, temperature: float = 0.0, top_p: float = 1.0, type_object: str = 'json_object'):
        """
        Sends a message to the model and receives a structured response.

        Input:
            - message (str): The message content to send to the model.
            - system_message (str): Optional system message to include at the start of the conversation.
            - max_tokens (int): Maximum number of tokens in the response.
            - temperature (float): Sampling temperature for creativity in responses.
            - top_p (float): Probability for nucleus sampling.
            - type_object (str): Specifies the response format, default is 'json_object'.

        Output:
            - response (object): The response from the language model.
        """
        chat_input = [{"role": "user", "content": message}]
        if system_message:
            chat_input.insert(0, {'role': 'system', 'content': system_message})

        response = self.client.chat.completions.create(
            model=self.model_name,
            response_format={"type": type_object},
            messages=chat_input,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )

        return response

    def get_response_chat(self, chat: list[dict], max_tokens: int = 200, temperature: float = 0.5, type_object: str = ''):
        """
        Sends a chat history to the model and receives a JSON-only response.

        Input:
            - chat (list of dict): List of messages representing the chat history.
            - max_tokens (int): Maximum number of tokens in the response.
            - temperature (float): Sampling temperature for creativity in responses.
            - type_object (str): Response format for the model output.

        Output:
            - response (object): The response from the language model.
        """
        system_message = {
            "role": "system",
            "content": "You are a helpful assistant designed to output JSON."
        }
        chat.insert(0, system_message)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=chat,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=1.0
        )

        return response
