import modelmorph.chatbot.repository as chatbot_repository
from dotenv import load_dotenv
import os
import configparser
from .chat import Chat

class ChatCompletionAssistant:
    """
    ChatCompletionAssistant is a class for managing chat sessions with a language model API.
    It initializes the chat environment, loads configuration, and handles message exchanges via plugins.

    Attributes:
        endpoint (str): API endpoint URL for the language model.
        api_key (str): API key for authentication.
        deployment_id (str): Deployment identifier for the language model.
        api_version (str): API version being used.
        initial_prompt (str): Initial prompt for the language model interaction.
        error_response (str): Default error response if an issue occurs.
        llm (OpenAILlm): Instance for managing API interactions with the language model.
    """

    def __init__(self, endpoint=None, api_key=None, deployment_id=None, api_version=None, config_path=''):
        """
        Initializes ChatCompletionAssistant by loading configuration settings and setting up API access.

        Args:
            endpoint (str, optional): API endpoint URL, defaults to environment variable 'ENDPOINT'.
            api_key (str, optional): API key, defaults to environment variable 'API_KEY'.
            deployment_id (str, optional): Deployment identifier, defaults to environment variable 'DEPLOYMENT_ID'.
            api_version (str, optional): API version, defaults to environment variable 'API_VERSION'.
            config_path (str): Path to the configuration file.
        
        Raises:
            KeyError: If the configuration file is missing or incomplete.
        """
        load_dotenv()
        self.endpoint = endpoint or os.getenv('ENDPOINT')
        self.api_key = api_key or os.getenv('API_KEY')
        self.deployment_id = deployment_id or os.getenv('DEPLOYMENT_ID')
        self.api_version = api_version or os.getenv('API_VERSION')
        self.load_chat_config(config_path)

        self.llm = chatbot_repository.OpenAILlm(
            api_key=self.api_key,
            api_url=self.endpoint,
            api_version=self.api_version,
            model_name=self.deployment_id
        )

    def load_chat_config(self, config_path=''):
        """
        Loads chat-specific configuration settings from a provided file.

        Args:
            config_path (str): Path to the configuration file.
        
        Sets:
            initial_prompt (str): Initial message sent by the assistant.
            error_response (str): Fallback message in case of errors.
        """
        config = configparser.ConfigParser()
        config.read(config_path)
        self.initial_prompt = config.get(
            'LLM_CHAT', 'INITIAL_PROMPT',
            fallback='Default initial prompt'
        )
        self.error_response = config.get(
            'LLM_CHAT', 'ERROR_RESPONSE',
            fallback='Default error response'
        )

    def plugin_run(self, chat: Chat, message: str, plugin, choice: int = 0):
        """
        Executes a plugin function using the provided message and appends the result to the chat session.

        Args:
            chat (Chat): An instance of the Chat class.
            message (str): Message to process via the plugin.
            plugin (function): Plugin function to process the message.
            choice (int): Index of the response choice to use.
        """
        response = plugin(message)
        response_text = response['choices'][choice]['text']
        chat.chat["messages"].append({'role': 'assistant', 'message': response_text})

    def init_chat(self, _id=None) -> Chat:
        """
        Initializes a new chat session with the provided ID or creates a new one.

        Args:
            _id (int, optional): ID for the chat session, defaults to None.

        Returns:
            Chat: An initialized Chat instance.
        """
        chat = Chat(_id, self.llm, self.initial_prompt)
        chat.save_chat()
        return chat
