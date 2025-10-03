DELIMITER $$
CREATE PROCEDURE StudentsinCourses(IN course INT)
BEGIN
	SELECT s.student_id, s.name 
    FROM Students s
    JOIN enrollments e ON s.student_id=e.student_id
    WHERE e.course_id=course;
END$$
DELIMITER ;
CALL StudentsinCourses(102);
