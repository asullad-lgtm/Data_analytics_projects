#Modules
import pandas as pd
import openpyxl
from pathlib import Path 
import glob

#Path
Base_path = Path.cwd()
excel_path = Base_path/"data"/"xlsx"
csv_path = Base_path/"data"/"raw"

csv_path.mkdir(parents=True,exist_ok=True)

# Reading Excel file
for excel_file in excel_path.glob("*.xlsx"):
    print(f"processing:{excel_file.name}")
    xls = pd.ExcelFile(excel_file)
    print(xls.sheet_names)

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls,sheet_name=sheet_name,header=1,engine='openpyxl')
        print(df.head())

    # To CSV file
    csv_name = f"{sheet_name}.csv"
    csv = csv_path/csv_name
    df.to_csv(csv,index=False)


