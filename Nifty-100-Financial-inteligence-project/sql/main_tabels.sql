-- dim tables

-- Companies
CREATE TABLE dim_company(
    symbol VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255),
    face_value NUMERIC,
    book_value NUMERIC,
    roce_percentage NUMERIC,
    roe_percentage NUMERIC,
    sector VARCHAR(50)
);

-- sector
CREATE TABLE dim_sector(
    sector_id NUMERIC PRIMARY KEY,
    sector_code VARCHAR(20),
    sector VARCHAR(255),
    Description_name TEXT
);

-- Year
CREATE TABLE dim_year(
    year_id NUMERIC PRIMARY KEY,
    year_label TEXT,
    fiscal_year NUMERIC,
    quarter TEXT,
    is_half_year BOOLEAN
);

-- Health_label
CREATE TABLE dim_health_label(
    label_id NUMERIC PRIMARY KEY,
    label_name TEXT,
    min_marks NUMERIC,
    max_marks FLOAT,
    color_hex TEXT
)


-- Fact tables

-- Analysis
CREATE TABLE fact_analysis(
    symbol VARCHAR(50),
    year VARCHAR(50),
    compounded_profit_growth NUMERIC,
    compounded_sales_growth NUMERIC,
    roe NUMERIC,
    stock_price_cagr NUMERIC,
    PRIMARY KEY(symbol,year)
);

-- Balancesheet
CREATE TABLE fact_balancesheet(
    symbol VARCHAR(50),
    year VARCHAR(50),
    equity_capital FLOAT,
    reserves NUMERIC,
    borrowings NUMERIC,
    other_liabilities NUMERIC,
    total_liabilities NUMERIC,
    fixed_assets NUMERIC,
    cwip NUMERIC,
    investments NUMERIC,
    other_asset NUMERIC,
    total_assets NUMERIC,
    debt_to_equity FLOAT,
    equity_ratio FLOAT,
    PRIMARY KEY(symbol,year)
);

-- Profitloss
CREATE TABLE fact_profitloss(
    symbol VARCHAR(50),
    year VARCHAR(50),
    sales NUMERIC,
    expenses NUMERIC,
    operating_profit FLOAT,
    opm_percentage FLOAT,
    other_income NUMERIC,
    interest NUMERIC,
    depreciation NUMERIC,
    profit_before_tax NUMERIC,
    tax_percentage FLOAT,
    net_profit NUMERIC,
    eps FLOAT,
    dividend_payout FLOAT,
    net_profit_margin_pct FLOAT,
    expenses_ratio_pct FLOAT,
    interest_coverage FLOAT,
    PRIMARY KEY(symbol,year)
);

-- Cashflow
CREATE TABLE fact_cashflow(
    symbol VARCHAR(50),
    year VARCHAR(50),
    operating_activity FLOAT,
    investing_activity FLOAT,
    financing_activity FLOAT,
    net_cash_flow FLOAT,
    free_cash_flow FLOAT,
    PRIMARY KEY(symbol,year)
);

-- ProsandCons
CREATE TABLE fact_proscons(
    symbol VARCHAR(50) PRIMARY KEY,
    is_pro BOOLEAN,
    text_name TEXT
);

-- Ml score
CREATE TABLE fact_ml_score(
    symbol VARCHAR(50) PRIMARY KEY,
    computed_time VARCHAR(50),
    overall_score FLOAT,
    profitability_score FLOAT,
    growth_score FLOAT,
    leverage_score FLOAT,
    cash_flow_score FLOAT,
    dividend_score FLOAT,
    trend_score FLOAT,
    health_label TEXT
);
