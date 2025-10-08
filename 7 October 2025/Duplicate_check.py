for emp in employees:
    if emp["name"].lower() == employee.name.lower():
        raise HTTPException(status_code=400, detail="Employee already exists")
