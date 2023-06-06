from fastapi import BackgroundTasks, Depends, FastAPI
from questions_app import models
from questions_app.crud import get_db_questions
from questions_app.db import SessionLocal, engine
from questions_app.schemas import PositiveIntHundred, Questions
from questions_app.utils import get_new_questions
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db() -> Session:
    with SessionLocal() as session:
        yield session


@app.post("/questions/", response_model=Questions)
def get_questions(
    questions_num: PositiveIntHundred,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    background_tasks.add_task(get_new_questions, db, questions_num.questions_num)

    return {
        "questions": [
            {"text": question.text, "answer": question.answer}
            for question in get_db_questions(db, questions_num.questions_num)
        ]
    }
