from pydantic import BaseModel

class CourseBase(BaseModel):
    CourseID: str
    Title: str
    Category: str
    Duration: int

class StudentBase(BaseModel):
    StudentID: str
    Name: str
    Email: str
    Country: str