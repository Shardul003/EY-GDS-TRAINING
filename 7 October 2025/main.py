from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic model for validation
class Student(BaseModel):
    id : int
    name : str
    age : int
    course : str

# In-memory database
students = [
    {"id" : 1, "name" : "Prince", "age" : 22, "course" : "RageBait"},
    {"id" : 2, "name" : "Mini Pekka", "age" : 20, "course" : "Pancakes"}
]

# GET Request
@app.get("/students")
def get_all_students():
    return {"student" : students }

# Another GET Request
@app.get("/students/{student_id}")
def get_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    raise HTTPException(status_code= 404, detail= "Student not found")
