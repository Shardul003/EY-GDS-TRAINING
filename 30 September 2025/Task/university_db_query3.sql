DELIMITER $$
CREATE PROCEDURE StudentsFromCity(IN city_name VARCHAR(50)) 
BEGIN  
	SELECT * FROM Students WHERE city=city_name; 
    END$$
DELIMITER ;
CALL StudentsFromCity('Delhi');
