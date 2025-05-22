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

# Filter out bins with 0 posts
filtered_bins = []
for label, count in zip(bin_labels, binned_counts):
    if count > 0:
        filtered_bins.append((label, count))

# 🔽 Sort bins by number of posts (ascending)
sorted_bins = sorted(filtered_bins, key=lambda x: x[1])  # sort by count

# Unzip into separate lists
sorted_labels = [label for label, _ in sorted_bins]
sorted_counts = [count for _, count in sorted_bins]

# Compute CDF in percentages
cumulative = np.cumsum(sorted_counts)
cdf = (cumulative / cumulative[-1]) * 100

# Plot CDF
plt.figure(figsize=(14, 6))
plt.plot(sorted_labels, cdf, color='orange', marker='o', linewidth=2)

# Labels and formatting
plt.xlabel('Like Count Range (sorted by frequency)', fontsize=12)
plt.ylabel('Cumulative % of Posts', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.ylim(0, 100)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/graph_likes_cdf_sorted_by_posts.png')
plt.show()
