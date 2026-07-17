import ontology
from ontology import model, FinancialSnapshot, Company, EarningsEstimate
from pyrel_duckdb import Float, Integer, String, Boolean

# --- 9. Growth, Valuation Drivers & Per-Share Metrics ---


# Earnings Per Share (EPS) is net earnings divided by shares outstanding.
# Rationale: Standard metric representing shareholder bottom-line profit allocation.
FinancialSnapshot.earnings_per_share_eps = model.Property(f"{FinancialSnapshot} has {Float:earnings_per_share_eps}")
model.define(FinancialSnapshot.earnings_per_share_eps(FinancialSnapshot.earnings / FinancialSnapshot.shares_outstanding))

# Revenue Per Share divides revenue by shares outstanding.
# Rationale: Evaluates sales generation per equity unit.
FinancialSnapshot.revenue_per_share = model.Property(f"{FinancialSnapshot} has {Float:revenue_per_share}")
model.define(FinancialSnapshot.revenue_per_share(FinancialSnapshot.revenue / FinancialSnapshot.shares_outstanding))

# Free Cash Flow Per Share divides free cash flow by shares outstanding.
# Rationale: Key valuation driver measuring actual distributable cash generated per share.
FinancialSnapshot.free_cash_flow_per_share = model.Property(f"{FinancialSnapshot} has {Float:free_cash_flow_per_share}")
model.define(FinancialSnapshot.free_cash_flow_per_share((FinancialSnapshot.net_cash_operating - FinancialSnapshot.capital_expenditures) / FinancialSnapshot.shares_outstanding))

# Operating Cash Flow Per Share divides core operating cash flow by shares outstanding.
# Rationale: Tracks organic cash flow generation per share unit.
FinancialSnapshot.operating_cash_flow_per_share = model.Property(f"{FinancialSnapshot} has {Float:operating_cash_flow_per_share}")
model.define(FinancialSnapshot.operating_cash_flow_per_share(FinancialSnapshot.net_cash_operating / FinancialSnapshot.shares_outstanding))

# Net Debt is total debt minus cash and cash equivalents.
# Rationale: Measures ultimate liability obligations if all cash were instantly applied to repay debt.
FinancialSnapshot.net_debt = model.Property(f"{FinancialSnapshot} has {Float:net_debt}")
model.define(FinancialSnapshot.net_debt(FinancialSnapshot.total_debt - FinancialSnapshot.cash_and_equivalents))

# Net Debt to Equity compares net debt directly to shareholder equity.
# Rationale: Solvency metric focusing on net liabilities exposure.
FinancialSnapshot.net_debt_to_equity = model.Property(f"{FinancialSnapshot} has {Float:net_debt_to_equity}")
model.define(FinancialSnapshot.net_debt_to_equity(FinancialSnapshot.net_debt / FinancialSnapshot.equity))

# Tangible Assets is total assets minus intangible assets.
# Rationale: Focuses on physical and liquid resources.
FinancialSnapshot.tangible_assets = model.Property(f"{FinancialSnapshot} has {Float:tangible_assets}")
model.define(FinancialSnapshot.tangible_assets(FinancialSnapshot.assets - FinancialSnapshot.intangible_assets))

# Tangible Equity is total equity minus intangible assets.
# Rationale: Strictest valuation base for physical book value calculations.
FinancialSnapshot.tangible_equity = model.Property(f"{FinancialSnapshot} has {Float:tangible_equity}")
model.define(FinancialSnapshot.tangible_equity(FinancialSnapshot.equity - FinancialSnapshot.intangible_assets))

# Tangible Debt to Equity compares total debt directly to tangible equity.
# Rationale: Credit risk metric isolating physical equity reserves.
FinancialSnapshot.tangible_debt_to_equity = model.Property(f"{FinancialSnapshot} has {Float:tangible_debt_to_equity}")
model.define(FinancialSnapshot.tangible_debt_to_equity(FinancialSnapshot.total_debt / FinancialSnapshot.tangible_equity))

