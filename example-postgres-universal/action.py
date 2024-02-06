import json
import os
import psycopg2
from robocorp.actions import action

CONNECTION_FILE_PATH = 'postgres_connection.json'

class ReadOnlyConnection:
    def __init__(self, conn_params):
        self.conn_params = conn_params
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(**self.conn_params)
        cur = self.conn.cursor()
        cur.execute("SET TRANSACTION READ ONLY;")
        cur.close()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.rollback()  # Rollback any changes (though there shouldn't be any)
        self.conn.close()

@action
def init_postgres_connection(dsn: str) -> str:
    """
    Initializes a connection to a PostgreSQL database using the provided Data Source Name (DSN).

    Args:
        dsn (str): The connection string for the PostgreSQL database.
                   This should be in the format 'postgresql://username:password@host:port/database'.

    Returns:
        str: A confirmation message indicating successful connection or details of any connection errors.
    """
    # The implementation would go here, likely involving establishing a connection to the database
    # For example, using psycopg2.connect(dsn) or similar method
    # This function currently returns a string, but you might want to return a connection object instead
    # Convert DSN to connection parameters
    conn_params = {'dsn': dsn}

    # Save connection parameters to a file
    try:
        with open(CONNECTION_FILE_PATH, 'w') as file:
            json.dump(conn_params, file)
        return "Connection parameters saved successfully."
    except Exception as e:
        return f"Failed to save connection parameters: {e}"

@action
def execute_query(query: str) -> str:
    """
    Executes a given SQL query on a PostgreSQL database connection ensured to be read-only.

    Args:
        query (str): The SQL query to be executed. Only read queries are allowed.

    Returns:
        str: The result of the query or an error message.
    """
    try:
        # Read connection parameters from the file
        if os.path.exists(CONNECTION_FILE_PATH):
            with open(CONNECTION_FILE_PATH, 'r') as file:
                conn_params = json.load(file)
        else:
            return "Connection parameters file not found."

        with ReadOnlyConnection(conn_params) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return str(results)
    except Exception as e:
        return f"An error occurred while executing the query: {e}"

