@app.get("/employees")
def get_all_employees(sort_by: str | None = None):
    if sort_by == "salary":
        return sorted(employees, key=lambda x: x["salary"])
    elif sort_by == "name":
        return sorted(employees, key=lambda x: x["name"])
    return employees
