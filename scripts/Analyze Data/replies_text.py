import json
import os

# Input and output files
input_file = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/comments3.json"
output_file = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/extracted_replies.json"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Store extracted replies
replies_data = []

# Recursive function to extract replies
def extract_replies(thread_node, parent_id=None, root_uri=None):
    if not thread_node:
        return

    post_info = thread_node.get("post")
    if post_info:
        current_uri = post_info.get("uri")
        text = post_info.get("record", {}).get("text", "")

        # If this is the root post, set root_uri
        if root_uri is None:
            root_uri = current_uri

        # Only collect replies (not the root/initial post)
        if parent_id:
            replies_data.append({
                "reply_id": current_uri,
                "parent_id": parent_id,
                "root_uri": root_uri,
                "text": text
            })

        # Process replies (if any)
        replies = thread_node.get("replies") or []
        for reply in replies:
            extract_replies(reply, parent_id=current_uri, root_uri=root_uri)

# Load the threads from input JSON file
with open(input_file, "r", encoding="utf-8") as file:
    threads = json.load(file)

# Process each thread in the list
for thread_block in threads:
    root = thread_block.get("response", {}).get("thread")
    extract_replies(root)

# Write the extracted replies to output file
with open(output_file, "w", encoding="utf-8") as out_file:
    json.dump(replies_data, out_file, ensure_ascii=False, indent=4)

print(f"Extracted {len(replies_data)} replies to {output_file}")
