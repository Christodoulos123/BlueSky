import json
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from googleapiclient import discovery

# === Setup VADER sentiment analyzer ===
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# === Configuration ===
JSON_PATH = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/comments3.json"
API_KEY = "AIzaSyD3qTfgNWzLNGaqIndfVlx7AaWuf93zog4"
URI_LIST = [
    "at://did:plc:qxudeqrdbv6676vzjssrhllo/app.bsky.feed.post/3laylqmyff22r"
]
OUTPUT_PATH = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/toxicity_results.json"

# === Setup Perspective API client ===
client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

# === Load data ===
with open(JSON_PATH, "r") as f:
    all_threads = json.load(f)

# === Prepare output ===
results = []

# === Process each URI ===
for uri in URI_LIST:
    thread = next((t for t in all_threads if t.get("post_uri") == uri), None)

    if not thread:
        print(f"Post not found: {uri}")
        results.append({
            "post_uri": uri,
            "main_toxicity": None,
            "avg_reply_toxicity": None,
            "main_sentiment": None,
            "replies": [],
            "error": "Post not found"
        })
        continue

    try:
        # Analyze main post
        main_text = thread["response"]["thread"]["post"]["record"]["text"]
        main_req = {
            "comment": {"text": main_text},
            "requestedAttributes": {"TOXICITY": {}}
        }
        main_res = client.comments().analyze(body=main_req).execute()
        main_tox = main_res["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        main_sentiment = sia.polarity_scores(main_text)["compound"]

        # Analyze replies
        replies = thread["response"]["thread"].get("replies", [])
        tox_scores = []
        reply_data = []

        for reply in replies:
            try:
                text = reply["post"]["record"]["text"]
                # Perspective API
                req = {
                    "comment": {"text": text},
                    "requestedAttributes": {"TOXICITY": {}}
                }
                res = client.comments().analyze(body=req).execute()
                score = res["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
                tox_scores.append(score)

                # Sentiment
                sentiment = sia.polarity_scores(text)["compound"]

                print(f"Reply text: {text}")
                print(f"Toxicity score: {score:.3f}")
                print(f"Sentiment score: {sentiment:.3f}\n")

                reply_data.append({
                    "text": text,
                    "toxicity": score,
                    "sentiment": sentiment
                })

                time.sleep(1)
            except Exception as e:
                print(f"Error analyzing reply for {uri}: {e}")

        avg_tox = sum(tox_scores) / len(tox_scores) if tox_scores else None

        results.append({
            "post_uri": uri,
            "main_toxicity": main_tox,
            "main_sentiment": main_sentiment,
            "avg_reply_toxicity": avg_tox,
            "replies": reply_data
        })

    except Exception as e:
        print(f"Error analyzing main post for {uri}: {e}")
        results.append({
            "post_uri": uri,
            "main_toxicity": None,
            "main_sentiment": None,
            "avg_reply_toxicity": None,
            "replies": [],
            "error": str(e)
        })

# === Save results to file ===
with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

print(f"Done. Results saved to {OUTPUT_PATH}")
