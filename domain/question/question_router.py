from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from database import SessionLocal
from domain.question import question_schema, question_crud

router = APIRouter(
    prefix="/api/question",
)

@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.get_question_list(db)
#    db = SessionLocal()     # db 세션을 생성
#    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()  # 질문 목록 API 출력
#    db.close()              # 사용한 세션을 컨넥션 풀에 반환
    return _question_list

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question