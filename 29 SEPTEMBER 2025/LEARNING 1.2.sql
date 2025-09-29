CREATE DATABASE RetailDB;
USE RetailDB;
 
CREATE TABLE Customers (
	customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    city VARCHAR(50),
    phone VARCHAR(15)
);
 
CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    price DECIMAL(10, 2)
);
 
CREATE TABLE Orders (
	order_id INT auto_increment primary key,
    customer_id INT,
    order_date DATE,
    FOREIGN KEY (customer_id) references Customers (customer_id)
);
 
CREATE TABLE OrderDetails (
	order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    foreign key (product_id) references Products (product_id)
);
 
INSERT INTO Customers (name, city, phone) VALUES
('Rahul', 'Mumbai', '9876543210'),
('Priya', 'Delhi', '9876501234'),
('Arjun', 'Bengaluru', '9876512345'),
('Neha', 'Hyderabad', '9876523456');
 
 
INSERT INTO Products (product_name, category, price) VALUES
('Laptop', 'Electronics', 60000.00),
('Smartphone', 'Electronics', 30000.00),
('Headphones', 'Accessories', 2000.00),
('Shoes', 'Fashion', 3500.00),
('T-Shirt', 'Fashion', 1200.00);
 
 
INSERT INTO Orders (customer_id, order_date) VALUES
(1, '2025-09-01'),
(2, '2025-09-02'),
(3, '2025-09-03'),
(1, '2025-09-04');
 
 
INSERT INTO OrderDetails (order_id, product_id, quantity) VALUES
(1, 1, 1),   -- Rahul bought 1 Laptop
(1, 3, 2),   -- Rahul bought 2 Headphones
(2, 2, 1),   -- Priya bought 1 Smartphone
(3, 4, 1),   -- Arjun bought 1 Shoes
(4, 5, 3);   -- Rahul bought 3 T-Shirts
 
DELIMITER $$
CREATE PROCEDURE GetAllProducts()
BEGIN
	SELECT product_id, product_name, category, price
    FROM Products;
END$$
DELIMITER ;
CALL GetAllProducts();
 
DELIMITER $$
CREATE PROCEDURE GetOrdersWithCustomers()
BEGIN
	SELECT o.order_id, o.order_data, c.name AS customer_name
    FROM Orders o
    JOIN Customers c
    ON o.customer_id = c.customer_id;
END$$
DELIMITER ;
 
DROP PROCEDURE GetOrdersWithCustomers;
DELIMITER $$
CREATE PROCEDURE GetFullOrderDetails()
BEGIN
	SELECT o.order_id,
           c.name AS customer_name,
           p.product_name,
           od.quantity,
           p.price,
		   (od.quantity * p.price) AS total
    FROM Orders o
    JOIN Customers c ON o.customer_id = c.customer_id
    JOIN OrderDetails od ON o.order_id = od.order_id
    JOIN Products p ON od.product_id = p.product_id;
END$$
DELIMITER ;
 
CALL GetFullOrderDetails();