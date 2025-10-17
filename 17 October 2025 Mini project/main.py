from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- Courses Endpoints --------------------

@app.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()

@app.post("/courses")
def add_course(course: schemas.CourseBase, db: Session = Depends(get_db)):
    new_course = models.Course(**course.dict())
    db.add(new_course)
    db.commit()
    return {"message": "Course added"}

@app.put("/courses/{course_id}")
def update_course(course_id: str, course: schemas.CourseBase, db: Session = Depends(get_db)):
    db.query(models.Course).filter(models.Course.CourseID == course_id).update(course.dict())
    db.commit()
    return {"message": "Course updated"}

@app.delete("/courses/{course_id}")
def delete_course(course_id: str, db: Session = Depends(get_db)):
    db.query(models.Course).filter(models.Course.CourseID == course_id).delete()
    db.commit()
    return {"message": "Course deleted"}

# -------------------- Students Endpoints --------------------

@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@app.post("/students")
def add_student(student: schemas.StudentBase, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    return {"message": "Student added"}

@app.put("/students/{student_id}")
def update_student(student_id: str, student: schemas.StudentBase, db: Session = Depends(get_db)):
    db.query(models.Student).filter(models.Student.StudentID == student_id).update(student.dict())
    db.commit()
    return {"message": "Student updated"}

@app.delete("/students/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    db.query(models.Student).filter(models.Student.StudentID == student_id).delete()
    db.commit()
    return {"message": "Student deleted"}