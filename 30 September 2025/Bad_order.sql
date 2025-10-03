CREATE TABLE BadOrders (
	order_id      INT PRIMARY KEY,
  order_date    DATE,
  customer_id   INT,
  customer_name VARCHAR(50),
  customer_city VARCHAR(50),
  products_ids VARCHAR(200),
  products_name VARCHAR(200),
  unit_prices VARCHAR(200),
  quantities VARCHAR(200),
  order_total DECIMAL(10,2) 
);
