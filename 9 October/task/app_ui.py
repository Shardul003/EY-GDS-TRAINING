from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allowing frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple GET API that returns 5 students
@app.get("/students")
def get_students():
    students = [
        {"id": 1, "name": "Shardul", "grade": "A"},
        {"id": 2, "name": "Manas", "grade": "A"},
        {"id": 3, "name": "George", "grade": "A"},
        {"id": 4, "name": "Myra", "grade": "B"},
        {"id": 5, "name": "Akash", "grade": "C"},
    ]
    return {"students": students}
