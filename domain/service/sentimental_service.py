from datetime import datetime, timedelta
from typing import List

from data.api.social.reddit_api import RedditAPI
from data.dao.sentiment_dao import SentimentDAO
from data.models.sentiment_data import SentimentData, SentimentDataSource, TimeRangeType
from domain.utils.sentymental_analyzer import SentimentalAnalyzer


class SentimentService:
    def __init__(self, db_engine):
        self._dao = SentimentDAO(db_engine)
        self._reddit_api = RedditAPI()
        self._analyzer = SentimentalAnalyzer()

    def fetch_reddit_data(self):
        return {}

    def analyze_reddit_data(self):
        return {}

    def save_reddit_data(self):
        {}
