import pandas as pd
from atproto import Client
import csv


# Load the CSV file
input_file = '../output/search_Posts.csv'  # Replace with your actual file name
df = pd.read_csv(input_file)

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


# Prepare the output file
output_file = '../output/profiles_of_searched_posts.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["did", "handle", "description","followers_count","follows_count","created_at",])  # Adjust columns as needed

    # Process DIDs in batches (max 25 as per API docs)
    batch_size = 25
    did_list = df["author's did"].tolist()
    
    for i in range(0, len(did_list), batch_size):
        batch = did_list[i:i + batch_size]
        print(f"Fetching batch {i // batch_size + 1}: {batch}")
        
        profiles = fetch_profiles(client, batch)
        
        for profile in profiles:
            writer.writerow([
                profile.did,
                profile.handle,
                profile.description,
                profile.followers_count,
                profile.follows_count,
                profile.created_at
            ])  # Adjust based on the API response structure
        

print(f"Profile data saved to {output_file}")
