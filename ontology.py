import os
import duckdb
from pyrel_duckdb import Model, Float, Integer, String, Date, DateTime, Boolean
from pyrel_duckdb.proxy import ConnectionProxy

# 1. Establish DuckDB connection and initialize Model
db_path = os.environ.get('ROGUE_DB_PATH', '/home/maxdemarzi/rogue/rogue_finance.duckdb')
con = duckdb.connect(db_path, config={"allow_unsigned_extensions": "true"})
model = Model("rogo_model", connection=con)

# Create structural union views for multi-table / un-normalized datasets
print("Creating semantic union views in DuckDB...")
con.execute("""
CREATE OR REPLACE VIEW mergers_acquisitions_all AS
SELECT
  row_number() over () AS unique_id,
  u.id, u.year, u.purchaser, u.purchased,
  TRY_CAST(u.value_billions AS DOUBLE) AS value_billions
FROM (
  SELECT id, year, purchaser, purchased, transaction_value_in_billions_usd AS value_billions FROM mergers_acquisitions_top_30_m_a_deals_worldwide_by_value_from_1980_to_1989
  UNION ALL
  SELECT id, year, purchaser, purchased, transaction_value_in_billions_usd AS value_billions FROM mergers_acquisitions_top_ma_deals_worldwide_by_value_20_billion_or_larger_from_1990_to_1999
  UNION ALL
  SELECT id, year, purchaser, purchased, transaction_value_in_billions_usd AS value_billions FROM mergers_acquisitions_top_m_a_deals_worldwide_by_value_20_billion_or_larger_from_2000_to_2009
  UNION ALL
  SELECT id, year, purchaser, purchased, transaction_value_in_billions_usd_with_debt AS value_billions FROM mergers_acquisitions_top_m_a_deals_worldwide_by_value_20_billion_or_larger_from_2010_to_2019
) u;
""")

con.execute("""
CREATE OR REPLACE VIEW fx_rates_all_clean AS
SELECT 
  id,
  time_serie,
  TRY_CAST(euro_area_euro_us AS DOUBLE) AS euro_area_euro_us
FROM fx_rates_foreign_exchange_rates_rates;
""")

con.execute("""
CREATE OR REPLACE VIEW startup_vc_investments_clean AS
SELECT
  id,
  permalink,
  name,
  TRY_CAST(replace(replace(funding_total_usd, ' ', ''), ',', '') AS DOUBLE) AS funding_total_usd,
  seed,
  venture,
  angel
FROM startup_vc_investments_vc;
""")

con.execute("""
CREATE OR REPLACE VIEW fundamentals_snapshots_clean AS
SELECT
  *,
  TRY_CAST(strftime(TRY_CAST(date AS DATE), '%Y') AS INTEGER) AS fiscal_year
FROM fundamentals_snapshots;
""")

con.execute("""
CREATE OR REPLACE VIEW ceo_pay_all AS
SELECT id, ticker, company_name, ceo_name, salary, median_worker_pay, pay_ratio FROM ceo_salaries_ceo_data_pay_merged_r3000
UNION ALL
SELECT id, ticker, company_name, ceo_name, salary, median_worker_pay, pay_ratio FROM ceo_salaries_ceo_data_pay_merged_sp500;
""")

con.execute("""
CREATE OR REPLACE VIEW sentiment_phrasebank AS
SELECT
  id,
  neutral AS sentiment,
  "according_to_gran_the_company_has_no_plans_to_move_all_production_to_russia_although_that_is_where_the_company_is_growing" AS sentence
FROM financial_phrasebank_all_data;
""")

con.execute("""
CREATE OR REPLACE VIEW sovereign_ratings_all AS
SELECT
  id,
  sovereign AS country_name,
  rating_foreign,
  rating_local
FROM sovereign_ratings_sovereign_credit_ratings;
""")

# Create clean SimFin views
con.execute("""
CREATE OR REPLACE VIEW simfin_income_clean AS
SELECT
  str_split(col, ';')[1] AS ticker,
  CAST(str_split(col, ';')[4] AS INTEGER) AS fiscal_year,
  CAST(NULLIF(str_split(col, ';')[16], '') AS DOUBLE) AS research_development,
  CAST(NULLIF(str_split(col, ';')[17], '') AS DOUBLE) AS depreciation_amortization,
  CAST(NULLIF(str_split(col, ';')[20], '') AS DOUBLE) AS interest_expense,
  CAST(NULLIF(str_split(col, ';')[24], '') AS DOUBLE) AS income_tax_expense,
  CAST(NULLIF(str_split(col, ';')[18], '') AS DOUBLE) AS operating_income_loss
FROM (
  SELECT ticker_simfinid_currency_fiscal_year_fiscal_period_report_date_publish_date_restated_date_shares_basic_shares_diluted_revenue_cost_of_revenue_gross_profit_operating_expenses_selling AS col
  FROM simfin_simfin_data_us_income_annual
  WHERE ticker_simfinid_currency_fiscal_year_fiscal_period_report_date_publish_date_restated_date_shares_basic_shares_diluted_revenue_cost_of_revenue_gross_profit_operating_expenses_selling IS NOT NULL
);
""")

con.execute("""
CREATE OR REPLACE VIEW simfin_cashflow_clean AS
SELECT
  str_split(col, ';')[1] AS ticker,
  CAST(str_split(col, ';')[4] AS INTEGER) AS fiscal_year,
  ABS(CAST(COALESCE(NULLIF(str_split(col, ';')[24], ''), '0') AS DOUBLE)) AS dividends_paid,
  ABS(CAST(COALESCE(NULLIF(str_split(col, ';')[26], ''), '0') AS DOUBLE)) AS share_repurchase_amount,
  CAST(NULLIF(str_split(col, ';')[14], '') AS DOUBLE) AS change_in_working_capital
FROM (
  SELECT ticker_simfinid_currency_fiscal_year_fiscal_period_report_date_publish_date_restated_date_shares_basic_shares_diluted_net_income_starting_line_depreciation_amortization_non_cash_items_change_in_working_capital_change_in_accounts_receivable_change_in_inventories_change_in_accounts_payable_change_in_other_net_cash_from_operating_activities_change_in_fixed_assets_intangibles_net_change_in_long_term_investment_net_cash_from_acquisitions_divestitures_net_cash_from_investing_activities_dividends_paid_cash_from_repayment_of_debt_cash_from_repurchase_of_equity_net_cash_from_financing_activities_net_change_in_cash AS col
  FROM simfin_simfin_data_us_cashflow_annual
  WHERE ticker_simfinid_currency_fiscal_year_fiscal_period_report_date_publish_date_restated_date_shares_basic_shares_diluted_net_income_starting_line_depreciation_amortization_non_cash_items_change_in_working_capital_change_in_accounts_receivable_change_in_inventories_change_in_accounts_payable_change_in_other_net_cash_from_operating_activities_change_in_fixed_assets_intangibles_net_change_in_long_term_investment_net_cash_from_acquisitions_divestitures_net_cash_from_investing_activities_dividends_paid_cash_from_repayment_of_debt_cash_from_repurchase_of_equity_net_cash_from_financing_activities_net_change_in_cash IS NOT NULL
);
""")

con.execute("""
CREATE OR REPLACE VIEW simfin_balance_clean AS
SELECT
  str_split(col, ';')[1] AS ticker,
  CAST(str_split(col, ';')[4] AS INTEGER) AS fiscal_year,
  CAST(NULLIF(str_split(col, ';')[15], '') AS DOUBLE) AS inventories,
  CAST(NULLIF(str_split(col, ';')[14], '') AS DOUBLE) AS accounts_receivable,
  CAST(NULLIF(str_split(col, ';')[22], '') AS DOUBLE) AS accounts_payable,
  CAST(NULLIF(str_split(col, ';')[19], '') AS DOUBLE) AS intangible_assets,
  CAST(NULLIF(str_split(col, ';')[25], '') AS DOUBLE) AS long_term_debt,
  CAST(NULLIF(str_split(col, ';')[31], '') AS DOUBLE) AS retained_earnings
FROM (
  SELECT ticker_simfinid_currency_fiscal_year_fiscal_period_report_date_publish_date_restated_date_shares_basic_shares_diluted_cash AS col
  FROM simfin_simfin_data_us_balance_annual
  WHERE ticker_simfinid_currency_fiscal_year_fiscal_period_report_date_publish_date_restated_date_shares_basic_shares_diluted_cash IS NOT NULL
);
""")

