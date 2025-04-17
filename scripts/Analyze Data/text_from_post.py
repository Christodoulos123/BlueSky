import json

# Input and output file paths
input_file = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/merged_posts.json"  # replace with your actual file name
output_file = "/~"

# Load data
with open(input_file, "r", encoding="utf-8") as file:
    posts = json.load(file)

# Extract only uri and text from each post
simplified_posts = []

for post in posts:
    uri = post.get("uri", "")
    text = post.get("record", {}).get("text", "")
    
    if uri and text:
        simplified_posts.append({
            "uri": uri,
            "text": text
        })

# Save the results
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(simplified_posts, outfile, ensure_ascii=False, indent=4)

print(f"Saved {len(simplified_posts)} posts to {output_file}")
