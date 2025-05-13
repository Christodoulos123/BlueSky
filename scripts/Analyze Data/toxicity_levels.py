import json
import pandas as pd

# === File paths ===
files = [
    ("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/quotes_toxicity.json", "quote", "quote_text"),
    ("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/replies_data.json", "reply", "text"),
    ("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/post_toxicity.json", "post", "text"),
]

# === Toxicity classification logic ===
def classify_toxicity(score):
    if score > 0.8:
        return "very high"
    elif score > 0.5:
        return "high"
    elif score > 0.2:
        return "moderate"
    else:
        return "low"

# === Load and classify data ===
dataframes = []

for path, source, text_field in files:
    with open(path, "r") as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    df["source"] = source
    df["text"] = df[text_field]
    df["toxicity"] = df["toxicity"].astype(float)
    df["toxicity_level"] = df["toxicity"].apply(classify_toxicity)
    dataframes.append(df[["text", "toxicity", "toxicity_level", "source"]])

# === Combine all data ===
combined_df = pd.concat(dataframes, ignore_index=True)

# === 1. Overall toxicity level counts ===
print("🧮 Overall Toxicity Counts (All Sources):")
print("(low: ≤0.2, moderate: 0.2–0.5, high: 0.5–0.8, very high: >0.8)")
overall_counts = combined_df["toxicity_level"].value_counts().reindex(
    ["low", "moderate", "high", "very high"], fill_value=0
)
print(overall_counts)

# === 2. Per-source breakdown ===
print("\n📊 Toxicity Counts by Source:")
print("(low: ≤0.2, moderate: 0.2–0.5, high: 0.5–0.8, very high: >0.8)")
source_grouped = combined_df.groupby(["source", "toxicity_level"]).size().unstack(fill_value=0)
source_grouped = source_grouped[["low", "moderate", "high", "very high"]]  # ordered columns
print(source_grouped)
