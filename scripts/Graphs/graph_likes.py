import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

# Load JSON data
with open('/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/merged_posts.json', 'r') as f:
    posts = json.load(f)

# Count how many posts have each like count
like_distribution = defaultdict(int)
for post in posts:
    likes = post.get('like_count', 0)
    like_distribution[likes] += 1

# Define bin width and bin ranges
bin_width = 50
max_likes = max(like_distribution.keys())
bins = np.arange(0, max_likes + bin_width, bin_width)
bin_labels = [f"{b}-{b + bin_width - 1}" for b in bins[:-1]]

# Aggregate like counts into bins
binned_counts = [0] * len(bin_labels)
for like, count in like_distribution.items():
    bin_index = min(like // bin_width, len(binned_counts) - 1)
    binned_counts[bin_index] += count

# Filter out bins with 0 posts to avoid empty space
filtered_labels = []
filtered_counts = []
for label, count in zip(bin_labels, binned_counts):
    if count > 0:
        filtered_labels.append(label)
        filtered_counts.append(count)

# Plot
plt.figure(figsize=(14, 6))
plt.bar(filtered_labels, filtered_counts, color='#1DA1F2', edgecolor='white')

# Log scale if needed
if max(filtered_counts) / max(1, min(c for c in filtered_counts if c > 0)) > 100:
    plt.yscale('log')
    plt.ylabel('Number of Posts (log scale)', fontsize=12)
else:
    plt.ylabel('Number of Posts', fontsize=12)

plt.xlabel('Like Count Range', fontsize=12)
plt.title('Distribution of Likes Across Posts (Binned)', fontsize=14, pad=20)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/graph_likes_binned_filtered.png')
plt.show()
