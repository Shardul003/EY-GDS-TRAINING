from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# create FastAPI instance
app = FastAPI()


class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float


employees = [
    {"id": 1, "name": "Alice", "department": "AI", "salary": 800000},
    {"id": 2, "name": "George", "department": "AI", "salary": 800000},
    {"id": 3, "name": "Raven", "department": "HR", "salary": 800000}
]


@app.get("/employees")
def get_all_employees():
    return {"employees": employees}


@app.get("/employees/{emp_id}")
def get_employees(emp_id: int):
    for employee in employees:
        if employee["id"] == emp_id:
            return employee
    raise HTTPException(status_code=404, detail="employee not found")

@app.get("/employees/count")
def get_count():
    return {"number of employees": len(employees)}

@app.post("/employees", status_code=201)
def add_employee(employee: Employee):
    employees.append(employee.dict())
    return {"message": "employee added succesfully", "employee":employees}

@app.post("/employees",status_code=201)
def add_employee(employee: Employee):
    emp=employee.dict()
    ids=[e['id'] for e in employees]
    if emp["id"] not in ids:
        employees.append(emp)
        return {"message": "employee added succesfully", "employee": employee}
    else:
        return{"message":"duplicate id not allowed"} 

@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, updated_employee: Employee):
    for i, e in enumerate(employees):
        if e["id"] == emp_id:
            employees[i] = updated_employee.dict()
            return {"message": "employee updated succesfully", "employee": updated_employee}
    raise HTTPException(status_code=404, detail="employee not found")


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for i, s in enumerate(employees):
        if s["id"] == employee_id:
            employees.pop(i)
            return {"message": "employee deleted succesfully"}
    raise HTTPException(status_code=404, detail="employee not found")

# uvicorn main:app --reload
