import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === File paths (adjust if needed) ===
quotes_path = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/quotes_toxicity.json"
replies_path = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/replies_data.json"
posts_path = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/post_toxicity.json"

# === Function to load and normalize ===
def load_and_normalize(path, source_label, text_field):
    with open(path, "r") as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    df["source"] = source_label
    df["text"] = df[text_field]
    df["toxicity"] = df["toxicity"].astype(float)
    df["sentiment_compound"] = df["sentiment.compound"].astype(float)
    return df[["text", "toxicity", "sentiment_compound", "source"]]

# === Load and combine all ===
quotes_df = load_and_normalize(quotes_path, "quote", "quote_text")
replies_df = load_and_normalize(replies_path, "reply", "text")
posts_df = load_and_normalize(posts_path, "post", "text")

combined_df = pd.concat([quotes_df, replies_df, posts_df], ignore_index=True)

# === Summary statistics ===
summary = combined_df.groupby("source").agg(
    avg_toxicity=("toxicity", "mean"),
    high_toxicity_pct=("toxicity", lambda x: (x > 0.5).mean() * 100),
    avg_sentiment=("sentiment_compound", "mean"),
    negative_sentiment_pct=("sentiment_compound", lambda x: (x < -0.05).mean() * 100)
).reset_index()

print("\n📊 Summary Statistics:")
print(summary)

# === Boxplot: Toxicity ===
plt.figure(figsize=(10, 6))
sns.boxplot(data=combined_df, x="source", y="toxicity")
plt.ylabel("Toxicity Score")
plt.xlabel("Source")
plt.grid(True)
plt.tight_layout()
plt.savefig("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/toxicity_boxplot.png")
plt.show()

# === Boxplot: Sentiment Compound ===
plt.figure(figsize=(10, 6))
sns.boxplot(data=combined_df, x="source", y="sentiment_compound")
plt.ylabel("Sentiment Compound Score")
plt.xlabel("Source")
plt.grid(True)
plt.tight_layout()
plt.savefig("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/sentiment_boxplot.png")
plt.show()