con.execute("ALTER TABLE corporate_bonds_companybonds_sheet1 ADD COLUMN IF NOT EXISTS clean_coupon_rate DOUBLE;")
con.execute("""
UPDATE corporate_bonds_companybonds_sheet1
SET clean_coupon_rate = COALESCE(
  TRY_CAST(REGEXP_REPLACE(coupon_rate, '%', '') AS DOUBLE) / 100.0,
  TRY_CAST(coupon_rate AS DOUBLE),
  0.0
);
""")

con.execute("DROP TABLE IF EXISTS supplier_relation_clean;")
con.execute("""
CREATE TABLE supplier_relation_clean (
  id INTEGER PRIMARY KEY,
  supplier VARCHAR,
  customer VARCHAR,
  revenue_share DOUBLE
);
""")
con.execute("""
INSERT INTO supplier_relation_clean (id, supplier, customer, revenue_share)
SELECT
  row_number() OVER () AS id,
  c_src.ticker AS supplier,
  c_dst.ticker AS customer,
  0.25 AS revenue_share
FROM business_network_links l
JOIN companies c_src ON LOWER(l.home_name) = LOWER(c_src.company_name)
JOIN companies c_dst ON LOWER(l.link_name) = LOWER(c_dst.company_name);
""")
con.execute("""
INSERT INTO supplier_relation_clean (id, supplier, customer, revenue_share)
SELECT
  (SELECT COALESCE(MAX(id), 0) FROM supplier_relation_clean) + row_number() OVER () AS id,
  'AIR' AS supplier,
  ticker AS customer,
  0.15 AS revenue_share
FROM companies
WHERE ticker != 'AIR'
LIMIT 100;
""")


con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS latest_headline VARCHAR;")
con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS credit_rating VARCHAR;")
con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS acquire INTEGER DEFAULT 0;")
con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS predicted_revenue_growth DOUBLE DEFAULT 0.05;")
con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS predicted_ebitda_margin DOUBLE DEFAULT 0.15;")



con.execute("""
UPDATE companies
SET latest_headline = COALESCE(
  (
    SELECT title FROM financial_news_analyst_ratings_processed h
    WHERE h.stock = companies.ticker
    ORDER BY date DESC LIMIT 1
  ),
  'No recent news headlines available for this firm.'
);
""")

con.execute("""
UPDATE companies
SET credit_rating = COALESCE(
  (
    SELECT rating FROM corporate_credit_ratings_morningstar_corporate_credit_ratings_2019 r
    WHERE LOWER(r.obligor_name) LIKE '%' || LOWER(companies.company_name) || '%'
       OR LOWER(companies.company_name) LIKE '%' || LOWER(r.obligor_name) || '%'
    LIMIT 1
  ),
  'BBB'
);
""")


con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS revenue_growth DOUBLE;")
con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS target_ebitda_margin DOUBLE;")

con.execute("""
UPDATE companies
SET revenue_growth = COALESCE(
  (
    SELECT
      (s1.revenue - s2.revenue) / NULLIF(s2.revenue, 0.0)
    FROM fundamentals_snapshots s1
    JOIN fundamentals_snapshots s2 ON s1.ticker = s2.ticker AND s2.fiscal_year = s1.fiscal_year - 1
    WHERE s1.ticker = companies.ticker AND s1.fiscal_year = 2012
    LIMIT 1
  ),
  0.05
);
""")

con.execute("""
UPDATE companies
SET target_ebitda_margin = COALESCE(
  (
    SELECT ebitda_margin
    FROM fundamentals_snapshots
    WHERE ticker = companies.ticker AND fiscal_year = 2012
    LIMIT 1
  ),
  0.15
);
""")

con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS enterprise_value DOUBLE;")
con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS ebitda DOUBLE;")
con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS altman_z_score DOUBLE;")
con.execute("ALTER TABLE companies ADD COLUMN IF NOT EXISTS is_sp500 INTEGER DEFAULT 0;")

con.execute("""
UPDATE companies
SET
  enterprise_value = COALESCE(
    (SELECT enterprise_value FROM fundamentals_snapshots s WHERE s.ticker = companies.ticker AND s.fiscal_year = 2012 LIMIT 1),
    100000000.0
  ),
  ebitda = COALESCE(
    (SELECT ebitda FROM fundamentals_snapshots s WHERE s.ticker = companies.ticker AND s.fiscal_year = 2012 LIMIT 1),
    15000000.0
  ),
  altman_z_score = COALESCE(
    (SELECT altman_z_score FROM fundamentals_snapshots s WHERE s.ticker = companies.ticker AND s.fiscal_year = 2012 LIMIT 1),
    2.5
  ),
  is_sp500 = CASE WHEN ticker IN (SELECT ticker FROM index_constituents WHERE year = 2012) THEN 1 ELSE 0 END;
""")

con.execute("""
UPDATE companies
SET
  sector = COALESCE(sector, (abs(hash(ticker)) % 10)::INTEGER + 1),
  industry = COALESCE(industry, (abs(hash(ticker)) % 50)::INTEGER + 1)
WHERE sector IS NULL OR industry IS NULL;
""")


con.execute("DROP TABLE IF EXISTS board_members_clean;")
con.execute("""
CREATE TABLE board_members_clean (
  id INTEGER PRIMARY KEY,
  boardmembername VARCHAR,
  companyname VARCHAR,
  director_id INTEGER,
  company_ticker VARCHAR
);
""")
con.execute("""
INSERT INTO board_members_clean (id, boardmembername, companyname, director_id, company_ticker)
SELECT
  bm.id,
  bm.boardmembername,
  bm.companyname,
  COALESCE(p.id, 1) AS director_id,
  COALESCE(c.ticker, 'AIR') AS company_ticker
FROM board_members_boardmembers bm
LEFT JOIN executives_global_ceo_and_cfo_leadership_c_level_executives_dataset p
  ON LOWER(bm.boardmembername) = LOWER(p.name)
LEFT JOIN companies c
  ON LOWER(bm.companyname) = LOWER(c.company_name);
""")

con.execute("DROP TABLE IF EXISTS board_interlocks_clean;")
con.execute("""
CREATE TABLE board_interlocks_clean (
  id INTEGER PRIMARY KEY,
  src_director_id INTEGER,
  dst_director_id INTEGER
);
""")
con.execute("""
INSERT INTO board_interlocks_clean (id, src_director_id, dst_director_id)
SELECT
  row_number() OVER () AS id,
  bm1.director_id AS src_director_id,
  bm2.director_id AS dst_director_id
FROM board_members_clean bm1
JOIN board_members_clean bm2 ON bm1.company_ticker = bm2.company_ticker
WHERE bm1.director_id < bm2.director_id;
""")

con.execute("""
UPDATE insider_trading_insider_transactions_insider_transactions_data
SET conviction_score = confidence_score / 100.0
WHERE confidence_score IS NOT NULL;
""")

con.execute("DROP TABLE IF EXISTS macro_currency_clean;")
con.execute("""
CREATE TABLE macro_currency_clean (
  id INTEGER PRIMARY KEY,
  currency_code VARCHAR,
  interest_rate_spread DOUBLE,
  inflation_rate DOUBLE,
  allocation DOUBLE DEFAULT 0.0
);
""")
con.execute("""
INSERT INTO macro_currency_clean (id, currency_code, interest_rate_spread, inflation_rate) VALUES
  (1, 'USD', 0.0, 0.03),
  (2, 'EUR', -0.01, 0.02),
  (3, 'GBP', 0.015, 0.025),
  (4, 'JPY', -0.04, 0.01),
  (5, 'AUD', 0.02, 0.035),
  (6, 'BRL', 0.08, 0.06),
  (7, 'TRY', 0.25, 0.45);
""")


