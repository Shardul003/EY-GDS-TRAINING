from operator import truediv
from pydantic import BaseModel
class Student(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True   #be def

#valid data
data={"name" : "Tarun", "age" : 27, "email" : "Tarun@88.com"}
student= Student(**data)

print(student)
print(student.name)
