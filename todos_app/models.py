# database 상속받아서 Table 만들고자 함.
# Table과 관련된 것은 여기에 모두 설계.

# ORM 사용 위한 sqlalchemy

from sqlalchemy import Column, Integer, Boolean, Text, String, Identity
from database import Base

# sqlite3의 테이블 class로 정의
# sqlalchemy와 DB 사이를 오감. id, task, completed로 class가 구성되며 이것들을 main에서 불러서 활용.
# class Todo(Base):
#     __tablename__ = 'todos'
#     id = Column(Integer, primary_key=True) # primary key. 이게 있어야 다른 row에도 access 가능하다.
#     task = Column(Text)
#     completed = Column(Boolean, default=False)

# OrcaleDB의 테이블 class로 정의
class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer,  Identity(), primary_key=True) # primary key. 이게 있어야 다른 row에도 access 가능하다.
    task = Column(String(300))
    completed = Column(Boolean, default=False)