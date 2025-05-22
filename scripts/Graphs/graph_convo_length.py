import json
import matplotlib.pyplot as plt
from collections import defaultdict

# Load the JSON file
with open('/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/merged_posts.json', 'r') as f:
    posts = json.load(f)

# Count how many posts have each reply count
reply_counts = defaultdict(int)
for post in posts:
    reply_count = post.get('reply_count', 0)
    reply_counts[reply_count] += 1

# Sort reply counts
sorted_replies = sorted(reply_counts.items())
reply_nums, post_counts = zip(*sorted_replies)

# Treat x as category indices (for equal spacing)
x_positions = list(range(len(reply_nums)))

plt.figure(figsize=(12, 6))
plt.bar(x_positions, post_counts, color='skyblue', width=0.8)

# Set custom labels for the evenly spaced ticks
plt.xticks(x_positions, labels=reply_nums, rotation=45, ha='right', fontsize=8)

plt.xlabel('Number of Replies')
plt.ylabel('Number of Posts')
# plt.ylim(0, 4500)  # Set y-axis range from 0 to 100
plt.yscale('log')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/graph_convo_length.png")
plt.show()
