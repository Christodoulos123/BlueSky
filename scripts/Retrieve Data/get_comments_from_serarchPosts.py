import os
import json
import time
from atproto import Client

# Step 1: Set up Bluesky Client and Login
client = Client(base_url='https://bsky.social')
client.login('blueskyuser123.bsky.social', '1234')  # Use your credentials

# Find the most recent folder inside 'output/'
base_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
latest_folder = max([os.path.join(base_output_dir, d) for d in os.listdir(base_output_dir) if os.path.isdir(os.path.join(base_output_dir, d))], key=os.path.getmtime)

# Get the latest JSON file (searched_posts.json)
# input_posts_json = os.path.join(latest_folder, "searched_posts.json")
input_posts_json = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/merged_posts.json"

# Define the output file for comments
# output_replies_json = os.path.join(latest_folder, "comments.json")
output_replies_json = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/comments3.json"

count = 1
all_replies = []  # List to store all reply data

# Read post data from the JSON file
with open(input_posts_json, "r", encoding="utf-8") as json_file:
    posts_data = json.load(json_file)

# Ensure posts_data is a list
if isinstance(posts_data, dict) and "posts" in posts_data:
    posts_data = posts_data["posts"]

# Step 2: Fetch Replies for Each Post and Save to JSON
for post in posts_data:
    post_uri = post.get("uri")  # Adjusted key based on standard structure
    comment_count = post.get("reply_count", 0)
    reply_data = post.get("record", {}).get("reply", {})


    if comment_count == 0 and not reply_data:
        print(f"Skipping post: {post_uri} not a thread")
        continue
    
    print(f"{count}) Fetching replies for post: {post_uri}")
    count += 1
    
    # Fetch replies for the post
    replies_params = {
        "uri": post_uri,  # Required
        "depth": 1000,  # Optional: specify how many levels of replies to include (default is 6)
        "parentHeight": 1000  # Optional: specify how many levels of parent posts to include (default is 80)
    }
    
    try:
        time.sleep(0.1)  # Rate limit handling
        replies_results = client.app.bsky.feed.get_post_thread(replies_params)
        
        # Store the entire response for each post
        all_replies.append({
            "post_uri": post_uri,
            "response": replies_results.dict()  # Convert response to dictionary format
        })
    
    except Exception as e:
        print(f"Error fetching replies for post {post_uri}: {e}")

# Save all replies to a JSON file
with open(output_replies_json, "w", encoding="utf-8") as json_file:
    json.dump(all_replies, json_file, ensure_ascii=False, indent=4)

print(f"Replies saved to {output_replies_json}")
