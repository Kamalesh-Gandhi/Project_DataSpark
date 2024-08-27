#Import required modules
import pandas as pd
import mysql.connector as db
from mysql.connector import Error

# this SQL_Connection will create the connection between python and mysql
def SQL_Connection():

    config = {
    "user":"root",
    "password":"6381581291",
    "host":"localhost",
    "database":"GlobalElectronics"
    }
    
    conn = db.connect(**config)
    cursor = conn.cursor()

    return conn,cursor

# this function will drop the table
def drop_table(cursor,query_drop):
    try:
        cursor.execute(query_drop)
        print("Table dropped successfully")
    
    except Error as e:
        print("Error occurred when dropping data",e)

#this ReadData_From_Excel will read the data from the .csv file
def ReadData_From_Excel(file_path):
    try:
        """Reads data from an Excel file and returns a DataFrame."""
        return pd.read_csv(file_path)
    except Exception as e:
        print(f'\nError in Reading the data from {file_path}: ', e)

#this Create_Table will create a table in the database
def Create_Table(Table,cursor,table_query):
    try:
        cursor.execute(table_query)
        print("\nSuccessfully Created Table")
    except Error as e:
        print(f"\nCreateTable_Error in {Table}: ", e)    

#this Insert_Table will insert the data into the table
def Insert_Table(tablename,cursor,conn,query,data):
    try:
        cursor.executemany(query,data)
        conn.commit()
        print("\nSuccessfully Inserted Data") 

    except Error as e:
        print(f"\nInsertData_Error in Table {tablename}: ", e)    

# This Function will convert the excel data to list type 
def ConvertingExcelToList(df):
    try:
        data = df.to_numpy().tolist()

        return data
    except Exception as e:
        print("\nError While converting the Excel data to List: ",e)

#this function will close the connection 
def Close_Connection(conn,cursor):
    try:
        conn.close()
    except Exception as e:
        print('\nError in closing the connection: ',e)    

    try:
        cursor.close()
    except Exception as e:
        print('\nError in closing the cursor: ', e)  


"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

#Connect the Sql Server 
conn,cursor = SQL_Connection() 

"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

# if the table already exists drop it to avoid the append of datas
drop_table(cursor,"drop table if exists Customers")
drop_table(cursor,"drop table if exists Exchange_Rates")
drop_table(cursor,"drop table if exists Products_Info")
drop_table(cursor,"drop table if exists Sales_Info")
drop_table(cursor,"drop table if exists Stores_Info")

"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

#Read Data from the Excel
DataFileName = r'DataSets\Cleaned_Customers.csv'
df1 = ReadData_From_Excel(DataFileName)
print("\n",df1)

#Read Data from the Excel
DataFileName = r'DataSets\Cleaned_Exchange_Rates.csv'
df2 = ReadData_From_Excel(DataFileName)
print("\n",df2)

#Read Data from the Excel
DataFileName = r'DataSets\Cleaned_Products.csv'
df3 = ReadData_From_Excel(DataFileName)
print("\n",df3)

#Read Data from the Excel
DataFileName = r'DataSets\Cleaned_Sales_Info2.csv'
df4 = ReadData_From_Excel(DataFileName)
print("\n",df4)

#Read Data from the Excel
DataFileName = r'DataSets\Cleaned_Stores.csv'
df5 = ReadData_From_Excel(DataFileName)
print("\n",df5)

"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

#Create Table Customers in MySql
TableName1 = 'Customers'
Create_Table(TableName1,cursor,"""CREATE table IF NOT EXISTS Customers(
             CustomerKey int Primary Key not null,
             Gender varchar(100) not null,
             Name varchar(50) not null,
             City varchar(100) not null,
             State varchar(50) not null,
             Country varchar(50) not null,
             Continent varchar(50) not null,
             Birthday date not null,
             Age int not null );""")


#Create Table Exchanges Rate in MySql
TableName2 = 'Exchange_Rates'
Create_Table(TableName2,cursor,"""CREATE table IF NOT EXISTS Exchange_Rates(
             Date date not null,
             Currency_Code varchar(50) not null,
             Exchange_Rate float not null);""")

#Create Table Productes Info in MySql
TableName3 = 'Products_Info'
Create_Table(TableName3,cursor,"""CREATE table IF NOT EXISTS Products_Info(
             ProductKey int Primary Key not null,
             ProductName varchar(100) not null,
             Brand varchar(50) not null,
             Color varchar(100) not null,
             Unit_Cost varchar(50) not null,
             Unit_Price varchar(50) not null,
             Profit varchar(50) not null,
             SubcategoryKey int not null,
             Subcategory varchar(50) not null,
             CategoryKey int not null,
             Category varchar(50) not null);""")

