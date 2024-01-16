import datetime
from pydantic import BaseModel, field_validator

from domain.user.user_schema import User

class AnswerCreate(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, v):          # AnswerCreate 스키마에 content 값이 저장될 때 실행되는 함수
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int
    modify_date: datetime.datetime | None = None  # modify_date는 수정이 발생할 경우에만 그 값이 생성되므로 디폴트 값으로 None을 설정한다.
    voter: list[User] = []


class AnswerUpdate(AnswerCreate):
    answer_id: int

class AnswerDelete(BaseModel):
    answer_id: int

class AnswerVote(BaseModel):
    answer_id: int