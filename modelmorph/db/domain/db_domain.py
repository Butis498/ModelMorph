from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class QueryAnswere:
    """
    A data class to represent the result of a database query.

    Attributes:
    ----------
    data : list[dict]
        The data returned by the query.
    error : str
        Any error message returned by the query.
    """
    data: list[dict]
    error: str

class DBRepository(ABC):
    """
    An abstract base class to represent a database repository.

    Attributes:
    ----------
    connection_string : str
        The connection string for the database.
    """

    _instances = {}

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of the class is created (singleton pattern).

        Parameters:
        ----------
        *args : tuple
            Variable length argument list.
        **kwargs : dict
            Arbitrary keyword arguments.

        Returns:
        -------
        DBRepository:
            The singleton instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(DBRepository, cls).__new__(cls)
        return cls._instances[cls]

    def __init__(self, connection_string: str):
        """
        Initializes the DBRepository class with a connection string.

        Parameters:
        ----------
        connection_string : str
            The connection string for the database.
        """
        self.connection_string = connection_string
        self._connect_db()

    @abstractmethod
    def _connect_db(self) -> None:
        """
        Connects to the database. Must be implemented by subclasses.
        """
        raise NotImplementedError

    @abstractmethod
    def execute_query(self, query: str) -> QueryAnswere:
        """
        Executes a query on the database. Must be implemented by subclasses.

        Parameters:
        ----------
        query : str
            The query to execute.

        Returns:
        -------
        QueryAnswere:
            The result of the query.
        """
        raise NotImplementedError

    @abstractmethod
    def find_chat_by_id(self, chat_id: int) -> QueryAnswere:
        """
        Finds a chat by its ID. Must be implemented by subclasses.

        Parameters:
        ----------
        chat_id : int
            The ID of the chat to find.

        Returns:
        -------
        QueryAnswere:
            The result of the query.
        """
        raise NotImplementedError

    @abstractmethod
    def save_chat(self, chat_id: int, chat: list) -> QueryAnswere:
        """
        Saves a chat to the database. Must be implemented by subclasses.

        Parameters:
        ----------
        chat_id : int
            The ID of the chat to save.
        chat : list
            The chat data to save.

        Returns:
        -------
        QueryAnswere:
            The result of the query.
        """
        raise NotImplementedError