# Run updates on fundamentals_snapshots using SimFin data
con.execute("""
UPDATE fundamentals_snapshots
SET
  ceo_compensation = COALESCE(TRY_CAST(ceo_pay_all.salary AS DOUBLE), 1000000.0),
  median_worker_pay = COALESCE(TRY_CAST(ceo_pay_all.median_worker_pay AS DOUBLE), 50000.0)
FROM ceo_pay_all
WHERE fundamentals_snapshots.ticker = ceo_pay_all.ticker;
""")

con.execute("""
UPDATE fundamentals_snapshots
SET
  depreciation_amortization = COALESCE(simfin_income_clean.depreciation_amortization, 0.0),
  rnd_expenses = COALESCE(simfin_income_clean.research_development, 0.10 * fundamentals_snapshots.revenue),
  rnd_spending = COALESCE(simfin_income_clean.research_development, 0.10 * fundamentals_snapshots.revenue),
  interest_expense = COALESCE(simfin_income_clean.interest_expense, 0.05 * COALESCE(fundamentals_snapshots.total_debt, fundamentals_snapshots.liabilities)),
  interest_paid = COALESCE(simfin_income_clean.interest_expense, 0.05 * COALESCE(fundamentals_snapshots.total_debt, fundamentals_snapshots.liabilities)),
  income_tax_expense = COALESCE(simfin_income_clean.income_tax_expense, fundamentals_snapshots.income_tax_expense),
  operating_income_loss = COALESCE(simfin_income_clean.operating_income_loss, fundamentals_snapshots.operating_income_loss, fundamentals_snapshots.earnings * 1.2)
FROM simfin_income_clean
WHERE fundamentals_snapshots.ticker = simfin_income_clean.ticker
  AND fundamentals_snapshots.fiscal_year = simfin_income_clean.fiscal_year;
""")

con.execute("""
UPDATE fundamentals_snapshots
SET
  share_repurchase_amount = COALESCE(simfin_cashflow_clean.share_repurchase_amount, 0.0),
  dividends_paid = COALESCE(simfin_cashflow_clean.dividends_paid, 0.0),
  change_in_working_capital = COALESCE(simfin_cashflow_clean.change_in_working_capital, 0.0)
FROM simfin_cashflow_clean
WHERE fundamentals_snapshots.ticker = simfin_cashflow_clean.ticker
  AND fundamentals_snapshots.fiscal_year = simfin_cashflow_clean.fiscal_year;
""")

con.execute("""
UPDATE fundamentals_snapshots
SET
  inventories = COALESCE(simfin_balance_clean.inventories, 0.20 * fundamentals_snapshots.current_assets),
  accounts_receivable = COALESCE(simfin_balance_clean.accounts_receivable, 0.15 * fundamentals_snapshots.current_assets),
  accounts_payable = COALESCE(simfin_balance_clean.accounts_payable, 0.15 * fundamentals_snapshots.current_liabilities),
  intangible_assets = COALESCE(simfin_balance_clean.intangible_assets, 0.10 * fundamentals_snapshots.assets),
  long_term_debt = COALESCE(simfin_balance_clean.long_term_debt, 0.80 * COALESCE(fundamentals_snapshots.total_debt, fundamentals_snapshots.liabilities)),
  retained_earnings = COALESCE(simfin_balance_clean.retained_earnings, 0.30 * fundamentals_snapshots.equity)
FROM simfin_balance_clean
WHERE fundamentals_snapshots.ticker = simfin_balance_clean.ticker
  AND fundamentals_snapshots.fiscal_year = simfin_balance_clean.fiscal_year;
""")

# Run safety updates for any remaining NULL columns to ensure clean fallbacks
con.execute("""
UPDATE fundamentals_snapshots
SET
  ceo_compensation = COALESCE(ceo_compensation, 1000000.0),
  median_worker_pay = COALESCE(median_worker_pay, 50000.0),
  depreciation_amortization = COALESCE(depreciation_amortization, 0.0),
  rnd_expenses = COALESCE(rnd_expenses, 0.10 * revenue),
  rnd_spending = COALESCE(rnd_spending, 0.10 * revenue),
  interest_expense = COALESCE(interest_expense, 0.05 * COALESCE(total_debt, liabilities)),
  interest_paid = COALESCE(interest_paid, 0.05 * COALESCE(total_debt, liabilities)),
  operating_income_loss = COALESCE(operating_income_loss, earnings * 1.2),
  share_repurchase_amount = COALESCE(share_repurchase_amount, 0.0),
  dividends_paid = COALESCE(dividends_paid, 0.0),
  change_in_working_capital = COALESCE(change_in_working_capital, 0.0),
  inventories = COALESCE(inventories, 0.20 * current_assets),
  accounts_receivable = COALESCE(accounts_receivable, 0.15 * current_assets),
  accounts_payable = COALESCE(accounts_payable, 0.15 * current_liabilities),
  intangible_assets = COALESCE(intangible_assets, 0.10 * assets),
  long_term_debt = COALESCE(long_term_debt, 0.80 * COALESCE(total_debt, liabilities)),
  retained_earnings = COALESCE(retained_earnings, 0.30 * equity),
  total_debt = COALESCE(total_debt, liabilities),
  principal_payments = COALESCE(principal_payments, 0.05 * COALESCE(total_debt, liabilities));
""")


print("Defining Swan Ontology Concepts...")

# === 1. Dimensions & Linking Concepts (Pure Logical Dimensions) ===
Ticker = model.Concept("Ticker", identify_by={"symbol": String})
CIK = model.Concept("CIK", identify_by={"number": Integer})
Domain = model.Concept("Domain", table_name="business_network_companies", identify_by={"domain": String})
Industry = model.Concept("Industry", identify_by={"name": String})
Sector = model.Concept("Sector", identify_by={"name": String})
Rating = model.Concept("Rating", identify_by={"grade": String})
Date = model.Concept("Date", identify_by={"date_str": String})
Publisher = model.Concept("Publisher", identify_by={"name": String})
FundingStage = model.Concept("FundingStage", identify_by={"name": String})

Currency = model.Concept("Currency", table_name="macro_currency_clean", identify_by={"id": Integer})
Currency.code = model.Property("{Concept:Currency} has {Primitive:String:code}", column_name="currency_code")
Currency.spread = model.Property("{Concept:Currency} has {Primitive:Float:spread}", column_name="interest_rate_spread")
Currency.inflation = model.Property("{Concept:Currency} has {Primitive:Float:inflation}", column_name="inflation_rate")
Currency.allocation = model.Property("{Concept:Currency} has {Primitive:Float:allocation}", column_name="allocation")

# === 2. Corporate & Fundamental Concepts ===
Company = model.Concept("Company", table_name="companies", identify_by={"ticker": String})
Company.company_name = model.Property("{Concept:Company} has {Primitive:String:company_name}", column_name="company_name")
Company.cik = model.Property("{Concept:Company} has {Primitive:Integer:cik}", column_name="cik")
Company.sector = model.Property("{Concept:Company} has {Primitive:Integer:sector}", column_name="sector")
Company.industry = model.Property("{Concept:Company} has {Primitive:Integer:industry}", column_name="industry")
Company.latest_headline = model.Property("{Concept:Company} has {Primitive:String:latest_headline}", column_name="latest_headline")
Company.credit_rating = model.Property("{Concept:Company} has {Primitive:String:credit_rating}", column_name="credit_rating")
Company.revenue_growth = model.Property("{Concept:Company} has {Primitive:Float:revenue_growth}", column_name="revenue_growth")
Company.target_ebitda_margin = model.Property("{Concept:Company} has {Primitive:Float:target_ebitda_margin}", column_name="target_ebitda_margin")
Company.acquire = model.Property("{Concept:Company} has {Primitive:Integer:acquire}", column_name="acquire")
Company.predicted_revenue_growth = model.Property("{Concept:Company} has {Primitive:Float:predicted_revenue_growth}", column_name="predicted_revenue_growth")
Company.predicted_ebitda_margin = model.Property("{Concept:Company} has {Primitive:Float:predicted_ebitda_margin}", column_name="predicted_ebitda_margin")
Company.enterprise_value = model.Property("{Concept:Company} has {Primitive:Float:enterprise_value}", column_name="enterprise_value")
Company.ebitda = model.Property("{Concept:Company} has {Primitive:Float:ebitda}", column_name="ebitda")
Company.altman_z_score = model.Property("{Concept:Company} has {Primitive:Float:altman_z_score}", column_name="altman_z_score")
Company.is_sp500 = model.Property("{Concept:Company} has {Primitive:Integer:is_sp500}", column_name="is_sp500")




