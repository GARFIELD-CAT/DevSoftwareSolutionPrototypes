import json
import os

import uvicorn
from fastapi import FastAPI

from homework_2.models import Request

app = FastAPI()
FILE_PATH = "request.json"


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в наш сервис!"}


@app.post("/addRequest")
async def add_request(request: Request):
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(request.json())

    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False)

    return {"result": "Обращение успешно зарегистрировано"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
