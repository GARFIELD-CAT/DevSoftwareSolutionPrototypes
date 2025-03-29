from homework_4.api.v1.course import course_router
from homework_4.api.v1.faculty import faculty_router
from homework_4.api.v1.student import student_router


import uvicorn
from fastapi import FastAPI


app = FastAPI(title="my_api")

app.include_router(student_router, prefix="/api/v1/students")
app.include_router(course_router, prefix="/api/v1/courses")
app.include_router(faculty_router, prefix="/api/v1/faculties")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
