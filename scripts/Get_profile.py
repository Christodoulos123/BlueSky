import requests
import json

# Endpoint URL for getProfile API
url = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile"

# Specify the actor (handle or DID) whose profile you want to retrieve
actor = "theonion.com"  # You can also use a DID like "did:plc:44ybard66vv44zksje25o7dz"

# Prepare the query parameters
params = {
    "actor": actor
}

# Optionally, if you need to authenticate, add the Authorization header (replace with your token)
headers = {
    # Uncomment if authentication is required:
    # "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}

# Make the API request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    profile_data = response.json()
    print("Profile Data: ", profile_data)

    # Save the profile data in a JSON file
    with open("../output/Get_profile.json", "w") as json_file:
        json.dump(profile_data, json_file, indent=4)  # indent=4 for pretty-printing the JSON
    print("Profile data has been saved to 'Get_profile.json'.")
else:
    print(f"Error: {response.status_code}")
    print(f"Response Text: {response.text}")
