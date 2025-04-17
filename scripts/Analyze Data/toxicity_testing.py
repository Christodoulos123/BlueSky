import json
import time
from googleapiclient import discovery

# Load your API key here
API_KEY = 'AIzaSyD3qTfgNWzLNGaqIndfVlx7AaWuf93zog4'

# Load input JSON
with open("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/extracted_quotes.json", "r") as f:
    data = json.load(f)

# Initialize the Perspective API client
client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

# Loop through entries and call the API
for item in data:
    text = item["quote_text"]

    analyze_request = {
        'comment': {'text': text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()
        score = response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        item["toxicity"] = score
        print(f"[✓] {item['quote_uri']} → TOXICITY: {score:.3f}")
    except Exception as e:
        print(f"[!] Error analyzing: {item['quote_uri']} → {e}")
        item["toxicity"] = None

    time.sleep(1)  # Respect API rate limits

# Save updated JSON to file
with open("quotes_toxicity.json", "w") as f:
    json.dump(data, f, indent=2)
