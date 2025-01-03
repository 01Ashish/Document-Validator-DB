import json
from db_config import get_db_connection, close_db_connection

def insert_request(user_input, file_url):
    """
    Insert a new request into the database with a 'Pending' status.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO requests (user_input, file_url, status)
            VALUES (%s, %s, 'Pending') RETURNING id;
        """, (user_input, file_url))
        request_id = cur.fetchone()[0]
        conn.commit()
        return request_id
    except Exception as e:
        print(f"Error inserting request: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        close_db_connection(conn)

def fetch_next_pending_request():
    """
    Fetch the next 'Pending' request from the database for processing.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, user_input, file_url
            FROM requests
            WHERE status = 'Pending'
            ORDER BY created_at
            LIMIT 1
            FOR UPDATE SKIP LOCKED;
        """)
        request = cur.fetchone()
        print("request: ",request)
        return request  # Returns a tuple (id, user_input, file_url) or None
    except Exception as e:
        print(f"Error fetching next request: {e}")
        raise
    finally:
        cur.close()
        close_db_connection(conn)

def update_request_status(request_id, status, result=None):
    """
    Update the status and result of a request in the database.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        if result:
            cur.execute("""
                UPDATE requests
                SET status = %s, result = %s::JSON, processed_at = CURRENT_TIMESTAMP
                WHERE id = %s;
            """, (status, json.dumps(result), request_id))
        else:
            cur.execute("""
                UPDATE requests
                SET status = %s, processed_at = CURRENT_TIMESTAMP
                WHERE id = %s;
            """, (status, request_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating request status: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        close_db_connection(conn)

def fetch_request_result(request_id):
    """
    Fetch the result of a specific request by its ID.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT result
            FROM requests
            WHERE id = %s;
        """, (request_id,))
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching request result: {e}")
        raise
    finally:
        cur.close()
        close_db_connection(conn)
