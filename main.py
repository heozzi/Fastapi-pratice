from fastapi import FastAPI
from database import Base,engine
import login
import auth

app = FastAPI()
# 테이블을 생성해주는 명령어
Base.metadata.create_all(bind=engine)

# 로그인과 인증에 apirouter를 app에다가 추가
app.include_router(login.router)
app.include_router(auth.router)
