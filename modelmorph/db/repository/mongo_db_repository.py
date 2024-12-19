from modelmorph.db.domain import DBRepository, QueryAnswere
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import os

class MongoDBRepository(DBRepository):

    def _connect_db(self) -> None:
        """
        Connects to the MongoDB database using the connection string.

        This method retrieves the database name from environment variables and attempts to establish a connection with MongoDB.

        Output:
            - None; initializes the `client` and `db` attributes if connection is successful.
            - Prints an error message if the connection fails.
        """
        db_name = os.getenv('DB_NAME')
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client.get_database(db_name)
        except PyMongoError as e:
            print(f"Failed to connect to MongoDB: {e}")

    def execute_query(self, query: str) -> QueryAnswere:
        """
        Executes a query to retrieve data from a MongoDB collection.

        Input:
            - query (str): The name of the collection to query.

        Output:
            - QueryAnswere: Contains the retrieved data and error information.
            - Returns an error message in `QueryAnswere` if the query fails.
        """
        try:
            collection = self.db[query]
            data = list(collection.find())
            return QueryAnswere(data=data, error="")
        except PyMongoError as e:
            return QueryAnswere(data=[], error=str(e))
        
    def find_chat_by_id(self, chat_id: int) -> QueryAnswere:
        """
        Finds a chat by its ID from the 'chats' collection.

        Input:
            - chat_id (int): The ID of the chat to find.

        Output:
            - QueryAnswere: Contains the retrieved chat data and error information.
            - Returns a `400` error in `QueryAnswere` if the chat is not found, or another error if an exception occurs.
        """
        try:
            collection = self.db['chats']
            data = list(collection.find({"_id": chat_id}))
            if data:
                return QueryAnswere(data=data, error="")
            else:
                return QueryAnswere(data=[], error=400)
        except PyMongoError as e:
            return QueryAnswere(data=[], error=str(e))
        
    def save_chat(self, chat_id: int, chat: dict) -> QueryAnswere:
        """
        Saves or updates a chat in the 'chats' collection.

        Input:
            - chat_id (int): The ID of the chat to save.
            - chat (dict): The chat data to save.

        Output:
            - QueryAnswere: Contains information on the save operation.
            - Returns an error in `QueryAnswere` if the save operation fails.
        """
        try:
            collection = self.db['chats']
            result = collection.update_one({"_id": chat_id}, {"$set": chat}, upsert=True)
            if result.modified_count > 0:
                return QueryAnswere(data=[], error="")
            else:
                return QueryAnswere(data=[], error="Failed to save chat")
        except PyMongoError as e:
            return QueryAnswere(data=[], error=str(e))
