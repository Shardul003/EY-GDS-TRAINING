CREATE DATABASE HospitalManagement;
USE HospitalManagement;
--  Patients Table
CREATE TABLE Patients (
patient_id INT PRIMARY KEY,
name VARCHAR(50),
age INT,
gender CHAR(1),
city VARCHAR(50)
);

CREATE TABLE Doctors (
doctor_id INT PRIMARY KEY,
name VARCHAR(50),
specialization VARCHAR(50),
experience INT
);

CREATE TABLE Appointments (
appointment_id INT PRIMARY KEY,
patient_id INT,
doctor_id INT,
appointment_date DATE,
status_s VARCHAR(20),
FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

CREATE TABLE MedicalRecords (
record_id INT PRIMARY KEY,
patient_id INT,
doctor_id INT,
FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
diagnosis VARCHAR(100),
treatment VARCHAR(100),
date DATE
);

CREATE TABLE Billing (
bill_id INT PRIMARY KEY,
patient_id INT,
FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
amount DECIMAL(10,2),
bill_date DATE,
status VARCHAR(20)
);

INSERT INTO Students VALUES
(1, 'Rahul', 'Mumbai'),
(2, 'Priya', 'Delhi'),
(3, 'Arjun', 'Bengaluru'),
(4, 'Neha', 'Hyderabad'),
(5, 'Vikram', 'Chennai');

INSERT INTO Courses VALUES
(101, 'Mathematics', 4),
(102, 'Computer Science', 3),
(103, 'Economics', 2),
(104, 'History', 3);

INSERT INTO Enrollments VALUES
(1, 1, 101, 'A'),
(2, 1, 102, 'B'),
(3, 2, 103, 'A'),
(4, 3, 101, 'C'),
(5, 4, 102, 'B'),
(6, 5, 104, 'A');
INSERT INTO Patients (patient_id, name, age, gender, city) VALUES
(1, 'Ritika Mehra', 33, 'F', 'Mumbai'),
(2, 'Siddharth Malhotra', 38, 'M', 'Delhi'),
(3, 'Anjali Nair', 31, 'F', 'Bangalore'),
(4, 'Manish Sharma', 37, 'M', 'Kolkata'),
(5, 'Neha Patil', 29, 'F', 'Pune'),
(6, 'Rajiv Reddy', 42, 'M', 'Hyderabad'),
(7, 'Tanya Menon', 32, 'F', 'Chennai'),
(8, 'Karan Desai', 36, 'M', 'Ahmedabad'),
(9, 'Priya Joshi', 30, 'F', 'Lucknow'),
(10, 'Vikas Kumar', 39, 'M', 'Jaipur');

INSERT INTO Doctors (doctor_id, name, specialization, experience) VALUES
(1, 'Dr. Varun Mehta', 'Cardiology', 15),
(2, 'Dr. Asha Kapoor', 'Orthopedics', 12),
(3, 'Dr. Sunil Iyer', 'Pediatrics', 10),
(4, 'Dr. Kavita Rao', 'Dermatology', 8),
(5, 'Dr. Pradeep Singh', 'Neurology', 20);

INSERT INTO Appointments (appointment_id, patient_id, doctor_id, appointment_date, status_s) VALUES
(1, 1, 1, '2025-09-01', 'Completed'),
(2, 2, 1, '2025-09-03', 'Pending'),
(3, 3, 2, '2025-09-05', 'Completed'),
(4, 4, 3, '2025-09-06', 'Completed'),
(5, 5, 4, '2025-09-07', 'Cancelled'),
(6, 6, 5, '2025-09-08', 'Pending'),
(7, 7, 1, '2025-09-10', 'Completed'),
(8, 8, 2, '2025-09-11', 'Completed'),
(9, 9, 3, '2025-09-12', 'Pending'),
(10, 10, 4, '2025-09-15', 'Completed');

INSERT INTO MedicalRecords (record_id, patient_id, doctor_id, diagnosis, treatment, date) VALUES
(1, 1, 1, 'Hypertension', 'Medication A', '2025-09-01'),
(2, 2, 1, 'Arrhythmia', 'Medication B', '2025-09-03'),
(3, 3, 2, 'Fracture', 'Cast', '2025-09-05'),
(4, 4, 3, 'Flu', 'Rest & Medication', '2025-09-06'),
(5, 5, 4, 'Acne', 'Topical Cream', '2025-09-07'),
(6, 6, 5, 'Migraine', 'Medication C', '2025-09-08'),
(7, 7, 1, 'High Cholesterol', 'Diet & Medication', '2025-09-10'),
(8, 8, 2, 'Sprain', 'Physiotherapy', '2025-09-11'),
(9, 9, 3, 'Chickenpox', 'Medication D', '2025-09-12'),
(10, 10, 4, 'Eczema', 'Ointment', '2025-09-15');

INSERT INTO Billing (bill_id, patient_id, amount, bill_date, status) VALUES
(1, 1, 5000.00, '2025-09-01', 'Paid'),
(2, 2, 7000.00, '2025-09-03', 'Unpaid'),
(3, 3, 3000.00, '2025-09-05', 'Paid'),
(4, 4, 1500.00, '2025-09-06', 'Unpaid'),
(5, 5, 2000.00, '2025-09-07', 'Paid'),
(6, 6, 4000.00, '2025-09-08', 'Unpaid'),
(7, 7, 6000.00, '2025-09-10', 'Paid'),
(8, 8, 3500.00, '2025-09-11', 'Unpaid'),
(9, 9, 4500.00, '2025-09-12', 'Paid'),
(10, 10, 2500.00, '2025-09-15', 'Unpaid');
