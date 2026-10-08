#%%
import pandas as pd
import os
import re
import numpy as np
from pathlib import Path
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
# %%
Base_dir = Path.cwd().parent
csv_dir = Base_dir/'data'/'csv'
clean_dir = Base_dir/'data'/'clean'
clean_dir.mkdir(parents=True,exist_ok=True)

#%%
# Sector mapping
# =================================================
df = pd.read_csv(csv_dir/'companies.csv')

sector_dict = {}
mapping = {'LTIM':'technology','TATAMOTORS':'automobile'}

for symbol in df['id']:
    try:
        ticker = yf.Ticker(str(symbol)+'.NS')
        sector = ticker.info.get('sectorKey')
    except Exception:
        sector = None

    if sector is None:
        sector = mapping.get(symbol,'unknown')

    sector = sector.upper()

    sector_dict[symbol] = sector
    print(sector_dict)

#%%
# parsing datetime
# ================================================
today = datetime.now()

def parse_relative_date(text):

    text = text.strip().lower()

    if 'year' in text:
        num = [int(s) for s in text.split() if s.isdigit()]
        year_back = num[0] if num else 1
        target_date = today-relativedelta(years=year_back)

    elif 'TTM' in text:
        target_date = today-relativedelta(months=12)

    else:
        return text

    return target_date.strftime("%b%Y")


# %%
# ====================Companies=======================
def clean_companies():
    df = pd.read_csv(csv_dir/'companies.csv')
    df = df.rename(columns={'id':'symbol'})
    df['sector'] = df['symbol'].map(sector_dict)
    df = df[['symbol','company_name','face_value', 'book_value',
        'roce_percentage', 'roe_percentage', 'sector']]
    df = df.dropna()
    print(df.columns)
    print('='*60)
    print(f'Shape : {df.shape}')
    print('='*60)
    print(df.info())
    df.to_csv(clean_dir/'clean_companies.csv',index=False)
    display(df)

# %%
# ======================Analysis=======================
def clean_analysis():
    df = pd.read_csv(csv_dir/'analysis.csv')
    df = df.rename(columns={'company_id':'symbol'})
    df = df.melt(
        id_vars=['id','symbol'],
        var_name= 'metric',
        value_name='value')

    df['year'] = df['value'].str.extract(r'(\d+\s*Years?|TTM|Last Year)')
    df['percentage'] = df['value'].str.extract(r'(\d+)%')

    df = df.pivot_table(
        index=['symbol','year'],
        columns='metric',
        values='percentage',
        aggfunc='first'
    ).reset_index()
    df['year'] = df['year'].apply(parse_relative_date)
    df['year'].unique().value_counts()
    df['compounded_profit_growth'] = df['compounded_profit_growth'].astype('Int64')  
    df['compounded_sales_growth'] = df['compounded_sales_growth'].astype('Int64')  
    df['stock_price_cagr'] = df['stock_price_cagr'].astype('Int64')  
    df['roe'] = df['roe'].astype('Int64')  
    df = df.fillna(0)
    print(df.columns)
    print('='*60)
    print(f'Shape : {df.shape}')
    print('='*60)
    print(df.info())
    df.to_csv(clean_dir/'clean_analysis.csv',index=False)
    display(df)
# %%
# ==================Balancesheet====================
def clean_balancesheet():
    df = pd.read_csv(csv_dir/'balancesheet.csv')
    df['year'] = pd.to_datetime(df['year'],errors='coerce')
    df['year'] = df['year'].dt.strftime('%b%Y') 
    df = df.rename(columns={'company_id':'symbol'})
    df = df.drop(columns=['id'])
    
    # computed columns
    df['debt_to_equity'] = (df['borrowings']/
                            (df['equity_capital']+df['reserves'])).round(2)

    df['equity_ratio'] = ((df['equity_capital']+df['reserves'])/
                                df['total_assets'].replace(0,np.nan)).round(2)
    print(df.columns)
    print('='*60)
    print(f'Shape : {df.shape}')
    print('='*60)
    print(df.info())
    df.to_csv(clean_dir/'clean_balancesheet.csv',index=False)
    display(df)                               
# %%
# =================Cashflow====================
def clean_cashflow():
    df = pd.read_csv(csv_dir/'cashflow.csv')
    df['year'] = df['year'].str.replace(r'^([A-Za-z]{3})-(\d{2})$',r'\g<1>20\g<2>',regex=True)
    df['year'] = pd.to_datetime(df['year'],errors='coerce')
    df['year'] = df['year'].dt.strftime('%b%Y')
    df = df.sort_values(by='company_id',ascending=True)
    df = df.rename(columns={'company_id':'symbol'})
    df = df.drop(columns=['id'])
    df = df.dropna()
    
    # computed_column
    df['free_cash_flow'] = (df['operating_activity']+df['investing_activity']).round(2)
    
    print(df.columns)
    print('='*60)
    print(f'Shape : {df.shape}')
    print('='*60)
    print(df.info())
    df.to_csv(clean_dir/'clean_cashflow.csv',index=False)
    display(df)  