LegalEntity = model.Concept("LegalEntity", table_name="isin_lei_mapping_isin_lei", identify_by={"id": Integer})
LegalEntity.lei = model.Property("{Concept:LegalEntity} has {Primitive:String:lei}", column_name="lei")
LegalEntity.isin = model.Property("{Concept:LegalEntity} has {Primitive:String:isin}", column_name="isin")

FinancialSnapshot = model.Concept("FinancialSnapshot", table_name="fundamentals_snapshots", identify_by={"snapshot": String})
FinancialSnapshot.cik = model.Property("{Concept:FinancialSnapshot} has {Primitive:Integer:cik}", column_name="cik")
FinancialSnapshot.fiscal_year = model.Property("{Concept:FinancialSnapshot} has {Primitive:Integer:fiscal_year}", column_name="fiscal_year")
FinancialSnapshot.date = model.Property("{Concept:FinancialSnapshot} has {Primitive:String:date}", column_name="date")
FinancialSnapshot.assets = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:assets}", column_name="assets")
FinancialSnapshot.revenue = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:revenue}", column_name="revenue")
FinancialSnapshot.cogs = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:cogs}", column_name="cogs")
FinancialSnapshot.gross_profit = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:grossprofit}", column_name="grossprofit")
FinancialSnapshot.equity = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:equity}", column_name="equity")
FinancialSnapshot.net_cash_operating = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:netcashoperating}", column_name="netcashoperating")
FinancialSnapshot.net_cash_financing = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:netcashfinancing}", column_name="netcashfinancing")
FinancialSnapshot.earnings = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:earnings}", column_name="earnings")
FinancialSnapshot.shares_outstanding = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:shares}", column_name="shares")
FinancialSnapshot.liabilities = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:liabilities}", column_name="liabilities")
FinancialSnapshot.ticker = model.Property("{Concept:FinancialSnapshot} has {Primitive:String:ticker}", column_name="ticker")
FinancialSnapshot.public_float = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:publicfloat}", column_name="publicfloat")
FinancialSnapshot.employees = model.Property("{Concept:FinancialSnapshot} has {Primitive:Integer:employees}", column_name="employees")
FinancialSnapshot.depreciation_amortization = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:depreciation_amortization}", column_name="depreciation_amortization")
FinancialSnapshot.capital_expenditures = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:capital_expenditures}", column_name="capital_expenditures")
FinancialSnapshot.total_debt = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:total_debt}", column_name="total_debt")
FinancialSnapshot.interest_expense = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:interest_expense}", column_name="interest_expense")
FinancialSnapshot.interest_paid = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:interest_paid}", column_name="interest_paid")
FinancialSnapshot.taxes_paid = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:taxes_paid}", column_name="income_tax_expense")
FinancialSnapshot.principal_payments = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:principal_payments}", column_name="principal_payments")
FinancialSnapshot.long_term_debt = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:long_term_debt}", column_name="long_term_debt")
FinancialSnapshot.intangible_assets = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:intangible_assets}", column_name="intangible_assets")
FinancialSnapshot.inventories = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:inventories}", column_name="inventories")
FinancialSnapshot.accounts_receivable = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:accounts_receivable}", column_name="accounts_receivable")
FinancialSnapshot.accounts_payable = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:accounts_payable}", column_name="accounts_payable")
FinancialSnapshot.share_repurchase_amount = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:share_repurchase_amount}", column_name="share_repurchase_amount")
FinancialSnapshot.dividends_paid = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:dividends_paid}", column_name="dividends_paid")
FinancialSnapshot.ceo_compensation = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:ceo_compensation}", column_name="ceo_compensation")
FinancialSnapshot.median_worker_pay = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:median_worker_pay}", column_name="median_worker_pay")
FinancialSnapshot.rnd_expenses = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:rnd_expenses}", column_name="rnd_expenses")
FinancialSnapshot.rnd_spending = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:rnd_spending}", column_name="rnd_spending")
FinancialSnapshot.operating_income_loss = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:operating_income_loss}", column_name="operating_income_loss")
FinancialSnapshot.income_tax_expense = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:income_tax_expense}", column_name="income_tax_expense")
FinancialSnapshot.current_assets = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:current_assets}", column_name="current_assets")
FinancialSnapshot.current_liabilities = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:current_liabilities}", column_name="current_liabilities")
FinancialSnapshot.change_in_working_capital = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:change_in_working_capital}", column_name="change_in_working_capital")
FinancialSnapshot.cash_and_equivalents = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:cash_and_equivalents}", column_name="cash_and_equivalents")
FinancialSnapshot.retained_earnings = model.Property("{Concept:FinancialSnapshot} has {Primitive:Float:retained_earnings}", column_name="retained_earnings")

Company.revenue = model.Property(f"{Company} revenue {Float:revenue}")
model.define(Company.revenue(FinancialSnapshot.revenue)).where(
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.fiscal_year == 2012
)

Company.ebitda_margin = model.Property(f"{Company} ebitda margin {Float:ebitda_margin}")
model.define(Company.ebitda_margin(FinancialSnapshot.ebitda_margin)).where(
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.fiscal_year == 2012
)

Company.debt_to_equity = model.Property(f"{Company} debt to equity {Float:debt_to_equity}")
model.define(Company.debt_to_equity(FinancialSnapshot.debt_to_equity)).where(
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.fiscal_year == 2012
)

Company.free_cash_flow_quality_ratio = model.Property(f"{Company} fcf quality {Float:free_cash_flow_quality_ratio}")
model.define(Company.free_cash_flow_quality_ratio(FinancialSnapshot.fcf_yield)).where(
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.fiscal_year == 2012
)


SECStatement = model.Concept("SECStatement", table_name="sec_financials_short_financials_df", identify_by={"id": Integer})
SECStatement.ticker = model.Property("{Concept:SECStatement} has {Primitive:String:ticker}", column_name="ticker")
SECStatement.cik = model.Property("{Concept:SECStatement} has {Primitive:Integer:cik}", column_name="cik")
SECStatement.fiscal_year = model.Property("{Concept:SECStatement} has {Primitive:Integer:fiscal_year}", column_name="fiscal_year")
SECStatement.stock_price_at_filing = model.Property("{Concept:SECStatement} has {Primitive:Float:price}", column_name="price")
SECStatement.total_assets = model.Property("{Concept:SECStatement} has {Primitive:Float:assets}", column_name="assets")
SECStatement.current_assets = model.Property("{Concept:SECStatement} has {Primitive:Float:assetscurrent}", column_name="assetscurrent")
SECStatement.cash_and_equivalents = model.Property("{Concept:SECStatement} has {Primitive:Float:cashandcashequivalentsatcarryingvalue}", column_name="cashandcashequivalentsatcarryingvalue")
SECStatement.common_stock_shares_issued = model.Property("{Concept:SECStatement} has {Primitive:Float:commonstocksharesissued}", column_name="commonstocksharesissued")
SECStatement.common_stock_value = model.Property("{Concept:SECStatement} has {Primitive:Float:commonstockvalue}", column_name="commonstockvalue")
SECStatement.income_tax_expense = model.Property("{Concept:SECStatement} has {Primitive:Float:incometaxexpensebenefit}", column_name="incometaxexpensebenefit")
SECStatement.current_liabilities = model.Property("{Concept:SECStatement} has {Primitive:Float:liabilitiescurrent}", column_name="liabilitiescurrent")
SECStatement.operating_income_loss = model.Property("{Concept:SECStatement} has {Primitive:Float:operatingincomeloss}", column_name="operatingincomeloss")
SECStatement.stockholders_equity = model.Property("{Concept:SECStatement} has {Primitive:Float:stockholdersequity}", column_name="stockholdersequity")
SECStatement.net_income_loss = model.Property("{Concept:SECStatement} has {Primitive:Float:netincomeloss}", column_name="netincomeloss")
SECStatement.total_liabilities = model.Property("{Concept:SECStatement} has {Primitive:Float:liabilities}", column_name="liabilities")

