import requests
import json

# Base URL of the API
base_url = "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts"

# Headers for authentication (replace YOUR_ACCESS_TOKEN with your actual token)
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}

# Parameters for the initial request
params = {
    "q": "123",  # Search keyword
    "sort": "latest",  # Sort by latest or top
}

# File to save the results
output_file = "../output/search_Post.json"  # Relative path to the output folder

# Store results
all_results = []

# Pagination loop
while True:
    # Make the API request
    response = requests.get(base_url, headers=headers, params=params)
    
    # Check the response
    if response.status_code == 200:
        # Parse the response
        results = response.json()
        
        # Append posts to the results list
        all_results.extend(results.get("posts", []))
        
        # Check if there's a next cursor for pagination
        cursor = results.get("cursor")
        if cursor:
            # Update params with the new cursor
            params["cursor"] = cursor
        else:
            # No more pages
            break
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        break

# Save results to a JSON file
with open(output_file, "w") as f:
    json.dump(all_results, f, indent=4)

print(f"Saved {len(all_results)} posts to {output_file}")
