# description: This is a test file to test the instagrapi library using only the private API
import time
from instagrapi import Client

cl = Client()
SESSION_ID = "73300373711%3AktDL7jfBQoffRd%3A6%3AAYdXUbtnXs1LtbGC5jIjOJO4Gx9A0NZ6E688crM7Vw"

cl.delay_range = [1, 3]

try:
    cl.login_by_sessionid(SESSION_ID)
    print("Login successful!")
except Exception as e:
    print(f"Login failed: {e}")
    exit()

try:
    user_info = cl.user_info_v1(cl.user_id)  #
    print(f"Username: {user_info.username}")
    print(f"Full Name: {user_info.full_name}")
    print(f"Biography: {user_info.biography}")
    print(f"Followers: {user_info.follower_count}")
except Exception as e:
    print(f"Failed to retrieve user info: {e}")

# this is a test