# description: This is a test file to test the instagrapi library using only the private API
from instagrapi import Client
import time
import signal
import os
from config import API_KEY, SESSION_ID, OWNER_USERNAME

cl = Client()
BOT_NAME = "raphael"
PROCESSED_FILE = "processed_dms.txt"
auto_responding = True

processed_message_ids = set()
if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE, 'r') as f:
        processed_message_ids = set(line.strip() for line in f)

def send_message_to_owner(message):
    global owner_id
    try:
        if owner_id is None:
            raise ValueError("Owner ID not initialized. Login may have failed.")
        cl.direct_send(message, [owner_id])
        print(f"Sent message to {OWNER_USERNAME}: {message}")
    except Exception as e:
        print(f"Failed to send message to owner: {e}")

def login():
    global owner_id, bot_id
    try:
        cl.login_by_sessionid(SESSION_ID)
        bot_info = cl.user_info_v1(cl.user_id)
        bot_id = bot_info.pk
        owner_info = cl.user_info_by_username_v1(OWNER_USERNAME)
        owner_id = owner_info.pk
        print(f"Logged in as {cl.username}, bot ID: {bot_id}, owner ID: {owner_id}")
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
    global auto_responding, processed_message_ids
    while True:
        if auto_responding:
            try:
                threads = cl.direct_threads(amount=20)
                for thread in threads:
                    thread_id = thread.id
                    messages = cl.direct_messages(thread_id, amount=5)
                    for message in messages:
                        message_id = message.id
                        if message_id in processed_message_ids:
                            print(f"Skipping processed message {message_id} in thread {thread_id}")
                            continue

                        print(f"Message {message_id} in thread {thread_id} from user_id: {message.user_id}, bot_id: {bot_id}")

                        if str(message.user_id) == str(bot_id):  # Convert to string for safety
                            print(f"Ignoring bot's own message {message_id} in thread {thread_id}: {message.text}")
                            processed_message_ids.add(message_id)
                            continue

                        message_text = message.text.strip().lower()
                        print(f"New DM in thread {thread_id} from {message.user_id}: {message.text}")

                        if BOT_NAME in message_text:
                            response = f"Greetings! Raphael here on {cl.username}. You said: '{message.text}'. How may I serve?"
                            cl.direct_send(response, [thread.users[0].pk])
                            print(f"Responded to {thread.users[0].pk} in thread {thread_id}")
                        elif "relinquish control" in message_text:
                            auto_responding = False
                            cl.direct_send("Auto-response paused.", [thread.users[0].pk])
                            print(f"Auto-response paused in thread {thread_id}")
                        elif "elevate awareness" in message_text:
                            send_message_to_owner(f"Raphael (on {cl.username}) was called in thread {thread_id}: '{message.text}'")
                            cl.direct_send(f"Notified {OWNER_USERNAME}.", [thread.users[0].pk])
                            print(f"Elevated awareness in thread {thread_id}")
                        else:
                            print(f"No action taken for message: {message.text}")

                        processed_message_ids.add(message_id)

            except Exception as e:
                print(f"Error in auto_respond: {e}")
        else:
            print(f"{time.ctime()} - Auto-response paused.")

        with open(PROCESSED_FILE, 'w') as f:
            for msg_id in processed_message_ids:
                f.write(f"{msg_id}\n")
        time.sleep(5)

def e_exit(signum, frame):
    print("\nShutting down...")
    with open(PROCESSED_FILE, 'w') as f:
        for msg_id in processed_message_ids:
            f.write(f"{msg_id}\n")
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, e_exit)

    if not login():
        exit()

    print_user_info()
    print("Starting auto-responder...")
    auto_respond()