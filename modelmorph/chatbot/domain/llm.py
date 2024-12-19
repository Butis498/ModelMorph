from abc import ABCMeta, abstractmethod
import json
from modelmorph.db.repository import DBRepository

class Llm(metaclass=ABCMeta):
    
    @abstractmethod
    def get_response_message(self, message: str, option: str):
        """
        Abstract method to get a response message from the language model based on a single prompt message.
        
        Input:
            - message (str): The input message or prompt for which a response is needed.
            - option (str): Additional options or parameters for response configuration.
            
        Output:
            - Returns a response object containing the model's response to the input message.
            
        Note:
            Must be implemented in any subclass of Llm.
        """
        raise NotImplementedError

    @abstractmethod
    def get_response_chat(self, chat: dict):
        """
        Abstract method to get a response message for a structured chat (conversation history) from the language model.
        
        Input:
            - chat (dict): Dictionary containing the conversation history with messages, roles, and other metadata.
            
        Output:
            - Returns a response object containing the model's response based on the chat history.
            
        Note:
            Must be implemented in any subclass of Llm.
        """
        raise NotImplementedError
