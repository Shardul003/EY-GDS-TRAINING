import json
import logging

# Configure logging
logging.basicConfig(filename='task_json.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Step 1: Read JSON file
    with open('data_students.json', 'r') as f:
        students = json.load(f)
    logging.info("File read successful")

    # Step 2: Print all student names
    print("Student Names:")
    for s in students:
        print(s["name"])

    # Step 3: Add a new student
    new_student = {"name": "Megha", "age": 23, "course": "Data Engineering", "marks": 85}
    students.append(new_student)
    logging.info("Student added")

    # Step 4: Save back to same file
    with open('data_students.json', 'w') as f:
        json.dump(students, f, indent=4)
    logging.info("File saved successfully")

except FileNotFoundError:
    logging.error("data_students.json file not found")
except json.JSONDecodeError:
    logging.error("Error decoding JSON file")
