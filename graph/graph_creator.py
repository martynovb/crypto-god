import matplotlib.pyplot as plt
import os
import json
import numpy as np
import matplotlib.dates as mdates
import datetime as dt


with open(os.path.join('../analyse/sentimental', 'reddit_analysis.json'), 'r') as f:
    data = json.load(f)


# Create a dictionary to hold the aggregated sentimental data
agg_sentiment = {}

# Iterate through each subreddit's historical data
for subreddit_data in data:
    subreddit = subreddit_data["subreddit"]
    sentiment_data = subreddit_data["sentiment_historical_data"]

    # Iterate through each chunk of sentimental data
    for chunk in sentiment_data:
        chunk_start = chunk["chunk_time_range_start"]
        tb_sentiment = chunk["total_sentimental"]["tb"]
        vd_sentiment = chunk["total_sentimental"]["vd"]
        sp_sentiment = chunk["total_sentimental"]["sp"]
        total_sentiment = chunk["total_sentimental"]["total"]

        # Add the sentimental data to the dictionary
        if chunk_start not in agg_sentiment:
            agg_sentiment[chunk_start] = {"tb": [], "vd": [], "sp": [], "total": []}
        agg_sentiment[chunk_start]["tb"].append(tb_sentiment)
        agg_sentiment[chunk_start]["vd"].append(vd_sentiment)
        agg_sentiment[chunk_start]["sp"].append(sp_sentiment)
        agg_sentiment[chunk_start]["total"].append(total_sentiment)

# Calculate the average sentimental for each chunk
avg_sentiment = {"tb": [], "vd": [], "sp": [], "total": []}
for chunk_start in sorted(agg_sentiment.keys()):
    avg_tb = np.mean(agg_sentiment[chunk_start]["tb"])
    avg_vd = np.mean(agg_sentiment[chunk_start]["vd"])
    avg_sp = np.mean(agg_sentiment[chunk_start]["sp"])
    avg_total = np.mean(agg_sentiment[chunk_start]["total"])
    avg_sentiment["tb"].append(avg_tb)
    avg_sentiment["vd"].append(avg_vd)
    avg_sentiment["sp"].append(avg_sp)
    avg_sentiment["total"].append(avg_total)

# Convert datetime objects to matplotlib date format
x = [mdates.date2num(dt) for dt in sorted(agg_sentiment.keys())]

# Plot the sentimental data
plt.plot(x, avg_sentiment["tb"], label="tb")
plt.plot(x, avg_sentiment["vd"], label="vd")
plt.plot(x, avg_sentiment["sp"], label="sp")
plt.plot(x, avg_sentiment["total"], label="total")
plt.legend()



# Convert matplotlib dates to strings
x_labels = [dt.datetime.fromtimestamp(chunk_start).strftime('%d/%m/%y') for chunk_start in sorted(agg_sentiment.keys())]



# Convert datetime objects to matplotlib date format
plt.gca().set_xticks(x)


# Set the x-tick labels
plt.gca().set_xticklabels(x_labels)



plt.show()
