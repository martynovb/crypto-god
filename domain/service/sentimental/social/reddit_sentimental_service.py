import datetime

from data.api.social.reddit_api import RedditAPI
from data.db.dao.sentiment_dao import SentimentDAO
from data.db.models.sentiment_data import TimeRangeType
from domain.service.sentimental.social.base_sentimental_service import BaseSentimentService, SentimentServiceConfigs
from domain.utils.sentymental_analyzer import SentimentalAnalyzer

subreddits = ["bitcoin", "ethereum"]


class RedditSentimentService(BaseSentimentService):

    def __init__(self, analyzer: SentimentalAnalyzer, api: RedditAPI):
        super().__init__(analyzer)
        self._reddit_api = api

    def start_analysis(self, configs: SentimentServiceConfigs):
        data = self._fetch_data(configs)
        self._analyze_data(data)

    def _fetch_data(self, configs: SentimentServiceConfigs):
        submissions = []
        comments = []
        for subreddit in subreddits:
            current_time = configs.start_time_to_fetch
            while current_time < configs.end_time_to_fetch:
                end_time_interval = self.calculate_end_time_interval(current_time, configs.time_range_type)
                print(f'Reddit _fetch_data: start: from {current_time} to {end_time_interval}')
                submissions_temp = self._reddit_api.get_submissions(
                    subreddit=subreddit,
                    after=int(current_time.timestamp()),
                    before=int(end_time_interval.timestamp())
                )
                for submissions in submissions:
                    print(str(submissions))
                print("***************")
                comments_temp = self._reddit_api.get_comments(
                    subreddit=subreddit,
                    after=int(current_time.timestamp()),
                    before=int(end_time_interval.timestamp())
                )
                for comment in comments:
                    print(str(comment))
                submissions.append(submissions_temp)
                comments.append(comments_temp)
                current_time = end_time_interval
        return {"submissions": submissions, "comments": comments}

    def _analyze_data(self, data):
        for submissions in data["submissions"]:
            print(str(submissions))
        print("***************")
        for comment in data["comments"]:
            print(str(comment))

    def _save_data(self, analyzed_data):
        pass

    def calculate_end_time_interval(self, start_time_interval: datetime.datetime, time_range_type: TimeRangeType):
        if time_range_type == TimeRangeType.HOUR_1:
            end_time_interval = start_time_interval + datetime.timedelta(hours=1)
        elif time_range_type == TimeRangeType.DAY_1:
            end_time_interval = start_time_interval + datetime.timedelta(days=1)
        elif time_range_type == TimeRangeType.HOUR_4:
            end_time_interval = start_time_interval + datetime.timedelta(hours=4)
        elif time_range_type == TimeRangeType.MINUTE_5:
            end_time_interval = start_time_interval + datetime.timedelta(minutes=5)
        else:
            raise ValueError("Invalid time range type")
        return end_time_interval
