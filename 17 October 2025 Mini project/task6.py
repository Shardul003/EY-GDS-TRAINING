import pandas as pd
import os

# Load data from CSVs
df_courses = pd.read_csv("courses.csv")
df_students = pd.read_csv("students.csv")
df_enrollments = pd.read_csv("enrollments.csv")

# Merge all data
df = df_enrollments.merge(df_students, on="StudentID").merge(df_courses, on="CourseID")

# Add CompletionStatus and EnrollMonth
df["CompletionStatus"] = df["Progress"].apply(lambda x: "Completed" if x >= 80 else "Incomplete")
df["EnrollMonth"] = pd.to_datetime(df["EnrollDate"]).dt.to_period("M")

# Completion rate per course
completion_rate = df.groupby("Title")["CompletionStatus"].apply(
    lambda x: (x == "Completed").mean()
).reset_index(name="CompletionRate")

# Total students per category
students_per_category = df.groupby("Category")["StudentID"].nunique().reset_index(name="TotalStudents")

# Country-wise enrollments
country_enrollments = df.groupby("Country")["StudentID"].count().reset_index(name="Enrollments")

# Monthly enrollment trends
monthly_trends = df.groupby("EnrollMonth")["EnrollmentID"].count().reset_index(name="MonthlyEnrollments")

# Combine all analytics into one DataFrame with labels
analytics = pd.concat([
    completion_rate.assign(Metric="CompletionRate"),
    students_per_category.assign(Metric="TotalStudentsPerCategory"),
    country_enrollments.assign(Metric="CountryWiseEnrollments"),
    monthly_trends.assign(Metric="MonthlyEnrollmentTrends")
], ignore_index=True)

# Ensure reports directory exists
os.makedirs("reports", exist_ok=True)

# Save to CSV
analytics.to_csv("reports/learning_analytics.csv", index=False)

print("✅ Analytics report saved to reports/learning_analytics.csv")