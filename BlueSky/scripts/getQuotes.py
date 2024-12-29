import requests
import json

# Endpoint URL for getQuotes API
url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getQuotes"

# Specify the AT-URI of the post you want to retrieve quotes for
params = {
    "uri": "at://did:plc:ynl2frkgfgqsi4s2v4q62gp6/app.bsky.feed.post/3l5ho3m2g642t",  # Replace with the actual AT-URI of the post
}

# Optionally, add an Authorization header if required
headers = {
    # "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Uncomment and replace with your token if authentication is required
}

# Make the API request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    quotes_data = response.json()
    print("Quotes Data:", json.dumps(quotes_data, indent=4))

    # Save the quotes data in a JSON file
    with open("quotes_data.json", "w") as json_file:
        json.dump(quotes_data, json_file, indent=4)  # Pretty-print JSON
    print("Quotes data has been saved to 'quotes_data.json'.")
else:
    print(f"Error: {response.status_code}")
    print(f"Response Text: {response.text}")
