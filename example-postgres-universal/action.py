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


def truncate_output_with_beginning_clue(output: str, max_chars: int = 2000) -> str:
    beginning_clue = "[Cut] "  # A very short clue at the beginning to indicate possible truncation

    if len(output) > max_chars:
        truncated_output = output[:max_chars - len(beginning_clue)]
        chars_missed = len(output) - len(truncated_output)
        truncated_message = f"[+{chars_missed}]"
        return beginning_clue + truncated_output + truncated_message
    else:
        return output

def get_database_schema(conn):
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


def truncate_query_results(results, max_chars=2000):
    if not results:
        return ""

    if len(str(results)) < max_chars:
        return str(results)

    cell_max = 50

    truncated_output = ""
    for i, row in enumerate(results):
        if i >= 10:
            # Indicate additional rows not shown
            row_count_not_shown = len(results) - 10
            truncated_output += f"...[+{row_count_not_shown} rows]\n"
            break

        row_output = ""
        for j, cell in enumerate(row):
            if j >= 30:
                # Indicate additional columns not shown
                col_count_not_shown = len(row) - 30
                row_output += f"...[+{col_count_not_shown} columns], "
                break

            cell_output = str(cell)
            # Truncate cell if necessary
            if len(cell_output) > cell_max:
                cell_output = cell_output[:cell_max - 3] + "..."
            row_output += cell_output + ", "

        # Remove last comma and space, add newline
        truncated_output += row_output.rstrip(", ") + "\n"

        # Check if we've reached the max characters
        if len(truncated_output) >= max_chars:
            # Further truncate and end the loop
            truncated_output = truncated_output[:max_chars - 3] + "..."
            break

    return truncated_output



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
        return truncate_output_with_beginning_clue(schema)
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
            return truncate_query_results(results)
    except Exception as e:
        return f"An error occurred while executing the query: {e}"

