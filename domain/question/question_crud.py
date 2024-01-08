from models import Question
from sqlalchemy.orm import Session


def get_question_list(db: Session):
    question_list = db.query(Question)\
        .order_by(Question.create_date.desc())\
        .all()
    return question_list

def get_question(db: Session, question_id: int):    # question_id에 해당하는 질문을 조회하여 리턴하는 함수
    question = db.query(Question).get(question_id)
    return question