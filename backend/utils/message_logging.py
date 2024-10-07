from sqlalchemy.orm import Session

from backend.constants import DB_ENGINE
from backend.utils.models import Query, Answer, Feedback


def log_message(content):
    with Session(DB_ENGINE) as session:
        db_message = Query(content=content)
        session.add(db_message)
        session.commit()
        session.refresh(db_message)
    return db_message.id


def log_answer(query_id, content):
    with Session(DB_ENGINE) as session:
        db_message = Answer(query_id=query_id, content=content)
        session.add(db_message)
        session.commit()
        session.refresh(db_message)
    return db_message.id


def log_feedback(query_id, rating):
    with Session(DB_ENGINE) as session:
        answer_record = session.query(Answer).filter_by(query_id=query_id).first()
        db_message = Feedback(answer_id=answer_record.id, rating=rating)
        session.add(db_message)
        session.commit()
        session.refresh(db_message)
    return db_message.id
