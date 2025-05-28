# Steamlit UI 생성

## 1. Container
- 영역을 설정해서 UI내 구역 구분
- 기본적인 container생성 코드

```python
container = st.continer()
```

- `key`값을 부여하여 container 별로 적용되는 css를 변경가능

```python
container1 = st.container(key="id_1")
```

```css
[data-testid='stContainer'][data-key="id_1"]{
    min-height: 400px;
    background-color: #00ff00;
    width: 100%;
    margin-left: auto;
    margin-right: auto;
}
```

## 2. Sidebar
- Streamlit은 기본적으로 Sidebar를 제공
- 기본적인 Sidebar의 형태

```python
with st.sidebar:
    st.title("Sidebar")
```


## 3. Input : st.write() / st.markdown()
- `st.write()` : 입력하는 내용의 형식을 자동으로 지정
- `st.markdown()` : 입력 내용에 markdown의 형식을 지정해 레이아웃을 반영

---
# Logging으로 log 관리
## 기본 사용법

```python
import logging

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/app.log'
)

# 로깅 사용
logging.debug('디버그 메시지')
logging.info('정보 메시지')
logging.warning('경고 메시지')
logging.error('오류 메시지')
logging.critical('심각한 오류 메시지')
```
---

# FastAPI Example API

이 프로젝트는 FastAPI를 사용하여 간단한 API 서버를 만드는 예제입니다.

## 주요 파일
- `api.py`: FastAPI 서버 코드

## 실행 방법
1. 필요한 패키지 설치
   ```bash
   pip install fastapi uvicorn
   ```
2. 서버 실행
   ```bash
   python api.py
   ```
3. 브라우저에서 접속
   - 기본: [http://localhost:8000](http://localhost:8000)

## API 엔드포인트

### 1. GET /
- 설명: 서버가 정상적으로 동작하는지 확인
- 예시 응답:
  ```json
  { "message": "Hello World" }
  ```

### 2. POST /process
- 설명: 입력된 문자열을 받아 대문자로 변환해 반환
- 요청 예시 (JSON):
  ```json
  { "text": "hello" }
  ```
- 응답 예시:
  ```json
  { "result": "HELLO" }
  ```

## Pydantic의 BaseModel이란?
- FastAPI에서 입력/출력 데이터의 구조와 타입을 정의할 때 사용하는 클래스입니다.
- Pydantic 라이브러리에서 제공하며, 데이터 검증과 자동 문서화에 활용됩니다.

### 예시 코드
```python
from pydantic import BaseModel

class TextInput(BaseModel):
    text: str
```
- 위 예시에서 `TextInput`은 반드시 `text`라는 문자열 필드를 가져야 함을 의미합니다.
- 잘못된 데이터가 들어오면 FastAPI가 자동으로 에러를 반환합니다.

## 참고
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Pydantic 공식 문서](https://docs.pydantic.dev/)