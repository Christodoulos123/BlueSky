import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


# Load the original file
with open("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/quotes_toxicity.json", "r") as f:
    data = json.load(f)

# Initialize VADER
sia = SentimentIntensityAnalyzer()

# Loop through the texts and compute sentiment
for item in data:
    text = item["quote_text"]
    sentiment = sia.polarity_scores(text)

    # Add the scores to the item
    item["sentiment"] = {
        "neg": sentiment["neg"],
        "neu": sentiment["neu"],
        "pos": sentiment["pos"],
        "compound": sentiment["compound"]
    }

    print(f"[✓] {item['quote_uri']} → compound: {sentiment['compound']}")

# Save the updated data back to the same file
with open("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/quotes_toxicity.json", "w") as f:
    json.dump(data, f, indent=2)
