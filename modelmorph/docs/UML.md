```plantuml

skinparam classAttributeIconSize 0

' Package for the chatbot repository
package "modelmorph.chatbot.repository" {
    class OpenAILlm {
        + api_key : str
        + api_url : str
        + api_version : str
        + api_chat : str
        --
        + OpenAILlm(api_key: str, api_url: str, api_version: str, api_chat: str)
        + get_response_message(message: str, max_tokens: int = 100, temperature: float = 0.5)
        + get_response_chat(chat: list[dict], max_tokens: int = 100, temperature: float = 0.5)
    }
}

' Package for the db repository
package "modelmorph.db.repository" {
    class MongoDBRepository {
        + connection_string : str
        --
        + MongoDBRepository(connection_string: str)
        + _connect_db() : void
        + execute_query(query: str) : QueryAnswere
        + find_chat_by_id(chat_id: int) : QueryAnswere
        + save_chat(chat_id: int, chat: dict) : QueryAnswere
    }
}

' Package for the chatbot domain
package "modelmorph.chatbot.domain" {
    class Llm {
    }
}

' Package for the db domain
package "modelmorph.db.domain" {
    class DBRepository {
        + connection_string : str
        --
        + DBRepository(connection_string: str)
        + _connect_db() : void
        + execute_query(query: str) : QueryAnswere
        + find_chat_by_id(chat_id: int) : QueryAnswere
        + save_chat(chat_id: int, chat: list) : QueryAnswere
    }

    class QueryAnswere {
        + data : list[dict]
        + error : str
        --
        + QueryAnswere(data: list[dict], error: str)
    }
}

' Package for the Cloud Domain
package "CloudDomain" {
    class CloudDomain {
        + cloud_id : str
        + cloud_name : str
        + cloud_type : str
        --
        + CloudDomain(cloud_id: str, cloud_name: str, cloud_type: str)
        + __str__() : str
        + __repr__() : str
    }
}

' The main ChatAssistant class
package "modelmorph.chatbot.assistant" {
    class ChatAssistant {
        - initial_prompt : str
        - error_response : str
        - llm : OpenAILlm
        --
        + ChatAssistant()
        + load_chat_config() : void
        + add_system_message(chat: Chat, message: str) : void
        + init_chat(_id=None) : str
    }
}
' The main CompletionAssistant class
package "modelmorph.chatbot.assistant" {
    class CompletionAssistant {
        - endpoint : str
        - api_key : str
        - deployment_id : str
        - api_version : str
        - config : ConfigParser
        - initial_prompt : str
        - error_response : str
        - llm : OpenAILlm
        --
        + CompletionAssistant(endpoint=None, api_key=None, deployment_id=None, api_version=None, config_path: str='')
        + load_completion_config(config_path: str) : void
        + generate_completion(prompt: str | Prompt, option: int = 0, response_type: str = "json_object", max_tokens: int = 200, temp: float = 0.0, top_p: float = 0.1) : str
    }
}
' The Chat class 
package "modelmorph.chatbot.assistant"{

	class Chat {
	        - chat_id : int
	        - chatbot : Llm
	        - chat : dict
	        - db_connection : MongoDBRepository
	        --
	        + Chat(chat_id: int, llm: Llm, initial_prompt: str)
	        + save_chat() : void
	        + __del__() : void
	        + _initialize_chat() : void
	        + send(message: str) : (dict, str)
	}
	
}

' The Llm abstract class
package "modelmorph.chatbot.domain" {
    abstract class Llm {
        + get_response_message(message: str)
        + get_response_chat(chat: dict)
    }
}

' The main Prompt class
package "modelmorph.chatbot.assistant" {
    class Prompt {
        - role_description : str
        - intro : str
        - how : str
        - format : str
        - error_response : str
        - content : str
        - role_connector : str
        - intro_connector : str
        - objectives_connector : str
        - how_connector : str
        - restrictions_connector : str
        - format_connector : str
        - parameter_connector : str
        - objective_delimiter : str
        - restriction_delimiter : str
        - parameter_delimiter : str
        - objectives : list
        - parameters : list
        - restrictions : list
        - output_format : str
        --
        + Prompt(config_path: str, role: str, output_format: str = None)
        + add_objective(objective: str, params: list = None) : void
        + add_param(param_description: str, param) : void
        + add_restriction(restriction: str) : void
        + clean_objectives(n: int = None) : void
        + clean_restrictions(n: int = None) : void
        + clean_parameters(n: int = None) : void
        + generate_prompt(text: str = None) : str
        - _fill_placeholders(template: str, values: list) : str
    }
}

Llm : <<Abstract Class>>

' Relationships
ChatAssistant ..> OpenAILlm : uses
ChatAssistant ..> Chat : uses

CompletionAssistant ..> OpenAILlm : uses
CompletionAssistant ..> Chat : uses
CompletionAssistant ..> Prompt : uses

Chat ..> MongoDBRepository : uses
Chat ..> Llm : uses
MongoDBRepository ..> QueryAnswere : returns
MongoDBRepository ..|> DBRepository : inherits

DBRepository ..> QueryAnswere : returns
DBRepository <|-- MongoDBRepository : inherits

QueryAnswere <|-- DBRepository : contains

OpenAILlm ..|> Llm : inherits

CloudDomain <|-- DBRepository : association



```