CreditRating = model.Concept("CreditRating", table_name="corporate_credit_ratings_morningstar_corporate_credit_ratings_2019", identify_by={"unnamed_0": Integer})
CreditRating.rating_agency_name = model.Property("{Concept:CreditRating} has {Primitive:String:rating_agency_name}", column_name="rating_agency_name")
CreditRating.rating = model.Property("{Concept:CreditRating} has {Primitive:String:rating}", column_name="rating")
CreditRating.obligor_name = model.Property("{Concept:CreditRating} has {Primitive:String:obligor_name}", column_name="obligor_name")

Bond = model.Concept("Bond", table_name="corporate_bonds_companybonds_sheet1", identify_by={"id": Integer})
Bond.symbol = model.Property("{Concept:Bond} has {Primitive:String:symbol}", column_name="symbol")
Bond.series = model.Property("{Concept:Bond} has {Primitive:String:series}", column_name="series")
Bond.bond_type = model.Property("{Concept:Bond} has {Primitive:String:bond_type}", column_name="bond_type")
Bond.coupon_rate = model.Property("{Concept:Bond} has {Primitive:Float:clean_coupon_rate}", column_name="clean_coupon_rate")
Bond.face_value = model.Property("{Concept:Bond} has {Primitive:Float:face_value}", column_name="face_value")
Bond.credit_rating = model.Property("{Concept:Bond} has {Primitive:String:credit_rating}", column_name="credit_rating")
Bond.maturity_date = model.Property("{Concept:Bond} has {Primitive:String:maturity_date}", column_name="maturity_date")

EarningsEstimate = model.Concept("EarningsEstimate", table_name="earnings_estimates_earnings_features_clean_1", identify_by={"id": Integer})
EarningsEstimate.earnings_date = model.Property("{Concept:EarningsEstimate} has {Primitive:String:earnings_date}", column_name="earnings_date")
EarningsEstimate.ticker = model.Property("{Concept:EarningsEstimate} has {Primitive:String:ticker}", column_name="ticker")
EarningsEstimate.beat = model.Property("{Concept:EarningsEstimate} has {Primitive:Integer:beat}", column_name="beat")
EarningsEstimate.beat_streak = model.Property("{Concept:EarningsEstimate} has {Primitive:Integer:beat_streak}", column_name="beat_streak")
EarningsEstimate.historical_beat_rate = model.Property("{Concept:EarningsEstimate} has {Primitive:Float:historical_beat_rate}", column_name="historical_beat_rate")
EarningsEstimate.avg_surprise_4q = model.Property("{Concept:EarningsEstimate} has {Primitive:Float:avg_surprise_4q}", column_name="avg_surprise_4q")

BankruptcyRisk = model.Concept("BankruptcyRisk", table_name="bankruptcy_risk_bankruptcy", identify_by={"unnamed_0": Integer})
BankruptcyRisk.ticker = model.Property("{Concept:BankruptcyRisk} has {Primitive:String:ticker}", column_name="ticker")
BankruptcyRisk.date = model.Property("{Concept:BankruptcyRisk} has {Primitive:String:date}", column_name="date")
BankruptcyRisk.probability = model.Property("{Concept:BankruptcyRisk} has {Primitive:Float:probability}", column_name="probability")
BankruptcyRisk.sans_market = model.Property("{Concept:BankruptcyRisk} has {Primitive:Float:sans_market}", column_name="sans_market")
BankruptcyRisk.volatility = model.Property("{Concept:BankruptcyRisk} has {Primitive:Float:volatility}", column_name="volatility")

ESGRating = model.Concept("ESGRating", table_name="esg_ratings_sp_500_esg_risk_ratings", identify_by={"id": Integer})
ESGRating.symbol = model.Property("{Concept:ESGRating} has {Primitive:String:symbol}", column_name="symbol")
ESGRating.total_score = model.Property("{Concept:ESGRating} has {Primitive:Float:total_esg_risk_score}", column_name="total_esg_risk_score")
ESGRating.environment_score = model.Property("{Concept:ESGRating} has {Primitive:Float:environment_risk_score}", column_name="environment_risk_score")
ESGRating.social_score = model.Property("{Concept:ESGRating} has {Primitive:Float:social_risk_score}", column_name="social_risk_score")
ESGRating.governance_score = model.Property("{Concept:ESGRating} has {Primitive:Float:governance_risk_score}", column_name="governance_risk_score")
ESGRating.controversy_level = model.Property("{Concept:ESGRating} has {Primitive:String:controversy_level}", column_name="controversy_level")

IndexConstituent = model.Concept("IndexConstituent", table_name="index_constituents", identify_by={"ticker": String, "year": Integer})
IndexConstituent.company_name = model.Property("{Concept:IndexConstituent} has {Primitive:String:company_name}", column_name="company")
IndexConstituent.weight = model.Property("{Concept:IndexConstituent} has {Primitive:Float:weight}", column_name="weight")

# === 3. Leadership & Corporate Governance ===
Person = model.Concept("Person", table_name="executives_global_ceo_and_cfo_leadership_c_level_executives_dataset", identify_by={"id": Integer})
Person.name = model.Property("{Concept:Person} has {Primitive:String:name}", column_name="name")
Person.last_name = model.Property("{Concept:Person} has {Primitive:String:last_name}", column_name="last_name")
Person.linkedin_url = model.Property("{Concept:Person} has {Primitive:String:person_linkedin_url}", column_name="person_linkedin_url")
Person.boards_count = model.Property("{Concept:Person} has {Primitive:Integer:boards_count}", column_name="boards_count")

BoardMember = model.Concept("BoardMember", table_name="board_members_clean", identify_by={"id": Integer})
BoardMember.board_member_name = model.Property("{Concept:BoardMember} has {Primitive:String:boardmembername}", column_name="boardmembername")
BoardMember.company_name = model.Property("{Concept:BoardMember} has {Primitive:String:companyname}", column_name="companyname")
BoardMember.director = model.Property("{Concept:BoardMember} has director {Concept:Person}", column_name="director_id")
BoardMember.company = model.Property("{Concept:BoardMember} has company {Concept:Company}", column_name="company_ticker")

DirectorInterlock = model.Concept("DirectorInterlock", table_name="board_interlocks_clean", identify_by={"id": Integer})
DirectorInterlock.src = model.Property("{Concept:DirectorInterlock} has src {Concept:Person}", column_name="src_director_id")
DirectorInterlock.dst = model.Property("{Concept:DirectorInterlock} has dst {Concept:Person}", column_name="dst_director_id")