# %%
# ===================Profitloss=================
def clean_profitloss():
    df = pd.read_csv(csv_dir/'profitandloss.csv')
    df_ttm = df[df['year']=='TTM']
    df_historical = df[df['year'] != 'TTM']
    df_historical['year'] = pd.to_datetime(df_historical['year'],errors='coerce')
    df_historical['year'] = df_historical['year'].dt.strftime('%b%Y')
    df = pd.concat([df_ttm,df_historical],ignore_index=False)
    df = df.sort_values(by='company_id')
    df = df.rename(columns={'company_id':'symbol'})
    df = df.drop(columns=['id'])
    df = df.fillna(0)

    # computed_column
    df['net_profit_margin_pct'] = ((df['net_profit']/df['sales'])*100).round(2)
    df['expenses_ratio_pct'] = ((df['expenses']/df['sales'])*100).round(2)
    df['interest_coverage'] = (df['operating_profit']/df['interest'].replace(0,np.nan)).round(2)
    
    print(df.columns)
    print('='*60)
    print(f'Shape : {df.shape}')
    print('='*60)
    print(df.info())
    df.to_csv(clean_dir/'clean_profitloss.csv',index=False)
    display(df)
# %%
# ================ProsandCons===================
def clean_prosandcons():
    df = pd.read_csv(csv_dir/'prosandcons.csv')
    df = df.drop(columns='id')

    df = df.melt(
        id_vars='company_id',
        var_name='is_pro',
        value_name='text',
        value_vars=['pros','cons']
    )
    df = df.dropna(subset=['text'])
    df['text'] = df['text'].str.strip()
    df['is_pro']= df['is_pro']=='pros'
    df = df.rename(columns={'company_id':'symbol'})
    print(df.columns)
    print('='*60)
    print(f'Shape : {df.shape}')
    print('='*60)
    print(df.info())
    df.to_csv(clean_dir/'clean_prosandcons.csv',index=False)
    display(df)

#%%
Description = {'FINANCIAL-SERVICES':
            'Companies providing banking,asset management,investing,lending,insurance',
            'CONSUMER-CYCLICAL':
            'Comnapnies selling non-essential goods and services',
            'UTILITIES':
            'Companies providing essetial services like gas,electriity,water others',
            'INDUSTRIALS':
            'Companies involving manfacturing engineering,machinary,construction,transportation services',
            'BASIC-MATERIALS':
            'Companies involved manufacturing of raw materials,cements,metal parts',
            'CONSUMER-DEFENSIVE':
            'Companies involved in manufacturing of Defense products',
            'ENERGY':
            'Companies inolved in refining,Exploration,distrubution services',
            'HEALTHCARE':
            'Companies involved in pharmaceticals,medical equipment healthcare services',
            'TECHNOLOGY':
            'Companies developing IT and software services',
            'COMMUNICATION-SERVICES':
            'Companies providing telecommunication,internet services',
            'REAL-ESTATE':
            'Companies involved in construction,sales,lease management,devolopement of properties',
            'AUTOMOBILE':
            'Companies inolved in manufacturing,sales of automobile parts'}

# %%
# sector
def clean_sector():
    sector_df = pd.DataFrame(list(sector_dict.items()),columns=['symbol','sector'])
    sector_df['sector_id'] = sector_df.index
    sector_df['sector_code'] = sector_df['sector'].str[:3]
    sector_df['sector'] = sector_df['sector'].str.upper()
    sector_df['Description'] = sector_df['sector'].map(Description)
    sector_df = sector_df[['sector_id','sector_code','sector','Description']]
    sector_df.to_csv(clean_dir/'sector_mapping.csv',index=False)
    print(sector_df.columns)
    print('='*60)
    print(f'Shape : {sector_df.shape}')
    print('='*60)
    print(sector_df.info())
    display(sector_df)
# %%
def clean_year():
    years =[]
    files = list(clean_dir.glob("*.csv"))
    for file in files:
        df = pd.read_csv(file)
        if 'year' in df.columns:
            years.extend(df['year'].dropna().drop_duplicates().to_list())

    year_df = pd.DataFrame({'year_label':years})
    year_df = year_df[year_df['year_label'].str.strip().str.upper()!='TTM']
    year_df['month'] = pd.to_datetime(year_df['year_label'],errors='coerce').dt.month
    year_df['calender_year'] = pd.to_datetime(year_df['year_label'],errors='coerce').dt.year
    year_df['year_id'] = (year_df['calender_year']*100 + year_df['month']).astype(int)
    year_df['fiscal_year'] = (year_df['calender_year'] + (year_df['month'] !=3)).astype(int)

    quarter_map = {1:'Q4',2:'Q4',3:'Q4',
                4:'Q1',5:'Q1',6:'Q1',
                7:'Q2',8:'Q2',9:'Q2',
                10:'Q3',11:'Q3',12:'Q3'}
    year_df['quarter'] = year_df['month'].map(quarter_map)
    year_df['is_half_year'] = year_df['quarter'].isin(['Q2','Q4'])
    year_df = year_df[['year_id','year_label','fiscal_year','quarter','is_half_year']]
    year_df.to_csv(clean_dir/'clean_year.csv',index=False)
    print(year_df.columns)
    print('='*60)
    print(f'Shape : {year_df.shape}')
    print('='*60)
    print(year_df.info())
    display(year_df)

