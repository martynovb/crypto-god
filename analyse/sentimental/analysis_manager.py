from analyse.sentimental.social.reddit_sent_analyser import RedditSentimentalAnalyser
from datetime import datetime

# subreddits = ['bitcoin', 'cryptocurrency', 'ethereum', 'solana', 'CryptoMarkets']
subreddits = ['bitcoin']

chunk_time_interval = 24 * 60 * 60  # 1 day
start_date = int(datetime(2023, 3, 1).timestamp())
end_date = int(datetime(2023, 3, 2).timestamp())

RedditSentimentalAnalyser().analyse(subreddits, start_date, end_date, chunk_time_interval, limit=10)
