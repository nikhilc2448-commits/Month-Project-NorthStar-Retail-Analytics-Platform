
-- MODULE 14: SQL BUSINESS ANALYSIS
-- NorthStar Retail Analytics

USE test;


-- 1. Total Revenue by Region (JOIN)
SELECT
    s.Region,
    SUM(t.LineAmount) AS TotalRevenue
FROM transactions t
JOIN stores s ON t.StoreID = s.StoreID
GROUP BY s.Region
ORDER BY TotalRevenue DESC;


-- 2. Top 10 Stores by Revenue (JOIN)
SELECT
    s.StoreName,
    SUM(t.LineAmount) AS TotalRevenue
FROM transactions t
JOIN stores s ON t.StoreID = s.StoreID
GROUP BY s.StoreID, s.StoreName
ORDER BY TotalRevenue DESC
LIMIT 10;


-- 3. Monthly Revenue
SELECT
    DATE_FORMAT(
        STR_TO_DATE(OrderDate, '%Y-%m-%d'),
        '%Y-%m'
    ) AS SalesMonth,
    SUM(LineAmount) AS Revenue
FROM transactions
WHERE STR_TO_DATE(OrderDate, '%Y-%m-%d') IS NOT NULL
GROUP BY SalesMonth
ORDER BY SalesMonth;


-- 4. Revenue by Product Category (JOIN)
SELECT
    p.Category,
    SUM(t.LineAmount) AS Revenue
FROM transactions t
JOIN products p ON t.ProductID = p.ProductID
GROUP BY p.Category
ORDER BY Revenue DESC;


-- 5. Top 10 Customers by Spending (JOIN)
SELECT
    c.CustomerID,
    SUM(t.LineAmount) AS TotalSpending
FROM transactions t
JOIN customers c ON t.CustomerID = c.CustomerID
GROUP BY c.CustomerID
ORDER BY TotalSpending DESC
LIMIT 10;


-- 6. Return Count and Refund Amount by Reason (JOIN)
SELECT
    r.Reason,
    COUNT(*) AS ReturnCount,
    SUM(r.RefundAmount) AS TotalRefund
FROM returns r
JOIN transactions t ON r.TransactionID = t.TransactionID
GROUP BY r.Reason
ORDER BY TotalRefund DESC;


-- 7. Rank Stores by Revenue (Window Function)
WITH StoreSales AS (
    SELECT
        s.StoreID,
        s.StoreName,
        SUM(t.LineAmount) AS TotalRevenue
    FROM transactions t
    JOIN stores s ON t.StoreID = s.StoreID
    GROUP BY s.StoreID, s.StoreName
)
SELECT
    StoreID,
    StoreName,
    TotalRevenue,
    RANK() OVER (ORDER BY TotalRevenue DESC) AS RevenueRank
FROM StoreSales;


-- 8. Classify Transactions Using CASE
SELECT
    TransactionID,
    LineAmount,
    CASE
        WHEN LineAmount >= 10000 THEN 'High'
        WHEN LineAmount >= 5000 THEN 'Medium'
        ELSE 'Low'
    END AS RevenueCategory
FROM transactions;


-- 9. Transactions Above Average Revenue (CTE)
WITH AverageSales AS (
    SELECT AVG(LineAmount) AS AvgRevenue
    FROM transactions
)
SELECT
    TransactionID,
    CustomerID,
    LineAmount
FROM transactions
WHERE LineAmount > (
    SELECT AvgRevenue FROM AverageSales
)
ORDER BY LineAmount DESC;


-- 10. Customers with Repeat Purchases (CTE)
WITH CustomerOrders AS (
    SELECT
        CustomerID,
        COUNT(DISTINCT TransactionID) AS TotalPurchases,
        SUM(LineAmount) AS TotalSpending
    FROM transactions
    GROUP BY CustomerID
)
SELECT
    CustomerID,
    TotalPurchases,
    TotalSpending
FROM CustomerOrders
WHERE TotalPurchases > 1
ORDER BY TotalPurchases DESC;

