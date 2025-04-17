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

# Define the output file for reposts
# output_reposts_json = os.path.join(latest_folder, "reposts.json")
output_reposts_json = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/reposts3.json"


print(f"Using input file: {input_posts_json}")
print(f"Saving reposts to: {output_reposts_json}")

count = 1
all_reposts = []  # List to store all repost data

# Read post data from the JSON file
with open(input_posts_json, "r", encoding="utf-8") as json_file:
    posts_data = json.load(json_file)

# Ensure posts_data is a list
if isinstance(posts_data, dict) and "posts" in posts_data:
    posts_data = posts_data["posts"]

# Step 2: Fetch Reposts for Each Post and Save to JSON
for post in posts_data:
    post_uri = post.get("uri")  # Adjusted key based on standard structure
    repost_count = post.get("repost_count", 0)

    # Skip posts with repost_count == 0
    if repost_count == 0:
        print(f"Skipping {post_uri} - No reposts")
        continue

    print(f"{count}) Fetching reposts for post: {post_uri}")
    count += 1

    # Fetch reposts for the post
    reposts_params = {
        "uri": post_uri,  # Required
        "limit": 100,  # Adjust limit as needed
    }

    try:
        time.sleep(0.1)  # Rate limit handling
        all_post_reposts = []  # List to store reposts for this post

        while True:
            reposts_results = client.app.bsky.feed.get_reposted_by(reposts_params)

            # Append reposts to the list
            if hasattr(reposts_results, 'reposted_by') and reposts_results.reposted_by:
                all_post_reposts.extend(reposts_results.reposted_by)

            # Check for pagination
            if hasattr(reposts_results, 'cursor') and reposts_results.cursor:
                reposts_params["cursor"] = reposts_results.cursor
                print(f"Fetching more reposts for post: {post_uri}")
            else:
                break  # No more reposts available

        # Store the entire response for each post
        all_reposts.append({
            "post_uri": post_uri,
            "reposts": [repost.dict() for repost in all_post_reposts]  # Convert to dictionary format
        })

    except Exception as e:
        print(f"Error fetching reposts for post {post_uri}: {e}")

# Save all reposts to a JSON file
with open(output_reposts_json, "w", encoding="utf-8") as json_file:
    json.dump(all_reposts, json_file, ensure_ascii=False, indent=4)

print(f"Reposts saved to {output_reposts_json}")