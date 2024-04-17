from fastapi import APIRouter
from fastapi import Request,Form
from models import users
from starlette.responses import HTMLResponse
from starlette.exceptions import HTTPException
from utils import bcrypt_context,templates,db_depandacy

router = APIRouter()

def check_id_pwd(db,username:str,password:str) :
    '''
    로그인 시 DB에 기록된 정보와 일치하는지 체크하는 함수
    
    :param db: DB의 세션
    :param username: login페이지에서 입력받은 username
    :param password: login페이지에서 입력받은 password
    :return: 
    문제없을시 True, 불일치시 False를 반환
    '''
    chkmodel = db.query(users).filter(users.username == username).first()
    if chkmodel is None : return False

    chk = bcrypt_context.verify(password, chkmodel.password) # 패스워드 비교
    if chk : return True
    return False

@router.get('/create')
async def main_page(request : Request) :
    return templates.TemplateResponse("/create.html", {"request":request})

# HTMLResponse == HTML 응답받을려면 사용
@router.post('/create',response_class=HTMLResponse)
async def create_user(db : db_depandacy,username: str=Form(...),password: str=Form(...)) :

    # pydantic의 Field로 처리가 안되어서 직접 수동으로 설정
    if len(username) < 3 or len(username) > 20 :
        raise HTTPException(status_code=401, detail='Please set your username to at least 3 characters and less than 20 characters.')
    if len(password) < 8 or len(password) > 20 :
        raise HTTPException(status_code=401, detail='Please set your password to at least 8 characters and less than 20 characters.')

    newuser = users(
        username = username,
        password = bcrypt_context.hash(password)) #Password 암호화

    db.add(newuser)
    db.commit()
    return 'Success'

# docs에서 DB에 기록된 유저들을 확인하는 함수
@router.get('/check')
async def check_user(db : db_depandacy  ) :
    return db.query(users).all()

# docs에서 DB에 기록된 유저들을 삭제하는 함수
@router.delete('/delete')
async def delete_user(db : db_depandacy,username : str) :
    tmpmodel = db.query(users).filter(users.username == username).first()
    # 해당 유저명이 DB에 기록되지 않는다면 에러 발생
    if tmpmodel is None :
        raise HTTPException(status_code=404,detail='username not found')
    db.query(users).filter(users.username == username).delete()
    db.commit()