#Create Table Sales Info in MySql
TableName4 = 'Sales_Info'
Create_Table(TableName4,cursor,"""CREATE table IF NOT EXISTS Sales_Info(
             Order_Number int not null,
             Line_Item int not null,
             Order_Date date not null,
             CustomerKey int not null,
             StoreKey int not null,
             ProductKey int not null,
             Quantity int not null,
             Currency_Code varchar(50) not null );""")


#Create Table Stores in MySql
TableName5 = 'Stores_info'
Create_Table(TableName5,cursor,"""CREATE table IF NOT EXISTS Stores_Info(
             StoreKey int Primary Key not null,
             Country varchar(100) not null,
             State varchar(50) not null,
             Area_of_Store int not null,
             Open_Date date not null,
             Store_Age int not null );""")

"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

#Insert Data's into Customers Table
Insert_query = """
                INSERT into Customers(CustomerKey,Gender,Name,City,State,Country,Continent,Birthday,Age) 
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE 
                    CustomerKey = VALUES(CustomerKey),    
                    Gender = VALUES(Gender), 
                    Name = VALUES(Name), 
                    City = VALUES(City),
                    State = VALUES(State),
                    Country = VALUES(Country),
                    Continent = VALUES(Continent),
                    Birthday = VALUES(Birthday),
                    Age = VALUES(Age)
                """

data = ConvertingExcelToList(df1) #converting the data into list of tuples to insert into the table
Insert_Table(TableName1,cursor,conn,Insert_query,data)


#Insert Data's into Exchange_Rates Table
Insert_query = """
                INSERT into Exchange_Rates(Date,Currency_Code,Exchange_Rate) 
                values(%s,%s,%s)
                ON DUPLICATE KEY UPDATE 
                    Date = VALUES(Date),    
                    Currency_Code = VALUES(Currency_Code), 
                    Exchange_Rate = VALUES(Exchange_Rate)
                """

data = ConvertingExcelToList(df2) #converting the data into list of tuples to insert into the table
Insert_Table(TableName2,cursor,conn,Insert_query,data)


#Insert Data's into Products Table
Insert_query = """
                INSERT into Products_Info(ProductKey,ProductName,Brand,Color,Unit_Cost,Unit_Price,Profit,SubcategoryKey,Subcategory,CategoryKey,Category) 
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE 
                    ProductKey = VALUES(ProductKey),    
                    ProductName = VALUES(ProductName), 
                    Brand = VALUES(Brand), 
                    Color = VALUES(Color),
                    Unit_Cost = VALUES(Unit_Cost),
                    Unit_Price = VALUES(Unit_Price),
                    Profit = VALUES(Profit),
                    SubcategoryKey = VALUES(SubcategoryKey),
                    Subcategory = VALUES(Subcategory),
                    CategoryKey = VALUES(CategoryKey),
                    Category = VALUES(Category)
                """

data = ConvertingExcelToList(df3) #converting the data into list of tuples to insert into the table
Insert_Table(TableName3,cursor,conn,Insert_query,data)


#Insert Data's into sales_Info Table
Insert_query = """
                INSERT into Sales_Info(Order_Number,Line_Item,Order_Date,CustomerKey,StoreKey,ProductKey,Quantity,Currency_Code) 
                values(%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE 
                    Order_Number = VALUES(Order_Number),    
                    Line_Item = VALUES(Line_Item), 
                    Order_Date = VALUES(Order_Date), 
                    CustomerKey = VALUES(CustomerKey),
                    StoreKey = VALUES(StoreKey),
                    ProductKey= VALUES(ProductKey),
                    Quantity = VALUES(Quantity),
                    Currency_Code = VALUES(Currency_Code)
                """

data = ConvertingExcelToList(df4) #converting the data into list of tuples to insert into the table
Insert_Table(TableName4,cursor,conn,Insert_query,data)


#Insert Data's into Stores_Info Table
Insert_query = """
                INSERT into Stores_Info(StoreKey,Country,State,Area_of_Store,Open_Date,Store_Age) 
                values(%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE 
                    StoreKey = VALUES(StoreKey),    
                    Country = VALUES(Country), 
                    State = VALUES(State), 
                    Area_of_Store = VALUES(Area_of_Store),
                    Open_Date = VALUES(Open_Date),
                    Store_Age = VALUES(Store_Age)
                """

data = ConvertingExcelToList(df5) #converting the data into list of tuples to insert into the table
Insert_Table(TableName5,cursor,conn,Insert_query,data)