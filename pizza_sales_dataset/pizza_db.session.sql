-- Active: 1784820165938@@127.0.0.1@5432@pizza_db
CREATE TABLE pizza_sales(
pizza_id INTEGER,
order_id INTEGER,
pizza_name_id VARCHAR(50),
quantity INTEGER,
order_date DATE,
order_time TEXT,
unit_price FLOAT,
total_price FLOAT,
pizza_size VARCHAR(20),
pizza_category VARCHAR(20),
pizza_ingredients VARCHAR(20),
pizza_name VARCHAR(20)
);

SELECT * FROM pizza_sales;

--A. KPI'S

-- 1. Total_revenue
SELECT CAST(SUM(total_price) AS DECIMAL(10,2)) AS total_revenue FROM pizza_sales;

-- 2.Avg order value
SELECT CAST(CAST(SUM(total_price) AS DECIMAL (10,2))/
CAST(COUNT(DISTINCT order_id) AS DECIMAL (10,2)) AS DECIMAL (10,2))
FROM pizza_sales;

-- 3. Total Pizzas Sold
SELECT CAST(SUM(quantity) AS DECIMAL (10,2)) AS total_pizza_sold FROM pizza_sales;

-- 4. Total Orders
SELECT COUNT(DISTINCT order_id) AS total_orders FROM pizza_sales;

-- 5. Average Pizzas Per Order
SELECT CAST(CAST(SUM(quantity) AS DECIMAL(10,2))/
CAST(COUNT(DISTINCT order_id) AS DECIMAL(10,2)) AS DECIMAL(10,2))
AS average_pizza_per_order FROM pizza_sales;


-- B. Daily Trend for Total Orders
SELECT to_char(order_date::DATE, 'Day') AS order_day,
COUNT(DISTINCT order_id) AS total_order
FROM pizza_sales
GROUP BY to_char(order_date::DATE, 'Day');

-- C. Monthly Trend for Orders
SELECT to_char(order_date::DATE, 'Month') AS order_month,
COUNT(DISTINCT order_id) as total_order
FROM pizza_sales
GROUP BY to_char(order_date::DATE, 'Month');

-- D. % of Sales by Pizza Category
SELECT pizza_category, CAST(SUM(total_price) AS DECIMAL (10,2)) AS total_revenue,
CAST(SUM(total_price)*100/(SELECT SUM(total_price) FROM pizza_sales)
AS DECIMAL (10,2)) AS PCT
FROM pizza_sales
GROUP BY pizza_category;

-- E. % of Sales by Pizza Size
SELECT pizza_size, CAST(SUM(total_price) AS DECIMAL (10,2)) AS total_revenue,
CAST(SUM(total_price)*100/(SELECT SUM(total_price) FROM pizza_sales)
AS DECIMAL (10,2)) AS PCT
from pizza_sales
GROUP BY pizza_size;

-- F. Total Pizzas Sold by Pizza Category
SELECT pizza_category, CAST(SUM(quantity) AS DECIMAL (10,2)) AS total_pizza_sold
FROM pizza_sales
GROUP BY pizza_category
ORDER BY total_pizza_sold ASC;

-- G. Top 5 Pizzas by Revenue

SELECT pizza_name, CAST(SUM(total_price) AS DECIMAL (10,2))  AS total_revenue
FROM pizza_sales
GROUP BY pizza_name
ORDER BY total_revenue DESC
LIMIT 5;

-- H. Bottom 5 Pizzas by Revenue
SELECT pizza_name, CAST(SUM(total_price) AS DECIMAL (10,2))  AS total_revenue
FROM pizza_sales
GROUP BY pizza_name
ORDER BY total_revenue ASC
LIMIT 5;

-- I. Top 5 Pizzas by Quantity
SELECT pizza_name, SUM(quantity) AS total_pizza_sold
FROM pizza_sales
GROUP BY pizza_name
ORDER BY total_pizza_sold DESC
LIMIT 5;

-- J. Bottom 5 Pizzas by Quantity
SELECT pizza_name, SUM(quantity) AS total_pizza_sold
FROM pizza_sales
GROUP BY pizza_name
ORDER BY total_pizza_sold ASC
LIMIT 5;

-- K. Top 5 Pizzas by Total Orders
SELECT pizza_name, COUNT(DISTINCT order_id) AS total_order 
FROM pizza_sales
GROUP BY  pizza_name
ORDER BY total_order DESC
LIMIT 5;

-- L. Borrom 5 Pizzas by Total Orders
SELECT pizza_name, COUNT(DISTINCT order_id) AS total_order 
FROM pizza_sales
GROUP BY  pizza_name
ORDER BY total_order ASC
LIMIT 5;