# %%
def clean_health_label():
    label_df = pd.DataFrame({
        'label_id':[1,2,3,4,5],
        'label_name':['EXCELLENT','GOOD','AVERAGE','WEAK','POOR'],
        'min_marks':[80,65,50,35,0],
        'max_marks':[100,79.99,64.99,49.99,34.99],
        'color_hex':['#008000','#70AD47','#FFC000','#ED7D31','#C00000']
    })
    label_df = label_df.set_index('label_id')
    label_df.to_csv(clean_dir/'clean_health_label.csv',index=False)
    print(label_df.columns)
    print('='*60)
    print(f'Shape : {label_df.shape}')
    print('='*60)
    print(label_df.info())
    display(label_df)
# %%
companies = pd.read_csv(clean_dir/'clean_companies.csv')
profitloss = pd.read_csv(clean_dir/'clean_profitloss.csv')
balancesheet = pd.read_csv(clean_dir/'clean_balancesheet.csv')
cashflow = pd.read_csv(clean_dir/'clean_cashflow.csv')
# %%
df = balancesheet.merge(
    companies,
    on = ['symbol'],
    how = 'left'
)
df['shares_outstanding'] = (df['equity_capital']/df['face_value'].replace(0,np.nan)).round(2)
df['book_value_per_share'] = ((df['equity_capital']+df['reserves'])/df['shares_outstanding'].replace(0,np.nan)).round(2)
# %%
def computed_metrics():
    df = profitloss.merge(
        balancesheet,
        on=['symbol','year'],
        how = 'inner'
    )
    df = df.merge(
        cashflow,
        on=['symbol','year'],
        how = 'inner'
    )

    # metrics to score conversion
    df['cash_conversion_ratio'] = (df['operating_activity']/df['net_profit'].replace(0,np.nan)).round(2)
    df['asset_turnover'] = (df['sales']/df['total_assets'].replace(0,np.nan)).round(2)
    df['return_on_asset'] = ((df['net_profit']/df['total_assets'].replace(0,np.nan))*100).round(2)
    df['profitability_score'] = (df['net_profit_margin_pct'].rank(pct=True)*100*0.5+df['return_on_asset'].rank(pct=True)*100*0.5).round(2)
    df['leverage_score'] = ((1-df['debt_to_equity'].rank(pct=True))*100).round(2)
    df['cash_flow_score'] = (df['cash_conversion_ratio'].rank(pct=True)*100).round(2)
    df['sales_growth'] = (df.groupby('symbol')['sales'].pct_change()*100).round(2)
    df['profit_growth'] = (df.groupby('symbol')['net_profit'].pct_change()*100).round(2)
    df['growth_score'] = (df['sales_growth'].rank(pct=True)*100*0.5 +
                        df['profit_growth'].rank(pct=True)*100*0.5).round(2)
    df['dividend_score'] = (df['dividend_payout'].rank(pct=True)*100).round(2)
    df['trend_score'] = (df['profit_growth'].rank(pct=True)*100).round(2)
    df['overall_score'] = (
        df['profitability_score']*0.25
        + df['growth_score']*0.20
        + df['leverage_score']*0.15
        + df['cash_flow_score']*0.15
        + df['dividend_score']*0.10
        + df['trend_score']*0.15
    ).round(2)


    def health_label(score):
        if score >= 80:
            return 'EXCELLENT' 
        elif score >= 65:
            return 'GOOD' 
        elif score >= 50:
            return 'AVERAGE' 
        elif score >= 35:
            return 'WEAK' 
        else:
            return 'POOR'

    df['health_label'] = df['overall_score'].apply(health_label)
    df['computed_time'] = datetime.now() 


    fact_ml_score = df[[
        'symbol','computed_time','overall_score','profitability_score',
        'growth_score','leverage_score','cash_flow_score','dividend_score','trend_score','health_label']]

    fact_ml_score = fact_ml_score.fillna(0)
    fact_ml_score.to_csv(clean_dir/'clean_ml_score.csv',index=False)
# %%

if __name__ == '__main__':
    print('cleaning starts...........')
    clean_companies()
    clean_analysis()
    clean_balancesheet()
    clean_profitloss()
    clean_cashflow()
    clean_prosandcons()
    clean_sector()
    clean_year()
    clean_health_label()
    computed_metrics()
    print('cleaning completed !')
# %%
