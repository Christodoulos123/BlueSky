import requests
import json

# Endpoint URL for getRepostedBy API
url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getRepostedBy"

# Set up query parameters
params = {
    "uri": "at://did:plc:a4pqq234yw7fqbddawjo7y35/app.bsky.feed.post/3lbufybe4i22f",  # Replace with the actual AT-URI of the post
}

#https://bsky.app/profile/theonion.com/post/3lbufybe4i22f

# Optionally, add an Authorization header if required
headers = {
    # "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Uncomment and replace with your token if authentication is required
}

# Make the API request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    reposts_data = response.json()
    print("Reposts Data:", json.dumps(reposts_data, indent=4))

    # Save the reposts data in a JSON file
    with open("../output/GetReposts.json", "w") as json_file:
        json.dump(reposts_data, json_file, indent=4)  # Pretty-print JSON
    print("Reposts data has been saved to 'GetReposts.json'.")
else:
    print(f"Error: {response.status_code}")
    print(f"Response Text: {response.text}")
