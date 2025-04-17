import os
import json

# === Input file ===
input_file = input("📄 Enter the path to the input JSON file: ").strip()

# === Output file path (persistent across runs) ===
output_file = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/unique_users.json"

# === Prompt for data type ===
print("\n🔍 What kind of data is in this file?")
print("1 - Posts")
print("2 - Quotes")
print("3 - Likes")
print("4 - Reposts")
print("5 - Comments")
data_type = input("Enter the number (1/2/3/4/5): ").strip()

mode_map = {
    "1": "posts",
    "2": "quotes",
    "3": "likes",
    "4": "reposts",
    "5": "comments"
}

mode = mode_map.get(data_type)
if not mode:
    raise ValueError("❌ Invalid selection. Please enter 1, 2, 3, 4, or 5.")

# === Load existing unique DIDs ===
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        unique_users = set(json.load(f))
else:
    unique_users = set()

# === Load input data ===
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# === Mode-specific DID extraction ===
def extract_dids_from_comments(thread):
    # Top-level post
    if "author" in thread.get("post", {}):
        unique_users.add(thread["post"]["author"].get("did"))

    # Safe fallback for replies
    replies = thread.get("replies") or []
    for reply in replies:
        if "post" in reply and "author" in reply["post"]:
            unique_users.add(reply["post"]["author"].get("did"))
        # Recurse safely
        extract_dids_from_comments(reply)


if mode == "posts":
    for post in data:
        if "author" in post and "did" in post["author"]:
            unique_users.add(post["author"]["did"])

elif mode == "quotes":
    for post in data:
        quotes = post.get("quotes", [])
        for quote in quotes:
            author = quote.get("author")
            if author and "did" in author:
                unique_users.add(author["did"])

elif mode == "likes":
    for post in data:
        likes = post.get("likes", [])
        for like in likes:
            actor = like.get("actor")
            if actor and "did" in actor:
                unique_users.add(actor["did"])

elif mode == "reposts":
    for post in data:
        reposts = post.get("reposts", [])
        for repost in reposts:
            if "did" in repost:
                unique_users.add(repost["did"])

elif mode == "comments":
    for item in data:
        thread = item.get("response", {}).get("thread")
        if thread:
            extract_dids_from_comments(thread)

# === Save updated unique users list ===
unique_users_list = sorted(unique_users)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(unique_users_list, f, ensure_ascii=False, indent=4)

# === Done! ===
print(f"\n✅ Done! Processed '{input_file}' as '{mode}'.")
print(f"📌 Total unique users (DIDs): {len(unique_users_list)}")
print(f"📁 DIDs saved to: {output_file}")
