import requests
import json
import time


time_differences = []


# Endpoint URL for searchPosts API
url = "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts"



# Set up initial query parameters
params = {
    "q": "Syria",  # Search query
    "sort": "latest",  # Sort by latest posts
    "limit": 100,  # Adjust limit as needed (default is 25)
    "cursor": "",
}

# Optionally, add an Authorization header if required
headers = {

}



all_results = []

while True:  # Keep fetching until there are no more results
    start = time.time()
    
    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    end = time.time()
    time_differences.append(end - start)
    
    if response.status_code == 200:
        search_results = response.json()
        print(f"search_results:\n {search_results}\n")  
        posts = search_results.get("posts", [])
        print(f"only the posts from search_results:\n {posts}")
        all_results.extend(posts)  # Add the posts to the results list
        print(f"Fetched {len(posts)} posts. Total so far: {len(all_results)}")
        
        # Check for the cursor to fetch the next page
        cursor = search_results.get("cursor")
        if cursor != None:
            params["cursor"] = cursor  # Update the cursor in the query parameters
            str(cursor)
            print(f"Next Cursor: {cursor}")
            print(f"params:\n {params}")
        else:
            print("No more results available.")
            break
    else:
        print(f"Error: {response.status_code}")
        print(f"Response Text: {response.text}")
        break


# Save the search results in a JSON file
with open("search_posts_results_paginated.json", "w") as json_file:
    json.dump(all_results, json_file, indent=4)  # indent=4 for pretty printing
print("All search results have been saved to 'search_posts_results_paginated.json'.")

# Print time differences
print(f"Time differences between requests: {time_differences}")
