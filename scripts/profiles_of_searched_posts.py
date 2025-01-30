from atproto import Client
import json
import time  # For delays (rate-limiting)

# Load the input JSON file
input_file = 'raw_response.json'  # Replace with your actual JSON file
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract the posts list from the response JSON
posts = data.get("posts", [])  # Get 'posts' or default to an empty list

# Extract the DIDs from each post
did_list = [post["author"]["did"] for post in posts if "author" in post and "did" in post["author"]]


# Initialize the Bluesky Client
client = Client(base_url="https://bsky.social")  # Adjust the base URL if needed
client.login('blueskyuser123.bsky.social', '1234')

# Function to fetch profiles for a batch of DIDs
def fetch_profiles(client, dids):
    try:
        # Fetch profiles using the client
        response = client.app.bsky.actor.get_profiles({"actors": dids})
        
        # Check if 'profiles' is an attribute of the response
        if hasattr(response, 'profiles'):
            return response.profiles  # Access the profiles attribute directly
        else:
            print("No profiles found in the response.")
            return []
    except Exception as e:
        print(f"Error fetching profiles: {e}")
        return []

# Prepare the output JSON file
output_file = f'profiles_from_{input_file}'
all_profiles = []

# Process DIDs in batches (max 25 as per API docs)
batch_size = 25

for i in range(0, len(did_list), batch_size):
    batch = did_list[i:i + batch_size]
    print(f"Fetching batch {i // batch_size + 1}: {batch}")
    
    profiles = fetch_profiles(client, batch)
    
    # Convert profiles to dictionaries (if needed) and add to the result list
    all_profiles.extend([profile.dict() for profile in profiles])  # Adjust if profile is not a Pydantic model
    
    time.sleep(1)  # Optional delay to respect rate limits

# Save the results to the JSON file
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(all_profiles, file, ensure_ascii=False, indent=4)

print(f"Profile data saved to {output_file}")
    