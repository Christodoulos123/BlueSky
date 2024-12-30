import json
from atproto import Client
import requests

# Create a session
client = Client(base_url='https://bsky.social')

# Log in with your username and password (use proper exception handling here in a real application)
client.login('blueskyuser123.bsky.social', '1234')

# Retrieve the access token after logging in
token = client._access_jwt  # Ensure this is the right way to retrieve the token in your API library

# Replace this with the actual AT-URIs list you want to retrieve
uris = [
        "at://did:plc:ynl2frkgfgqsi4s2v4q62gp6/app.bsky.feed.post/3l5ho3m2g642t",
        
]
#https://bsky.app/profile/blueskyuser123.bsky.social/post/3l5ho3m2g642t

# Public API endpoint for Bluesky's app.bsky.feed.getPosts
url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts"

# Convert the list of URIs into a string, joined by commas (as required for GET query parameters)
params = {
    'uris': ','.join(uris)
}

# Prepare headers with the Bearer Token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"  # Ensure content type is set correctly
}

# Make the API request (using GET with query parameters)
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("Post Data: ", data)

    # Save the response in a JSON file
    with open("../output/Get_post.json", "w") as json_file:
        json.dump(data, json_file, indent=4)  # indent=4 for pretty printing
    print("Response has been saved to 'Get_post.json'.")
else:
    print(f"Error: {response.status_code}")
    print(f"Response Text: {response.text}")
