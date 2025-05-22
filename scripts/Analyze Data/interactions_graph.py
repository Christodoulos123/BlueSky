import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict

# === Config ===
input_path = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/interactions.json"
output_mapping_path = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/handle_id_map.json"
focus_users = {"naroop.bsky.social", "artcandee.bsky.social"}
MAX_PER_USER = 100  # Total max interactions per user, spread across interaction types

# === Load interactions ===
with open(input_path, "r") as f:
    all_interactions = json.load(f)

# === Distribute MAX_PER_USER evenly across interaction types ===
interaction_types = ["like", "reply", "repost", "quote"]
per_type_limit = MAX_PER_USER // len(interaction_types)

# === Track per-user, per-type counts ===
user_type_counts = defaultdict(lambda: defaultdict(int))
limited_interactions = []

for i in all_interactions:
    actor = i["actor_handle"]
    target = i["target_handle"]
    interaction_type = i["interaction"]

    if actor in focus_users or target in focus_users:
        for user in [actor, target]:
            if user in focus_users:
                if user_type_counts[user][interaction_type] < per_type_limit:
                    limited_interactions.append(i)
                    user_type_counts[user][interaction_type] += 1
                break  # Only count once for the first matching focus user

interactions = limited_interactions
print(f"Collected {len(interactions)} limited interactions involving focus users")

# === Get all handles involved ===
handles = set(i["actor_handle"] for i in interactions) | set(i["target_handle"] for i in interactions)
handle_to_id = {handle: idx for idx, handle in enumerate(sorted(handles))}
id_to_handle = {v: k for k, v in handle_to_id.items()}

# === Save handle-to-ID mapping ===
with open(output_mapping_path, "w") as f:
    json.dump(handle_to_id, f, indent=2)
print(f"Saved handle-to-ID mapping to '{output_mapping_path}'")

# === Build undirected graph ===
G = nx.Graph()
interaction_colors = {
    "like": "blue",
    "repost": "green",
    "reply": "orange",
    "quote": "purple"
}

for i in interactions:
    actor = handle_to_id[i["actor_handle"]]
    target = handle_to_id[i["target_handle"]]
    interaction_type = i["interaction"]
    color = interaction_colors.get(interaction_type, "gray")

    G.add_edge(
        actor,
        target,
        label=interaction_type,
        color=color
    )

# === Draw graph ===
pos = nx.spring_layout(G, k=1.0, seed=42)
edge_colors = [d['color'] for u, v, d in G.edges(data=True)]

plt.figure(figsize=(14, 10))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color='lightblue',
    node_size=800,
    font_size=9,
    arrows=True,
    edge_color=edge_colors,
    connectionstyle='arc3,rad=0.1'
)

legend_patches = [
    mpatches.Patch(color='blue', label='Like'),
    mpatches.Patch(color='green', label='Repost'),
    mpatches.Patch(color='orange', label='Reply'),
    mpatches.Patch(color='purple', label='Quote')
]
plt.legend(handles=legend_patches, loc='lower left', fontsize=10)

plt.title(f"Interaction Graph for {', '.join(focus_users)}", fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.savefig("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/User_graph.png", dpi=300)
print("Graph saved as 'User_graph.png'")
