# Import Required modules
import pandas as pd

# This Function Use to Read Data from the CSV File
def Read_CSV(File_Name):
    try:
        df = pd.read_csv(File_Name,encoding='ISO-8859-1')
        return df

    except Exception as e:  
        print(f'The Error while reading the file {File_Name} :',e)

# This Function use to Understand the Data
def DataUnderstanding(df):

    try:
        # df.shape
        print(df.shape,'\n')

    except Exception as e:
        print("The Error in finding shape --- ",e,'\n')

    try:
        # df.head
        print(df.head(),'\n')

    except Exception as e:
        print("The Error in finding Head --- ",e,'\n')

    try:   
        # df.columns
        print(df.columns,'\n')

    except Exception as e:
        print("The Error in finding columns --- ",e,'\n')

    try:
        # df.dtypes
        print(df.dtypes,'\n')

    except Exception as e:
        print("The Error in finding dtypes --- ",e,'\n')

    try:
        # df.describe
        print(df.describe(),'\n')

    except Exception as e:
        print("The Error in finding describe --- ",e,'\n')    
    
    return df

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------           

# This Function use to drop the column from the table
def DropingColumn(df,dropcolumns):
    if dropcolumns:
        try:
            df = df.drop(dropcolumns, axis=1).copy()
            print(f"Dropped columns: {dropcolumns}")
        except Exception as e:
            print("The Error while dropping the Columns: ", e, '\n')
    else:
        print("No Columns are dropped", '\n')

    return df
    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------           

# This Function Change the DataType to datetime
def DataType_Change(df,columnname):
    if columnname != "" :
        try:
            df[columnname] = pd.to_datetime(df[columnname])
            print(f'Datatype of the {columnname} : ', df[columnname].dtypes,'\n')
           
        except Exception as e:
            print("The Error while Changing DataType: ",e,'\n')     
    
    else:
        print("No header Datatype was changed",'\n')
    return df    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------           

# This Function use to check null values in the tables
def Check_NA(df):
    try:
        print("Missing values before deletion: ", df.isna().sum(),'\n')
        
        # Drop rows with any NA values
        df_cleaned = df.dropna()
        
        print("\nMissing values after deletion: ", df_cleaned.isna().sum(),'\n')
        return df_cleaned
    except Exception as e:
        print("The Error while checking and deleting NA: ", e,'\n')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------           

# This Function use to check the duplicates values in the table
def CheckFor_DuplicateValues(df):
    try:
        val = df.duplicated().sum()
        print('Number of Duplicate Values: ',val,'\n')

        if val != 0:
            df = df.drop_duplicated().reset_index(drop =True)
        
            return df
        else:
            return df
    
    except Exception as e:
        print("The Error while checking for duplicate values: ",e,"\n")    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------           

# This Function use to create the .CSV file
def WriteData_toCSV(df,File_Name):
    try:
        df.to_csv(File_Name, index=False)
        print(f"Cleaned data has been saved to {File_Name}")
    except Exception as e:
        print(f"Error while saving the file {File_Name}: ", e)

# Configure the FileName based on the requirement
FileName = ""

Data = Read_CSV(FileName)


#This function have properties which will use for understanding about the variables of the  DataSets
df = DataUnderstanding(Data)

#Droping the useless Column from the dataset 
ColumnNames = ''
df = DropingColumn(df,ColumnNames)

#Changing the data type of the column
dataTypeChange = ''
df = DataType_Change(df,dataTypeChange)

#check for empty cells in the datasets
df = Check_NA(df)

#Checking the dataSets for duplicate values and droping the duplicate values
df = CheckFor_DuplicateValues(df)

#writing the Cleaned DataSets into new CSV File
File_Name = r'DataSets\Cleaned_Stores.csv'
WriteData_toCSV(df,File_Name)