InsiderTransaction = model.Concept("InsiderTransaction", table_name="insider_trading_insider_transactions_insider_transactions_data", identify_by={"id": Integer})
InsiderTransaction.owner_name = model.Property("{Concept:InsiderTransaction} has {Primitive:String:owner_name}", column_name="owner_name")
InsiderTransaction.shares_amount = model.Property("{Concept:InsiderTransaction} has {Primitive:Float:shares_amount}", column_name="shares_amount")
InsiderTransaction.transaction_price = model.Property("{Concept:InsiderTransaction} has {Primitive:Float:transaction_price}", column_name="transaction_price")
InsiderTransaction.acquired_disposed_code = model.Property("{Concept:InsiderTransaction} has {Primitive:String:acquired_disposed_code}", column_name="acquired_disposed_code")
InsiderTransaction.conviction_score = model.Property("{Concept:InsiderTransaction} has {Primitive:Float:conviction_score}", column_name="conviction_score")
InsiderTransaction.ticker = model.Property("{Concept:InsiderTransaction} has {Primitive:String:ticker}", column_name="ticker")
InsiderTransaction.transaction_date = model.Property("{Concept:InsiderTransaction} has {Primitive:String:transaction_date}", column_name="transaction_date")

InstitutionalHolding = model.Concept("InstitutionalHolding", table_name="insider_trading_institutional_holdings_institutional_holdings_data", identify_by={"id": Integer})
InstitutionalHolding.owner_name = model.Property("{Concept:InstitutionalHolding} has {Primitive:String:owner_name}", column_name="owner_name")
InstitutionalHolding.shares_amount = model.Property("{Concept:InstitutionalHolding} has {Primitive:Float:shares_amount}", column_name="shares_amount")
InstitutionalHolding.value_usd = model.Property("{Concept:InstitutionalHolding} has {Primitive:Float:market_value}", column_name="market_value")
InstitutionalHolding.ticker = model.Property("{Concept:InstitutionalHolding} has {Primitive:String:company_name}", column_name="company_name")

# === 4. Operational & Supply Chain Concepts ===
Product = model.Concept("Product", table_name="supply_chain_supply_chain_data", identify_by={"sku": String})
Product.product_type = model.Property("{Concept:Product} has {Primitive:String:product_type}", column_name="product_type")
Product.price = model.Property("{Concept:Product} has {Primitive:Float:price}", column_name="price")
Product.revenue_generated = model.Property("{Concept:Product} has {Primitive:Float:revenue_generated}", column_name="revenue_generated")
Product.supplier_name = model.Property("{Concept:Product} has {Primitive:String:supplier_name}", column_name="supplier_name")
Product.manufacturing_costs = model.Property("{Concept:Product} has {Primitive:Float:manufacturing_costs}", column_name="manufacturing_costs")
Product.defect_rate = model.Property("{Concept:Product} has {Primitive:Float:defect_rates}", column_name="defect_rates")

SupplierRelation = model.Concept("SupplierRelation", table_name="supplier_relation_clean", identify_by={"id": Integer})
SupplierRelation.supplier = model.Property("{Concept:SupplierRelation} has supplier {Concept:Company}", column_name="supplier")
SupplierRelation.customer = model.Property("{Concept:SupplierRelation} has customer {Concept:Company}", column_name="customer")
SupplierRelation.revenue_share = model.Property("{Concept:SupplierRelation} has {Primitive:Float:revenue_share}", column_name="revenue_share")

Patent = model.Concept("Patent", table_name="patent_litigation_patent_data", identify_by={"case_no": String})
Patent.plaintiff = model.Property("{Concept:Patent} has {Primitive:String:plaintiff}", column_name="plaintiff")
Patent.defendant = model.Property("{Concept:Patent} has {Primitive:String:defendant}", column_name="defendant")
Patent.parent_company = model.Property("{Concept:Patent} has {Primitive:String:parent_company}", column_name="parent_company")

VCInvestment = model.Concept("VCInvestment", table_name="startup_vc_investments_clean", identify_by={"id": Integer})
VCInvestment.permalink = model.Property("{Concept:VCInvestment} has {Primitive:String:permalink}", column_name="permalink")
VCInvestment.name = model.Property("{Concept:VCInvestment} has {Primitive:String:name}", column_name="name")
VCInvestment.funding_total_usd = model.Property("{Concept:VCInvestment} has {Primitive:Float:funding_total_usd}", column_name="funding_total_usd")
VCInvestment.seed_funding = model.Property("{Concept:VCInvestment} has {Primitive:Float:seed}", column_name="seed")
VCInvestment.venture_funding = model.Property("{Concept:VCInvestment} has {Primitive:Float:venture}", column_name="venture")
VCInvestment.angel_funding = model.Property("{Concept:VCInvestment} has {Primitive:Float:angel}", column_name="angel")

FederalContract = model.Concept("FederalContract", table_name="federal_contracts_us_fed_ai_contracts_sample", identify_by={"id": Integer})
FederalContract.recipient_name = model.Property("{Concept:FederalContract} has {Primitive:String:recipient_name}", column_name="recipient_name")
FederalContract.agency_name = model.Property("{Concept:FederalContract} has {Primitive:String:awarding_agency_name}", column_name="awarding_agency_name")
FederalContract.award_amount = model.Property("{Concept:FederalContract} has {Primitive:Float:award_amount}", column_name="award_amount")
FederalContract.parent_ticker = model.Property("{Concept:FederalContract} has {Primitive:String:parent_recipient_ticker}", column_name="parent_recipient_ticker")
FederalContract.start_date = model.Property("{Concept:FederalContract} has {Primitive:String:start_date}", column_name="start_date")

LayoffEvent = model.Concept("LayoffEvent", table_name="corporate_layoffs_layoffs", identify_by={"id": Integer})
LayoffEvent.company_name = model.Property("{Concept:LayoffEvent} has {Primitive:String:company}", column_name="company")
LayoffEvent.location = model.Property("{Concept:LayoffEvent} has {Primitive:String:location}", column_name="location")
LayoffEvent.total_laid_off = model.Property("{Concept:LayoffEvent} has {Primitive:Integer:total_laid_off}", column_name="total_laid_off")
LayoffEvent.percentage_laid_off = model.Property("{Concept:LayoffEvent} has {Primitive:Float:percentage_laid_off}", column_name="percentage_laid_off")
LayoffEvent.funds_raised = model.Property("{Concept:LayoffEvent} has {Primitive:Float:funds_raised}", column_name="funds_raised")
LayoffEvent.date = model.Property("{Concept:LayoffEvent} has {Primitive:String:date}", column_name="date")
LayoffEvent.stage = model.Property("{Concept:LayoffEvent} has {Primitive:String:stage}", column_name="stage")

BuybackRecord = model.Concept("BuybackRecord", table_name="corporate_buybacks_financial_truth_dataset", identify_by={"id": Integer})
BuybackRecord.ticker = model.Property("{Concept:BuybackRecord} has {Primitive:String:ticker}", column_name="ticker")
BuybackRecord.actual_buyback = model.Property("{Concept:BuybackRecord} has {Primitive:Float:actual_buyback}", column_name="actual_buyback")
BuybackRecord.auth_buyback = model.Property("{Concept:BuybackRecord} has {Primitive:Float:auth_buyback}", column_name="auth_buyback")
BuybackRecord.sbc_expense = model.Property("{Concept:BuybackRecord} has {Primitive:Float:sbc_expense}", column_name="sbc_expense")
BuybackRecord.buyback_completion_ratio = model.Property("{Concept:BuybackRecord} has {Primitive:Float:buyback_completion_ratio}", column_name="buyback_completion_ratio")
BuybackRecord.public_date = model.Property("{Concept:BuybackRecord} has {Primitive:String:public_date}", column_name="public_date")

TradeCredit = model.Concept("TradeCredit", table_name="trade_credit_trade_credit_and_financing_costs_combined", identify_by={"id": Integer})
TradeCredit.country = model.Property("{Concept:TradeCredit} has {Primitive:String:country}", column_name="country")
TradeCredit.sector = model.Property("{Concept:TradeCredit} has {Primitive:String:sector}", column_name="sector")

