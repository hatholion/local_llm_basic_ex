# ORM 사용 위한 sqlalchemy
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker 
# network 통신에서 session 연결해야 통신 가능
from sqlalchemy.ext.declarative import declarative_base
# session이 연결된 유저만 table 생성, 데이터 CRUD 하도록

import os
from dotenv import load_dotenv
load_dotenv(override=True)  # .env 파일을 읽어 환경 변수로 등록. 실행 때마다 갱신.

#############################################################

# sqlite database 1개를 넣어 file로 저장.
# mysql, oracle을 바꾸려면 이 부분을 바꿔주면 됨.
# DB_URL = 'sqlite:///todos.sqlite3' # sqlite는 python에 내장되어 있음.

# 데이터베이스에 연결하는 엔진을 생성하는 함수
# 'check_same_thread': False를 해줘야 file access 때 문제 발생 X
# connect_args={'check_same_thread': False} 부분은 myslq 파트라 oracle로 바꾸려면 이 부분 제거.
# engine = create_engine(DB_URL, connect_args={'check_same_thread': False})

#############################################################

# Oracle DB 설정
# Ocale 데이터베이스 Url 설정
# oracle+oracledb:// 를 반드시 붙여줘야 한다. oracle+oracledb : 프로토콜
# 다음은 아이디, 패스워드, 호스트, 포트, ? 다음은 service_name. DB의 이름이 서비스 이름.
# URL에 아이디, 패스워드 전부 다 보이므로 숨겨야 함.
# DB_URL = 'oracle+oracledb://joy:1234@localhost:1521/?service_name=FREEPDB1'

# oracle 데이터베이스 URL 설정
#  URL에 아이디, 패스워드 표시되지 않도록 숨김.

DB_URL = URL.create(
    "oracle+oracledb", # 프로토콜
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "1521")), # .env 파일은 다 문자열로 들어가게 되므로 int로 바꿔줘야 함.
    query={"service_name": os.getenv("DB_SERVICE", "FREEPDB1")},
)

#Oracl의 경우 ceck_same_thread 옵션이 필요하지 않음.
engine = create_engine(DB_URL, echo=True, future=True)

# 데이터베이스와 상호 작용하는 세션을 생성하는 클래스
# 엔진을 넣음(binding)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy의 선언적 모델링을 위한 기본 클래스
Base = declarative_base()