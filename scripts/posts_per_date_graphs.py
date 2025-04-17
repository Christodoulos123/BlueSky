import json
import matplotlib.pyplot as plt
from datetime import datetime

# --- Load the JSON data from file ---
with open("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/post_counts.json", "r") as f:
    data = json.load(f)

# --- Monthly Plot ---
months = list(data["monthly_counts"].keys())
monthly_values = list(data["monthly_counts"].values())

plt.figure(figsize=(12, 5))
plt.bar(months, monthly_values, color='orange')
plt.title("Number of Posts Per Month")
plt.xlabel("Month")
plt.ylabel("Number of Posts")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/monthly_posts.png")
plt.show()

# --- Daily Plot ---
daily_dates = [datetime.strptime(date, "%Y-%m-%d") for date in data["daily_counts"].keys()]
daily_values = list(data["daily_counts"].values())

# Sort by date to ensure the line plot is correct
sorted_pairs = sorted(zip(daily_dates, daily_values))
sorted_dates, sorted_values = zip(*sorted_pairs)

plt.figure(figsize=(15, 5))
plt.plot(sorted_dates, sorted_values, color='orange', linewidth=1.2)
plt.title("Number of Posts Per Day")
plt.xlabel("Date")
plt.ylabel("Number of Posts")
plt.tight_layout()
plt.savefig("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/daily_posts.png")
plt.show()
