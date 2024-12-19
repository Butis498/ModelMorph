from .plugin import Plugin
from modelmorph.chatbot.domain import Llm

class NlpToSql(Plugin):
    """
    A class to convert natural language input to SQL queries using a specified plugin.

    Attributes:
    ----------
    plugin_name : str
        The name of the plugin to use.
    plugin_data : dict
        The data of the loaded plugin.
    prompt_template : str
        The prompt template of the loaded plugin.
    """

    def __init__(self, plugin_directory, plugin_name, llm: Llm):
        """
        Initializes the NlpToSql class with the specified directory, plugin name, and Llm instance.

        Parameters:
        ----------
        plugin_directory : str
            The directory where plugins are stored.
        plugin_name : str
            The name of the plugin to use.
        llm : Llm
            An instance of the Llm class.
        
        Raises:
        ------
        ValueError:
            If the specified plugin is not found in the directory.
        """
        super().__init__(plugin_directory, llm)
        self.plugin_name = plugin_name
        self.plugin_data = self.get_plugin(plugin_name)
        if self.plugin_data:
            self.prompt_template = self.plugin_data['prompt_template']
        else:
            raise ValueError(f"Plugin '{plugin_name}' not found in directory '{plugin_directory}'.")

    def generate_sql(self, input_data):
        """
        Generates an SQL query from the given natural language input using the loaded plugin.

        Parameters:
        ----------
        input_data : str
            The natural language input to convert to an SQL query.

        Returns:
        -------
        str:
            The generated SQL query.

        Raises:
        ------
        ValueError:
            If the plugin is not loaded properly.
        """
        if not self.plugin_data:
            raise ValueError(f"Plugin '{self.plugin_name}' is not loaded properly.")
        
        prompt = self.prompt_template.replace("{{$input}}", input_data)

        max_tokens = self.plugin_data['config'].get('max_tokens', 100)
        temperature = self.plugin_data['config'].get('temperature', 0)
        top_p = self.plugin_data['config'].get('top_p', 1.0)
        n = self.plugin_data['config'].get('n', 1)
        stop = self.plugin_data['config'].get('stop', ["\n"])

        response = self.llm.get_response_message(prompt, max_tokens=max_tokens, temperature=temperature, top_p=top_p, n=n, stop=stop)
        return response