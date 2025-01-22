import csv
from atproto import Client
import time

# Step 1: Set up Bluesky Client and Login
client = Client(base_url='https://bsky.social')
client.login('blueskyuser123.bsky.social', '1234')  # Use your credentials

# Input CSV file with searched posts
input_posts_csv = "../output/21_01_25/keywords_hashtags_phase1/search_Posts.csv"

# Output CSV file for replies
output_replies_csv = "../output/21_01_25/keywords_hashtags_phase1/comments_from_searchPost.csv"

count = 1

# Step 2: Fetch Replies for Each Post and Save to CSV
# Open the replies CSV for writing
with open(output_replies_csv, "w", newline="", encoding="utf-8") as replies_file:
    writer = csv.writer(replies_file)
    writer.writerow(["post_uri", "reply_uri", "reply_author", "reply_text", "reply_createdAt"])
    

    # Read post URIs from the posts CSV
    with open(input_posts_csv, "r", encoding="utf-8") as posts_file:
        posts_reader = csv.DictReader(posts_file)

        for row in posts_reader:
            post_uri = row["post's uri"]
            print(f"{count}) Fetching replies for post: {post_uri}")
            count += 1
            # Fetch replies for the post
            replies_params = {
                "uri": post_uri, # Required
                "depth": 1000,         # Optional: specify how many levels of replies to include (default is 6)
                "parentHeight": 1000  # Optional: specify how many levels of parent posts to include (default is 80)
            }

            try:
                time.sleep(0.1)
                replies_results = client.app.bsky.feed.get_post_thread(replies_params)

                # Save replies to the replies CSV
                for reply in replies_results.thread.replies:
                    writer.writerow([
                        post_uri,
                        reply.post.uri,
                        reply.post.author.did,
                        reply.post.record.text,
                        reply.post.record.created_at
                        ])

            except Exception as e:
                print(f"Error fetching replies for post {post_uri}: {e}")

print(f"Replies saved to {output_replies_csv}")
