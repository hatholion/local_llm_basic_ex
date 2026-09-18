# database 상속받아서 Table 만들고자 함.

from sqlalchemy import Column, Integer, Boolean, Text
from database import Base

# sqlalchemyrhk DB 사이를 오감.
class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True) # primary key
    task = Column(Text)
    completed = Column(Boolean, default=False)