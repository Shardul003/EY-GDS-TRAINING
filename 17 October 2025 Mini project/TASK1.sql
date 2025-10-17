CREATE DATABASE COURSES_MANAGEMENT;
USE COURSES_MANAGEMENT;
-- Create Courses Table
CREATE TABLE Courses (
    CourseID VARCHAR(10) PRIMARY KEY,
    Title VARCHAR(100),
    Category VARCHAR(50),
    Duration INT
);

-- Create Students Table
CREATE TABLE Students (
    StudentID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(50),
    Email VARCHAR(100),
    Country VARCHAR(50)
);

-- Insert Courses
INSERT INTO Courses (CourseID, Title, Category, Duration) VALUES
('C101', 'Python for Beginners', 'Programming', 40),
('C102', 'Machine Learning Basics', 'AI', 60),
('C103', 'Data Visualization with Power BI', 'Analytics', 30),
('C104', 'Cloud Fundamentals', 'Cloud', 50);

-- Insert Students
INSERT INTO Students (StudentID, Name, Email, Country) VALUES
('S001', 'Neha', 'neha@example.com', 'India'),
('S002', 'Arjun', 'arjun@example.com', 'UAE'),
('S003', 'Sophia', 'sophia@example.com', 'UK'),
('S004', 'Ravi', 'ravi@example.com', 'India'),
('S005', 'Meena', 'meena@example.com', 'USA');

INSERT INTO Courses (CourseID, Title, Category, Duration)
VALUES ('C105', 'DevOps Essentials', 'DevOps', 45);

UPDATE Courses
SET Duration = 65
WHERE CourseID = 'C105';

DELETE FROM Students
WHERE StudentID = 'S003';

SELECT * FROM Students
WHERE Country = 'India';
