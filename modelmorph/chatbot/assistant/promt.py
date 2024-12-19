import configparser
import re

class Prompt:
    def __init__(self, config_path: str = None, role: str = "", output_format: str = None):
        """
        Initializes the Prompt class with configuration settings.
        
        Input:
            - config_path (str, optional): Path to the configuration file.
            - role (str): Role of the user or assistant, used as a fallback for role description if not specified in config.
            - output_format (str, optional): Template for the prompt format. Defaults to a pre-defined format.
            
        Output: 
            Initializes the object with prompt configuration and section connectors.
        """
        # Default configuration as a fallback if config file is not provided or has missing values
        default_config = {
            'LLM_COMPLETATION': {
                'INITIAL_PROMPT': '',
                'INTRO': '',
                'HOW': '',
                'FORMAT': '',
                'ERROR_RESPONSE': 'Lo siento, no puedo ayudarte con eso'
            },
            'CONNECTORS': {
                'ROLE': 'Rol:',
                'INTRO': 'Introducción:',
                'OBJECTIVES': 'Objetivos:',
                'HOW': 'Enfoque:',
                'RESTRICTIONS': 'Condiciones:',
                'FORMAT': 'Formato de salida:',
                'PARAMETERS': 'Parametros:'
            }
        }
        
        # Load configuration from file if provided; otherwise, use default
        config = configparser.ConfigParser()
        if config_path:
            config.read(config_path)
        else:
            config.read_dict(default_config)

        self.config = config

        # Load prompt sections from the role configuration
        self.role_description = config['LLM_COMPLETATION'].get('INITIAL_PROMPT', "") or role
        self.intro = config['LLM_COMPLETATION'].get('INTRO', "")
        self.how = config['LLM_COMPLETATION'].get('HOW', "")
        self.format = config['LLM_COMPLETATION'].get('FORMAT', "")
        self.error_response = config['LLM_COMPLETATION'].get('ERROR_RESPONSE', "Lo siento, no puedo ayudarte con eso")
        self.content = ''

        # Load connectors and delimiters from the CONNECTORS section
        self.role_connector = config['CONNECTORS'].get('ROLE', "Role:")
        self.intro_connector = config['CONNECTORS'].get('INTRO', "Introduction:")
        self.objectives_connector = config['CONNECTORS'].get('OBJECTIVES', "Objectives:")
        self.how_connector = config['CONNECTORS'].get('HOW', "Approach:")
        self.restrictions_connector = config['CONNECTORS'].get('RESTRICTIONS', "Conditions:")
        self.format_connector = config['CONNECTORS'].get('FORMAT', "Output Format:")
        self.parameter_connector = config['CONNECTORS'].get('PARAMETERS', "Parametros:")
        self.objective_delimiter = config['LLM_COMPLETATION'].get('OBJECTIVE_DELIMITER', "\n")
        self.restriction_delimiter = config['LLM_COMPLETATION'].get('RESTRICTION_DELIMITER', "\n")
        self.parameter_delimiter = config['LLM_COMPLETATION'].get('PARAMETER_DELIMITER', "\n")

        # Initialize lists for objectives, parameters, and restrictions
        self.objectives = []
        self.parameters = []
        self.restrictions = []

        # Set the output format or default format if none provided
        self.output_format = output_format or "{role}\n{intro}\n{objectives}\n{parameters}\n{how}\n{restrictions}\n{format}\n{content}"

    def _fill_placeholders(self, template: str, values) -> str:
        """
        Helper function to replace placeholders in a template string with provided values.
        
        Input:
            - template (str): String containing placeholders in the format {{placeholder}}.
            - values (dict or list): Dict of key-value pairs or list of values to replace placeholders.
        
        Output:
            - Returns a formatted string with placeholders replaced by the respective values.
        """
        if isinstance(values, dict):
            for key, value in values.items():
                template = template.replace(f"{{{{{key}}}}}", str(value))
        elif isinstance(values, list):
            placeholders = re.findall(r"\{\{(.*?)\}\}", template)
            if len(placeholders) == len(values):
                for placeholder, value in zip(placeholders, values):
                    template = template.replace(f"{{{{{placeholder}}}}}", str(value))
        return template

    def add_objective(self, objective: str, params=None):
        """
        Adds an objective to the objectives list, with optional parameters to replace placeholders.
        
        Input:
            - objective (str): Objective text, potentially containing placeholders.
            - params (dict or list, optional): Values to fill in placeholders within the objective text.
            
        Output:
            - Updates the objectives list with the formatted objective.
        """
        if params:
            objective = self._fill_placeholders(objective, params)
        self.objectives.append(objective)

    def add_param(self, param_description: str, param):
        """
        Adds a parameter description and value to the parameters list.
        
        Input:
            - param_description (str): Description or name of the parameter.
            - param: Value of the parameter to be added.
            
        Output:
            - Updates the parameters list with the formatted parameter description and value.
        """
        if param:
            self.parameters.append(f"\n{param_description}: {param}")

    def add_restriction(self, restriction: str):
        """
        Adds a restriction to the list of restrictions.
        
        Input:
            - restriction (str): Text describing a restriction.
        
        Output:
            - Updates the restrictions list with the specified restriction.
        """
        self.restrictions.append(restriction)

    def clean_objectives(self, n=None):
        """
        Cleans objectives. If n is None, cleans all objectives. If n is an int, cleans the last n objectives.
        
        Input:
            - n (int, optional): Number of objectives to remove from the end. If None, clears all objectives.
        
        Output:
            - Updates the objectives list by removing specified entries.
        """
        if n is None:
            self.objectives.clear()
        elif isinstance(n, int):
            self.objectives = self.objectives[:-n]

    def clean_restrictions(self, n=None):
        """
        Cleans restrictions. If n is None, cleans all restrictions. If n is an int, cleans the last n restrictions.
        
        Input:
            - n (int, optional): Number of restrictions to remove from the end. If None, clears all restrictions.
        
        Output:
            - Updates the restrictions list by removing specified entries.
        """
        if n is None:
            self.restrictions.clear()
        elif isinstance(n, int):
            self.restrictions = self.restrictions[:-n]

    def clean_parameters(self, n=None):
        """
        Cleans parameters. If n is None, cleans all parameters. If n is an int, cleans the last n parameters.
        
        Input:
            - n (int, optional): Number of parameters to remove from the end. If None, clears all parameters.
        
        Output:
            - Updates the parameters list by removing specified entries.
        """
        if n is None:
            self.parameters.clear()
        elif isinstance(n, int):
            self.parameters = self.parameters[:-n]

    def clear_all(self):
        """
        Resets objectives, parameters, and restrictions lists to empty state.
        
        Output:
            - Clears all lists (objectives, parameters, restrictions).
        """
        self.objectives.clear()
        self.parameters.clear()
        self.restrictions.clear()

    def _format_section(self, connector, content):
        """
        Helper method to format a section with a connector if content is present.
        
        Input:
            - connector (str): The connector text for the section.
            - content (str): The content of the section.
            
        Output:
            - Returns formatted string with connector if content is present, otherwise empty string.
        """
        return f"{connector} {content}" if content else ""

    def generate_prompt(self, text: str = None) -> str:
        """
        Generates the final structured prompt string, including all formatted sections.
        
        Input:
            - text (str, optional): Additional text to append to the prompt content.
            
        Output:
            - Returns a formatted string containing the full prompt with sections, objectives, parameters, and restrictions.
        """
        # Construct each section using the helper method
        role_text = self._format_section(self.role_connector, self.role_description)
        intro_text = self._format_section(self.intro_connector, self.intro)
        objectives_text = self._format_section(self.objectives_connector, self.objective_delimiter.join(self.objectives))
        how_text = self._format_section(self.how_connector, self.how)
        restrictions_text = self._format_section(self.restrictions_connector, self.restriction_delimiter.join(self.restrictions))
        parameters_text = self._format_section(self.parameter_connector, self.parameter_delimiter.join(self.parameters))
        format_text = self._format_section(self.format_connector, self.format)
        content_text = f"Content to perform the objective: {text}" if text else ""

        # Populate the output format with the formatted sections
        final_prompt = self.output_format.format(
            role=role_text,
            intro=intro_text,
            objectives=objectives_text,
            parameters=parameters_text,
            how=how_text,
            restrictions=restrictions_text,
            format=format_text,
            content=content_text
        )

        return final_prompt.strip() + '\n'
