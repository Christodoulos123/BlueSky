import json
from atproto import Client
import requests

# Create a session
client = Client(base_url='https://bsky.social')
client.login('blueskyuser123.bsky.social', '1234')

# Get the Bearer token
token = client._access_jwt  # Ensure you have the right attribute to get the token

# Define the AT-URI for the feed you want to get
feed_uri = "at://did:plc:q6gjnaw2blty4crticxkmujt/app.bsky.feed.generator/cv:cat"  # Replace with the actual feed URI

# Prepare the request
url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getFeed"
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}
params = {
    "feed": feed_uri,  # Pass the feed AT-URI here
}

# Make the GET request to retrieve the feed
response = requests.get(url, headers=headers, params=params)

# Check the response
if response.status_code == 200:
    # Parse and print the feed in the console
    feed_data = response.json()
    print("Feed:", feed_data)
    
    # Save the response to a JSON file
    with open('../output/feed_output.json', 'w') as json_file:
        json.dump(feed_data, json_file, indent=4)
    print("Output saved to feed_output.json")
else:
    print("Error:", response.status_code, response.text)

