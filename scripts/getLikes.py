import requests
import json
from atproto import Client

# Create a session
client = Client(base_url='https://bsky.social')

# Log in with your username and password (use proper exception handling here in a real application)
client.login('blueskyuser123.bsky.social', '1234')

# Retrieve the access token after logging in
token = client._access_jwt  # Ensure this is the right way to retrieve the token in your API library


# Endpoint URL for getLikes API
url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getLikes"

# Set up query parameter
params = {
    "uri": "at://did:plc:4lx6nur5wstwoc4wtgj56kyu/app.bsky.feed.post/3lbeozhjunc2d",  # Corrected AT-URI format
    "limit": 100  # Set limit to maximum
}
#https://bsky.app/profile/squoid.bsky.social/post/3lbekx4zsvc2e
#https://bsky.app/profile/squoid.bsky.social
#https://bsky.app/profile/gtconway.bsky.social/post/3lbeozhjunc2d

# Optionally, add an Authorization header if required
headers = {
    # "Authorization": f"Bearer {token}",
    # "Content-Type": "application/json"  # Ensure content type is set correctly
}

# Make the API request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    likes_data = response.json()
    print("Likes Data: ", likes_data)

    # Save the likes data in a JSON file
    with open("likes_data3.json", "w") as json_file:
        json.dump(likes_data, json_file, indent=4)  # indent=4 for pretty printing
    print("Likes data has been saved to 'likes_data.json'.")
else:
    print(f"Error: {response.status_code}")
    print(f"Response Text: {response.text}")
