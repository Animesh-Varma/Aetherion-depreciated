# description: This is a test file to test the instagrapi library using only the private API
import time
from instagrapi import Client

cl = Client()
SESSION_ID = "73300373711%3AktDL7jfBQoffRd%3A6%3AAYdXUbtnXs1LtbGC5jIjOJO4Gx9A0NZ6E688crM7Vw"

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
        user_info = cl.user_info(cl.user_id)
        print(f"Username: {user_info.username}")
        print(f"Full Name: {user_info.full_name}")
        print(f"Biography: {user_info.biography}")
        print(f"Followers: {user_info.follower_count}")
    except Exception as e:
        print(f"Failed to retrieve user info: {e}")

def auto_respond():
    last_message_id = None

    while True:
        try:
            threads = cl.direct_threads(amount=20)

            for thread in threads:
                messages = cl.direct_messages(thread.id, amount=1)
                if not messages:
                    continue

                latest_message = messages[0]
                message_id = latest_message.id

                if (last_message_id is None or message_id > last_message_id) and latest_message.user_id != cl.user_id:
                    print(f"New DM from {latest_message.user_id}: {latest_message.text}")

                    if len(thread.users) == 1:
                        recipient_id = thread.users[0].pk
                        cl.direct_send("request acknowledged", [recipient_id])
                        print(f"Sent response to {recipient_id}")
                    else:
                        print("Group chat detected, not auto-responding.")

                    last_message_id = message_id

            time.sleep(5)

        except Exception as e:
            print(f"Error in auto-responder: {e}")
            time.sleep(30)

if __name__ == "__main__":
    if not login():
        exit()

    print_user_info()

    print("Starting auto-responder...")
    auto_respond()