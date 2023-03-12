from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class TimeRangeType(Enum):
    MINUTE_5 = '5m'
    HOUR_1 = '1h'
    HOUR_4 = '4h'
    DAY_1 = '1d'


class SentimentDataSource(Enum):
    REDDIT = 'reddit'
    TWITTER = 'twitter'
    TELEGRAM = 'telegram'
    DISCORD = 'discord'
    OTHER = 'other'


class SentimentData(Base):
    __tablename__ = 'sentiment_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_source = Column(Enum(SentimentDataSource), nullable=False)
    time_range_type = Column(Enum(TimeRangeType), nullable=False)
    time_range_start = Column(DateTime, nullable=False)
    time_range_end = Column(DateTime, nullable=False)
    submissions_sentimental_id = Column(Integer, ForeignKey('sentiment_score_data.id'))
    submissions_sentimental = relationship('SentimentScoreData', foreign_keys=[submissions_sentimental_id])
    comments_sentimental_id = Column(Integer, ForeignKey('sentiment_score_data.id'))
    comments_sentimental = relationship('SentimentScoreData', foreign_keys=[submissions_sentimental_id])
    total_sentimental_id = Column(Integer, ForeignKey('sentiment_score_data.id'))
    total_sentimental = relationship('SentimentScoreData', foreign_keys=[submissions_sentimental_id])
    created_at = Column(DateTime, default=datetime.now, nullable=False)


class SentimentScoreData(Base):
    __tablename__ = 'sentiment_score_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tb_score = Column(Float, nullable=False)
    vd_score = Column(Float, nullable=False)
    sp_score = Column(Float, nullable=False)
    total_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # Define one-to-one relationship with SentimentData
    sentiment_data_id = Column(Integer, ForeignKey('sentiment_data.id'))
    sentiment_data = relationship('SentimentData', back_populates='score_data')
