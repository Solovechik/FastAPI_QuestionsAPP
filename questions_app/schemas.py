from datetime import datetime

from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    text: str
    answer: str


class QuestionCreate(QuestionBase):
    id: int
    created_at: datetime
    added_at: datetime

    class Config:
        orm_mode = True


class Question(QuestionBase):
    pass


class Questions(BaseModel):
    questions: list[Question]


class PositiveIntHundred(BaseModel):
    questions_num: int = Field(gt=0, le=100)
