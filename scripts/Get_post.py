import json
from atproto import Client

# Create a session with the Bluesky API
client = Client(base_url='https://bsky.social')

# Log in with your username and password (ensure proper exception handling in real applications)
client.login('blueskyuser123.bsky.social', '1234')

# Replace this with the actual AT-URIs list you want to retrieve
uris = [
    "at://did:plc:ynl2frkgfgqsi4s2v4q62gp6/app.bsky.feed.post/3lknctw4z2s24"
]
#https://bsky.app/profile/blueskyuser123.bsky.social/post/3lknctw4z2s24
# Fetch posts directly using the atproto Client's API method
try:
    # Correcting function call by passing `uris` list directly
    response = client.app.bsky.feed.get_posts({"uris" : uris})  # Corrected method name and argument

    data = response.model_dump()
    
    print("Post Data:", data)

    # Save the response in a JSON file
    with open("../output/Get_post.json", "w") as json_file:
        json.dump(data, json_file, indent=4)  # indent=4 for pretty printing
    print("Response has been saved to 'Get_post.json'.")
    
except Exception as e:
    print(f"Error fetching posts: {e}")
