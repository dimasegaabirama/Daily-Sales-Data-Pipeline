-- =====================================
-- Snowflake Landing Schema
-- =====================================

CREATE DATABASE IF NOT EXISTS RETAIL_SUPPLY_CHAIN;

CREATE SCHEMA IF NOT EXISTS LANDING;
CREATE SCHEMA IF NOT EXISTS DIMENSION;
CREATE SCHEMA IF NOT EXISTS FACT;
CREATE SCHEMA IF NOT EXISTS SNAPSHOT;

USE DATABASE RETAIL_SUPPLY_CHAIN;
USE SCHEMA LANDING;

-- ================= Products =================
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2)
);

-- ================= Suppliers =================
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INT AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(100),
    contact_name VARCHAR(100),
    contact_email VARCHAR(100)
);

-- ================= Warehouses =================
CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id INT AUTOINCREMENT PRIMARY KEY,
    location VARCHAR(100),
    capacity INT
);

-- ================= Stock =================
CREATE TABLE IF NOT EXISTS stock (
    warehouse_id INT,
    product_id INT,
    quantity INT,
    PRIMARY KEY (warehouse_id, product_id)
    -- FOREIGN KEY di Snowflake opsional, bisa dihapus
);

-- ================= Orders =================
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTOINCREMENT PRIMARY KEY,
    order_date DATE,
    customer_name VARCHAR(100),
    customer_address VARCHAR(100)
);

-- ================= Order Items =================
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTOINCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2)
    -- FOREIGN KEY opsional
);

-- ================= Shipments =================
CREATE TABLE IF NOT EXISTS shipments (
    shipment_id INT AUTOINCREMENT PRIMARY KEY,
    supplier_id INT,
    warehouse_id INT,
    shipment_date DATE
    -- FOREIGN KEY opsional
);

-- ================= Shipment Items =================
CREATE TABLE IF NOT EXISTS shipment_items (
    shipment_item_id INT AUTOINCREMENT PRIMARY KEY,
    shipment_id INT,
    product_id INT,
    quantity INT
    -- FOREIGN KEY opsional
);

-- ================= Sales =================
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTOINCREMENT PRIMARY KEY,
    sale_date DATE,
    product_id INT,
    quantity INT,
    total_amount DECIMAL(10,2)
    -- FOREIGN KEY opsional
);
