from atproto import Client
import json
import os

# Create a session
client = Client(base_url="https://bsky.social")

# Log in with your username and password
client.login("blueskyuser123.bsky.social", "1234")  # Replace with actual credentials

# Specify the AT-URI of the post you want to retrieve the thread for
at_uri = "at://blueskyuser123.bsky.social/app.bsky.feed.post/3l5hoaf53742j"
#https://bsky.app/profile/blueskyuser123.bsky.social/post/3l5hoaf53742j

# Parameters for fetching the post thread
params = {
    "uri": at_uri,  # Required
    "depth": 1000,  # Optional: specify how many levels of replies to include (default is 6)
    "parentHeight": 1000  # Optional: specify how many levels of parent posts to include (default is 80)
}

# Make the API request
try:
    thread_data = client.app.bsky.feed.get_post_thread(params)

    # Convert response to dictionary format
    thread_dict = thread_data.dict()

    # Define the output directory
    output_dir = "../output"
    os.makedirs(output_dir, exist_ok=True)

    # Save the thread data in a JSON file
    output_file = os.path.join(output_dir, "getThread_of_repost.json")
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(thread_dict, json_file, ensure_ascii=False, indent=4)

    print(f"Thread data has been saved to '{output_file}'.")

except Exception as e:
    print(f"Error fetching post thread: {e}")
