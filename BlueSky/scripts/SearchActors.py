import requests
import json

# Endpoint URL for searchActors API
url = "https://public.api.bsky.app/xrpc/app.bsky.actor.searchActors"

# Prepare the query parameters
params = {
    "q": "Katie",  # The search query, modify this to search for other terms
    "limit": 10    # Optional: limit the number of results, default is 25
    # Optionally add "cursor" for pagination if needed
}

# Optionally, if authentication is required, add the Authorization header (replace with your token)
headers = {
    # "Authorization": "Bearer YOUR_ACCESS_TOKEN"
}

# Make the API request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    search_results = response.json()
    print("Search Results: ", search_results)

    # Save the search results in a JSON file
    with open("search_Actors.json", "w") as json_file:
        json.dump(search_results, json_file, indent=4)  # indent=4 for pretty printing
    print("Search results have been saved to 'search_results.json'.")
else:
    print(f"Error: {response.status_code}")
    print(f"Response Text: {response.text}")

