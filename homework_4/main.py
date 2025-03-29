from homework_4.api.v1.student import student_router


import uvicorn
from fastapi import FastAPI



app = FastAPI(title="my_api")

app.include_router(student_router, prefix="/api/v1/students")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
