CREATE database GlobalElectronics;
USE GlobalElectronics;

Select * from customers;
select * from Exchange_Rates;
select * from Products_Info;
select * from Sales_Info;
select * from Stores_Info;


SELECT * FROM product_popularity;
SELECT * FROM totalsalesbycategory;
SELECT * FROM totalprofitbybrand;

SELECT * FROM customerdistributionbygender;
SELECT * FROM topcustomersbysales;
SELECT * FROM totalsalesbygender;
SELECT * FROM totalnumbercustomersbystate;

SELECT * FROM impactofstoreageonsales;
SELECT * FROM storecustomerdata;
SELECT * FROM areaofstorebycountry;
SELECT * FROM topstorekeybytotalsales;

SELECT * FROM TotalProfitAndSalesByCurrencyCode;
SELECT * FROM exchangeratestrendovertime;
SELECT * FROM MAX_MIN_LowestExchangeRates;


Drop table MAX_MIN_LowestExchangeRates;

Alter table products_info
Modify Unit_Cost float,
Modify Unit_Price float,
Modify Profit float;

-- Total Profit w.r.t the SubCategory Data---------------------------------------------------------------

SELECT Subcategory,SUM(Profit) AS Total_Profit_USD
FROM products_info
GROUP BY Subcategory;
   
-- Adding New Column 'Sales Column' in the Sales_info Table -------------------------------------------------------------------   
   
ALTER TABLE sales_info
ADD COLUMN Sales_Volume FLOAT;

UPDATE sales_info si
JOIN (
    SELECT ProductKey, SUM(Quantity) AS Total_Sales_Volume
    FROM sales_info
    GROUP BY ProductKey
) AS temp ON si.ProductKey = temp.ProductKey
SET si.Sales_Volume = temp.Total_Sales_Volume;

-- Product Analysis Insights ------------------------------------------------------------------------
-- 1: Create New Table Popular Product ---

CREATE TABLE product_popularity (
    ProductKey INT,
    ProductName VARCHAR(255),
    Total_Sales_Volume FLOAT,
    Popularity_Status VARCHAR(50)
);

INSERT INTO product_popularity (ProductKey, ProductName, Total_Sales_Volume, Popularity_Status)
SELECT p.ProductKey, p.ProductName, SUM(si.Quantity) AS Total_Sales_Volume, 'Most Popular' AS Popularity_Status
FROM sales_info si
JOIN products_info p ON si.ProductKey = p.ProductKey
GROUP BY p.ProductKey, p.ProductName
ORDER BY Total_Sales_Volume DESC
LIMIT 10;  -- Adjust the limit as needed

INSERT INTO product_popularity (ProductKey, ProductName, Total_Sales_Volume, Popularity_Status)
SELECT p.ProductKey, p.ProductName, SUM(si.Quantity) AS Total_Sales_Volume, 'Least Popular' AS Popularity_Status
FROM sales_info si
JOIN products_info p ON si.ProductKey = p.ProductKey
GROUP BY p.ProductKey, p.ProductName
ORDER BY Total_Sales_Volume ASC
LIMIT 10;  -- Adjust the limit as needed

-- 2: Create New Table Total Profit By Brands --
CREATE TABLE TotalProfitByBrand AS
SELECT Brand, sum(Profit) AS Total_Sales
From products_info 
GROUP BY Brand;

-- 3: Create New Table for Total Sales By Category

CREATE TABLE TotalSalesByCategory AS
SELECT p.Category,SUM(s.Quantity * p.Unit_Price) AS Total_Sales
FROM Sales_info s
JOIN Products_info p 
ON s.ProductKey = p.ProductKey
GROUP BY p.Category;
-- -----------------------------------------------------------------------------------------------------------------

-- Customer Analysis Insights --------------------------------------------------------------------------------------
-- 1: Create New Table Customer Distribution by Gender ---

CREATE TABLE CustomerDistributionByGender
SELECT Gender,Count(CustomerKey) As NumbersOfCustomers
FROM customers
GROUP BY Gender ;

-- 2: Create NEw Table ,Top 10 Customers by sales---------------------------------------------------------------------

SELECT s.CustomerKey, SUM(s.Quantity * p.Unit_Price) AS total_sales
FROM sales_info s
JOIN products_info p ON s.Productkey = p.Productkey
GROUP BY s.CustomerKey;

DROP TABLE  TopCustomersBySales;
CREATE TABLE TopCustomersBySales (CustomerKey INT,gender VARCHAR(50),total_sales DECIMAL(10, 2));


