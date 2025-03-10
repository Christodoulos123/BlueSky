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


# Define the output file for quotes
# output_quotes_json = os.path.join(latest_folder, "quotes.json")
output_quotes_json = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/quotes3.json"


print(f"Using input file: {input_posts_json}")
print(f"Saving quotes to: {output_quotes_json}")

count = 1
all_quotes = []  # List to store all quote data

# Read post data from the JSON file
with open(input_posts_json, "r", encoding="utf-8") as json_file:
    posts_data = json.load(json_file)

# Ensure posts_data is a list
if isinstance(posts_data, dict) and "posts" in posts_data:
    posts_data = posts_data["posts"]

# Step 2: Fetch Quotes for Each Post and Save to JSON
for post in posts_data:
    post_uri = post.get("uri")  # Adjusted key based on standard structure
    quote_count = post.get("quote_count", 0)

    # Skip posts with quoteCount == 0
    if quote_count == 0:
        print(f"Skipping {post_uri} - No quotes")
        continue

    print(f"{count}) Fetching quotes for post: {post_uri}")
    count += 1

    # Fetch quotes for the post
    quotes_params = {
        "uri": post_uri,  # Required
        "limit": 100,  # Adjust limit as needed
    }

    try:
        time.sleep(0.1)  # Rate limit handling
        all_post_quotes = []  # List to store quotes for this post

        while True:
            quotes_results = client.app.bsky.feed.get_quotes(quotes_params)

            # Append quotes to the list
            if hasattr(quotes_results, 'posts') and quotes_results.posts:
                all_post_quotes.extend(quotes_results.posts)

            # Check for pagination
            if hasattr(quotes_results, 'cursor') and quotes_results.cursor:
                quotes_params["cursor"] = quotes_results.cursor
                print(f"Fetching more quotes for post: {post_uri}")
            else:
                break  # No more quotes available

        # Store the entire response for each post
        all_quotes.append({
            "post_uri": post_uri,
            "quotes": [post.dict() for post in all_post_quotes]  # Convert to dictionary format
        })

    except Exception as e:
        print(f"Error fetching quotes for post {post_uri}: {e}")

# Save all quotes to a JSON file
with open(output_quotes_json, "w", encoding="utf-8") as json_file:
    json.dump(all_quotes, json_file, ensure_ascii=False, indent=4)

print(f"Quotes saved to {output_quotes_json}")