import pandas as pd
import numpy as np
from pathlib import Path

# Path
Basepath= Path.cwd()
xlsx_path =Basepath/'data'/'sales_raw_data.xlsx'

# Reading Excel file
df = pd.read_excel(xlsx_path,engine='openpyxl')
df.head()
df.columns
df.info()

# Missing values
df.isnull().sum()
df.dtypes
numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
categorical_cols = df.select_dtypes(include=['string']).columns.tolist()
numerical_cols
categorical_cols
df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
df = df.dropna(subset=['Date'])

# formatting 
df['Date'] = pd.to_datetime(df['Date'],errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'],errors ='coerce')
df['UnitPrice'] = pd.to_numeric(df['UnitPrice'],errors = 'coerce')
df.dtypes

# Feature Engineering
df['Revenue'] = df['Quantity']*df['UnitPrice']
df['Revenue'].head()
df['month'] = df['Date'].dt.month
df['month'].head()
df['year'] = df['Date'].dt.year
df['year'].head()
df['MonthName'] = df['Date'].dt.strftime('%b')
df['MonthName'].head()

df = df.sort_values('Date')
df.head()
df.info()

df.to_csv(Basepath/'data'/'sales_clean_data.csv',index=False)