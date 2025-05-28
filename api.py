from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/process")
async def process_text(input: TextInput):
    # 예시: 입력된 문자열을 대문자로 변환
    result = input.text.upper()
    return {"result": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
