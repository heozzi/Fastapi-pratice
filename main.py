from fastapi import FastAPI,Depends,Request,Form
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse
from database import Base,engine,session
from sqlalchemy.orm import Session
from models import users
from typing import Annotated
from pydantic import BaseModel,Field
from auth import check_id_pwd
from passlib.context import CryptContext

app = FastAPI()
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='templates/')

SECRET_KEY = 'a4b42b742bb126fb0ae71a290bdaea676b804737df4061667616ecaab5c33447'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def get_db() :
    db = session()
    try :
        yield db
    finally:
        db.close()

db_depandacy = Annotated[Session,Depends(get_db)]

class Createuserrequest(BaseModel) :
    username : str = Field(min_length=3,max_length=20)
    password : str = Field(min_length=8,max_length=20)

@app.get('/')
async def main_page(request : Request) :
    return templates.TemplateResponse("/index.html", {"request":request})

@app.post('/',response_class=HTMLResponse)
async def main_page(db : db_depandacy,username: str=Form(...),
                      password: str=Form(...)) :
    chk = check_id_pwd(db, username, password)
    if chk :
        return 'Success'
    else :
        raise HTTPException(status_code=401, detail='Authentication Failed')


@app.get('/create')
async def main_page(request : Request) :
    return templates.TemplateResponse("/create.html", {"request":request})

# HTMLResponse == HTML 응답받을려면 사용
@app.post('/create',response_class=HTMLResponse)
async def create_user(db : db_depandacy,username: str=Form(...),
                      password: str=Form(...)) :
    if len(username) < 3 or len(username) > 20 :
        raise HTTPException(status_code=401, detail='Please set your username to at least 3 characters and less than 20 characters.')
    if len(password) < 8 or len(password) > 20 :
        raise HTTPException(status_code=401, detail='Please set your password to at least 8 characters and less than 20 characters.')
    newuser = users(
        username = username,
        password = bcrypt_context.hash(password),
    )
    db.add(newuser)
    db.commit()
    return 'Success'

@app.get('/check')
async def check_user(db : db_depandacy  ) :
    return db.query(users).all()

@app.delete('/delete')
async def delete_user(db : db_depandacy,username : str) :
    tmpmodel = db.query(users).filter(users.username == username).first()
    if tmpmodel is None :
        raise HTTPException(status_code=404,detail='username not found')
    db.query(users).filter(users.username == username).delete()
    db.commit()

