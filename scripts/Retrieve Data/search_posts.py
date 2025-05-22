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
with open("/home/christodoulos/Documents/BlueSky/dates_between.json", "r", encoding="utf-8") as json_file:
    dates_list = json.load(json_file)

# Containers for posts and counts
all_posts = []
daily_counts = defaultdict(int)
monthly_counts = defaultdict(int)

# Iterate over each date range
for date_range in dates_list:
    since = date_range["start_of_day"]
    until = date_range["end_of_day"]
    
    month_key = since[:7]  # YYYY-MM
    day_key = since[:10]   # YYYY-MM-DD

    params = {
        "q": lucene_query,
        "sort": "latest",
        "limit": 100,
        "since": since,
        "until": until,
    }

    print(f"Fetching data for the date: {since}")

    # Fetch data for this interval
    while True:
        try:
            search_results = client.app.bsky.feed.search_posts(params)
            time.sleep(0.1)

            if hasattr(search_results, 'posts'):
                all_posts.extend(search_results.posts)
                daily_counts[day_key] += len(search_results.posts)
                monthly_counts[month_key] += len(search_results.posts)

            if hasattr(search_results, 'cursor') and search_results.cursor:
                params["cursor"] = search_results.cursor
                print(f"Next cursor: {search_results.cursor}")
            else:
                print("No more results available for this interval.")
                break

        except Exception as e:
            print(f"Error during API request: {e}")
            break



# Save all posts to a single file
output_file = "/home/christodoulos/Documents/BlueSky/this_one/Search_results_all.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump([post.dict() for post in all_posts], f, ensure_ascii=False, indent=4)
print(f"Saved {len(all_posts)} posts to {output_file}")

# Save counts
counts_file = "/home/christodoulos/Documents/BlueSky/this_one/post_counts.json"
counts_data = {
    "daily_counts": dict(daily_counts),
    "monthly_counts": dict(monthly_counts)
}
with open(counts_file, 'w', encoding='utf-8') as f:
    json.dump(counts_data, f, ensure_ascii=False, indent=4)
print(f"Saved post counts to {counts_file}")
