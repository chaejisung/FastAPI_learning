# Fast API

[첫걸음 - FastAPI](https://fastapi.tiangolo.com/ko/tutorial/first-steps/)

---

# 0. 설치하기

- 2가지를 설치
    - fastapi - 프레임워크
    - uvicorn - ASGI 서버

```python
pip install fastapi
pip install "uvicorn[standard]"
```

# 1. FastAPI의 기본 구조

**/main.py**

```python
from fastapi import FastAPI # #1

app = FastAPI() # #2

@app.get('/') # #3
async def root():
    return {'message': 'hi'}
```

> #1 fastapi에서 FastAPI 객체 임포트
#2 FastAPI() 인스턴스 생성
#3 데코레이터 문법으로 작동 및 경로 지정
> 

**실행 방법**

```python
uvicorn main:app --reload
```

> `uvicorn` : uvicorn 서버 실행
`main` : [main.py](http://main.py) 파일
`app` : [main.py](http://main.py) 파일 내부의 app = FastAPI()의 객체
`--reload`  : 코드 변경 시 자동으로 서버 재시작
                     (nodemon 같은거, 개발 시에만 사용)
> 
- 이렇게 입력하면 실행 완료

```python
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

- 위와 같이 나오는데 해당 주소로 들어가보면 fastapi 서버가 실행되고 있다.

**경로 작동 함수**

```python
@app.get('/') #1
async def root(): #2
    return {'message': 'hi'}
```

- **경로**: 는 `/`
- **작동**: 은 `get`
- **함수**: 는 "데코레이터" 아래에 있는 함수 (`@app.get("/")` 아래).
- 이는 **“/” 경로**에 대한 **GET 작동**을 사용하는 요청을 받을 때 마다 **함수**를 호출함

**FastAPI 오퍼레이션(작동)**

- HTTP 메서드 중 하나를 가리킴
    - 아래 1~5번은 주로 쓰이는 HTTP 메서드
    1. `GET`: 데이터 조회
    2. `POST`: 데이터 생성
    3. `PUT`: 데이터 수정(전체 수정)
    4. `DELETE`: 데이터 삭제
    5. `PATCH` : 데이터 수정(일부 수정)
    6. `HEAD` : 데이터 조회(Body를 제외한, 상태, 헤더만 조회)
    7. `OPTIONS` : 대상 리소스에 대한 통신 가능 옵션 설정
    8. `TRACE` : 경로를 따라 메시지 루프백 테스트 수행
    9. `CONNECT` : 대상 자원으로 식별되는 서버에 대한 터널 설정
- 각각 대응되는 FastAPI 오퍼레이션이 있음
    1. `@app.get()` - 데이터 조회
    2. `@app.post()` - 데이터 생성
    3. `@app.put()` - 데이터 수정
    4. `@app.delete()` - 데이터 삭제
    5. `@app.patch()` - 데이터 수정
    6. `@app.options()`
    7. `@app.head()`
    8. `@app.trace()`

**주소**

 `[http://127.0.0.1:8000](http://127.0.0.1:8000/)` 

- FastAPI 서버가 작동되는 주소

 `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`

- 대화형 API 문서

[`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)

- 대체 API 문서

# 2. 경로 매개변수

/main.py

```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'hi'}

@app.get('/items/{items_id}') #1
async def root(items_id): #2
    return {'message': items_id} #3
```

> #1 중괄호({})로 변수명을 감싸 경로에 추가
#2 사용하고자 하는 변수명을 파라미터로 넣어주기(일치해야 함)
#3 파라미터로 넣어준 변수명을 변수로 사용
> 
- 위와 같은 방식으로 경로에서 데이터를 받아서 사용 가능하다.
- 경로의 값은 알맞은 타입으로 형 변환된다.

**경로 매개변수 타입 지정**

```python
@app.get('/items/{items_id}')
async def root(items_id:int):
    return {'message': items_id}
```

- **파이썬 표준 타입 어노테이션**으로 함수의 경로 매개변수 타입을 선언할 수 있다.

<aside>
💡 파이썬 표준 타입 어노테이션
- 변수, 파라미터, 반환값의 예상 데이터 타입을 명시적으로 선언하는

</aside>

- 타입이 다른 데이터를 경로에 입력하면 HTTP 오류가 남

**순서 문제**

```python
## 잘못된 코드
@app.get('/items/{items_id}')
async def root(items_id):
    return {'message': items_id}

@app.get('/items/me')
async def root(items_id):
    return {'message': mememe}

```

- 위와 같은 순서로 코드 작성 시, 경로 작동은 순차적이므로 `/items/me` 로 접속하더라도 `/items/{items_id}` 에서 items_id가 “me” 인 것으로 판단하므로 정상적인 작동을 하지 않는다.
- 순서를 바꿔줘야 정상적으로 작동한다.

**사전에 정의된 값으로만 접근하기**

```python
from enum import Enum #1
from fastapi import FastAPI

class itemID(int, Enum): #2
    id1 = '111'
    id2 = '222'

app = FastAPI()

@app.get('/items/{items_id}')
async def root(items_id: itemID): #3
    return {'message': items_id}
```

> #1 Enum 자료형 불러오기
#2 사용할 경로의 타입과 Enum타입을 상속하는 클래스 생성
     (위 예제는 정수형 값을 받고 있기 때문에 int 값 사용)
#3 경로 매개면수 뒤에 표준 타입 어노테이션으로 생성한 클래스명을 기입
> 
- Enum 자료형을 사용해 사전에 정의된 값으로만 경로 매개변수를 받을 수 있다.
- 그 외 값 사용 시 오류가 뜬다.

**경로를 포함하는 경로 매개변수**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/files/{file_path:path}") #1
async def read_file(file_path: str): #2
    return {"file_path": file_path}
```

> #1 경로 매개변수 이름 뒤에 `:path` 를 사용해 지정해줌
#2 파라미터로 사용 시에는 타입 표준 어노테이션을 str로 지정
> 
- 경로에 `/file/myfile/myfile1.txt` 같은 것을 사용하는 경우에는 문제가 생길 수 있음

# 3. 쿼리 매개변수