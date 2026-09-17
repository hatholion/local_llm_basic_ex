# Web apllication 개발
# 이 모든 것은 Back End
# browser가 clinet. 주소로 요청을 하면 server에 access.
# TCP 80번 포트를 쓰는 http
# TCP 443 포트를 쓰는 https --> 웹 데이터를 암호화하여 보내는 통신 프로토콜.
# https://nid.naver.com/nidlogin.login : 전체 url
# 로그인시 서버에 보내는 내용은 중요 내용이므로 암호화해야 함. Post 방식으로 보내 사용자가 보낸 내용이 url에 표시되지 않게 함.
# F12로 백엔드 코딩 내용을 볼 수 있음.

# html + CSS + js : 웹페이지를 만드는 데 필요한 3가지 핵심 기술
# html은 data 구조 만듦. DOM(document object model) tree
# CSS : design
# js(java script) : 동적인 것. 나머지 위는 정적인 것. 바뀌지 않음. 무한 스크롤링은 동적.
# 스크롤 내릴 때마다 서버와 통신해서 스크롤한 아래 내용을 보여줌.

# 웹으로 만들면 앱으로 만들 수 있고, 서비스를 배포하는 방법 중 웹이 가장 배포하기 쉽다.

from fastapi import FastAPI

# fast api 객체 생성
app = FastAPI()

# fast api는 웹 어플리케이션을 만든느 도구.
# get의 sub 쪽에서 읽기 할 때의 통신 방식.
# sub 쪽에 데이터를 보내서 업데이트 하거나 delete 할 때 post 방식 사용함.

# http://localhost:8000/ 컴퓨터가 8000 포트에서 통신
# http://localhost:8000/docs 치면 fast api 서버에 docs api 제공. 직접 test 가능하도록 됨.
# http://127.0.0.1:8000/itmes

# API
@app.get("/")
def read_root():
    # 비즈니스 로직
    data = "db에서 데이터 읽어오기"
    return {"message" : data}

# API
@app.get("/items") # path
def read_item():
    item_id = 1
    q = '사과'
    return {"item_id": item_id, "q": q} # json 데이터로 return되어 표시.

# API
# clinet 쪽에서 값을 입력해서 서버 쪽으러 넘김.
@app.get("/items/{item_id}") # end point path, {item_id} : 경로 매게 변수.
# 웹에서 명령한 내용이 저 패스 라우팅하여 서버로 요청 내용 들어옴.
# def read_item(item_id , q): # 변수 타입 선정 안 할 경우 아무거나 다 받음. 그러나, 그렇게 해선 안되므로 int, str 등 형태 checking 함.
def read_item(item_id: int, q: str | None = None): # clinet 쪽에서 변하는 값을 받음. | : or 이고 없을 수도 있음을 None으로 나타냄.
    # 비즈니스 로직 처리 부분. back end에서 ai, db 등과 연결되는 부분.
    # item_id, q : query 매게 변수. 사용자에게서 값을 받아서 여기에 넘겨 받음.
    print(f'item_id: {item_id}, q: {q}') # 이렇게 할 경우 서버에서 print됨.
    return {"item_id": item_id, "q": q} # path로 받은 클라이언트의 주소로 값이 return됨.


#http://127.0.0.1:8000/items/100?q=사과
#http://127.0.0.1:8000/items/200?q=배
#http://127.0.0.1:8000/items/300?q=치킨

# 클라이언트 쪽에서 바뀌는 값들 중 경로와 관련된 건 경로 매게변수. query는 물음표 다음에 오는 것. q 변수에 쿼리 매게 변수로 저장하고 
# 서버에서 받는 이름을 그대로 받음. 즉, q는 주소에도 반영되게 됨. 다시 clinet로 보낼 때에는 key, value 형태로 보내야 함.  


# https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=사과&ackey=80jct25t

# 앞 부분 : domain name , search.naver : path, TCP port 80번 생략. ? 다음은 다 query. 내용을 숨기고 query=사과로 전달.


from pydantic import BaseModel, HttpUrl
from typing import Optional # 2가지 이상 case를 넣어 줌.

# DTO : 데이터 전송 객체. 이걸 정의.
class UserCreate(BaseModel): # 반드시 BaseModel을 상속받아야 함.
    username : str 
    password : str
    avatar_url: Optional[HttpUrl] = None
    user_fullname : Optional[str] = None


@app.post("/user_info/")
def create_item(user : UserCreate): # 객체 변수 user 로 user 정보가 담겨 있는 UserCreate에 access
    print(f'username: {user.username}') 
    print(f'avatar_url: {user.avatar_url}')
    print(f'user_fullname: {user.user_fullname}')

    return user
    # return {"user" : user}



# get 방식이 아닌 post 방식 사용.
@app.post("/user_info/{user_id}")
def create_item(user_id: int, q: str | None = None): # end point 함수
    print(f'user_id: {user_id}, q: {q}') 
    return {"user_id": user_id, "q": q} 
    # python에서는 key, value 값으로 되는 건 dictionary 형태임.
    # clinet 쪽에서는 네트워크 타고 json 형태로 전달됨. json도 key, value 형태로 되어 있음.
    # json의 j : java script. Java script에서 key value 형태로 되어 있는 걸 json이라고 함.
    # java script가 web에서 표현되는 데 쓰는 표준.


# http://127.0.0.1:8000/user_info/1234?q=LJH --> swagger 오류. post면 원래 query string이 url에서 표시되지 않아야 함.
# {"detail":"Method Not Allowed"} --> 이렇게 넣으면 안된다는 증거.
# 왜냐하면, post 방식은 url에 quuery string을 붙이면 안됨. q는 body에 담아서 모내야 함.


# 올바른 경로 : # http://127.0.0.1:8000/user_info/1234