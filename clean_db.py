from db_config import get_db_connection, close_db_connection
from datetime import datetime
import time

def delete_old_data():
    """
    Delete rows from the 'requests' table where the created_at timestamp
    is older than 20 days.
    """
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # SQL query to delete rows older than 20 days
        delete_query = """
        DELETE FROM requests
        WHERE created_at < NOW() - INTERVAL '20 days';
        """

        cur.execute(delete_query)
        deleted_rows = cur.rowcount
        conn.commit()

        print(f"Deleted {deleted_rows} rows older than 20 days.")

    except Exception as e:
        print(f"Error deleting old data: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            close_db_connection(conn)

if __name__ == "__main__":
    print("Starting the data cleaning service...")
    while True:
        try:
            delete_old_data()
            print("Data cleaning completed. Waiting for the next run...")
            # Sleep for 24 hours before the next cleanup
            time.sleep(15)
        except KeyboardInterrupt:
            print("Data cleaning service stopped.")
            break
