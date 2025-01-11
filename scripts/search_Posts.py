from atproto import Client
import csv

# Create a session
client = Client(base_url='https://bsky.social')

# Log in with your username and password
client.login('blueskyuser123.bsky.social', '1234')

# Set up initial query parameters
params = {
    "q": "Syria",  # Search query
    "sort": "latest",  # Sort by latest posts
    "limit": 100,  # Adjust limit as needed
}

# Variable to store results
all_results = []

while True:
    try:
        # Make the API request
        search_results = client.app.bsky.feed.search_posts(params)

        # Validate and sanitize posts
        valid_posts = []
        for post in search_results.posts:
            try:
                # Check for valid embed data or patch it
                if hasattr(post, 'embed') and post.embed:
                    if not hasattr(post.embed, 'aspectRatio'):
                        post.embed.aspectRatio = 'default_value'  # Replace with a valid default
                valid_posts.append(post)
            except Exception as post_error:
                print(f"Skipped a post due to an error: {post_error}")

        # Append the valid posts to the results list
        all_results.extend(valid_posts)

        # Check if there's a next cursor for pagination
        if search_results.cursor:
            params["cursor"] = search_results.cursor  # Update the cursor in the query parameters
            print(f"Next cursor: {search_results.cursor}")
        else:
            print("No more results available.")
            break
    except Exception as e:
        print(f"Error during API request: {e}")
        break

# Write results to CSV
with open('../output/search_Posts.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["post's uri", "author's did", "post's text", "replyCount", "repostCount", "likeCount"])

    for post in all_results:
        writer.writerow([
            post.uri,
            post.author.did,
            getattr(post.record, 'text', 'N/A'),
            getattr(post, 'reply_count', 0),
            getattr(post, 'repost_count', 0),
            getattr(post, 'like_count', 0)
        ])
