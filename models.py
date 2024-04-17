from database import Base
from sqlalchemy import Column,Integer,String

# 데이터베이스에서 선언된 Base를 사용하여 클래스로 매핑
class users(Base) :
    __tablename__ = "users" # 테이블 이름
    id = Column(Integer, primary_key=True, index=True) # 인덱스 설정
    username = Column(String,unique=True) # 유저명
    password = Column(String) # 패스워드