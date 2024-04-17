from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DBURL = 'sqlite:///project.db'

engine = create_engine(DBURL,connect_args={'check_same_thread' : False})

session = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base() # 자동 매핑