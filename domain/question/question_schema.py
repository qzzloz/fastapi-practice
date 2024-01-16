import datetime

from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []
    user: User | None   # user 항목은 Question 모델을 Question 스키마에 매핑할 때 자동으로 값이 채워질 것이다.
    modify_date: datetime.datetime | None = None    # modify_date는 수정이 발생할 경우에만 그 값이 생성되므로 디폴트 값으로 None을 설정한다.
    voter: list[User] = []

class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []

class QuestionUpdate(QuestionCreate):   # QuestionCreate 스키마 상속받아서 subject랑 content 사용 가능
    question_id: int

class QuestionDelete(BaseModel):
    question_id: int

class QuestionVote(BaseModel):
    question_id: int