# COGS Margin measures direct manufacturing costs relative to revenue.
# Rationale: Direct operating efficiency indicator.
FinancialSnapshot.cogs_margin = model.Property(f"{FinancialSnapshot} has {Float:cogs_margin}")
model.define(FinancialSnapshot.cogs_margin(FinancialSnapshot.cogs / FinancialSnapshot.revenue))

# Effective Tax Rate is tax expense divided by operating income.
# Rationale: Measures real corporate tax drag.
FinancialSnapshot.effective_tax_rate = model.Property(f"{FinancialSnapshot} has {Float:effective_tax_rate}")
model.define(FinancialSnapshot.effective_tax_rate(FinancialSnapshot.income_tax_expense / FinancialSnapshot.operating_income_loss))



# --- 10. Advanced Financial Strength & Predictive Analytics ---

# Altman Z-Score calculates corporate bankruptcy risk using five weighted financial ratios.
# Rationale: Standard quantitative tool for predicting corporate insolvency probability within 2 years.
FinancialSnapshot.altman_z_score = model.Property(f"{FinancialSnapshot} has {Float:altman_z_score}")
model.define(FinancialSnapshot.altman_z_score(
    1.2 * (FinancialSnapshot.working_capital / FinancialSnapshot.assets) +
    1.4 * (FinancialSnapshot.retained_earnings / FinancialSnapshot.assets) +
    3.3 * (FinancialSnapshot.operating_income_loss / FinancialSnapshot.assets) +
    0.6 * (FinancialSnapshot.market_capitalization / FinancialSnapshot.total_debt) +
    0.999 * (FinancialSnapshot.revenue / FinancialSnapshot.assets)
))

# Altman Distress Zone flags firms with Altman Z-Scores below 1.81.
# Rationale: Indicates high probability of corporate failure.
FinancialSnapshot.is_altman_distress_zone = model.Property(f"{FinancialSnapshot} is Altman distress {Boolean:is_altman_distress_zone}")
model.define(FinancialSnapshot.is_altman_distress_zone(True)).where(FinancialSnapshot.altman_z_score < 1.81)

# Altman Gray Zone flags firms with Altman Z-Scores between 1.81 and 2.99.
# Rationale: Indicates moderate insolvency risk.
FinancialSnapshot.is_altman_gray_zone = model.Property(f"{FinancialSnapshot} is Altman gray {Boolean:is_altman_gray_zone}")
model.define(FinancialSnapshot.is_altman_gray_zone(True)).where(
    FinancialSnapshot.altman_z_score >= 1.81,
    FinancialSnapshot.altman_z_score <= 2.99
)

# Altman Safe Zone flags firms with Altman Z-Scores above 2.99.
# Rationale: Low default risk profiles.
FinancialSnapshot.is_altman_safe_zone = model.Property(f"{FinancialSnapshot} is Altman safe {Boolean:is_altman_safe_zone}")
model.define(FinancialSnapshot.is_altman_safe_zone(True)).where(FinancialSnapshot.altman_z_score > 2.99)


# P/E Multiple compares share price directly to earnings per share.
# Rationale: Primary valuation tool representing price paid per unit of profit.
FinancialSnapshot.pe_multiple = model.Property(f"{FinancialSnapshot} has {Float:pe_multiple}")
model.define(FinancialSnapshot.pe_multiple(FinancialSnapshot.stock_price / FinancialSnapshot.earnings_per_share_eps))

# P/S Multiple compares share price to sales per share.
# Rationale: Valuation tool useful for pre-profit or early growth firms.
FinancialSnapshot.ps_multiple = model.Property(f"{FinancialSnapshot} has {Float:ps_multiple}")
model.define(FinancialSnapshot.ps_multiple(FinancialSnapshot.stock_price / FinancialSnapshot.revenue_per_share))

# P/B Multiple compares share price directly to book value per share.
# Rationale: Valuation tool commonly used in financial and capital-intensive sectors.
FinancialSnapshot.pb_multiple = model.Property(f"{FinancialSnapshot} has {Float:pb_multiple}")
model.define(FinancialSnapshot.pb_multiple(FinancialSnapshot.stock_price / FinancialSnapshot.book_value_per_share))

