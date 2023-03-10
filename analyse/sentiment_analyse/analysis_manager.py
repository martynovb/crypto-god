from analyse.sentiment_analyse.reddit_sentiment_analyse import RedditSentimentalAnalyser
from datetime import datetime

subreddits = ['bitcoin', 'cryptocurrency', 'ethereum', 'solana', 'CryptoMarkets']

subreddit = "ethereum"
chunk_time_interval = 24 * 60 * 60  # 1 day
start_date = int(datetime(2015, 9, 24).timestamp())
end_date = int(datetime(2015, 9, 26).timestamp())

RedditSentimentalAnalyser().fetch_submission_ids_in_time_range("bitcoin", chunk_time_interval, start_date)
