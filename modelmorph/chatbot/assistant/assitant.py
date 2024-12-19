import modelmorph.chatbot.repository as completion_repository
import configparser
from .promt import Prompt
import os
from dotenv import load_dotenv

class CompletionAssistant:
    """
    CompletionAssistant is a class designed to interact with a language model API for generating text completions.
    It loads configuration settings from environment variables and configuration files to initialize the model.
    
    Attributes:
        endpoint (str): API endpoint URL for language model.
        api_key (str): API key for authentication.
        deployment_id (str): Model identifier.
        api_version (str): API version.
        config (ConfigParser): Configuration object for loading settings.
        llm (OpenAILlm): Instance of OpenAILlm for generating language model completions.
        initial_prompt (str): Initial prompt for model interaction.
        error_response (str): Default error response.
    """

    def __init__(self, endpoint=None, api_key=None, deployment_id=None, api_version=None, config_path: str = ''):
        """
        Initializes CompletionAssistant by loading configuration from environment variables and a config file.

        Args:
            endpoint (str, optional): API endpoint URL, defaults to environment variable 'ENDPOINT'.
            api_key (str, optional): API key, defaults to environment variable 'API_KEY'.
            deployment_id (str, optional): Model identifier, defaults to environment variable 'DEPLOYMENT_ID'.
            api_version (str, optional): API version, defaults to environment variable 'API_VERSION'.
            config_path (str): Path to the configuration file.
        
        Raises:
            KeyError: If configuration file or required key is missing.
        """
        load_dotenv()
        self.endpoint = endpoint or os.getenv('ENDPOINT')
        self.api_key = api_key or os.getenv('API_KEY')
        self.deployment_id = deployment_id or os.getenv('DEPLOYMENT_ID')
        self.api_version = api_version or os.getenv('API_VERSION')

        self.load_completion_config(config_path)
 

        # Initialize LLM for completion, not chat
        self.llm = completion_repository.OpenAILlm(
            api_key=self.api_key,
            api_url=self.endpoint,
            api_version=self.api_version,
            model_name=self.deployment_id
        )

    def load_completion_config(self, config_path=''):
        """
        Loads completion settings from the provided configuration file path.

        Args:
            config_path (str): Path to the configuration file.
        
        Attributes set:
            initial_prompt (str): Initial prompt used by the model.
            error_response (str): Default response in case of errors.
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.initial_prompt = self.config.get(
            'LLM_COMPLETATION', 'INITIAL_PROMPT',
            fallback=self.config.get('DEFAULT', 'INITIAL_PROMPT', fallback='Default initial prompt')
        )
        self.error_response = self.config.get(
            'LLM_COMPLETATION', 'ERROR_RESPONSE',
            fallback=self.config.get('DEFAULT', 'ERROR_RESPONSE', fallback='Default error response')
        )

    def generate_completion(self, prompt: str | Prompt, option: int = 0, response_type: str = "json_object", max_tokens=200, temp=0.0, top_p=0.1) -> str:
        """
        Generates a completion response from the language model based on a given prompt.

        Args:
            prompt (str | Prompt): Input prompt for the language model. Can be a string or an instance of the Prompt class.
            option (int): Choice index from the response to return.
            response_type (str): Expected response format type (e.g., "json_object").
            max_tokens (int): Maximum number of tokens to generate.
            temp (float): Temperature parameter for sampling (0-1 range).
            top_p (float): Nucleus sampling probability threshold.

        Returns:
            str: Generated response text from the language model.

        Raises:
            Exception: If prompt is not a valid type (str or Prompt) or other error occurs.
        """
        # Configure settings for completion generation
        self.max_tokens = int(self.config.get('LLM_COMPLETATION', 'MAX_TOKENS', fallback=max_tokens))
        self.temp = float(self.config.get('LLM_COMPLETATION', 'TEMP', fallback=temp))
        self.top_p = float(self.config.get('LLM_COMPLETATION', 'TOP_P', fallback=top_p))
        self.type_object = self.config.get('LLM_COMPLETATION', 'TYPE', fallback=response_type)

        # Process the prompt input
        if type(prompt) == str:
            prompt_final = prompt
        elif type(prompt) == Prompt:
            prompt_final = prompt.generate_prompt('')
        else:
            raise Exception('Not Valid Prompt Type')

    # Generate response from the language model
        response = self.llm.get_response_message(
            message=prompt_final,
            sytem_message=self.initial_prompt,
            type_object=self.type_object,
            max_tokens=self.max_tokens,
            temperature=self.temp,
            top_p=self.top_p
        )
        return response.choices[option].message.content
    