# Enterprise Value (EV) measures total firm value (Equity Cap + Net Debt).
# Rationale: Provides a comprehensive buyout cost baseline.
FinancialSnapshot.enterprise_value = model.Property(f"{FinancialSnapshot} has {Float:enterprise_value}")
model.define(FinancialSnapshot.enterprise_value(FinancialSnapshot.market_capitalization + FinancialSnapshot.total_debt - FinancialSnapshot.cash_and_equivalents))

# EV to Revenue compares Enterprise Value directly to revenue.
# Rationale: Valuation multiple adjusting for different capital structures.
FinancialSnapshot.ev_to_revenue = model.Property(f"{FinancialSnapshot} has {Float:ev_to_revenue}")
model.define(FinancialSnapshot.ev_to_revenue(FinancialSnapshot.enterprise_value / FinancialSnapshot.revenue))

# EBITDA is operating profits before D&A.
FinancialSnapshot.ebitda = model.Property(f"{FinancialSnapshot} has {Float:ebitda}")
model.define(FinancialSnapshot.ebitda(FinancialSnapshot.operating_income_loss + FinancialSnapshot.depreciation_amortization))

# EV to EBITDA compares Enterprise Value directly to EBITDA.
# Rationale: Standard valuation multiple for cash flow acquisition analysis.
FinancialSnapshot.ev_to_ebitda = model.Property(f"{FinancialSnapshot} has {Float:ev_to_ebitda}")
model.define(FinancialSnapshot.ev_to_ebitda(FinancialSnapshot.enterprise_value / FinancialSnapshot.ebitda))

# Price to FCF compares stock price to free cash flow per share.
# Rationale: Valuation metric analyzing price relative to organic cash yields.
FinancialSnapshot.price_to_fcf = model.Property(f"{FinancialSnapshot} has {Float:price_to_fcf}")
model.define(FinancialSnapshot.price_to_fcf(FinancialSnapshot.stock_price / FinancialSnapshot.free_cash_flow_per_share))


# --- 16. Economic Value Added (EVA), Asset Quality & Impairment Alerting ---


# Intangibles to Assets measures intangible assets relative to total assets.
# Rationale: Tracks intellectual capital intensity.
FinancialSnapshot.intangibles_to_assets = model.Property(f"{FinancialSnapshot} has {Float:intangibles_to_assets}")
model.define(FinancialSnapshot.intangibles_to_assets(FinancialSnapshot.intangible_assets / FinancialSnapshot.assets))


# Dividend Yield compares dividends directly to market valuation.
# Rationale: Measures yield returns distributed to shareholders.
FinancialSnapshot.dividend_yield = model.Property(f"{FinancialSnapshot} has {Float:dividend_yield}")
model.define(FinancialSnapshot.dividend_yield(FinancialSnapshot.dividends_paid / FinancialSnapshot.market_capitalization))


# Operating Cash to Working Capital evaluates cash coverage over working capital.
# Rationale: Analyzes structural quality of short-term capital.
FinancialSnapshot.operating_cash_to_working_capital = model.Property(f"{FinancialSnapshot} has {Float:operating_cash_to_working_capital}")
model.define(FinancialSnapshot.operating_cash_to_working_capital(FinancialSnapshot.net_cash_operating / FinancialSnapshot.working_capital))

# Retained Earnings to Total Liabilities compares cumulative reserves to liabilities.
# Rationale: Solvency balance metric representing accumulated profits buffer.
FinancialSnapshot.retained_earnings_to_total_liabilities = model.Property(f"{FinancialSnapshot} has {Float:retained_earnings_to_total_liabilities}")
model.define(FinancialSnapshot.retained_earnings_to_total_liabilities(FinancialSnapshot.retained_earnings / FinancialSnapshot.liabilities))