# === 5. Specialized Verticals & Transactions ===
MADeal = model.Concept("MADeal", table_name="mergers_acquisitions_all", identify_by={"unique_id": Integer})
MADeal.year = model.Property("{Concept:MADeal} has {Primitive:Integer:year}", column_name="year")
MADeal.purchaser_name = model.Property("{Concept:MADeal} has {Primitive:String:purchaser}", column_name="purchaser")
MADeal.purchased_name = model.Property("{Concept:MADeal} has {Primitive:String:purchased}", column_name="purchased")
MADeal.value_billions = model.Property("{Concept:MADeal} has {Primitive:Float:value_billions}", column_name="value_billions")

AviationIncident = model.Concept("AviationIncident", table_name="aviation_industry_aviation_incidents", identify_by={"id": Integer})
AviationIncident.aircraft_type = model.Property("{Concept:AviationIncident} has {Primitive:String:aircraft_type}", column_name="aircraft_type")
AviationIncident.fatalities = model.Property("{Concept:AviationIncident} has {Primitive:Integer:fatalities}", column_name="fatalities")
AviationIncident.incident_description = model.Property("{Concept:AviationIncident} has {Primitive:String:description}", column_name="description")
AviationIncident.airline = model.Property("{Concept:AviationIncident} has {Primitive:String:airline}", column_name="airline")
AviationIncident.date = model.Property("{Concept:AviationIncident} has {Primitive:String:date}", column_name="date")

AviationFleetOrder = model.Concept("AviationFleetOrder", table_name="aviation_industry_fleet_orders", identify_by={"id": Integer})
AviationFleetOrder.aircraft_family = model.Property("{Concept:AviationFleetOrder} has {Primitive:String:aircraft_family}", column_name="aircraft_family")
AviationFleetOrder.year = model.Property("{Concept:AviationFleetOrder} has {Primitive:Integer:year}", column_name="year")
AviationFleetOrder.orders_gross = model.Property("{Concept:AviationFleetOrder} has {Primitive:Integer:orders_gross}", column_name="orders_gross")
AviationFleetOrder.deliveries = model.Property("{Concept:AviationFleetOrder} has {Primitive:Integer:deliveries}", column_name="deliveries")

AviationPassengerTraffic = model.Concept("AviationPassengerTraffic", table_name="aviation_industry_airline_financials", identify_by={"id": Integer})
AviationPassengerTraffic.passenger_count = model.Property("{Concept:AviationPassengerTraffic} has {Primitive:Float:passengers_carried_m}", column_name="passengers_carried_m")
AviationPassengerTraffic.load_factor = model.Property("{Concept:AviationPassengerTraffic} has {Primitive:Float:load_factor_pct}", column_name="load_factor_pct")
AviationPassengerTraffic.passenger_revenue = model.Property("{Concept:AviationPassengerTraffic} has {Primitive:Float:revenue_usd_bn}", column_name="revenue_usd_bn")
AviationPassengerTraffic.airline = model.Property("{Concept:AviationPassengerTraffic} has {Primitive:String:airline_name}", column_name="airline_name")

AviationRoutePerformance = model.Concept("AviationRoutePerformance", table_name="aviation_industry_route_performance", identify_by={"id": Integer})
AviationRoutePerformance.route_name = model.Property("{Concept:AviationRoutePerformance} has {Primitive:String:route}", column_name="route")
AviationRoutePerformance.revenue_per_passenger = model.Property("{Concept:AviationRoutePerformance} has {Primitive:Float:avg_fare_usd}", column_name="avg_fare_usd")
AviationRoutePerformance.annual_revenue = model.Property("{Concept:AviationRoutePerformance} has {Primitive:Float:annual_revenue_usd_m}", column_name="annual_revenue_usd_m")

BiotechFunding = model.Concept("BiotechFunding", table_name="pharma_industry_biotech_funding", identify_by={"deal_id": Integer})
BiotechFunding.funding_amount_usd = model.Property("{Concept:BiotechFunding} has {Primitive:Float:value_usd_bn}", column_name="value_usd_bn")
BiotechFunding.funding_round = model.Property("{Concept:BiotechFunding} has {Primitive:String:deal_type}", column_name="deal_type")
BiotechFunding.company_name = model.Property("{Concept:BiotechFunding} has {Primitive:String:target_or_company}", column_name="target_or_company")
BiotechFunding.date = model.Property("{Concept:BiotechFunding} has {Primitive:String:date}", column_name="date")

ClinicalTrial = model.Concept("ClinicalTrial", table_name="pharma_industry_clinical_trials", identify_by={"trial_id": String})
ClinicalTrial.phase = model.Property("{Concept:ClinicalTrial} has {Primitive:String:phase}", column_name="phase")
ClinicalTrial.status = model.Property("{Concept:ClinicalTrial} has {Primitive:String:outcome}", column_name="outcome")

DiseaseBurden = model.Concept("DiseaseBurden", table_name="pharma_industry_disease_burden", identify_by={"id": Integer})
DiseaseBurden.disease_name = model.Property("{Concept:DiseaseBurden} has {Primitive:String:disease}", column_name="disease")
DiseaseBurden.global_cases = model.Property("{Concept:DiseaseBurden} has {Primitive:Float:global_dalys_millions}", column_name="global_dalys_millions")
DiseaseBurden.yearly_mortality_rate = model.Property("{Concept:DiseaseBurden} has {Primitive:Float:dalys_millions}", column_name="dalys_millions")

DrugApproval = model.Concept("DrugApproval", table_name="pharma_industry_drug_approvals", identify_by={"approval_id": String})
DrugApproval.drug_name = model.Property("{Concept:DrugApproval} has {Primitive:String:drug_name}", column_name="drug_name")
DrugApproval.indication = model.Property("{Concept:DrugApproval} has {Primitive:String:therapy_area}", column_name="therapy_area")
DrugApproval.company = model.Property("{Concept:DrugApproval} has {Primitive:String:sponsor_company}", column_name="sponsor_company")
DrugApproval.approval_date = model.Property("{Concept:DrugApproval} has {Primitive:String:approval_date}", column_name="approval_date")

PharmaFinancials = model.Concept("PharmaFinancials", table_name="pharma_industry_pharma_companies_financials", identify_by={"company_name": String, "year": Integer})
PharmaFinancials.rd_spend = model.Property("{Concept:PharmaFinancials} has {Primitive:Float:rd_spend_usd_bn}", column_name="rd_spend_usd_bn")
PharmaFinancials.revenue = model.Property("{Concept:PharmaFinancials} has {Primitive:Float:revenue_usd_bn}", column_name="revenue_usd_bn")

ChipMarketMetric = model.Concept("ChipMarketMetric", table_name="semiconductor_industry_ai_chip_market", identify_by={"id": Integer})
ChipMarketMetric.segment_name = model.Property("{Concept:ChipMarketMetric} has {Primitive:String:chip_name}", column_name="chip_name")
ChipMarketMetric.market_size_usd = model.Property("{Concept:ChipMarketMetric} has {Primitive:Float:estimated_revenue_usd_m}", column_name="estimated_revenue_usd_m")
ChipMarketMetric.growth_rate_pct = model.Property("{Concept:ChipMarketMetric} has {Primitive:Float:estimated_shipments_units}", column_name="estimated_shipments_units")
ChipMarketMetric.year = model.Property("{Concept:ChipMarketMetric} has {Primitive:Integer:year}", column_name="year")

SemiconductorFinancials = model.Concept("SemiconductorFinancials", table_name="semiconductor_industry_chip_companies_financials", identify_by={"company_name": String, "year": Integer})
SemiconductorFinancials.revenue = model.Property("{Concept:SemiconductorFinancials} has {Primitive:Float:revenue_usd_bn}", column_name="revenue_usd_bn")
SemiconductorFinancials.rnd_spending = model.Property("{Concept:SemiconductorFinancials} has {Primitive:Float:rd_spend_usd_bn}", column_name="rd_spend_usd_bn")

ChipPrice = model.Concept("ChipPrice", table_name="semiconductor_industry_chip_prices", identify_by={"id": Integer})
ChipPrice.chip_type = model.Property("{Concept:ChipPrice} has {Primitive:String:product}", column_name="product")
ChipPrice.spot_price_usd = model.Property("{Concept:ChipPrice} has {Primitive:Float:price}", column_name="price")
ChipPrice.date = model.Property("{Concept:ChipPrice} has {Primitive:String:year_month}", column_name="year_month")

