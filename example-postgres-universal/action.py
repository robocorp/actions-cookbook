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

def get_database_schema(conn):
    """
    Retrieves the database schema including table relationships.

    Args:
        conn: The database connection object.

    Returns:
        str: Textual representation of the database schema.
    """
    schema_info = "Database Schema:\n"

    with conn.cursor() as cursor:
        # Retrieve tables
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            schema_info += f"\nTable: {table_name}\n"

            # Get columns and primary key info
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s
            """, (table_name,))
            columns = cursor.fetchall()

            for col in columns:
                column_name, data_type, is_nullable, column_default = col
                schema_info += f"  Column: {column_name}, Type: {data_type}, Nullable: {'YES' if is_nullable == 'YES' else 'NO'}"
                if column_default is not None:
                    schema_info += ", Default: " + column_default
                schema_info += "\n"

            # Get primary key info
            cursor.execute("""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY'
            """, (table_name,))
            primary_keys = cursor.fetchall()

            # Get foreign key info
            cursor.execute("""
                SELECT kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                WHERE tc.table_name = %s AND tc.constraint_type = 'FOREIGN KEY'
            """, (table_name,))
            foreign_keys = cursor.fetchall()

            for pk in primary_keys:
                schema_info += f"  Primary Key: {pk[0]}\n"
            for fk in foreign_keys:
                schema_info += f"  Foreign Key: {fk[0]}, References {fk[1]}({fk[2]})\n"

    return schema_info



@action
def init_postgres_connection(dsn: str) -> str:
    """
    Initializes a connection to a PostgreSQL database using the provided Data Source Name (DSN).

    Args:
        dsn (str): The connection string for the PostgreSQL database.
                   This should be in the format 'postgresql://username:password@host:port/database'.

    Returns:
        str: A textual representation of the database schema.
    """
    conn_params = {'dsn': dsn}

    # Save connection parameters to a file
    try:
        with open(CONNECTION_FILE_PATH, 'w') as file:
            json.dump(conn_params, file)
        with ReadOnlyConnection(conn_params) as conn:
            schema = get_database_schema(conn)
        return schema
    except Exception as e:
        return f"Failed: {e}"

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