# Cash to Total Assets compares cash to total asset footprint.
# Rationale: Measures general liquid reserve allocations.
FinancialSnapshot.cash_to_total_assets = model.Property(f"{FinancialSnapshot} has {Float:cash_to_total_assets}")
model.define(FinancialSnapshot.cash_to_total_assets(FinancialSnapshot.cash_and_equivalents / FinancialSnapshot.assets))

# Tangible Assets to Liabilities compares physical assets to total obligations.
# Rationale: Hard coverage ratio for senior debt security analysis.
FinancialSnapshot.tangible_assets_to_total_liabilities = model.Property(f"{FinancialSnapshot} has {Float:tangible_assets_to_total_liabilities}")
model.define(FinancialSnapshot.tangible_assets_to_total_liabilities(FinancialSnapshot.tangible_assets / FinancialSnapshot.liabilities))

# Cash Flow to Reinvestment Ratio compares operating cash directly to capital expenditures.
# Rationale: Evaluates capability to self-fund capital growth.
FinancialSnapshot.cash_flow_to_reinvestment_ratio = model.Property(f"{FinancialSnapshot} has {Float:cash_flow_to_reinvestment_ratio}")
model.define(FinancialSnapshot.cash_flow_to_reinvestment_ratio(FinancialSnapshot.net_cash_operating / FinancialSnapshot.capital_expenditures))

# Earnings Beater flags companies that beat their quarterly earnings estimates.
# Rationale: Short term positive earnings surprise event indicator.
Company.is_earnings_beater = model.Property(f"{Company} is earnings beater {Boolean:is_earnings_beater}")
model.define(Company.is_earnings_beater(True)).where(
    EarningsEstimate.ticker == Company.ticker,
    EarningsEstimate.beat == 1
)

# Earnings Beat Streak flags companies beating estimates for at least 3 consecutive quarters.
# Rationale: High consistency operational momentum.
Company.has_earnings_beat_streak = model.Property(f"{Company} has beat streak {Boolean:has_earnings_beat_streak}")
model.define(Company.has_earnings_beat_streak(True)).where(
    EarningsEstimate.ticker == Company.ticker,
    EarningsEstimate.beat_streak >= 3
)

# Earnings Risk Profile flags companies with highly irregular or poor beat histories.
# Rationale: High forecast error and volatility risks.
Company.earnings_risk_profile = model.Property(f"{Company} has earnings risk profile {Boolean:earnings_risk_profile}")
model.define(Company.earnings_risk_profile(True)).where(
    EarningsEstimate.ticker == Company.ticker,
    EarningsEstimate.historical_beat_rate < 0.40
)

# Market Darling flags companies holding both outstanding quality compounder metrics and solid earnings beat records.
# Rationale: Higher-tier nested rule building on is_quality_compounder and is_earnings_beater.
Company.is_market_darling = model.Property(f"{Company} is market darling {Boolean:is_market_darling}")
model.define(Company.is_market_darling(True)).where(
    Company.is_quality_compounder == True,
    Company.is_earnings_beater == True
)

# Valuation Arbitrage Opportunity flags market darlings that are also priced within solid Altman default safety metrics.
# Rationale: Higher-tier nested rule building on is_market_darling and is_altman_safe_zone.
Company.valuation_arbitrage_opportunity = model.Property(f"{Company} has valuation arbitrage {Boolean:valuation_arbitrage_opportunity}")
model.define(Company.valuation_arbitrage_opportunity(True)).where(
    Company.is_market_darling == True,
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.is_altman_safe_zone == True
)

# Earnings Surprise Restructuring Alert flags companies posting positive earnings beats that are simultaneously contracting labor.
# Rationale: Higher-tier nested rule building on avg_surprise_4q and has_recent_layoffs.
Company.earnings_surprise_restructuring = model.Property(f"{Company} has surprise restructuring {Boolean:earnings_surprise_restructuring}")
model.define(Company.earnings_surprise_restructuring(True)).where(
    EarningsEstimate.ticker == Company.ticker,
    EarningsEstimate.avg_surprise_4q > 0.20,
    Company.has_recent_layoffs == True
)


