import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration details
DB_CONFIG = {
    'dbname': 'database_name',  # Replace with your database name
    'user': 'postgresql_username',      # Replace with your PostgreSQL username
    'password': 'postgresql_password',  # Replace with your PostgreSQL password
    'host': 'localhost',          # Replace with your database host (e.g., localhost)
    'port': 5432                  # Replace with your PostgreSQL port (default: 5432)
}

def get_db_connection():
    """
    Establish a connection to the PostgreSQL database.
    Returns a connection object.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def close_db_connection(conn):
    """
    Close the database connection.
    """
    if conn:
        conn.close()
