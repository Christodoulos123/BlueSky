import json
import matplotlib.pyplot as plt
from collections import defaultdict

# Load the JSON file
with open('/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/merged_posts.json', 'r') as f:
    posts = json.load(f)

# Count posts per instance
instance_counts = defaultdict(int)

for post in posts:
    handle = post['author']['handle']
    
    parts = handle.split('.')
    if len(parts) >= 2:
        instance = parts[-2] + '.' + parts[-1]
    else:
        instance = 'unknown'
    
    instance_counts[instance] += 1

# Sort all instances by count (no filtering), and get top 50
sorted_instances = sorted(instance_counts.items(), key=lambda x: x[1], reverse=True)[:100]
instances, counts = zip(*sorted_instances) if sorted_instances else ([], [])

# Plot
plt.figure(figsize=(14, 6))
plt.bar(instances, counts, color='skyblue')
plt.xlabel('Instance (Server)')
plt.ylabel('Number of Posts')
plt.yscale('log')
plt.title('Top 50 Instances by Number of Posts')
plt.xticks(rotation=45, ha='right', fontsize=6)
plt.tight_layout()
plt.savefig("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/graph_instance_top100.png")
plt.show()
