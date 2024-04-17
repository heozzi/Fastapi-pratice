from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sqlalchemy 사용법
# 사용할 db명://{db_id}:{db_password}@{db_host}:{db_port} /db이름
DBURL = 'sqlite:///project.db'

# 데이터베이스와 연결할 엔진 마들기
# sqlite는 쓰레드통신이 안되어서 connect_args={'check_same_thread' : False} 필수로 적어야함
engine = create_engine(DBURL,connect_args={'check_same_thread' : False})

# 세션의 공장 같은 걸로 이해하시면 됩니다.
# 원문 : sessionmaker : A configurable Session factory.
session = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# 데이터베이스와 클래스 매핑을 사용하기 위해서 사용됩니다.
Base = declarative_base()