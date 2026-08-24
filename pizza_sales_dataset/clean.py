import pandas as pd
import numpy as np
from pathlib import Path
from sqlalchemy import create_engine,VARCHAR

# directory
Base_dir = Path.cwd()
excel_dir = Base_dir/'pizza_sales_excel_file.xlsx'

df = pd.read_excel(excel_dir,engine='openpyxl')
df.head()
df.columns
df.shape
df.isnull().sum()
df.info()
df.head()
df['order_time'].value_counts()
df['order_date'].value_counts()
df['pizza_size'].value_counts()
df['pizza_category'].value_counts()
df.to_csv(Base_dir/'pizza_sales.csv',index=False)

pizza_csv = pd.read_csv(Base_dir/'pizza_sales.csv')
pizza_csv.head()

engine = create_engine('postgresql://postgres:sql123@127.0.0.1:5432/pizza_db')
print(engine)
pizza_csv.to_sql('pizza_sales',con=engine,if_exists='append',index=False)

pizza_sql = pd.read_sql('SELECT * FROM pizza_sales',engine)
pizza_sql.shape
pizza_csv.shape