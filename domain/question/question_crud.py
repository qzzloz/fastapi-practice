from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from models import Question, User
from sqlalchemy.orm import Session


def get_question_list(db: Session, skip: int = 0, limit: int = 10):     # skip: 조회한 데이터의 시작 위치(1~10이면 skip은 0), limit: 시작위치부터 가져올 데이터 건수
    _question_list = db.query(Question)\
        .order_by(Question.create_date.desc())

    total = _question_list.count()
    question_list =_question_list.offset(skip).limit(limit).all()
    return total, question_list     # (전체 건수, 페이징 적용된 질문 목록)

def get_question(db: Session, question_id: int):    # question_id에 해당하는 질문을 조회하여 리턴하는 함수
    question = db.query(Question).get(question_id)
    return question

def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(subject=question_create.subject, content=question_create.content, create_date=datetime.now(), user=user)
    db.add(db_question)
    db.commit()

def update_question(db: Session, db_question: Question,
                    question_update: QuestionUpdate):
# db_question: 원래 Question
# question_update: 수정한 Question
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()

def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()