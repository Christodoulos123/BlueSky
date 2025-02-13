from atproto import Client
import json

# Step 1: Set up Bluesky Client and Login
client = Client(base_url='https://bsky.social')
client.login('blueskyuser123.bsky.social', '1234')  # Replace with valid credentials

# Specify the AT-URI of the post you want to retrieve quotes for
post_uri = "at://did:plc:ynl2frkgfgqsi4s2v4q62gp6/app.bsky.feed.post/3l5ho3m2g642t"  # Replace with the actual AT-URI

# Output JSON file for storing quotes
output_file = "getQuotess.json"

try:
    # Fetch quotes using the Bluesky API
    quotes_results = client.app.bsky.feed.get_quotes({"uri": post_uri})
    
    # Convert the response to a dictionary
    quotes_data = quotes_results.dict()
    
    # Save the quotes data to a JSON file
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(quotes_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Quotes data has been saved to '{output_file}'.")

except Exception as e:
    print(f"Error fetching quotes for post {post_uri}: {e}")
