from atproto import Client
import json
from datetime import datetime
import time
import os
from collections import defaultdict

# Create a session
client = Client(base_url='https://bsky.social')

# Log in with your username and password
client.login('blueskyuser123.bsky.social', '1234')

# Read the query from the file
with open("/home/christodoulos/Documents/supplementary_files/combined_query.txt", "r", encoding="utf-8") as file:
    lucene_query = file.read().strip()

# Load the dates from the dates_between.json file
with open("dates_between.json", "r", encoding="utf-8") as json_file:
    dates_list = json.load(json_file)

# Dictionary to store results grouped by month and day
monthly_results = defaultdict(list)
daily_counts = defaultdict(int)
monthly_counts = defaultdict(int)

# Iterate over each date range in the dates_between.json file
for date_range in dates_list:
    since = date_range["start_of_day"]
    until = date_range["end_of_day"]
    
    # Extract year and month for file naming
    month_key = since[:7]  # Format: YYYY-MM
    day_key = since[:10]  # Format: YYYY-MM-DD
    
    # Set up query parameters for this interval
    params = {
        "q": lucene_query,  # Use the query from the file
        "sort": "latest",  # Sort by latest posts
        "limit": 100,  # Adjust limit as needed
        "since": since,
        "until": until,
    }

    print(f"Fetching data for the date: {since}")

    # Fetch data for this interval
    while True:
        try:
            # Make the API request
            search_results = client.app.bsky.feed.search_posts(params)
            time.sleep(0.1)

            # Append the raw response to the results list for this month
            if hasattr(search_results, 'posts'):
                monthly_results[month_key].extend(search_results.posts)
                daily_counts[day_key] += len(search_results.posts)
                monthly_counts[month_key] += len(search_results.posts)

            # Check if there's a next cursor for pagination
            if hasattr(search_results, 'cursor') and search_results.cursor:
                params["cursor"] = search_results.cursor  # Update the cursor in the query parameters
                print(f"Next cursor: {search_results.cursor}")
            else:
                print("No more results available for this interval.")
                break

        except Exception as e:
            print(f"Error during API request: {e}")
            break

# Ensure output directory exists
output_dir = "months/3"
os.makedirs(output_dir, exist_ok=True)

# Write results to separate JSON files per month
for month, posts in monthly_results.items():
    output_file_name = os.path.join(output_dir, f"Search_results_{month}.json")
    with open(output_file_name, 'w', encoding='utf-8') as json_file:
        json.dump([post.dict() for post in posts], json_file, ensure_ascii=False, indent=4)
    print(f"Saved {len(posts)} posts to {output_file_name}")

# Save daily and monthly counts to a JSON file
counts_file = os.path.join(output_dir, "post_counts.json")
counts_data = {
    "daily_counts": dict(daily_counts),
    "monthly_counts": dict(monthly_counts)
}
with open(counts_file, 'w', encoding='utf-8') as json_file:
    json.dump(counts_data, json_file, ensure_ascii=False, indent=4)
print(f"Saved post counts to {counts_file}")
