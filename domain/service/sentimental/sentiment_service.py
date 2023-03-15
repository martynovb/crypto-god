from data.api.social.reddit_api import RedditAPI
from data.db.models.sentiment_data import SentimentDataSource
from domain.service.sentimental.social.base_sentimental_service import SentimentServiceConfigs
from domain.service.sentimental.social.reddit_sentimental_service import RedditSentimentService
from domain.utils.sentymental_analyzer import SentimentalAnalyzer
from datetime import datetime


class SentimentService:
    def __init__(self, analyzer: SentimentalAnalyzer, reddit_api: RedditAPI):
        self._analyzer = analyzer
        self._reddit_sent_service = RedditSentimentService(analyzer, reddit_api)

    def start(self):
        self._reddit_sent_service.start_analysis(
            SentimentServiceConfigs(
                sentimental_data_source=SentimentDataSource.REDDIT,
                start_time_to_fetch=datetime(2023, 3, 1),
                end_time_to_fetch=datetime(2023, 3, 3),
            )
        )


SentimentService(SentimentalAnalyzer(), RedditAPI()).start()
