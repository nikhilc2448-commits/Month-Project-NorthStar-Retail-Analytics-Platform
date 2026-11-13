-- Module 15: NorthStar Retail Analytics - Data Warehouse
-- MySQL 8.0+
-- Source data expected in test.transactions.
-- WARNING: This script drops and recreates the five warehouse tables only.
-- It does NOT drop or modify the source database/table.

CREATE DATABASE IF NOT EXISTS northstar_warehouse;
USE northstar_warehouse;

-- Drop in dependency order so this script can be rerun from a clean warehouse.
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_store;
DROP TABLE IF EXISTS dim_date;

-- 1. Dimension tables
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    day_of_week INT NOT NULL,
    is_weekend TINYINT(1) NOT NULL
);

CREATE TABLE dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL UNIQUE,
    customer_name VARCHAR(150) NULL,
    email VARCHAR(150) NULL,
    join_date DATE NULL,
    city VARCHAR(100) NULL,
    state VARCHAR(50) NULL,
    rfm_segment VARCHAR(50) NULL
);

CREATE TABLE dim_product (
    product_key INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL UNIQUE,
    product_name VARCHAR(200) NULL,
    category VARCHAR(100) NULL,
    unit_cost DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    retail_price DECIMAL(12,2) NOT NULL DEFAULT 0.00
);

CREATE TABLE dim_store (
    store_key INT AUTO_INCREMENT PRIMARY KEY,
    store_id VARCHAR(50) NOT NULL UNIQUE,
    store_name VARCHAR(100) NULL,
    state VARCHAR(50) NULL,
    region VARCHAR(50) NULL,
    quarterly_target DECIMAL(14,2) NOT NULL DEFAULT 0.00
);

-- 2. Fact table
-- Grain: one source transaction line (transaction + product + date).
CREATE TABLE fact_sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    date_key INT NOT NULL,
    customer_key INT NULL,
    product_key INT NULL,
    store_key INT NULL,
    channel VARCHAR(50) NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    discount_amount DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    net_revenue DECIMAL(16,2) NOT NULL DEFAULT 0.00,
    cost_amount DECIMAL(16,2) NOT NULL DEFAULT 0.00,
    profit_margin DECIMAL(16,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_sales_date FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    CONSTRAINT fk_sales_product FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    CONSTRAINT fk_sales_store FOREIGN KEY (store_key) REFERENCES dim_store(store_key)
);

CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_store ON fact_sales(store_key);
CREATE INDEX idx_fact_sales_channel ON fact_sales(channel);

-- 3. Load date dimension from valid transaction dates.
INSERT INTO dim_date (
    date_key, full_date, day, month, month_name, quarter, year,
    day_of_week, is_weekend
)
SELECT
    YEAR(x.order_date) * 10000 + MONTH(x.order_date) * 100 + DAY(x.order_date),
    x.order_date,
    DAY(x.order_date),
    MONTH(x.order_date),
    MONTHNAME(x.order_date),
    QUARTER(x.order_date),
    YEAR(x.order_date),
    DAYOFWEEK(x.order_date),
    CASE WHEN DAYOFWEEK(x.order_date) IN (1, 7) THEN 1 ELSE 0 END
FROM (
    SELECT DISTINCT STR_TO_DATE(
        NULLIF(TRIM(CAST(OrderDate AS CHAR)), ''), '%Y-%m-%d'
    ) AS order_date
    FROM test.transactions
) AS x
WHERE x.order_date IS NOT NULL;

-- 4. Load customer dimension using distinct valid customer IDs.
-- Other customer attributes remain NULL because they are not sourced here.
INSERT INTO dim_customer (customer_id)
SELECT DISTINCT TRIM(CustomerID)
FROM test.transactions
WHERE CustomerID IS NOT NULL
  AND TRIM(CustomerID) <> ''
  AND LOWER(TRIM(CustomerID)) <> 'unknown';

-- 5. Load product dimension using distinct product IDs.
-- Product descriptions, category, cost, and retail price remain default/NULL
-- until they are loaded from the product master data.
INSERT INTO dim_product (product_id)
SELECT DISTINCT TRIM(ProductID)
FROM test.transactions
WHERE ProductID IS NOT NULL
  AND TRIM(ProductID) <> '';

-- 6. Load store dimension using distinct physical store IDs.
-- ONLINE is a sales channel, not a physical store, so it is excluded.
INSERT INTO dim_store (store_id)
SELECT DISTINCT TRIM(StoreID)
FROM test.transactions
WHERE StoreID IS NOT NULL
  AND TRIM(StoreID) <> ''
  AND UPPER(TRIM(StoreID)) <> 'ONLINE';

-- 7. Load fact sales. LineAmount is treated as net revenue.
-- Cost and profit are set to zero until reliable cost data is joined.
INSERT INTO fact_sales (
    transaction_id, date_key, customer_key, product_key, store_key,
    channel, quantity, unit_price, discount_amount, net_revenue,
    cost_amount, profit_margin
)
SELECT
    TRIM(t.TransactionID),
    d.date_key,
    c.customer_key,
    p.product_key,
    s.store_key,
    NULLIF(TRIM(t.Channel), ''),
    CASE WHEN t.Quantity IS NULL OR t.Quantity <= 0 THEN 1 ELSE t.Quantity END,
    CASE
        WHEN t.Quantity > 0 THEN COALESCE(t.LineAmount, 0) / t.Quantity
        ELSE 0.00
    END,
    COALESCE(t.Discount, 0.00),
    COALESCE(t.LineAmount, 0.00),
    0.00,
    0.00
FROM test.transactions AS t
JOIN dim_date AS d
    ON d.full_date = STR_TO_DATE(
        NULLIF(TRIM(CAST(t.OrderDate AS CHAR)), ''), '%Y-%m-%d'
    )
LEFT JOIN dim_customer AS c
    ON c.customer_id = TRIM(t.CustomerID)
LEFT JOIN dim_product AS p
    ON p.product_id = TRIM(t.ProductID)
LEFT JOIN dim_store AS s
    ON s.store_id = TRIM(t.StoreID)
WHERE t.TransactionID IS NOT NULL
  AND TRIM(t.TransactionID) <> ''
  AND t.OrderDate IS NOT NULL
  AND TRIM(CAST(t.OrderDate AS CHAR)) <> '';

-- 8. Validation checks
SELECT 'dim_date' AS table_name, COUNT(*) AS total_rows FROM dim_date
UNION ALL
SELECT 'dim_customer', COUNT(*) FROM dim_customer
UNION ALL
SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL
SELECT 'dim_store', COUNT(*) FROM dim_store
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM fact_sales;

SELECT
    COUNT(*) AS total_sales,
    SUM(net_revenue) AS total_revenue,
    SUM(quantity) AS total_quantity,
    COUNT(DISTINCT customer_key) AS customers_linked_to_sales,
    COUNT(DISTINCT product_key) AS products_linked_to_sales
FROM fact_sales;

-- Check unusually high calculated unit prices before final submission.
SELECT transaction_id, quantity, unit_price, net_revenue
FROM fact_sales
ORDER BY unit_price DESC
LIMIT 20;


USE northstar_warehouse;

INSERT INTO dim_date (
    date_key,
    full_date,
    day,
    month,
    month_name,
    quarter,
    year,
    day_of_week,
    is_weekend
)
VALUES (
    20240922,
    '2024-09-22',
    22,
    9,
    'September',
    3,
    2024,
    DAYOFWEEK('2024-09-22'),
    1
);