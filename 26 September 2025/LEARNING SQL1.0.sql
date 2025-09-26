	#	Time	Action	Message	Duration / Fetch
3	1	12:49:38	CREATE DATABASE SCHOOLDB	1 row(s) affected	0.047 sec
0	5	14:37:43	CREATE TABLE Students(
 id INT PRIMARY KEY,
 Name varchar(50),
 Age INT,
 Course Varchar(50),
 Marks int)	Error Code: 1046. No database selected
 Select the default DB to be used by double-clicking its name in the SCHEMAS list in the sidebar.	0.000 sec
0	6	14:38:09	USE schooldb
 CREATE TABLE Students(
 id INT PRIMARY KEY,
 Name varchar(50),
 Age INT,
 Course Varchar(50),
 Marks int)	Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'CREATE TABLE Students(
 id INT PRIMARY KEY,
 Name varchar(50),
 Age INT,
 Course Var' at line 2	0.000 sec
3	7	14:38:17	USE schooldb	0 row(s) affected	0.000 sec
3	8	14:38:17	CREATE TABLE Students(
 id INT PRIMARY KEY,
 Name varchar(50),
 Age INT,
 Course Varchar(50),
 Marks int)	0 row(s) affected	0.063 sec
3	9	14:50:01	INSERT INTO students(
 id, Name , Age, Course, Marks)
 values(101,'Shardul',23,'Btech',98),
 (102,'Om',33,'Mtech',89),
 (103,'Vaibhav',24,'Btech',88),
 (104,'Michael',25,'MBBS',90)	4 row(s) affected
 Records: 4  Duplicates: 0  Warnings: 0	0.000 sec
0	10	14:50:55	INSERT INTO students(
 id, Name , Age, Course, Marks)
 values(101,'Shardul',23,'Btech',98),
 (102,'Om',33,'Mtech',89),
 (103,'Vaibhav',24,'Btech',88),
 (104,'Michael',25,'MBBS',90)	Error Code: 1062. Duplicate entry '101' for key 'students.PRIMARY'	0.000 sec
0	11	14:51:03	View students	Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'View students' at line 1	0.000 sec
0	12	14:51:16	View table students	Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'View table students' at line 1	0.000 sec
3	13	14:52:31	Select * from students
 LIMIT 0, 1000	4 row(s) returned	0.000 sec / 0.000 sec
3	14	14:54:36	Insert Into students(
 id,Name,Age,Course,Marks)
 Values(105, "Irith",25,"MS",99)	1 row(s) affected	0.047 sec
3	15	14:54:58	Select * from students
 LIMIT 0, 1000	5 row(s) returned	0.000 sec / 0.000 sec
3	16	14:56:31	Select DISTINCT(Marks) from students
 LIMIT 0, 1000	5 row(s) returned	0.000 sec / 0.000 sec
3	17	14:57:34	SELECT Name from students where Marks>90
 LIMIT 0, 1000	2 row(s) returned	0.016 sec / 0.000 sec
0	18	14:58:06	SELECT Name from students where Marks IN 90	Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '90' at line 1	0.016 sec
0	19	15:00:22	SELECT Name,Age from students where Marks NOT EQUAL 98	Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'EQUAL 98' at line 1	0.000 sec
3	20	15:01:38	SELECT Name,Age from students where Marks <>98
 LIMIT 0, 1000	4 row(s) returned	0.000 sec / 0.000 sec
3	21	15:02:08	SELECT Name,Age from students where Marks Between 90 and 98
 LIMIT 0, 1000	2 row(s) returned	0.000 sec / 0.000 sec
3	22	15:05:24	Select * from students where name like '%S'
 LIMIT 0, 1000	0 row(s) returned	0.000 sec / 0.000 sec
3	23	15:05:35	Select * from students where name like 'S%'
 LIMIT 0, 1000	1 row(s) returned	0.016 sec / 0.000 sec
3	24	15:26:07	ALTER TABLE students ADD GENDER varchar (50)	0 row(s) affected
 Records: 0  Duplicates: 0  Warnings: 0	0.047 sec
0	25	15:26:55	UPDATE students SET GENDER="Male" where name="Shardul"	Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column. 
 To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.	0.000 sec
0	26	15:29:56	UPDATE students SET GENDER="Male" where name="Shardul"	Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column. 
 To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.	0.000 sec
3	27	15:30:55	SELECT * FROM students
 LIMIT 0, 1000	5 row(s) returned	0.000 sec / 0.000 sec
0	28	15:51:37	Update students SET GENDER='MALE' WHERE Name='Shardul'	Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column. 
 To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.	0.016 sec
3	29	15:52:13	Update students SET GENDER='MALE' WHERE id=101	1 row(s) affected
 Rows matched: 1  Changed: 1  Warnings: 0	0.031 sec
3	30	15:52:15	Update students SET GENDER='MALE' WHERE id=101	0 row(s) affected
 Rows matched: 1  Changed: 0  Warnings: 0	0.000 sec
