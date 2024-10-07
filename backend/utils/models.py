from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from backend.constants import DB_ENGINE

Base = declarative_base()


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    answer_id = Column(Integer, ForeignKey("answers.id"), nullable=False)
    rating = Column(Integer)
    timestamp = Column(
        DateTime,
        default=datetime.now(),
    )


if __name__ == "__main__":
    Base.metadata.create_all(bind=DB_ENGINE)
