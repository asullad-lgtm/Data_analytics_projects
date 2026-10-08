#%%
import pandas as pd
import os
import glob
from pathlib import Path
# %%
Base_dir = Path.cwd().parent
raw_dir = Base_dir/'data'/'raw'
csv_dir = Base_dir/'data'/'csv'
csv_dir.mkdir(parents=True,exist_ok=True)
# %%
def load_tables():
    files = list(raw_dir.glob("*.xlsx"))

    for file in files:
        dfs = pd.read_excel(file,sheet_name=None,header=1)

        for name,df in dfs.items():
            print('='*60)
            print(f"filename:{os.path.basename(file)}")
            print(df.shape)
            print('='*60)
            display(df.head())

            # Saving file to csv
            output_file = csv_dir/f"{file.stem}.csv"
            df.to_csv(output_file,index=False)
# %%
if __name__ == '__main__':
    print('---Loading Starts---')
    load_tables()
    print('---Loading Completed---')

# %%
