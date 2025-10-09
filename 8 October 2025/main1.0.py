from fastapi.testclient import TestClient
from main import app

client=TestClient(app)

#----test 1----
def test_get_all_emp():
    response = client.get("/employees") #ACT
    assert response.status_code==200 #assert
    assert isinstance(response.json(),list)#assert

#---- test 2 ----
def test_add_emp():
    new_emp = {
        "id":2,
        "name":"Neha Verma",
        "department":"IT",
        "salary":50000
    }
    response = client.post("/employees",json=new_emp)
    assert response.status_code==201
    assert response.json()["name"]=="Neha Verma"

#----test 3----
def test_get_emo_by_id():
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Aarav"

#----test 4----
def test_get_emp_not_found():
    response = client.get("/employees/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Employee Not Found"

#---test 5 - put -----
def test_update_emp():
    new_emp={
        "id": 2,
        "name": "Riya",
        "department": "IT",
        "salary": 50000
    }
    response = client.post("/employees", json=new_emp)

    updated_emp={
        "id":2,
        "name":"Aashi",
        "department":"IT",
        "salary":60000
    }
    response = client.put("/employees/2",json=updated_emp)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Employee updated successfully"
    assert data["name"] == "Aashi"
    assert data["salary"] == 60000
