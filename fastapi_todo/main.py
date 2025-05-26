from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

students = []


# Pydantic model for full data (POST)
class Student(BaseModel):
    name: str
    age: int
    grade: str


# Pydantic model for partial data (PATCH)
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None


# Custom exception class
class StudentNotFound(Exception):
    def __init__(self, student_id: int):
        self.student_id = student_id


# Custom exception handler
@app.exception_handler(StudentNotFound)
def student_not_found_handler(request: Request, exc: StudentNotFound):
    return JSONResponse(


        status_code=404,
        content={"message": f"Student with ID {exc.student_id} not found."},
    )


# POST - Add a new student
@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    students.append(student.model_dump())
    return {
        "message": "Student added successfully",
        "data": student
    }


# PATCH - Update existing student partially
@app.patch("/students/{student_id}")
def partial_update_student(student_id: int, student: UpdateStudent):
    if student_id < 0 or student_id >= len(students):
        raise StudentNotFound(student_id)

    updated_data = student.model_dump(exclude_unset=True)
    students[student_id].update(updated_data)

    return {
        "message": "Student updated successfully",
        "data": students[student_id]
    }


# GET - Retrieve all students (optional utility)
@app.get("/students")
def get_all_students():
    return {
        "message": "List of all students",
        "data": students
    }
