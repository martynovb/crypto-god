from analyse.sentiment_analyse.reddit_sentiment_analyse import RedditSentimentalAnalyser
from datetime import datetime

# subreddits = ['bitcoin', 'cryptocurrency', 'ethereum', 'solana', 'CryptoMarkets']
subreddits = ['bitcoin', 'cryptocurrency']

subreddit = "ethereum"
chunk_time_interval = 24 * 60 * 60  # 1 day
start_date = int(datetime(2023, 3, 1).timestamp())
end_date = int(datetime(2023, 3, 10).timestamp())

RedditSentimentalAnalyser().analyse(subreddits, start_date, end_date, chunk_time_interval, 10)
