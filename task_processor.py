import time
from helpers import fetch_next_pending_request, update_request_status
from app import prompts_callback  # Import your processing logic from app.py

def process_pending_requests():
    """
    Continuously fetch and process pending requests from the database.
    """
    while True:
        try:
            # Fetch the next pending request
            request = fetch_next_pending_request()
            if not request:
                print("No pending requests. Waiting for new tasks...")
                time.sleep(5)  # Wait for 5 seconds before checking again
                continue

            # Extract request details
            request_id, user_input, file_url = request
            print(f"Processing request ID: {request_id}")
            print(f"Processing request ID: {user_input}")
            print(f"Processing request ID: {file_url}")

            # Mark request as 'Processing'
            update_request_status(request_id, status="Processing")

            try:
                # Process the request
                result = prompts_callback(user_input, file_url)

                # Ensure result is JSON-serializable
                if isinstance(result, tuple):
                    result = result[0]  # Extract the actual result (dictionary)

                # Mark request as 'Completed' and store the result
                update_request_status(request_id, status="Completed", result=result)
                print(f"Request ID {request_id} processed successfully.")
            except Exception as e:
                # Mark request as 'Failed' in case of errors
                print(f"Error processing request ID {request_id}: {e}")
                update_request_status(request_id, status="Failed")

        
        except Exception as e:
            print(f"Error in task processor: {e}")

        # Short pause between tasks
        time.sleep(1)

if __name__ == "__main__":
    print("Starting task processor...")
    process_pending_requests()
