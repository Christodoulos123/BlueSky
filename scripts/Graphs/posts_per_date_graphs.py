import json
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import matplotlib.dates as mdates

# --- Load the JSON data from file ---
with open("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/post_counts.json", "r") as f:
    data = json.load(f)

# --- Monthly CDF Plot ---
months = list(data["monthly_counts"].keys())
monthly_values = list(data["monthly_counts"].values())

# Compute cumulative sum and normalize (for CDF)
cumulative = np.cumsum(monthly_values)
cdf = (cumulative / cumulative[-1])*100  # Normalize to 0–1

plt.figure(figsize=(12, 5))
plt.plot(months, cdf, marker='o', color='orange')
plt.xlabel("Month")
plt.ylabel("Cumulative Percentage of Posts")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/monthly_posts_cdf.png")
plt.show()

# --- Daily Plot with more x-axis labels ---
daily_dates = [datetime.strptime(date, "%Y-%m-%d") for date in data["daily_counts"].keys()]
daily_values = list(data["daily_counts"].values())

# Sort by date
sorted_pairs = sorted(zip(daily_dates, daily_values))
sorted_dates, sorted_values = zip(*sorted_pairs)

plt.figure(figsize=(15, 5))
plt.plot(sorted_dates, sorted_values, color='orange', linewidth=1.2)
plt.xlabel("Date")
plt.ylabel("Number of Posts")

# More x-axis labels
locator = mdates.AutoDateLocator(minticks=50, maxticks=50)
formatter = mdates.DateFormatter("%Y-%m-%d")
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig("/home/christodoulos/Documents/GitHub/BlueSky/output/timeStamp_Posts/info/daily_posts_dense_ticks.png")
plt.show()