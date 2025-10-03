DELIMITER $$
CREATE PROCEDURE CountStudentsPerCourse()
BEGIN
	SELECT c.course_name, COUNT(e.student_id) AS student_count
    FROM Courses c
    LEFT JOIN enrollments e ON c.course_id=E.course_id
    GROUP BY c.course_name;
END$$
DELIMITER ;
CALL CountStudentsPerCourse;
