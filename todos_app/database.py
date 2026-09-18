from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
# network 통신에서 session 연결해야 통신 가능
from sqlalchemy.ext.declarative import declarative_base
# session이 연결된 유저만 table 생성, 데이터 CRUD 하도록

# sqlite database 1개를 넣어 file로 저장.
# mysql, oracle을 바꾸려면 이 부분을 바꿔주면 됨.
DB_URL = 'sqlite:///todos.sqlite3' # sqlite는 python에 내장되어 있음.

# 데이터베이스에 연결하는 엔진을 생성하는 함수
# 'check_same_thread': False를 해줘야 file access 때 문제 발생 X
engine = create_engine(DB_URL, connect_args={'check_same_thread': False})

# 데이터베이스와 상호 작용하는 세션을 생성하는 클래스
# 엔진을 넣음(binding)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy의 선언적 모델링을 위한 기본 클래스
Base = declarative_base()