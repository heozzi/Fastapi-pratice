from models import users
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')


SECRET_KEY = 'a4b42b742bb126fb0ae71a290bdaea676b804737df4061667616ecaab5c33447'
ALGORITHM = 'HS256'

def check_id_pwd(db,id:str,pwd:str) :
    chkmodel = db.query(users).filter(users.username == id).first()
    if chkmodel is None : return False

    chk = bcrypt_context.verify(pwd, chkmodel.password) # 패스워드 비교
    if chk : return True
    return False
