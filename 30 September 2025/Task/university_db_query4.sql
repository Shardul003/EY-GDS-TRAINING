DELIMITER $$
CREATE PROCEDURE StudentswithCourses()
BEGIN
	SELECT s.student_id, s.name, c.course_name
    FROM Students s
    JOIN enrollments e ON s.student_id=e.student_id
    JOIN courses c ON e.course_id=c.course_id;
    
END$$
DELIMITER ;
CALL StudentswithCourses;
