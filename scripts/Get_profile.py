from atproto import Client
import json
import os

# Create a session
client = Client(base_url="https://bsky.social")

# Log in with your username and password
client.login("blueskyuser123.bsky.social", "1234")  # Replace with actual credentials

# Specify the actor (handle or DID) whose profile you want to retrieve
actor = "did:plc:wx6hbspq4uaedrnpa77jfysz"  # You can also use a DID like "did:plc:44ybard66vv44zksje25o7dz"

# Make the API request
try:
    profile_data = client.app.bsky.actor.get_profile({"actor": actor})

    # Convert response to dictionary format
    profile_dict = profile_data.dict()

    # Define the output directory
    output_dir = "../output"
    os.makedirs(output_dir, exist_ok=True)

    # Save the profile data in a JSON file
    output_file = os.path.join(output_dir, "Get_profile.json")
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(profile_dict, json_file, ensure_ascii=False, indent=4)

    print(f"Profile data has been saved to '{output_file}'.")

except Exception as e:
    print(f"Error fetching profile: {e}")
