import json
import time
from atproto import Client

# Initialize client and login
client = Client(base_url='https://bsky.social')
client.login('blueskyuser123.bsky.social', '1234')  # Replace with your credentials

# Input and output paths
input_file = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/unique_users.json"  # File containing list of DIDs
output_file = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/fetched_profiles.json"      # Output JSON file

# Load DIDs
with open(input_file, "r", encoding="utf-8") as file:
    dids = json.load(file)

# Function to batch DIDs into chunks of 25
def chunked(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

# Store all profile results
all_profiles = []

# Process in batches of 25
for idx, batch in enumerate(chunked(dids, 25), start=1):
    print(f"Batch {idx}: Fetching {len(batch)} profiles")
    try:
        response = client.app.bsky.actor.get_profiles({"actors": batch})
        if hasattr(response, "profiles"):
            all_profiles.extend([profile.dict() for profile in response.profiles])
    except Exception as e:
        print(f"Error in batch {idx}: {e}")
    
    time.sleep(0.3)  # Be kind to the API

# Save results to output file
with open(output_file, "w", encoding="utf-8") as out_file:
    json.dump(all_profiles, out_file, ensure_ascii=False, indent=4)

print(f"Saved {len(all_profiles)} profiles to {output_file}")
