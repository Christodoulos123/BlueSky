from atproto import Client
import json
import time

# Initialize the Bluesky Client
client = Client(base_url="https://bsky.social")

# Log in with your username and password
client.login("blueskyuser123.bsky.social", "1234")  # Replace with actual credentials

# AT-URI of the post to fetch likes for
post_uri = "at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.post/3lgu4lg6j2k2v"

# Output file to save likes
output_file = "../ouput/getLikes.json"

# Pagination variables
cursor = None
all_likes = []
count = 0 

while True:
    try:
        # Set up parameters for fetching likes
        params = {"uri": post_uri, "limit": 100}  # Maximum limit per request
        if cursor:
            params["cursor"] = cursor  # Add pagination cursor if available

        # Fetch likes using Atproto Client
        response = client.app.bsky.feed.get_likes(params)

        # Ensure response contains likes data
        if hasattr(response, "likes"):
            all_likes.extend(response.likes)  # Append likes to list

        # Check if there is a next cursor for pagination
        if hasattr(response, "cursor") and response.cursor:
            cursor = response.cursor
            count += 1
            print(f"{count}Next cursor: {cursor}")
            time.sleep(1)  # Optional delay to respect API limits
        else:
            print("No more likes available.")
            break  # Exit loop if no more pages

    except Exception as e:
        print(f"Error fetching likes: {e}")
        break  # Stop if an error occurs

# Save all collected likes into a JSON file
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump([like.dict() for like in all_likes], json_file, ensure_ascii=False, indent=4)

print(f"Saved {len(all_likes)} likes to {output_file}")
