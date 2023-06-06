import requests
from sqlalchemy.orm import Session

from questions_app.config import API_LINK, API_ATTEMPTS
from questions_app.crud import get_db_question_by_id, insert_db_new_questions
from questions_app.models import Question


def make_api_request(questions_num: int = 1) -> list[dict]:
    """
    Makes requests to jservice.io API.
    """
    try:
        return requests.get(f'{API_LINK}?count={questions_num}').json()
    except requests.exceptions.JSONDecodeError:
        return []


def get_new_questions(db: Session, questions_num: int) -> None:
    """
    Gets new questions, checks them for duplicates and saves them to the db.
    """
    response: list[dict] = make_api_request(questions_num)
    new_questions: list[Question] = []

    for question_obj in response:
        question_exists: Question = get_db_question_by_id(db, question_obj['id'])

        if not question_exists:
            new_questions.append(Question(question_obj['id'],
                                          question_obj['question'],
                                          question_obj['answer'],
                                          question_obj['created_at'])
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
                question_exists: Question = get_db_question_by_id(db, new_question.get('id', 0))
                attempt += 1

            if new_question and not get_db_question_by_id(db, new_question['id']):
                new_questions.append(Question(new_question['id'],
                                              new_question['question'],
                                              new_question['answer'],
                                              new_question['created_at'])
                                     )

    insert_db_new_questions(db, new_questions)
