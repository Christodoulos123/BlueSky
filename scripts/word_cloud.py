import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords

# Make sure stopwords are available
nltk.download('stopwords')

# --- Load your data (replace with your actual file path if needed) ---
with open("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/uris_and_texts.json", "r") as f:
    posts = json.load(f)

# --- Extract all text from the posts ---
all_text = " ".join(post["text"] for post in posts if "text" in post)

# --- Clean and preprocess ---
words = re.findall(r'\b\w+\b', all_text.lower())  # lowercase and extract words
filtered_words = [
    word for word in words
    if word not in stopwords.words("english") and len(word) > 2
]

# --- Prepare the cleaned text for the WordCloud ---
clean_text = " ".join(filtered_words)

# --- Generate Word Cloud ---
wordcloud = WordCloud(
    width=1200,
    height=600,
    background_color='white',
    colormap='viridis'
).generate(clean_text)

# --- Plot it ---
plt.figure(figsize=(14, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud of Frequent Words from Bluesky Posts")
plt.tight_layout()
plt.savefig("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/word_cloud.png")  # optional
plt.show()
