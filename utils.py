from fastapi import Depends
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from database import session
from typing import Annotated
from sqlalchemy.orm import Session

# bcrypt 암호화 객체 생성
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
# HTML 템플릿을 설정
templates = Jinja2Templates(directory='templates/')

def get_db() :
    '''
    DB의 세션을 반환하는 함수

    :return:
    session을 반환
    '''
    db = session()
    try :
        yield db
    finally:
        db.close()

db_depandacy = Annotated[Session,Depends(get_db)]
