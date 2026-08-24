-- Active: 1784820165938@@127.0.0.1@5432@sales_data
CREATE TABLE sales(
    OrderID INT,
    Date DATE,
    Region TEXT,
    Product TEXT,
    Category TEXT,
    Quantity FLOAT,
    UnitPrice FLOAT,
    SalesPerson TEXT,
    Revenue FLOAT,
    month FLOAT,
    year FLOAT,
    MonthName TEXT
);

SELECT * FROM sales
ORDER BY orderid;

-- Adding row number for better visual
SELECT ROW_NUMBER() OVER (ORDER BY date,orderid) AS RowNum, 
sales.*FROM sales;

-- Total Business Performance
CREATE OR REPLACE VIEW vw_Total_Business_Performance AS
SELECT COUNT(DISTINCT orderid) AS Total_orders,
SUM(revenue) AS Total_revenue,
AVG(revenue) as avg_order_value
FROM sales;

SELECT * FROM vw_Total_Business_Performance;

-- Monthly Sales Trend

SELECT
year,
month,
monthname,
ROUND(SUM(revenue)::NUMERIC,2) AS Monthly_revenue
FROM sales
GROUP BY year,month,monthname
ORDER BY year,month;

-- Region-wise Performance
SELECT
region,
ROUND(SUM(revenue)::NUMERIC,2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- Top 5 Products
SELECT 
product,
ROUND(SUM(revenue)::NUMERIC,2) AS revenue
from sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 5;

-- Best Salesperson
SELECT
salesperson,
ROUND(SUM(revenue)::NUMERIC,2) AS  revenue
FROM sales
GROUP BY salesperson
ORDER BY revenue DESC;

-- Month-over-Month Growth

WITH monthly AS(
    SELECT 
    year,
    month,
    SUM(revenue) AS revenue
    FROM sales
    GROUP BY year,month
)
SELECT 
year,
month,
revenue,
revenue - COALESCE(LAG(revenue) OVER(ORDER BY year,month),revenue) AS Mom_changes
FROM monthly
ORDER BY year,month;
