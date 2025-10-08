from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app=FastAPI()

class Employee(BaseModel):
    id:int
    name:str
    department:str
    salary:float

employees=[
    {"id":1,"name":"Ankit","department":"IT","salary":750000}
]

@app.get("/employees")
def get_all():
    return employees

@app.post("/employees",status_code=201)
def add_employee(employee:Employee):
    employees.append(employee.dict())
    return employee

@app.get("/employees/{emp_id}")
def get_employee(emp_id:int):
    for emp in employees:
        if emp["id"]==emp_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee Not Found")

#--put---
@app.put("/employees/{emp_id}")
def updated_employee(emp_id:int, updated_employee: Employee):
    for i,emp in enumerate(employees):
        if emp["id"] == emp_id:
            employees[i]=updated_employee.dict()
            return {"message":"employee updated","employee":updated_employee}
        raise HTTPException(status_code=404,detail="employee not found")

#---DELETE---
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id:int):
    for i, emp in enumerate(employees):
        if emp["id"]==emp_id:
            deleted_employee=employees.pop(i)
            return {
                "message":f"Employee with ID{emp_id} deleted successfully",
                "deleted_employee": deleted_employee
            }
    raise HTTPException(status_code=404,detail=f"employee with ID {emp_id} not found")
