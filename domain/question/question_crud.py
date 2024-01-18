from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from sqlalchemy import and_     # outerjoin에서 and_ 함수 사용
from models import Question, User, Answer
from sqlalchemy.orm import Session


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):     # skip: 조회한 데이터의 시작 위치(1~10이면 skip은 0), limit: 시작위치부터 가져올 데이터 건수
    question_list = db.query(Question)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username) \
            .outerjoin(User, and_(Answer.user_id == User.id)).subquery()
        question_list = question_list \
            .outerjoin(User) \
            .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id)) \
            .filter(Question.subject.ilike(search) |    # 질문 제목
                    Question.content.ilike(search) |    # 질문 내용
                    User.username.ilike(search) |       # 질문 작성자
                    sub_query.c.content.ilike(search) | # 답변 내용
                    sub_query.c.username.ilike(search)  # 답변 작성자
                    )
    total = question_list.distinct().count()
    question_list = question_list.order_by(Question.create_date.desc()) \
        .offset(skip).limit(limit).distinct().all()
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

def vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    db.commit()