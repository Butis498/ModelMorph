# ModelMorph Development Guide

## Overview
ModelMorph is a modular library designed to integrate and customize Large Language Models (LLMs) for a variety of AI applications, including chatbots, virtual assistants, data analytics, and content generation. It is available for deployment both locally and in the cloud (Linux, macOS, Windows). This README provides developers with an understanding of the architecture, setup, and how to contribute to the project.

### Key Features
- **Modular Architecture:** Dynamic conversation flow, adaptable LLM prompts, and integration with OpenAI API and custom models.
- **Storage:** Chat history management with MongoDB or other backend solutions.
- **Flexible Querying:** Customizable queries and prompt management to meet different use cases.
- **Deployment:** Supports both cloud and local environments.
- **Integration:** Easy integration of LLMs into various applications such as chatbots, AI assistants, and data-driven systems.

---

## Project Structure
ModelMorph follows a modular design with clear separation of concerns between different components of the system. The project structure is as follows:

```text
ModelMorph/
├── modelmorph
│   ├── chatbot
│   │   ├── assistant           # Main chatbot assistant classes
│   │   ├── domain              # Abstracts for LLMs
│   │   ├── plugins             # Optional plugins for chatbot functionality
│   │   └── repository          # Interfaces for storage and chat history management
│   ├── db
│   │   ├── domain              # DB abstractions for various DB backends
│   │   └── repository          # MongoDB and other DB repository implementations
│   ├── docs                    # Documentation and developer guides
│   │   ├── CONTRIBUTING.md
│   │   ├── dev                 # Development setup
│   │   └── icons               # Icons for documentation and UI
│   ├── logger                  # Logging utilities
│   └── tests                   # Unit tests
│       └── main_test.py
├── pyproject.toml              # Python project metadata
├── requirements.txt            # Dependencies
└── setup.cfg                   # Configuration for building and distribution
```

---

## Core Components

### `OpenAILlm` (LLM Integration)
The `OpenAILlm` class facilitates integration with OpenAI's API. It provides methods for generating responses from the model using the provided API key and endpoint.

```python
class OpenAILlm:
    def __init__(self, api_key: str, api_url: str, api_version: str, api_chat: str):
        self.api_key = api_key
        self.api_url = api_url
        self.api_version = api_version
        self.api_chat = api_chat

    def get_response_message(self, message: str, max_tokens: int = 100, temperature: float = 0.5):
        # Fetches a response from OpenAI based on the input message
        pass
```

### `MongoDBRepository` (Storage)
The `MongoDBRepository` class provides an interface for interacting with a MongoDB database, allowing you to save and retrieve chat histories.

```python
class MongoDBRepository:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def _connect_db(self):
        # Connect to MongoDB
        pass

    def save_chat(self, chat_id: int, chat: dict):
        # Saves chat to the database
        pass
```

### `ChatAssistant` (Main Assistant Logic)
The `ChatAssistant` class is responsible for initializing and managing a chat session, integrating with the `OpenAILlm` and `MongoDBRepository` for conversation handling and storage.

```python
class ChatAssistant:
    def __init__(self):
        self.llm = OpenAILlm(...)
        self.db_connection = MongoDBRepository(...)

    def init_chat(self, chat_id: int = None):
        # Initializes the chat, optionally using a pre-existing chat session
        pass

    def send(self, message: str):
        # Sends a message to the LLM and retrieves a response
        pass
```

---

## UML Diagram
The project follows a well-defined object-oriented structure. The UML diagram below illustrates the relationships between the key classes.

![ModelMorph UML Diagram](modelmorph/docs/icons/main_icon.png)

### Key Relationships:
- **`ChatAssistant`** uses **`OpenAILlm`** and **`MongoDBRepository`** to manage chats.
- **`OpenAILlm`** extends the abstract **`Llm`** class, allowing future integration with other LLM providers.
- **`MongoDBRepository`** and **`DBRepository`** handle database interactions, supporting chat history management and queries.

---

## Installation

To install **ModelMorph** and its dependencies, follow these steps:

### Prerequisites
- Python 3.8 or higher
- MongoDB (for local deployments)[OPTIONAL]
- An OpenAI API key (if using OpenAI’s model)

### Install Dependencies

Clone the repository and install the dependencies:

```bash
git clone https://github.com/Butis498/ModelMorph.git
cd ModelMorph
pip install -r requirements.txt
```

For cloud environments, ensure the appropriate configuration for the cloud provider is set.

---

## Development

### Setting Up the Development Environment

1. Clone the repository:

   ```bash
   git clone https://github.com/Butis498/ModelMorph.git
   ```

2. Install dependencies in a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # Linux/macOS
   env\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

3. Build the project:

   If you plan to contribute or build from source, follow the [build instructions](modelmorph/docs/dev/BUILD.md).

---

## Tests

ModelMorph uses unit tests to ensure the functionality of core components. To run the tests, use `pytest`:

```bash
pytest
```

---

## Contribution

We welcome contributions to ModelMorph! Please refer to the [Contributing Guide](modelmorph/docs/CONTRIBUTING.md) for instructions on how to report issues or submit pull requests.

---

## License

ModelMorph is licensed under the [MIT License](LICENSE). You can freely modify and distribute the code, as long as the original license is maintained.