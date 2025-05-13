import json
import os

# === Constant Output Path ===
output_path = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/interactions.json"

# === User selection ===
mode = input("Extract interactions of type: 'reply', 'repost', 'quote', or 'like'? ").strip().lower()
if mode not in {"reply", "repost", "quote", "like"}:
    print("Invalid input. Choose 'reply', 'repost', 'quote', or 'like'.")
    exit()

# === Append helper ===
def append_to_output(new_data, output_path):
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            existing = json.load(f)
    else:
        existing = []
    existing.extend(new_data)
    with open(output_path, "w") as f:
        json.dump(existing, f, indent=2)
    print(f"Appended {len(new_data)} interactions to '{output_path}'")

# === Replies ===
if mode == "reply":
    reply_input_path = input("Path to replies file (e.g., comments3.json): ").strip()
    with open(reply_input_path, "r") as f:
        thread_data = json.load(f)

    def extract_reply_interactions(thread_node, parent_author=None):
        interactions = []
        post = thread_node.get("post", {})
        author = post.get("author", {})
        actor_did = author.get("did")
        actor_handle = author.get("handle")

        if parent_author:
            interactions.append({
                "actor": actor_did,
                "actor_handle": actor_handle,
                "target": parent_author["did"],
                "target_handle": parent_author["handle"],
                "interaction": "reply"
            })

        if "parent" in thread_node and isinstance(thread_node["parent"], dict):
            parent_post = thread_node["parent"].get("post", {})
            parent_author_info = parent_post.get("author", {})
            if parent_author_info:
                interactions += extract_reply_interactions(thread_node["parent"], author)

        replies = thread_node.get("replies")
        if isinstance(replies, list):
            for reply in replies:
                interactions += extract_reply_interactions(reply, author)

        return interactions

    all_interactions = []
    for thread in thread_data:
        if "response" in thread and "thread" in thread["response"]:
            root = thread["response"]["thread"]
            all_interactions.extend(extract_reply_interactions(root))

    append_to_output(all_interactions, output_path)

# === Reposts ===
elif mode == "repost":
    repost_input_path = input("Path to reposts file: ").strip()
    posts_input_path = input("Path to original posts file: ").strip()

    with open(repost_input_path, "r") as f:
        repost_data = json.load(f)
    with open(posts_input_path, "r") as f:
        original_posts = json.load(f)

    uri_to_author = {
        post["uri"]: {
            "did": post["author"]["did"],
            "handle": post["author"]["handle"]
        }
        for post in original_posts
    }

    def extract_repost_interactions(data, uri_map):
        interactions = []
        for entry in data:
            post_uri = entry.get("post_uri")
            original = uri_map.get(post_uri)
            if not original:
                continue
            for reposter in entry.get("reposts", []):
                interactions.append({
                    "actor": reposter.get("did"),
                    "actor_handle": reposter.get("handle"),
                    "target": original["did"],
                    "target_handle": original["handle"],
                    "interaction": "repost"
                })
        return interactions

    repost_interactions = extract_repost_interactions(repost_data, uri_to_author)
    append_to_output(repost_interactions, output_path)

# === Quotes ===
elif mode == "quote":
    quote_input_path = input("Path to quotes file: ").strip()
    posts_input_path = input("Path to original posts file: ").strip()

    with open(quote_input_path, "r") as f:
        quote_data = json.load(f)
    with open(posts_input_path, "r") as f:
        original_posts = json.load(f)

    uri_to_author = {
        post["uri"]: {
            "did": post["author"]["did"],
            "handle": post["author"]["handle"]
        }
        for post in original_posts
    }

    def extract_quote_interactions(data, uri_map):
        interactions = []
        for entry in data:
            for quote in entry.get("quotes", []):
                actor = quote.get("author", {})
                embedded_uri = (
                    quote.get("embed", {})
                         .get("record", {})
                         .get("uri")
                )
                original = uri_map.get(embedded_uri)
                if not (actor and original):
                    continue
                interactions.append({
                    "actor": actor.get("did"),
                    "actor_handle": actor.get("handle"),
                    "target": original["did"],
                    "target_handle": original["handle"],
                    "interaction": "quote"
                })
        return interactions

    quote_interactions = extract_quote_interactions(quote_data, uri_to_author)
    append_to_output(quote_interactions, output_path)

# === Likes ===
elif mode == "like":
    like_input_path = input("Path to likes file: ").strip()
    posts_input_path = input("Path to original posts file: ").strip()

    with open(like_input_path, "r") as f:
        like_data = json.load(f)
    with open(posts_input_path, "r") as f:
        original_posts = json.load(f)

    uri_to_author = {
        post["uri"]: {
            "did": post["author"]["did"],
            "handle": post["author"]["handle"]
        }
        for post in original_posts
    }

    def extract_like_interactions(data, uri_map):
        interactions = []
        for entry in data:
            post_uri = entry.get("post_uri")
            original = uri_map.get(post_uri)
            if not original:
                continue
            for like in entry.get("likes", []):
                actor = like.get("actor", {})
                interactions.append({
                    "actor": actor.get("did"),
                    "actor_handle": actor.get("handle"),
                    "target": original["did"],
                    "target_handle": original["handle"],
                    "interaction": "like"
                })
        return interactions

    like_interactions = extract_like_interactions(like_data, uri_to_author)
    append_to_output(like_interactions, output_path)
