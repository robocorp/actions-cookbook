"""
AI Actions for dvdrental PostgreSQL database queries.
"""

import psycopg2
from robocorp.actions import action

def _connect():
    # Use some .env or vault rather than adding your password here.
    params = {
        'database': 'dvdrental',
        'user': 'postgres',
        'password': 'SOMEPASSWD',
        'host': 'localhost',
        'port': '5432'
    }

    return psycopg2.connect(**params)


@action(is_consequential=False)
def customers_by_name(first_name: str) -> str:
    """
    List customers by first name.

    Args:
        first_name (str): Customer's first name in string format. Example: "Jill"

    Returns:
        str: List of customers based on the first name (customer number, first name, last name, email address).
    """

    conn = _connect()
    cur = conn.cursor()

    sql_query = """
    SELECT customer_id, first_name, last_name, email
    FROM customer
    WHERE first_name = %s;
    """
    cur.execute(sql_query, (first_name,))
    rows = cur.fetchall()

    output = []
    for c_num, fn, ln, email in rows:
        output.append(f"ID: {c_num}, {fn}, {ln}, {email}")

    output_str = "\n".join(output)
    print(output_str)
    cur.close()
    conn.close()
    return output_str


@action(is_consequential=False)
def customers_rentals(first_name: str, last_name: str) -> str:
    """
    List customers latest rental transactions.

    Args:
        first_name (str): Customer's first name in string format. Example: "Jill"
        last_name (str): Customer's last name in string format. Example: "Jones"

    Returns:
        str: List of customers latest rental transactions containing rental date and the movie title.
    """

    conn = _connect()
    cur = conn.cursor()

    sql_query = """
    SELECT r.rental_date, f.title AS movie_title
    FROM rental r
    JOIN customer c ON r.customer_id = c.customer_id
    JOIN inventory i ON r.inventory_id = i.inventory_id
    JOIN film f ON i.film_id = f.film_id
    WHERE c.first_name = %s AND c.last_name = %s
    ORDER BY rental_date DESC
    LIMIT 5;
    """

    cur.execute(sql_query, (first_name, last_name))
    rows = cur.fetchall()

    output = []
    for rental_date, movie_title in rows:
        formatted_date = rental_date.strftime("%Y-%m-%d %H:%M:%S")
        output.append(f"{formatted_date}, {movie_title}")

    output_str = "\n".join(output)
    cur.close()
    conn.close()
    return output_str


@action(is_consequential=False)
def availability_in_stores(movie_title: str) -> str:
    """
    List availabitilty of a movie in different stores by the title.

    Args:
        title (str): Movie title. Example: "League Hellfighters"

    Returns:
        str: List of stores where the movie is available.
    """

    conn = _connect()
    cur = conn.cursor()
    limit = 5

    sql_query = """
    SELECT DISTINCT s.store_id, a.address, a.district, ci.city, co.country
    FROM film f
    JOIN inventory i ON f.film_id = i.film_id
    JOIN store s ON i.store_id = s.store_id
    JOIN address a ON s.address_id = a.address_id
    JOIN city ci ON a.city_id = ci.city_id
    JOIN country co ON ci.country_id = co.country_id
    WHERE f.title = %s
    LIMIT %s;
    """

    cur.execute(sql_query, (movie_title, limit))
    rows = cur.fetchall()
    output = []
    for row in rows:
        output.append(f"Store ID: {row[0]}, Address: {row[1]}, {row[2]}, {row[3]}, {row[4]}")

    output_str = "\n".join(output)
    print(output_str)
    cur.close()
    conn.close()
    return output_str


@action
def update_customer(id: int, new_email: str) -> str:
    """
    Update customers email address.

    Args:
        id (int): Customer ID. Example: 123
        new_email (str): New email address. Example: "first.last@example.com"

    Returns:
        str: Information whether the update was successful.
    """

    conn = _connect()
    cur = conn.cursor()

    sql_query = """
    UPDATE customer
    SET email = %s
    WHERE customer_id = %s;
    """

    cur.execute(sql_query, (new_email, id))

    conn.commit()
    if cur.rowcount == 1:
        print(f"Email updated successfully for customer ID {id}.")
        output = f"Email updated successfully for customer ID {id}."
    else:
        print(f"No record found for customer ID {id}.")
        output = f"No record found for customer ID {id}."

    cur.close()
    conn.close()
    return output
