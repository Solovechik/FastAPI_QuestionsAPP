import requests
from questions_app.config import API_ATTEMPTS, API_LINK
from questions_app.crud import get_db_question_by_id, insert_db_new_questions
from questions_app.models import Question
from sqlalchemy.orm import Session


def make_api_request(questions_num: int = 1) -> list[dict]:
    """
    Makes requests to jservice.io API.
    """
    try:
        return requests.get(f"{API_LINK}?count={questions_num}").json()
    except requests.exceptions.JSONDecodeError:
        return []


def get_new_questions(db: Session, questions_num: int) -> None:
    """
    Gets new questions, checks them for duplicates and saves them to the db.
    """
    response: list[dict] = make_api_request(questions_num)
    new_questions: list[Question] = []

    for question_obj in response:
        question_exists: Question = get_db_question_by_id(db, question_obj["id"])

        if not question_exists:
            new_questions.append(
                Question(
                    id=question_obj["id"],
                    text=question_obj["question"],
                    answer=question_obj["answer"],
                    created_at=question_obj["created_at"],
                )
            )
        else:
            attempt: int = 0
            new_question: dict = {}

            while question_exists and attempt < API_ATTEMPTS:
                # in case API stops responding
                try:
                    new_question: dict = make_api_request()[0]
                except IndexError:
                    pass
                question_exists: Question = get_db_question_by_id(
                    db, new_question.get("id", 0)
                )
                attempt += 1

            if new_question and not get_db_question_by_id(db, new_question["id"]):
                new_questions.append(
                    Question(
                        id=new_question["id"],
                        text=new_question["question"],
                        answer=new_question["answer"],
                        created_at=new_question["created_at"],
                    )
                )

    insert_db_new_questions(db, new_questions)
