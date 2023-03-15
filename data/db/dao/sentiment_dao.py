from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from data.db.dao.base_dao import BaseDAO
from data.db.models.sentiment_data import SentimentData, SentimentScoreData, TimeRangeType


class SentimentDAO(BaseDAO):
    def __init__(self, db_engine):
        super().__init__(db_engine)
        self._db_engine = db_engine

    def get_sentiment_data_by_time_range_type(self, time_range_type: TimeRangeType, start_date: datetime,
                                              end_date: datetime) -> List[SentimentData]:
        with Session(bind=self._db_engine) as session:
            result = session.query(SentimentData).filter(SentimentData.time_range_type == time_range_type,
                                                         SentimentData.time_range_start >= start_date,
                                                         SentimentData.time_range_end <= end_date).all()
            return result

    def get_sentiment_data_by_time_range(self, start_date: datetime, end_date: datetime) -> List[SentimentData]:
        with Session(bind=self._db_engine) as session:
            result = session.query(SentimentData).filter(SentimentData.time_range_start >= start_date,
                                                         SentimentData.time_range_end <= end_date).all()
            return result

    def save_sentiment_data(self, data: List[SentimentData]) -> None:
        with Session(bind=self._db_engine) as session:
            session.add_all(data)
            session.commit()

    def save_sentiment_score_data(self, data: List[SentimentScoreData]) -> None:
        with Session(bind=self._db_engine) as session:
            session.add_all(data)
            session.commit()
