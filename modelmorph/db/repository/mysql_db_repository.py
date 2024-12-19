from modelmorph.db.domain import DBRepository, QueryAnswere
import mysql.connector
from mysql.connector import Error

class MySQLRepository(DBRepository):

    def _connect_db(self) -> None:
        try:
            self.connection = mysql.connector.connect(self.connection_string)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
        except Error as e:
            print(f"Failed to connect to MySQL: {e}")

    def execute_query(self, query: str) -> QueryAnswere:
        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            return QueryAnswere(data=data, error="")
        except Error as e:
            return QueryAnswere(data=[], error=str(e))
