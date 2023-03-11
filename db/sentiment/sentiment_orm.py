from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Create a new engine for SQLite
engine = create_engine('sqlite:///sentiment_data.db')

# Create a new base class for our models
Base = declarative_base()

# Define the SentimentData model
class SentimentData(Base):
    __tablename__ = 'sentiment_data'

    id = Column(Integer, primary_key=True)
    chunk_time_range_start = Column(DateTime, nullable=False)
    chunk_time_range_end = Column(DateTime, nullable=False)
    source = Column(String, nullable=False)
    tb_score = Column(Float, nullable=False)
    vd_score = Column(Float, nullable=False)
    sp_score = Column(Float, nullable=False)
    total_score = Column(Float, nullable=False)

    def __repr__(self):
        return f"SentimentData(id={self.id}, chunk_time_range_start={self.chunk_time_range_start}, chunk_time_range_end={self.chunk_time_range_end}, source='{self.source}', tb_score={self.tb_score}, vd_score={self.vd_score}, sp_score={self.sp_score}, total_score={self.total_score})"