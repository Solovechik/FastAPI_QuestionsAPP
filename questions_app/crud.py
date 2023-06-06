from sqlalchemy import func
from sqlalchemy.orm import Query, Session

from .models import Question
from .schemas import Question as scQuestion


def get_db_questions(db: Session, question_num: int) -> Query:
    """
    Returns randomly sorted number of question objects from the db.
    """
    db_questions: Query = db.query(Question).order_by(func.random()).limit(question_num)

    return db_questions


def get_db_question_by_id(db: Session, question_id: int) -> Question:
    """
    Returns a single question object from the db.
    """
    return db.query(Question).get(question_id)


def insert_db_new_questions(db: Session, new_questions: list[scQuestion]) -> None:
    """
    Saves question objects retrieved from API to the db.
    """
    db.add_all(new_questions)
    db.commit()
