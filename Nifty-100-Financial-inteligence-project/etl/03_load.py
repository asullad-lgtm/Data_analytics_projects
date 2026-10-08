-- Active: 1784820165938@@127.0.0.1@5432@nifty_100_db
-- Active: 1784820165938@@127.0.0.1@5432@nifty_100_db@public
#%%
import pandas as pd
from sqlalchemy import create_engine,text,MetaData,Table
from pathlib import Path
import numpy as np
from sqlalchemy.dialects.postgresql import insert
# %%
base_dir = Path.cwd().parent
clean_dir = base_dir/'data'/'clean'
# %%
engine = create_engine("postgresql://postgres:sql123@localhost:5432/nifty_100_db")

with engine.connect() as conn:
    results = conn.execute(text('SELECT 1'))
    print('Connection successful!',results.fetchone)

# %%
def load_csv_to_sql_on_upsert(df,table,engine,conflict_key_name):
    
    records = df.to_dict(orient='records')
    table_name = Table(table,MetaData(),autoload_with=engine)
    conflict_keys = [table_name.c[key] for key in conflict_key_name]
    with engine.begin() as conn:
        for record in records:
            stmt = insert(table_name).values(**record)
            update_dict = {k:v for k,v in record.items() if k != conflict_key_name}
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements = conflict_keys,
                set_ = update_dict
            )
            conn.execute(upsert_stmt)
    print(f'Successfully upserted {len(df)} records in to {table} on unique target {conflict_key_name}')
# %%
# dimension data
companies = pd.read_csv(clean_dir/'clean_companies.csv')
sector_df = pd.read_csv(clean_dir/'sector_mapping.csv')
year_df = pd.read_csv(clean_dir/'clean_year.csv')
label_df = pd.read_csv(clean_dir/'clean_health_label.csv')
label = pd.read_csv(clean_dir/'clean_health_label.csv')

# Fact data
analysis = pd.read_csv(clean_dir/'clean_analysis.csv')
balancesheet = pd.read_csv(clean_dir/'clean_balancesheet.csv')
profitloss = pd.read_csv(clean_dir/'clean_profitloss.csv')
cashflow = pd.read_csv(clean_dir/'clean_cashflow.csv')
proscons = pd.read_csv(clean_dir/'clean_prosandcons.csv')
proscons = proscons.rename(columns = {'text':'text_name'})
ml_score = pd.read_csv(clean_dir/'clean_ml_score.csv')
ml_score.info()

# %%
def load_dim_tables():
    load_csv_to_sql_on_upsert(
        df = companies,
        table='dim_company',
        engine=engine,
        conflict_key_name=['symbol']
    )

    load_csv_to_sql_on_upsert(
        df = sector_df,
        table='dim_sector',
        engine=engine,
        conflict_key_name=['sector_id']
    )

    load_csv_to_sql_on_upsert(
        df = year_df,
        table='dim_year',
        engine=engine,
        conflict_key_name=['year_id']
    )

    load_csv_to_sql_on_upsert(
        df = label,
        table='dim_health_label',
        engine=engine,
        conflict_key_name=['label_id']
    )

# %%
def load_fact_tables():
    load_csv_to_sql_on_upsert(
        df = analysis,
        table='fact_analysis',
        engine = engine,
        conflict_key_name=['symbol','year']
    )

    load_csv_to_sql_on_upsert(
        df = balancesheet,
        table='fact_balancesheet',
        engine = engine,
        conflict_key_name=['symbol','year']
    )

    load_csv_to_sql_on_upsert(
        df = profitloss,
        table='fact_profitloss',
        engine = engine,
        conflict_key_name=['symbol','year']
    )

    load_csv_to_sql_on_upsert(
        df = cashflow,
        table='fact_cashflow',
        engine = engine,
        conflict_key_name=['symbol','year']
    )

    load_csv_to_sql_on_upsert(
        df = proscons,
        table='fact_proscons',
        engine = engine,
        conflict_key_name=['symbol']
    )
    
    load_csv_to_sql_on_upsert(
        df = ml_score,
        table='fact_ml_score',
        engine = engine,
        conflict_key_name=['symbol']
    )
# %%
if __name__ == '__main__':
    print('Loading Starts....')
    load_dim_tables()
    load_fact_tables()
    print('Loading Completed....!')
# %%
