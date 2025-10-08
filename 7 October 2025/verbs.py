from fastapi import FastAPI
app = FastAPI()

# root
@app.get("/")
def read_root():
    return {"message" : "welcome to FastAPI Demo"}

# GET
@app.get("/students")
def get_students():
    return {"This is a GET request"}

# POST
@app.post("/students")
def create_students():
    return {"This is a POST request"}

# PUT
@app.put("/students")
def update_students():
    return {"This is a GET Request"}

# DELETE
@app.delete("/students")
def delete_students():
    return {"This is a delete request"}
