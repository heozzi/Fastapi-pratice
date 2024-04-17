from fastapi import APIRouter
from starlette.responses import HTMLResponse
from fastapi import Request,HTTPException,Form
from utils import templates,db_depandacy
from auth import check_id_pwd

router = APIRouter()

@router.get('/')
async def main_page(request : Request) :
    return templates.TemplateResponse("/index.html", {"request":request})

@router.post('/',response_class=HTMLResponse)
async def main_page(db : db_depandacy,username: str=Form(...),password: str=Form(...)) :
    chk = check_id_pwd(db, username, password)
    if chk : return 'Success'
    else :
        raise HTTPException(status_code=401, detail='Authentication Failed')