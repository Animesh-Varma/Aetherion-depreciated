# description: This is a test file to test the instagrapi library using only the private API
from instagrapi import Client
import time
import signal

cl = Client()
SESSION_ID = "73300373711%3AktDL7jfBQoffRd%3A6%3AAYdXUbtnXs1LtbGC5jIjOJO4Gx9A0NZ6E688crM7Vw"
processed_message_ids = set()

def login():
    try:
        cl.login_by_sessionid(SESSION_ID)
        print("Login successful!")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False


def print_user_info():
    try:
        user_info = cl.user_info_v1(cl.user_id)
        print(f"Username: {user_info.username}")
        print(f"Full Name: {user_info.full_name}")
        print(f"Biography: {user_info.biography}")
        print(f"Followers: {user_info.follower_count}")
    except Exception as e:
        print(f"Failed to retrieve user info: {e}")


def auto_respond():
    while True:
        try:
            # Fetch the latest 20 DM threads
            threads = cl.direct_threads(amount=20)

            for thread in threads:
                thread_id = thread.id
                # Get the latest message in the thread
                messages = cl.direct_messages(thread_id, amount=1)
                if not messages:
                    continue

                latest_message = messages[0]
                message_id = latest_message.id

                # Skip if this message has already been processed
                if message_id in processed_message_ids:
                    print(f"Skipping already processed message {message_id} in thread {thread_id}")
                    continue

                # Only respond if the message is not from the bot and not "request acknowledged"
                if (latest_message.user_id != cl.user_id and
                        latest_message.text.strip().lower() != "request acknowledged"):
                    print(f"New DM in thread {thread_id} from {latest_message.user_id}: {latest_message.text}")

                    if len(thread.users) == 1:
                        recipient_id = thread.users[0].pk
                        cl.direct_send("request acknowledged", [recipient_id])
                        print(f"Sent response to {recipient_id} in thread {thread_id}")
                        # Track the incoming message ID, not the response
                        processed_message_ids.add(message_id)
                    else:
                        print(f"Group chat detected in thread {thread_id}, not auto-responding.")
                        processed_message_ids.add(message_id)

        except Exception as e:
            print(f"Error in auto_respond: {e}")

def e_exit(signum, frame):
    print("\nShutting down...")
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, e_exit)

    if not login():
        exit()

    print_user_info()

    print("Starting auto-responder...")
    auto_respond()