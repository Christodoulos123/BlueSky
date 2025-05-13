import json
from collections import Counter, defaultdict

# === Load interactions.json ===
interactions_path = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/interactions.json"
with open(interactions_path, "r") as f:
    interactions = json.load(f)

# === Count actions performed, received, and by type ===
actor_counts = Counter()
target_counts = Counter()
actor_by_type = defaultdict(lambda: Counter())
target_by_type = defaultdict(lambda: Counter())

# Go through each interaction once
for interaction in interactions:
    actor = interaction["actor_handle"]
    target = interaction["target_handle"]
    interaction_type = interaction["interaction"]

    actor_counts[actor] += 1
    target_counts[target] += 1

    actor_by_type[actor][interaction_type] += 1
    target_by_type[target][interaction_type] += 1

# === Build summary for all users ===
all_users = set(actor_counts.keys()).union(target_counts.keys())
summary = []

for user in all_users:
    performed = actor_counts.get(user, 0)
    received = target_counts.get(user, 0)
    total = performed + received

    summary.append({
        "user": user,
        "actions_performed": performed,
        "actions_received": received,
        "total_involved": total,
        "performed_by_type": dict(actor_by_type.get(user, {})),
        "received_by_type": dict(target_by_type.get(user, {}))
    })

# === Optional: Sort by total involvement
summary.sort(key=lambda x: x["total_involved"], reverse=True)

# === Save to JSON ===
output_path = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/interactions_all_users_summary.json"
with open(output_path, "w") as f:
    json.dump(summary, f, indent=2)

print(f"Saved summary of {len(summary)} users to '{output_path}'")
