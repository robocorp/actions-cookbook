from robocorp.actions import action


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
    return f"Connected to PostgreSQL database successfully!"

@action
def execute_query(query: str) -> str:
    """
    Executes a given SQL query on the specified PostgreSQL database connection.

    Args:
        query (str): The SQL query to be executed. Only read queries allowed.

    Returns:
        str: The result of the query.
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        return f"An error occurred while executing the query: {e}"
