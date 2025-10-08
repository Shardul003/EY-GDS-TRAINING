@app.get("/employees/search")
def search_employees(department: str):
    results = [emp for emp in employees if emp["department"].lower() == department.lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No employees found in department")
    return results