INSERT INTO TopCustomersBySales (CustomerKey, gender, total_sales)
SELECT c.CustomerKey, c.gender, ts.total_sales
FROM (
    SELECT s.customerKey, SUM(s.Quantity * p.Unit_Price) AS total_sales
    FROM sales_info s
    JOIN products_info p ON s.ProductKey = p.ProductKey
    GROUP BY s.customerKey
) ts
JOIN customers c ON ts.customerKey = c.CustomerKey
ORDER BY ts.total_sales DESC
LIMIT 10;

-- 3: Total sales by Gender ----------------------------------------------------------------------------------
CREATE TABLE totalsalesgender AS
SELECT c.gender, SUM(ts.total_sales) AS Total_Sales
FROM (
    SELECT s.customerKey, SUM(s.Quantity * p.Unit_Price) AS total_sales
    FROM sales_info s
    JOIN products_info p ON s.ProductKey = p.ProductKey
    GROUP BY s.customerKey
) ts
JOIN customers c 
ON ts.customerKey = c.CustomerKey
GROUP BY gender;

-- 4: Number of Customers by State ----------------------------------------------------------------------------------
CREATE TABLE totalnumbercustomersbystate AS 
SELECT State, Gender, COUNT(CustomerKey) AS Number_Of_Customers
FROM customers 
GROUP BY State, Gender;

-- Store Analysis Insights --------------------------------------------------------------------------------------
-- 1:impactofstoreageonsales-------------------------------------------------------------------------------------

CREATE TABLE ImpactOfStoreAgeOnSales AS
SELECT c.Store_Age, SUM(ts.total_sales) AS TotalSales 
FROM (
    SELECT s.StoreKey, SUM(s.Quantity * p.Unit_Price) AS total_sales
    FROM sales_info s
    JOIN products_info p ON s.ProductKey = p.ProductKey
    GROUP BY s.StoreKey
) ts
JOIN stores_info c ON ts.StoreKey = c.StoreKey
GROUP BY c.Store_Age;

-- 2:impactofstoreageonsales-------------------------------------------------------------------------------------

CREATE TABLE StoreCustomerData AS
SELECT s.Country, COUNT(DISTINCT s.StoreKey) AS Store_Count, COUNT(DISTINCT si.CustomerKey) AS Customer_Count
FROM stores_info s
JOIN sales_info si 
ON s.StoreKey = si.StoreKey
GROUP BY s.Country
ORDER BY Customer_Count DESC;

-- 3: AreaOfStoreByCountry-------------------------------------------------------------------------------------

CREATE TABLE areaofstorebycountry AS
SELECT DISTINCT Country, Area_of_Store
FROM stores_info;

-- 4: Top StoreKey by Sales -------------------------------------------------------------------------------------

CREATE TABLE topstorekeybytotalsales AS
SELECT s.StoreKey, SUM(s.Quantity * p.Unit_Price) AS TotalSales
FROM sales_info s
JOIN products_info p 
ON s.ProductKey = p.ProductKey
GROUP BY s.StoreKey
ORDER BY TotalSales DESC
LIMIT 10;


-- ExchangeRate Analysis Insights --------------------------------------------------------------------------------------
-- 1: Total PROFIT And SALES by Currency Code----------------------------------------------------------------------------

CREATE TABLE TotalProfitAndSalesByCurrencyCode AS
SELECT si.Currency_Code, SUM(pi.Profit) AS Total_Profit,SUM(si.Sales_Volume) AS Total_Sales
FROM sales_info si
JOIN products_info pi 
ON si.ProductKey = pi.ProductKey
GROUP BY si.Currency_Code;


-- 2: Trend of Exchange Rates Over Time --------------------------------------------------------------------------------------

CREATE TABLE ExchangeRatesTrendOverTime AS
SELECT Date, Currency_Code, Exchange_Rate
FROM exchange_rates
ORDER BY Date ASC;

-- 3:  Highest and Lowest Exchange Rates ------------------------------------------------------------------------------------

CREATE TABLE MAX_MIN_LowestExchangeRates AS
SELECT Currency_Code, YEAR(Date) AS Year, 
	MAX(Exchange_Rate) AS Highest_Exchange_Rate, 
    MIN(Exchange_Rate) AS Lowest_Exchange_Rate
FROM exchange_rates
GROUP BY Currency_Code, YEAR(Date);
