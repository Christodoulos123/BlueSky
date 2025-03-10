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

# Define the output file for likes
# output_likes_json = os.path.join(latest_folder, "likes.json")
output_likes_json = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/likes3.json"

print(f"Using input file: {input_posts_json}")
print(f"Saving likes to: {output_likes_json}")

count = 1
all_likes = []  # List to store all like data

# Read post data from the JSON file
with open(input_posts_json, "r", encoding="utf-8") as json_file:
    posts_data = json.load(json_file)

# Ensure posts_data is a list
if isinstance(posts_data, dict) and "posts" in posts_data:
    posts_data = posts_data["posts"]

# Step 2: Fetch Likes for Each Post and Save to JSON
for post in posts_data:
    post_uri = post.get("uri")  # Adjusted key based on standard structure
    like_count = post.get("like_count")
    if not post_uri or like_count == 0:
        print(f"Skipping post: {post_uri} - it has {like_count} likes")
        continue
    
    print(f"{count}) Fetching likes for post: {post_uri}")
    count += 1
    
    # Fetch likes for the post
    likes_params = {
        "uri": post_uri,  # Required
        "limit": 100,  # Adjust limit as needed
    }
    
    try:
        time.sleep(0.5)  # Rate limit handling
        all_post_likes = []  # List to store likes for this post

        while True:
            likes_results = client.app.bsky.feed.get_likes(likes_params)
            
            # Append likes to the list
            if hasattr(likes_results, 'likes'):
                all_post_likes.extend(likes_results.likes)
            
            # Check for pagination
            if hasattr(likes_results, 'cursor') and likes_results.cursor:
                likes_params["cursor"] = likes_results.cursor
                print(f"Fetching more likes for post: {post_uri}")
            else:
                break  # No more likes available
        
        # Store the entire response for each post
        all_likes.append({
            "post_uri": post_uri,
            "likes": [like.dict() for like in all_post_likes]  # Convert to dictionary format
        })
    
    except Exception as e:
        print(f"Error fetching likes for post {post_uri}: {e}")

# Save all likes to a JSON file
with open(output_likes_json, "w", encoding="utf-8") as json_file:
    json.dump(all_likes, json_file, ensure_ascii=False, indent=4)

print(f"Likes saved to {output_likes_json}")
