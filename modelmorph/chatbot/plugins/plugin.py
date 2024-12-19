import os
import json
from modelmorph.chatbot.repository import Llm

class Plugin:
    """
    A class to manage plugins for the chatbot.

    Attributes:
    ----------
    plugin_directory : str
        The directory where plugins are stored.
    plugins : dict
        A dictionary to store loaded plugins.
    llm : Llm
        An instance of the Llm class.
    """

    def __init__(self, plugin_directory, llm: Llm):
        """
        Initializes the Plugin class with the specified directory and Llm instance.

        Parameters:
        ----------
        plugin_directory : str
            The directory where plugins are stored.
        llm : Llm
            An instance of the Llm class.
        """
        self.plugin_directory = plugin_directory
        self.plugins = {}
        self.llm = llm

        self.load_plugins()

    def load_plugins(self):
        """
        Loads plugins from the specified directory. Each plugin must have a 'config.json' 
        and 'skprompt.txt' file. The plugins are stored in the 'plugins' dictionary.
        
        Raises:
        ------
        ValueError:
            If a plugin is missing a required file.
        """
        # Load plugins from the specified directory
        plugins = os.listdir(self.plugin_directory)
        # Ignore __pycache__ 
        plugins = [plugin for plugin in plugins if plugin != "__pycache__"]
        
        for plugin_name in plugins:
            plugin_path = os.path.join(self.plugin_directory, plugin_name)
            if os.path.isdir(plugin_path):
                config_path = os.path.join(plugin_path, "config.json")
                prompt_path = os.path.join(plugin_path, "skprompt.txt")

                if os.path.exists(config_path) and os.path.exists(prompt_path):
                    with open(config_path, 'r') as config_file:
                        config = json.load(config_file)

                    with open(prompt_path, 'r') as prompt_file:
                        prompt_template = prompt_file.read()
                        prompt_template = prompt_template.replace("\n", " ")

                    # Store the loaded plugin in the plugins dictionary
                    self.plugins[plugin_name] = {
                        "config": config,
                        "prompt_template": prompt_template
                    }
                else:
                    raise ValueError(f"Plugin '{plugin_name}' is missing a required file.")

    def get_plugin(self, plugin_name):
        """
        Retrieves a plugin by its name.

        Parameters:
        ----------
        plugin_name : str
            The name of the plugin to retrieve.

        Returns:
        -------
        dict or None:
            The plugin data if found, otherwise None.
        """
        return self.plugins.get(plugin_name, None)
