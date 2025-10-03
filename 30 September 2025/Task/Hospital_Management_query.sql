1. List all patients assigned to a cardiologist.
2. Find all appointments for a given doctor.
3. Show unpaid bills of patients.
4. Procedure: GetPatientHistory(patient_id) → returns all visits, diagnoses, and treatments for a patient.
5. Procedure: GetDoctorAppointments(doctor_id) → returns all appointments for a doctor.

SELECT p.patient_id, p.name, p.city
FROM Patients p
JOIN Appointments a ON p.patient_id = a.patient_id
JOIN Doctors d ON a.doctor_id = d.doctor_id
WHERE d.specialization = 'Cardiology';

SELECT a.appointment_id, p.name AS patient_name, a.appointment_date, a.status_s
FROM Appointments a
JOIN Patients p ON a.patient_id = p.patient_id
WHERE a.doctor_id = 4; 

SELECT b.bill_id, p.name AS patient_name, b.amount, b.bill_date
FROM Billing b
JOIN Patients p ON b.patient_id = p.patient_id
WHERE b.status = 'Unpaid';

DELIMITER $$
CREATE PROCEDURE GetPatientHistory(IN p_id INT)
BEGIN
    SELECT m.record_id, m.date, d.name AS doctor_name, m.diagnosis, m.treatment
    FROM MedicalRecords m
    JOIN Doctors d ON m.doctor_id = d.doctor_id
    WHERE m.patient_id = p_id
    ORDER BY m.date;
END$$
DELIMITER ;
CALL GetPatientHistory(5);

DELIMITER $$
CREATE PROCEDURE GetDoctorAppointments(IN d_id INT)
BEGIN
    SELECT a.appointment_id, p.name AS patient_name, a.appointment_date, a.status_s
    FROM Appointments a
    JOIN Patients p ON a.patient_id = p.patient_id
    WHERE a.doctor_id = d_id
    ORDER BY a.appointment_date;
END$$
DELIMITER ;
CALL GetDoctorAppointments(2);
