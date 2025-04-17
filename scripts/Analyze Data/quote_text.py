import json

# Input and output paths
input_file = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/quotes3.json"
output_file = "/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/extracted_quotes.json"

# Load the input data
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# List to hold extracted quote info
extracted_quotes = []

# Process each quoted thread
for item in data:
    original_post_uri = item.get("post_uri")
    quotes = item.get("quotes", [])

    for quote in quotes:
        quote_uri = quote.get("uri")
        quote_text = quote.get("record", {}).get("text", "")

        extracted_quotes.append({
            "quote_uri": quote_uri,
            "original_post_uri": original_post_uri,
            "quote_text": quote_text
        })

# Save to output file
with open(output_file, "w", encoding="utf-8") as out_file:
    json.dump(extracted_quotes, out_file, ensure_ascii=False, indent=4)

print(f"Extracted {len(extracted_quotes)} quotes to {output_file}")
