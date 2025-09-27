CREATE DATABASE IF NOT EXISTS retail_supply_chain;
USE retail_supply_chain;

-- ================= Products =================
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10,2)
);

INSERT INTO products VALUES
(1, 'T-Shirt', 'Clothing', 10.99),
(2, 'Jeans', 'Clothing', 29.99),
(3, 'Sofa', 'Home', 399.99),
(4, 'Coffee Table', 'Home', 89.99),
(5, 'Dress', 'Clothing', 49.99),
(6, 'Curtains', 'Home', 29.99),
(7, 'Cushion', 'Home', 19.99),
(8, 'Blouse', 'Clothing', 35.99),
(9, 'Jacket', 'Clothing', 79.99),
(10, 'Dining Table', 'Home', 499.99),
(11, 'Sweater', 'Clothing', 45.99),
(12, 'Bed', 'Home', 699.99),
(13, 'Desk', 'Home', 249.99),
(14, 'Skirt', 'Clothing', 39.99),
(15, 'Armchair', 'Home', 299.99),
(16, 'Shoes', 'Clothing', 59.99),
(17, 'Lamp', 'Home', 49.99),
(18, 'Bookshelf', 'Home', 199.99),
(19, 'Hat', 'Clothing', 15.99),
(20, 'Rug', 'Home', 129.99);

-- ================= Suppliers =================
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INT PRIMARY KEY,
    name VARCHAR(255),
    contact_name VARCHAR(255),
    contact_email VARCHAR(255)
);

INSERT INTO suppliers VALUES
(1, 'Supplier A', 'John Doe', 'john.doe@example.com'),
(2, 'Supplier B', 'Jane Smith', 'jane.smith@example.com'),
(3, 'Supplier C', 'Michael Johnson', 'michael.johnson@example.com'),
(4, 'Supplier D', 'Emily White', 'emily.white@example.com'),
(5, 'Supplier E', 'Andrew Johnson', 'andrew.johnson@example.com'),
(6, 'Supplier F', 'Emma Brown', 'emma.brown@example.com'),
(7, 'Supplier G', 'Olivia King', 'olivia.king@example.com'),
(8, 'Supplier H', 'Liam Scott', 'liam.scott@example.com');

-- ================= Warehouses =================
CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id INT PRIMARY KEY,
    location VARCHAR(255),
    capacity INT
);

INSERT INTO warehouses VALUES
(1, 'London', 5000),
(2, 'Manchester', 3000),
(3, 'Birmingham', 4000),
(4, 'Glasgow', 2500),
(5, 'Liverpool', 3500),
(6, 'Leeds', 2800),
(7, 'Bristol', 3200),
(8, 'Sheffield', 2700);

-- ================= Stock =================
CREATE TABLE IF NOT EXISTS stock (
    warehouse_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (warehouse_id, product_id)
);

INSERT INTO stock VALUES
(1,1,100),(1,2,200),(1,3,50),(1,4,75),(1,5,120),
(2,6,150),(2,7,180),(2,8,90),(2,9,60),(2,10,100),
(3,11,80),(3,12,50),(3,13,40),(3,14,70),(3,15,30),
(4,1,60),(4,2,90),(4,3,70),(4,4,80),(4,5,110),
(5,6,120),(5,7,130),(5,8,95),(5,9,85),(5,10,60),
(6,11,40),(6,12,30),(6,13,20),(6,14,25),(6,15,15),
(7,16,70),(7,17,60),(7,18,50),(7,19,90),(7,20,40),
(8,1,80),(8,5,60),(8,10,30),(8,15,20),(8,20,50);

-- ================= Orders =================
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    order_date DATE,
    customer_name VARCHAR(255),
    customer_address VARCHAR(255)
);

INSERT INTO orders VALUES
(1,'2025-09-23','Alice Brown','123 Main St, London'),
(2,'2025-09-23','Bob Green','456 Elm St, Manchester'),
(3,'2025-09-23','Charlie Black','789 Maple St, Birmingham'),
(4,'2025-09-19','Diana Blue','321 Pine St, Glasgow'),
(5,'2025-09-22','Edward Brown','654 Oak St, London'),
(6,'2025-09-22','Fiona Green','987 Willow St, Manchester'),
(7,'2025-09-20','George White','222 Cherry St, Liverpool'),
(8,'2025-09-20','Hannah Green','333 Maple St, Leeds'),
(9,'2025-09-25','Isaac Black','444 Elm St, Birmingham'),
(10,'2025-09-20','Jessica Blue','555 Oak St, Glasgow'),
(11,'2025-09-24','Kevin Long','101 River St, London'),
(12,'2025-09-23','Laura King','202 Hill St, Manchester');

-- ================= Order Items =================
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2)
);

INSERT INTO order_items VALUES
(1,1,1,2,21.98),(2,1,3,1,399.99),(3,2,2,1,29.99),(4,2,5,2,99.98),
(5,3,6,3,89.97),(6,3,7,4,79.96),(7,4,8,2,71.98),(8,4,9,1,79.99),
(9,5,10,1,499.99),(10,5,11,2,91.98),(11,6,12,1,59.98),(12,7,15,2,599.98),
(13,7,12,1,699.99),(14,8,13,3,749.97),(15,8,14,2,79.98),(16,9,11,2,91.98),
(17,9,12,1,699.99),(18,10,15,1,299.99),(19,10,11,1,45.99),
(20,11,16,2,119.98),(21,12,17,1,49.99);

-- ================= Shipments =================
CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INT PRIMARY KEY,
    supplier_id INT,
    warehouse_id INT,
    shipment_date DATE
);

INSERT INTO shipments VALUES
(1,1,1,'2025-09-25'),(2,2,2,'2025-09-21'),(3,3,3,'2025-09-25'),
(4,4,4,'2025-09-25'),(5,5,5,'2025-09-25'),(6,6,6,'2025-09-23'),
(7,3,4,'2025-09-22'),(8,5,3,'2025-09-25'),(9,1,6,'2025-09-22'),
(10,2,5,'2025-09-23'),(11,7,7,'2025-09-19'),(12,8,8,'2025-09-20');

-- ================= Shipment Items =================
CREATE TABLE IF NOT EXISTS shipment_items (
    shipment_item_id INT PRIMARY KEY,
    shipment_id INT,
    product_id INT,
    quantity INT
);

INSERT INTO shipment_items VALUES
(1,1,1,50),(2,1,2,100),(3,2,4,75),(4,2,5,150),
(5,3,6,50),(6,3,7,30),(7,4,8,100),(8,4,9,50),
(9,5,10,120),(10,5,11,80),(11,6,12,40),(12,6,13,20),
(13,7,11,50),(14,7,12,15),(15,8,13,30),(16,8,14,20),
(17,9,15,40),(18,9,11,30),(19,10,12,10),(20,10,13,20),
(21,11,16,20),(22,12,17,15);

-- ================= Sales =================
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT PRIMARY KEY,
    sale_date DATE,
    product_id INT,
    quantity INT,
    total_amount DECIMAL(10,2)
);

INSERT INTO sales VALUES
(1,'2025-09-23',1,2,21.98),
(2,'2025-09-25',2,1,29.99),
(3,'2025-09-21',3,1,399.99);
