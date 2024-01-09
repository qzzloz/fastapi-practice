from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.question import question_router
from domain.answer import answer_router

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#@app.get("/hello")
#def hello():
#    return {"message" : "hihihi"}

app.include_router(question_router.router)      # 생성한 router 객체를 FastAPI 앱에 등록
app.include_router(answer_router.router)