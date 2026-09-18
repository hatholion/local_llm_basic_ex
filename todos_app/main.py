from fastapi import FastAPI, Request, Form, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal
import uvicorn

import os

# 데이터 CRUD 외 data base 관련은 맨 앞에 오면 됨.
from database import engine, SessionLocal, Base

# FAST API에서 도릴 때마다 전체를 memory에 로딩시키므로 modle를 improt
# CPU가 modles 안의 일을 수행. --> 표 만듦.
import models

# models에 정의한 모든 클래스, 연결한 DB엔진에 테이블로 생성. 테이블 한 번 생산 후엔 다시 적지 않음.
Base.metadata.create_all(bind=engine)

# FastAPI() 객체 생성. 반드시 해줘야 함.
app = FastAPI()

#의존성 주입(DB open, close와 같이 반복되는 부분을 정의하여 만들기 쉽게 함) 함수
def get_db():
    db = SessionLocal()
    try:
        yield db # 모든 작업이 다 끝날 때까지 대기.
        # DB에 적고 Commit해서 반영할 때까지 모두 기다림.
    finally: # try, except 이후 finally는 무조건수행됨. 
        # 마지막에 무조건 닫음
        db.close()

# 현재 base 경로 절대 경로로 가져옴.
 # Linux, Docker에서 배포시 절대 경로로 구성해야 함.
abs_path = os.path.dirname(os.path.realpath(__file__))

# print(abs_path)
# html 템플릿 폴더를 지정하여 jinja템플릿 객체 생성
# templates = Jinja2Templates(directory="templates")
# templates 폴더 식별 개체 변수. 객체로 만들어서 객체로 식별.
templates = Jinja2Templates(directory=f"{abs_path}/templates")

# static 폴더(정적파일 폴더)를 app에 연결
# name="static" : 식별자 이름 지정.
# app.mount("/static", StaticFiles(directory=f"static"), name="static")
# 객체에 넣지 않고 mount시켜서 바로 사용.
# static/ 폴더를 fastapi에서 인식할 수 잇도록 마운트시킴.
app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name="static")

# http://localhost:8000
@app.get("/") # 여기로 routing되어 아래로 실행. Show API
async def home(
    request: Request,
    db_ss :  Session = Depends(get_db),
    ): # request 요청이 들어오면 아랠르 수행.
    # Table 조회
    todos_list = db_ss.query(models.Todo).order_by(models.Todo.id.desc()).all() # 데이터 가져 옴. 최근 것이 위쪽으로 오도록 내림차순(descending).
    # print(todos_list) # SELECT todos.id AS todos_id, todos.task AS todos_task, todos.completed AS todos_completed FROM todos --> record 여러개.
    for todo in todos_list:
        print(f"{todo.id}, {todo.task}")
    # json으로 넘겨서 html에서 Server 쪽으로 넘겨서 lendering 수행 후 출력.
    return templates.TemplateResponse( # Request 들어와 TemplateResponse를 통해 response 수행. 아래 내용 실행 후 return
        request = request,
        name = "index.html", # jinjatemplate의 해석기가 해석. 형태는 dictionary여야 함.
        context={ "todos": todos_list} # Python의 data todos_list를 html에 넘김. python 해석기가 해석. 
        # Json으로 html에 넘기기 위해선 형태 : dictionary여야 함.
    )


# todo 데이터를 받아서 db 테이블에 저장하기. Html에서 저장 권한 넘겨 받음. post로. Write API
# http://localhost:8000/add/
@app.post("/add") # add 누를 때마다 server의 cpu
def add(request : Request, 
        task : str = Form(...), # db에 넣을 데이터 받음.
        db_ss :  Session = Depends(get_db), # Session 연결해서 db 처리 commit & close까지 기다리는 get_db
        ): 
    # 데이터 받아서 저장. 의존성 주입 위한 객체 Depends 추가.
    # 비즈니스 로직 처리
    # 클라이언트에서 textarea에서 입력 데이터 넘어온것 확인
    print(task)
    
    # task data를 받고, todo class를 통해서 table과 연결된 객체를 생성. client의 정보를 task로 mapping.
    todo = models.Todo(task=task) 
    # 넣은 내용을 db table에 넣음.
    db_ss.add(todo)
    # DB table에 넣은 것 반영. 자동 commit 껐으므로 수동으로 commit해야 DB에 반영됨.
    db_ss.commit()
    # endpoint 함수 home으로 redirect(제어를 넘겨서 다시 실행. 그럼 todos를 다시 읽고 todo 더한 내용을 유저에게 표시.)
    # home 엔드포인함수로 제어권을 넘김. home: todo 내용을 db에서 받아서 home page에 적용.
    return RedirectResponse(url=app.url_path_for("home"), # url_path_for 함수 내부는 str 문자열로 end point 함수를 지정해서 가게 됨. 
                            status_code=status.HTTP_303_SEE_OTHER)

# todo 수정(Edit) API

# todo 수정할 레코드 조회 
@app.get("/edit/{todo_id}")
def edit(request : Request, 
         todo_id = int, 
         db_ss :  Session = Depends(get_db),
         ):
    # todo_id 조회
    # 요청 수정 처리
    # 수정할 위치 찾기. 어차피 1개라 .first()
    todo = db_ss.query(models.Todo).filter(models.Todo.id==todo_id).first()
    print(todo.task) # 잘 조회되는지 확인

    if todo is None: # 예외 발생 처리. DB 내용이 삭제된 경우 등.
        raise HTTPException(status_code=404, detail="Todo not found")

    # edit 폼에 lendering -> return
    return templates.TemplateResponse(
        request=request,
        name = "edit.html", # edit에 lendering해 넘겨줌.
        context = {"todo": todo}
    )
   
    
# todo 수정 내용 반영하기
@app.post("/edit/{todo_id}")
def edit(request : Request, 
         todo_id = int, 
         db_ss : Session = Depends(get_db),
         task : str = Form(...),
         completed : bool = Form(False),
         ):
    todo = db_ss.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.task = task
    todo.completed = completed
    db_ss.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


# todo 삭제(Delete) API
@app.get("/delete/{todo_id}")
def edit(request : Request, 
         todo_id = int, 
         db_ss : Session = Depends(get_db),
         completed : bool = Form(False),
         ):
    todo = db_ss.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        db_ss.delete(todo)      # query가 아니라 delete!
        db_ss.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

# uv run fastapi dev (dev : 개발자 모드. main file 있는 위치에서 반드시 실행해야 함.)

if __name__ == '__main__':
    # uvicorn.run("main(현재 file 이름):app(Fast Api 객체_식별자)", reload=True(개발자 모드))
    uvicorn.run("main:app", reload=True)

