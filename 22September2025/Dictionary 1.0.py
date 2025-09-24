student={
    "name":"Shardul",
    "age":22,
    "gender":"male",
    "Percentage":95
}
print(student["name"])
print(student.get("age"))
student["grade"]="A"
print(student)
student["age"]=23
print(student)
student.pop("age")
print(student)
del student["gender"]
print(student)
for key,value in student.items():
    print(key,":",value)