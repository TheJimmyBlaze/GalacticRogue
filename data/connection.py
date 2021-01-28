from sqlite3 import Error

class DbConnection:
    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}, in query: {query}")
            raise e

    def get_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(f"Error: {e}, in query: {query}")
            raise e
            