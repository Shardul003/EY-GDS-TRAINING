import pandas as pd

# Step 1: Extract
enrollments = pd.read_csv('enrollments.csv')
students = pd.read_csv('students.csv')
courses = pd.read_csv('courses.csv')

# Step 2: Transform
# Join enrollments with students and courses
merged = enrollments.merge(students, on='StudentID', how='left')
merged = merged.merge(courses, on='CourseID', how='left')

# Add CompletionStatus
merged['CompletionStatus'] = merged['Progress'].apply(lambda x: 'Completed' if x >= 80 else 'In Progress')

# Add EnrollMonth
merged['EnrollMonth'] = pd.to_datetime(merged['EnrollDate']).dt.month

# Step 3: Load
merged.to_csv('processedenrollments.csv', index=False)


print("✅ ETL process completed. File saved as 'processed_enrollments.csv'.")
