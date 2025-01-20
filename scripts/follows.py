import requests
import json
import time 

time_differences = []

# Endpoint URL for getFollows API
url = "https://public.api.bsky.app/xrpc/app.bsky.graph.getFollows"

# Specify the actor (handle or DID) whose follows you want to enumerate
params = {
    "actor": "joncooper-us.bsky.social",  # Replace with the actor handle or DID
    "limit": 100,  # Optional: Number of results to fetch per request (default: 50, max: 100)
    "cursor": "",  # Optional: Cursor for pagination
}

# Optionally, add an Authorization header if authentication is required
headers = {
    # "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Uncomment and replace with your token if needed
}

while True:
    
    start = time.time()
    
    response = requests.get(url, headers=headers, params=params)
    
    end = time.time()
    
    time_differences.append(end - start)

    if response.status_code == 200:
        follows_data = response.json()
        print("Follows Data:", json.dumps(follows_data, indent=4))
        
        # Save the current page of results
        with open("../output/follows_data.json", "a") as json_file:
            json.dump(follows_data, json_file, indent=4)

        # Check for a cursor to fetch the next page
        if "cursor" in follows_data:
            params["cursor"] = follows_data["cursor"]
        else:
            break  # No more pages
    else:
        print(f"Error: {response.status_code}")
        print(f"Response Text: {response.text}")
        break
print(f"Time differences between requests: {time_differences}")
