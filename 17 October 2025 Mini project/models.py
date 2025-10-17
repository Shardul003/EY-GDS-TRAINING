from sqlalchemy import Column, String, Integer
from database import Base

class Course(Base):
    __tablename__ = "Courses"
    CourseID = Column(String(10), primary_key=True)
    Title = Column(String(100))
    Category = Column(String(50))
    Duration = Column(Integer)

class Student(Base):
    __tablename__ = "Students"
    StudentID = Column(String(10), primary_key=True)
    Name = Column(String(50))
    Email = Column(String(100))
    Country = Column(String(50))