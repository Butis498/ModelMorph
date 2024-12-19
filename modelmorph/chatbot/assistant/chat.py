from modelmorph.db.repository import MongoDBRepository
from modelmorph.chatbot.domain.llm import Llm
import os
from .promt import Prompt

class Chat(object):


    def __init__(self, chat_id: int, llm:Llm ,initial_prompt:str | Prompt):
        """
        Initializes the Chat class with a chat ID, language model (Llm), and initial system prompt.
        
        Input:
            - chat_id (int): Unique identifier for the chat session.
            - llm (Llm): Language model instance for handling responses.
            - initial_prompt (str): Initial system prompt for the chatbot.
            
        Output:
            Initializes the chat dictionary with the initial prompt and connects to the MongoDBRepository.
        """
        self._initialize_prompt = ''
        if type(initial_prompt) == str:
            self._initialize_prompt = initial_prompt
        elif type(initial_prompt) == Prompt:
            self._initialize_prompt = initial_prompt.generate_prompt()

        
        self.chat_id = chat_id
        self.chatbot = llm
        self.chat = {"messages":[{"role":"system","content":initial_prompt}], "_id":chat_id}
        self.db_connection = MongoDBRepository(os.getenv('CONNECTION_STRING'))


    def save_chat(self):
        """
        Saves the current chat state to the database.
        
        Input:
            None
            
        Output:
            - Calls the save_chat function in the database repository to save the chat data.
        """
        # Save the chat to the database
        self.db_connection.save_chat(self.chat_id, self.chat)

    
    def __del__(self):
        """
        Destructor for Chat class, called when the object is deleted.
        
        Input:
            None
            
        Output:
            Automatically saves the current chat state to the database upon object deletion.
        """
        # Save the chat when the object is deleted
        self.db_connection.save_chat(self.chat_id, self.chat)
        


    def _initialize_chat(self):
        """
        Initializes the chat by checking if a chat with the provided chat_id exists in the database.
        
        Input:
            None
            
        Output:
            - Loads chat messages from the database if they exist.
            - If chat does not exist or there’s a 400 error, starts with a new chat initialized with the initial_prompt.
            - Handles other database errors by printing error messages.
        """
        # Use the chatbot's db attribute (which should be an instance of MongoDBRepository)
        if self.chat_id is None:
            pass
        
        result = self.db_connection.find_chat_by_id(self.chat_id)
        if result.error:
            if result.error == 400:
                # If the chat does not exist, start with an empty chat
                self.chat = {"messages":[{"role":"system","content":self.initial_prompt}], "_id":self.chat_id}
            else:
                # Handle other errors (e.g., database connection issues)
                print(f"Error retrieving chat: {result.error}")
        else:
            # If the chat exists, load the existing messages
            self.chat = result.data[0]

    def send(self,message:str):
        """
        Adds a user message to the chat, gets a response from the chatbot, and adds it to the chat.
        
        Input:
            - message (str): The user’s message to be sent to the chatbot.
            
        Output:
            - Appends the user’s message and the chatbot’s response to the chat messages.
            - Returns the raw response from the chatbot API and the content of the assistant’s message.
            - Handles and prints any errors encountered when retrieving a chatbot response.
        """
        # Implement functionality for adding messages to the chat or other chat-related operations
        
        if len(self.chat['messages']) <= 1:
            self._initialize_chat()
        self.chat['messages'].append({"role":"user","content":message})
        try:
            response = self.chatbot.get_response_chat(self.chat['messages'])
            self.chat['messages'].append({"role":"assistant","content":response['choices'][0]['message']['content']})
            message = response['choices'][0]['message']['content']
            return response,message
        
        except Exception as e:

            print(f"Error getting response: {e}")

        


        