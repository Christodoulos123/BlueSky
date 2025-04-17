from atproto import Client
import json
from datetime import datetime
import os

# Create a session
client = Client(base_url='https://bsky.social')

# Log in with your username and password
client.login('blueskyuser123.bsky.social', '1234')

#Generate today's date for folder naming
current_date = datetime.now().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD

#Ensure the 'output' folder is located **outside** the 'scripts' folder
base_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
output_folder = os.path.join(base_output_dir, current_date)

os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn't exist

#Define the output file path
output_file = os.path.join(output_folder, "searched_posts.json")

# Read the query from the file
with open("/home/christodoulos/Documents/supplementary_files/combined_query.txt", "r", encoding="utf-8") as file:
    lucene_query = file.read().strip()

# Set up initial query parameters
params = {
    "q": lucene_query,  # Use the query from the file
    "limit": 100,  # Adjust limit as needed 
}

# Variable to store results
all_results = []

while True:
    try:
        # Make the API request
        search_results = client.app.bsky.feed.search_posts(params)

        # Append the raw response to the results list
        if hasattr(search_results, 'posts'):
            all_results.extend(search_results.posts)

        # Check if there's a next cursor for pagination
        if hasattr(search_results, 'cursor') and search_results.cursor:
            params["cursor"] = search_results.cursor  # Update the cursor in the query parameters
            print(f"Next cursor: {search_results.cursor}")
        else:
            print("No more results available.")
            break
    except Exception as e:
        print(f"Error during API request: {e}")
        break

# Define the output file path

# Write raw data to JSON
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump([post.dict() for post in all_results], json_file, ensure_ascii=False, indent=4)

print(f"Saved {len(all_results)} posts to {output_file}")