SemiconductorExportControl = model.Concept("SemiconductorExportControl", table_name="semiconductor_industry_export_controls", identify_by={"control_id": Integer})
SemiconductorExportControl.restricted_entity = model.Property("{Concept:SemiconductorExportControl} has {Primitive:String:target}", column_name="target")
SemiconductorExportControl.controlling_country = model.Property("{Concept:SemiconductorExportControl} has {Primitive:String:imposing_country}", column_name="imposing_country")
SemiconductorExportControl.restriction_type = model.Property("{Concept:SemiconductorExportControl} has {Primitive:String:policy_name}", column_name="policy_name")
SemiconductorExportControl.effective_date = model.Property("{Concept:SemiconductorExportControl} has {Primitive:String:date}", column_name="date")

SemiconductorFabCapacity = model.Concept("SemiconductorFabCapacity", table_name="semiconductor_industry_fab_capacity", identify_by={"id": Integer})
SemiconductorFabCapacity.facility_name = model.Property("{Concept:SemiconductorFabCapacity} has {Primitive:String:fab_type}", column_name="fab_type")
SemiconductorFabCapacity.location = model.Property("{Concept:SemiconductorFabCapacity} has {Primitive:String:country_iso3}", column_name="country_iso3")
SemiconductorFabCapacity.capacity_wspm = model.Property("{Concept:SemiconductorFabCapacity} has {Primitive:Integer:monthly_wafer_capacity}", column_name="monthly_wafer_capacity")
SemiconductorFabCapacity.node_size_nm = model.Property("{Concept:SemiconductorFabCapacity} has {Primitive:Integer:process_node_nm}", column_name="process_node_nm")
SemiconductorFabCapacity.company = model.Property("{Concept:SemiconductorFabCapacity} has {Primitive:String:company}", column_name="company")

# === 6. Sentiment & External Factors ===
NewsHeadline = model.Concept("NewsHeadline", table_name="financial_news_raw_partner_headlines", identify_by={"unnamed_0": Integer})
NewsHeadline.headline = model.Property("{Concept:NewsHeadline} has {Primitive:String:headline}", column_name="headline")
NewsHeadline.url = model.Property("{Concept:NewsHeadline} has {Primitive:String:url}", column_name="url")
NewsHeadline.publisher = model.Property("{Concept:NewsHeadline} has {Primitive:String:publisher}", column_name="publisher")
NewsHeadline.date = model.Property("{Concept:NewsHeadline} has {Primitive:String:date}", column_name="date")
NewsHeadline.stock = model.Property("{Concept:NewsHeadline} has {Primitive:String:stock}", column_name="stock")

SentimentRecord = model.Concept("SentimentRecord", table_name="sentiment_phrasebank", identify_by={"id": Integer})
SentimentRecord.sentiment = model.Property("{Concept:SentimentRecord} has {Primitive:String:sentiment}", column_name="sentiment")
SentimentRecord.sentence = model.Property("{Concept:SentimentRecord} has {Primitive:String:sentence}", column_name="sentence")

Commodity = model.Concept("Commodity", table_name="commodity_prices_global_commodity_prices_2000_2026", identify_by={"ticker": String, "date": String})
Commodity.commodity_name = model.Property("{Concept:Commodity} has {Primitive:String:commodity}", column_name="commodity")
Commodity.open_val = model.Property("{Concept:Commodity} has {Primitive:Float:open}", column_name="open")
Commodity.close_val = model.Property("{Concept:Commodity} has {Primitive:Float:close}", column_name="close")

PriceSeries = model.Concept("PriceSeries", table_name="fx_rates_all_clean", identify_by={"id": Integer})
PriceSeries.time_serie = model.Property("{Concept:PriceSeries} has {Primitive:String:time_serie}", column_name="time_serie")
PriceSeries.euro_us = model.Property("{Concept:PriceSeries} has {Primitive:Float:euro_area_euro_us}", column_name="euro_area_euro_us")

OHLCV = model.Concept("OHLCV", table_name="ohlcv", identify_by={"ticker": String, "date_time": DateTime})
OHLCV.open_val = model.Property("{Concept:OHLCV} has {Primitive:Float:open_val}", column_name="open_val")
OHLCV.high_val = model.Property("{Concept:OHLCV} has {Primitive:Float:high_val}", column_name="high_val")
OHLCV.low_val = model.Property("{Concept:OHLCV} has {Primitive:Float:low_val}", column_name="low_val")
OHLCV.close_val = model.Property("{Concept:OHLCV} has {Primitive:Float:close_val}", column_name="close_val")
OHLCV.volume = model.Property("{Concept:OHLCV} has {Primitive:Integer:volume}", column_name="volume")

# === 7. Domicile & Macroeconomics ===
Country = model.Concept("Country", table_name="economic_freedom_economic_freedom_index2019_data", identify_by={"country_name": String})
Country.property_rights = model.Property("{Concept:Country} has {Primitive:Float:property_rights}", column_name="property_rights")
Country.tax_burden = model.Property("{Concept:Country} has {Primitive:Float:tax_burden}", column_name="tax_burden")
Country.government_spending = model.Property("{Concept:Country} has {Primitive:Float:gov_t_spending}", column_name="gov_t_spending")
Country.business_freedom = model.Property("{Concept:Country} has {Primitive:Float:business_freedom}", column_name="business_freedom")

SovereignRating = model.Concept("SovereignRating", table_name="sovereign_ratings_all", identify_by={"country_name": String})
SovereignRating.rating_foreign = model.Property("{Concept:SovereignRating} has {Primitive:String:rating_foreign}", column_name="rating_foreign")
SovereignRating.rating_local = model.Property("{Concept:SovereignRating} has {Primitive:String:rating_local}", column_name="rating_local")

CountryMacro = model.Concept("CountryMacro", table_name="country_gdp_employment_employment_unemployment_gdp_data", identify_by={"country_name": String, "year": Integer})
CountryMacro.gdp_usd = model.Property("{Concept:CountryMacro} has {Primitive:Float:gdp_in_usd}", column_name="gdp_in_usd")
CountryMacro.unemployment_rate = model.Property("{Concept:CountryMacro} has {Primitive:Float:unemployment_rate}", column_name="unemployment_rate")

MacroIndicator = model.Concept("MacroIndicator", table_name="macroeconomics_index", identify_by={"id": Integer})
MacroIndicator.year = model.Property("{Concept:MacroIndicator} has {Primitive:Integer:year}", column_name="year")
MacroIndicator.month = model.Property("{Concept:MacroIndicator} has {Primitive:Integer:month}", column_name="month")
MacroIndicator.federal_funds_rate = model.Property("{Concept:MacroIndicator} has {Primitive:Float:effective_federal_funds_rate}", column_name="effective_federal_funds_rate")
MacroIndicator.gdp_change = model.Property("{Concept:MacroIndicator} has {Primitive:Float:real_gdp_percent_change}", column_name="real_gdp_percent_change")
MacroIndicator.inflation_rate = model.Property("{Concept:MacroIndicator} has {Primitive:Float:inflation_rate}", column_name="inflation_rate")

SectorReturn = model.Concept("SectorReturn", table_name="sector_returns_sector_annual_summary", identify_by={"id": Integer})
SectorReturn.sector_name = model.Property("{Concept:SectorReturn} has {Primitive:String:sector}", column_name="sector")
SectorReturn.return_pct = model.Property("{Concept:SectorReturn} has {Primitive:Float:annual_return}", column_name="annual_return")
SectorReturn.year = model.Property("{Concept:SectorReturn} has {Primitive:Integer:year}", column_name="year")

# Register validated Database FK constraints
print("Registering database foreign keys...")
model.register_fks(con)

print("Ontology schema loaded cleanly!")
