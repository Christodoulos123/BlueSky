import requests
import json

# Endpoint URL for getPostThread API
url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread"

# Specify the AT-URI of the post you want to retrieve the thread for
at_uri = "at://paulwalker44.bsky.social/app.bsky.feed.post/3l73phdnooc23"  
    

# parameters
params = {
    "uri": at_uri, # Required
    "depth": 1000,         # Optional: specify how many levels of replies to include (default is 6)
    "parentHeight": 1000  # Optional: specify how many levels of parent posts to include (default is 80)
}
    
# Optionally, add an Authorization header if required
headers = {
    # "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Uncomment and replace if authentication is needed
}

# Make the API request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    thread_data = response.json()
    print("Thread Data: ", thread_data)

    # Save the thread data in a JSON file
    with open("../output/getThread.json", "w") as json_file:
        json.dump(thread_data, json_file, indent=4)  # indent=4 for pretty printing
    print("Thread data has been saved to 'getThread.json'.")
else:
    print(f"Error: {response.status_code}")
    print(f"Response Text: {response.text}")
    