3	31	15:52:34	Select * from students
 LIMIT 0, 1000	5 row(s) returned	0.000 sec / 0.000 sec
0	32	15:58:17	Update students set Course='phd' where name ='Om'	Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column. 
 To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.	0.015 sec
3	33	15:58:32	Select * from students
 LIMIT 0, 1000	5 row(s) returned	0.000 sec / 0.000 sec
0	34	15:59:16	DELETE FROM students where name='Irith'	Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column. 
 To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.	0.015 sec
0	35	15:59:31	DELETE FROM students where Name='Irith'	Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column. 
 To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.	0.000 sec
3	36	16:00:05	Select * from students
 LIMIT 0, 1000	5 row(s) returned	0.000 sec / 0.000 sec
0	37	16:00:26	DELETE FROM students where id-105	Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column. 
 To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.	0.015 sec
3	38	16:00:35	DELETE FROM students where id=105	1 row(s) affected	0.015 sec
3	39	16:00:50	select * from students
 LIMIT 0, 1000	4 row(s) returned	0.000 sec / 0.000 sec
3	40	16:00:50	select * from students
 LIMIT 0, 1000	4 row(s) returned	0.000 sec / 0.000 sec
3	41	16:12:53	CREATE DATABASE EMPLOYEES	1 row(s) affected	0.000 sec
0	42	16:12:53	USE ENPLOYEES	Error Code: 1049. Unknown database 'enployees'	0.015 sec
3	43	16:13:08	USE EMPLOYEES	0 row(s) affected	0.000 sec
3	44	16:14:55	CREATE TABLE EMP(
 EMPID INT PRIMARY KEY,
 ENAME VARCHAR(50),
 AGE INT,
 DEPARTMENT VARCHAR (50),
 SALARY float
 )	0 row(s) affected	0.015 sec
0	45	16:20:18	INSERT INTO employees(
 EMPID,ENAME,AGE,DEPARTMENT,SALARY)
 VALUES(101,'ASHOK',40,'HR',50000.00),
 (102,'AKASH',45,'TECH',90000.00),
 (103,'ANURAG',49,'TAX',120000.00),
 (104,'MANOJ',40,'AUDIT',50000.00),
 (105,'ASHOK',42,'TAX',70000.00),
 (106,'ROHAN',35,'HR',85000.00)	Error Code: 1146. Table 'employees.employees' doesn't exist	0.000 sec
3	46	16:20:47	INSERT INTO EMP(
 EMPID,ENAME,AGE,DEPARTMENT,SALARY)
 VALUES(101,'ASHOK',40,'HR',50000.00),
 (102,'AKASH',45,'TECH',90000.00),
 (103,'ANURAG',49,'TAX',120000.00),
 (104,'MANOJ',40,'AUDIT',50000.00),
 (105,'ASHOK',42,'TAX',70000.00),
 (106,'ROHAN',35,'HR',85000.00)	6 row(s) affected
 Records: 6  Duplicates: 0  Warnings: 0	0.000 sec
3	47	16:20:58	SELECT * FROM EMP
 LIMIT 0, 1000	6 row(s) returned	0.000 sec / 0.000 sec
3	48	16:21:45	SELECT * FROM EMP WHERE SALARY BETWEEN 60000 AND 85000
 LIMIT 0, 1000	2 row(s) returned	0.015 sec / 0.000 sec
3	49	16:21:58	SELECT ENAME,AGE FROM EMP WHERE SALARY BETWEEN 60000 AND 85000
 LIMIT 0, 1000	2 row(s) returned	0.000 sec / 0.016 sec
3	50	16:22:23	SELECT * FROM EMP
 LIMIT 0, 1000	6 row(s) returned	0.000 sec / 0.000 sec
0	51	16:22:52	DELETE * FROM EMP WHERE EMPID=105	Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '* FROM EMP WHERE EMPID=105' at line 1	0.000 sec
0	52	16:22:56	DELETE * FROM EMP WHERE EMPID=105	Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '* FROM EMP WHERE EMPID=105' at line 1	0.000 sec
3	53	16:23:21	SELECT * FROM EMP
 LIMIT 0, 1000	6 row(s) returned	0.000 sec / 0.000 sec
3	55	16:24:42	SELECT * FROM EMP
 LIMIT 0, 1000	6 row(s) returned	0.000 sec / 0.000 sec
3	56	16:25:47	UPDATE EMP SET ENAME='OM' WHERE EMPID=102	1 row(s) affected
 Rows matched: 1  Changed: 1  Warnings: 0	0.031 sec
3	57	16:25:58	SELECT * FROM EMP
 LIMIT 0, 1000	6 row(s) returned	0.000 sec / 0.000 sec
3	58	16:26:36	DELETE FROM EMP WHERE EMPID=105	1 row(s) affected	0.031 sec
3	59	16:26:55	SELECT * FROM EMP
 LIMIT 0, 1000	5 row(s) returned	0.000 sec / 0.000 sec
