from data.db.models.sentiment_data import SentimentDataSource, TimeRangeType


class SentimentServiceConfigs:
    def __init__(
            self,
            sentimental_data_source=SentimentDataSource.NONE,
            start_time_to_fetch=None,
            end_time_to_fetch=None,
            time_range_type=TimeRangeType.DAY_1
    ):
        self.sentimental_data_source = sentimental_data_source
        self.start_time_to_fetch = start_time_to_fetch
        self.end_time_to_fetch = end_time_to_fetch
        self.time_range_type = time_range_type


class BaseSentimentService:
    def __init__(self, analyzer):
        self._analyzer = analyzer

    def start_analysis(self, configs: SentimentServiceConfigs):
        raise NotImplementedError

    def _fetch_data(self, configs):
        raise NotImplementedError

    def _analyze_data(self, data):
        raise NotImplementedError

    def _save_data(self, analyzed_data):
        raise NotImplementedError
