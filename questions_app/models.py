from sqlalchemy import Column, Integer, String, DateTime

from questions_app.db import Base


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False)
    answer = Column(String(100), nullable=False)
    created_at = Column(DateTime(), nullable=False)

    def __init__(self, id_, text, answer, date):
        self.id = id_
        self.text = text
        self.answer = answer
        self.created_at = date
