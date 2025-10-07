import json
student = {
    "name": "Manvi",
    "age": 23,
    "course": ["AI","ML"],
    "marks":  {"AI": 75, "ML": 80}
}

#write from json file
with open("student.json",'w') as f:
    json.dump(student,f,indent=4)

#read from json file
with open("student.json",'r') as f:
    data= json.load(f)

print(data["name"])
print(data["marks"]["AI"])
