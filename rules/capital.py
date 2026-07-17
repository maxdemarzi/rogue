import ontology
from ontology import model, Company, FinancialSnapshot
from pyrel_duckdb import Float, Integer, String, Boolean

# --- 12. Cost of Capital, Margin Expansion & Dividend Security ---

# Cost of Debt is interest expense divided by total debt.
# Rationale: Measures corporate borrowing interest rates.
FinancialSnapshot.cost_of_debt = model.Property(f"{FinancialSnapshot} has {Float:cost_of_debt}")
model.define(FinancialSnapshot.cost_of_debt(FinancialSnapshot.interest_expense / FinancialSnapshot.total_debt))

# Free Cash Flow is operating cash minus capital expenditures.
# Rationale: Real cash generated for servicing all capital providers.
FinancialSnapshot.free_cash_flow = model.Property(f"{FinancialSnapshot} has {Float:free_cash_flow}")
model.define(FinancialSnapshot.free_cash_flow(FinancialSnapshot.net_cash_operating - FinancialSnapshot.capital_expenditures))

# EV to FCF compares Enterprise Value to Free Cash Flow.
# Rationale: Measures price paid relative to organic cash yield generation.
FinancialSnapshot.ev_to_fcf = model.Property(f"{FinancialSnapshot} has {Float:ev_to_fcf}")
model.define(FinancialSnapshot.ev_to_fcf(FinancialSnapshot.enterprise_value / FinancialSnapshot.free_cash_flow))

# EV to Invested Capital compares Enterprise Value to invested capital base.
# Rationale: Evaluates valuation multiples on capital allocated.
FinancialSnapshot.ev_to_invested_capital = model.Property(f"{FinancialSnapshot} has {Float:ev_to_invested_capital}")
model.define(FinancialSnapshot.ev_to_invested_capital(FinancialSnapshot.enterprise_value / (FinancialSnapshot.equity + FinancialSnapshot.total_debt - FinancialSnapshot.cash_and_equivalents)))

# Equity Value Headroom compares market capitalization directly to total liabilities.
# Rationale: Measures safety buffer protecting creditors.
FinancialSnapshot.equity_value_headroom = model.Property(f"{FinancialSnapshot} has {Float:equity_value_headroom}")
model.define(FinancialSnapshot.equity_value_headroom(FinancialSnapshot.market_capitalization / FinancialSnapshot.liabilities))

# Accounts Receivable as a Percentage of Revenue.
# Rationale: Tracks inventory collection cycles relative to sales scales.
FinancialSnapshot.accounts_receivable_pct_revenue = model.Property(f"{FinancialSnapshot} has {Float:accounts_receivable_pct_revenue}")
model.define(FinancialSnapshot.accounts_receivable_pct_revenue(FinancialSnapshot.accounts_receivable / FinancialSnapshot.revenue))

# Inventory as a Percentage of COGS.
# Rationale: Tracks raw materials storage efficiency.
FinancialSnapshot.inventory_pct_cogs = model.Property(f"{FinancialSnapshot} has {Float:inventory_pct_cogs}")
model.define(FinancialSnapshot.inventory_pct_cogs(FinancialSnapshot.inventories / FinancialSnapshot.cogs))

# Accounts Payable as a Percentage of COGS.
# Rationale: Tracks supplier credit utilization levels.
FinancialSnapshot.accounts_payable_pct_cogs = model.Property(f"{FinancialSnapshot} has {Float:accounts_payable_pct_cogs}")
model.define(FinancialSnapshot.accounts_payable_pct_cogs(FinancialSnapshot.accounts_payable / FinancialSnapshot.cogs))

# Working Capital Intensity is working capital divided by revenue.
# Rationale: Measures operating capital required to drive sales growth.
FinancialSnapshot.working_capital_intensity = model.Property(f"{FinancialSnapshot} has {Float:working_capital_intensity}")
model.define(FinancialSnapshot.working_capital_intensity(FinancialSnapshot.working_capital / FinancialSnapshot.revenue))

# Dividend Coverage Ratio is net earnings divided by dividends paid.
# Rationale: Assesses safety headroom of dividend payout policy.
FinancialSnapshot.dividend_coverage_ratio = model.Property(f"{FinancialSnapshot} has {Float:dividend_coverage_ratio}")
model.define(FinancialSnapshot.dividend_coverage_ratio(FinancialSnapshot.earnings / FinancialSnapshot.dividends_paid))

# FCF Dividend Coverage Ratio divides Free Cash Flow by dividends.
# Rationale: Strictest dividend safety check verifying cash-based coverage.
FinancialSnapshot.fcf_dividend_coverage_ratio = model.Property(f"{FinancialSnapshot} has {Float:fcf_dividend_coverage_ratio}")
model.define(FinancialSnapshot.fcf_dividend_coverage_ratio(FinancialSnapshot.free_cash_flow / FinancialSnapshot.dividends_paid))


# --- 13. Capital Allocation Integrity, Operating Leverage & Cash Flow Conversion ---

# Plowback Ratio is 1 - Dividend Payout Ratio.
# Rationale: Tracks proportion of earnings retained for capital reinvestment.
FinancialSnapshot.plowback_ratio = model.Property(f"{FinancialSnapshot} has {Float:plowback_ratio}")
model.define(FinancialSnapshot.plowback_ratio(1.0 - FinancialSnapshot.dividend_payout_ratio))

# Capital Return to EBITDA compares capital returns directly to EBITDA.
# Rationale: Measures payout policy safety relative to operational cash flow power.
FinancialSnapshot.capital_return_to_ebitda = model.Property(f"{FinancialSnapshot} has {Float:capital_return_to_ebitda}")
model.define(FinancialSnapshot.capital_return_to_ebitda((FinancialSnapshot.share_repurchase_amount + FinancialSnapshot.dividends_paid) / FinancialSnapshot.ebitda))

# Degree of Operating Leverage (DOL) evaluates EBIT changes relative to sales volume changes.
# Rationale: Measures fixed operating cost leverage sensitivity.
FinancialSnapshot.degree_of_operating_leverage_dol = model.Property(f"{FinancialSnapshot} has {Float:degree_of_operating_leverage_dol}")
model.define(FinancialSnapshot.degree_of_operating_leverage_dol(FinancialSnapshot.gross_profit / FinancialSnapshot.operating_income_loss))

# Degree of Financial Leverage (DFL) evaluates EPS changes relative to EBIT changes.
# Rationale: Measures interest expense leverage sensitivity.
FinancialSnapshot.degree_of_financial_leverage_dfl = model.Property(f"{FinancialSnapshot} has {Float:degree_of_financial_leverage_dfl}")
model.define(FinancialSnapshot.degree_of_financial_leverage_dfl(FinancialSnapshot.operating_income_loss / (FinancialSnapshot.operating_income_loss - FinancialSnapshot.interest_expense)))

# Degree of Total Leverage (DTL) is DOL multiplied by DFL.
# Rationale: Measures total earnings sensitivity to sales volume shifts.
FinancialSnapshot.degree_of_total_leverage_dtl = model.Property(f"{FinancialSnapshot} has {Float:degree_of_total_leverage_dtl}")
model.define(FinancialSnapshot.degree_of_total_leverage_dtl(FinancialSnapshot.degree_of_operating_leverage_dol * FinancialSnapshot.degree_of_financial_leverage_dfl))

# Tax Shield calculates interest payment tax deductions.
# Rationale: Valuation benefit driven by debt financing configurations.
FinancialSnapshot.tax_shield_usd = model.Property(f"{FinancialSnapshot} has {Float:tax_shield_usd}")
model.define(FinancialSnapshot.tax_shield_usd(FinancialSnapshot.interest_expense * FinancialSnapshot.effective_tax_rate))

# Free Cash Flow to Firm (FCFF) evaluates cash available to both debt and equity holders.
# Rationale: Core valuation baseline for corporate valuations.
FinancialSnapshot.free_cash_flow_to_firm_fcff = model.Property(f"{FinancialSnapshot} has {Float:free_cash_flow_to_firm_fcff}")
model.define(FinancialSnapshot.free_cash_flow_to_firm_fcff(
    FinancialSnapshot.operating_income_loss * (1.0 - FinancialSnapshot.effective_tax_rate) +
    FinancialSnapshot.depreciation_amortization - FinancialSnapshot.capital_expenditures -
    FinancialSnapshot.change_in_working_capital
))

# Free Cash Flow to Equity (FCFE) evaluates cash available to equity holders after debt service.
# Rationale: Directly determines dividend/buyback capacity.
FinancialSnapshot.free_cash_flow_to_equity_fcfe = model.Property(f"{FinancialSnapshot} has {Float:free_cash_flow_to_equity_fcfe}")
model.define(FinancialSnapshot.free_cash_flow_to_equity_fcfe(
    FinancialSnapshot.free_cash_flow_to_firm_fcff -
    FinancialSnapshot.interest_expense * (1.0 - FinancialSnapshot.effective_tax_rate)
))

# Free Cash Flow Conversion Ratio divides free cash flow by EBITDA.
# Rationale: Measures how efficiently EBITDA translates into usable free cash.
FinancialSnapshot.fcf_conversion_ratio = model.Property(f"{FinancialSnapshot} has {Float:fcf_conversion_ratio}")
model.define(FinancialSnapshot.fcf_conversion_ratio(FinancialSnapshot.free_cash_flow / FinancialSnapshot.ebitda))

# Tobin's Q evaluates firm valuation relative to replacement costs of assets.
# Rationale: Values above 1.0 indicate equity premium value; below indicates undervalued asset plays.
FinancialSnapshot.tobin_q_proxy = model.Property(f"{FinancialSnapshot} has {Float:tobin_q_proxy}")
model.define(FinancialSnapshot.tobin_q_proxy((FinancialSnapshot.market_capitalization + FinancialSnapshot.liabilities) / FinancialSnapshot.assets))


# --- 14. Growth Quality Trends, Payout Yields & Economic Differentials ---

# Interest Expense to Debt ratio checks general corporate borrow pricing.
FinancialSnapshot.interest_expense_to_debt_ratio = model.Property(f"{FinancialSnapshot} has {Float:interest_expense_to_debt_ratio}")
model.define(FinancialSnapshot.interest_expense_to_debt_ratio(FinancialSnapshot.interest_expense / FinancialSnapshot.total_debt))

# Fixed Charge Coverage Ratio Post-Tax evaluates solvency safety post corporate tax deductions.
FinancialSnapshot.fixed_charge_coverage_ratio_post_tax = model.Property(f"{FinancialSnapshot} has {Float:fixed_charge_coverage_ratio_post_tax}")
model.define(FinancialSnapshot.fixed_charge_coverage_ratio_post_tax(
    (FinancialSnapshot.operating_income_loss * (1.0 - FinancialSnapshot.effective_tax_rate) + FinancialSnapshot.lease_payments) /
    (FinancialSnapshot.interest_expense + FinancialSnapshot.lease_payments)
))

# Days Working Capital Outstanding represents days working capital funds operations.
FinancialSnapshot.days_working_capital_outstanding = model.Property(f"{FinancialSnapshot} has {Float:days_working_capital_outstanding}")
model.define(FinancialSnapshot.days_working_capital_outstanding((FinancialSnapshot.working_capital * 365.0) / FinancialSnapshot.revenue))

# Shareholder Payout Yield is total payouts divided by market cap.
# Rationale: Total cash yield generated for equity holders.
FinancialSnapshot.shareholder_payout_yield = model.Property(f"{FinancialSnapshot} has {Float:shareholder_payout_yield}")
model.define(FinancialSnapshot.shareholder_payout_yield((FinancialSnapshot.dividends_paid + FinancialSnapshot.share_repurchase_amount) / FinancialSnapshot.market_capitalization))


# --- 15. Quality of Earnings, Rollover Risk & Growth Capital Efficacy ---

# Net Debt to Capital compares net debt directly to total capital base.
FinancialSnapshot.net_debt_to_capital = model.Property(f"{FinancialSnapshot} has {Float:net_debt_to_capital}")
model.define(FinancialSnapshot.net_debt_to_capital(FinancialSnapshot.net_debt / (FinancialSnapshot.net_debt + FinancialSnapshot.equity)))

# Enterprise Value to Operating Cash compares EV to core cash flow generation.
# Rationale: Standard cash flow valuation multiple.
FinancialSnapshot.enterprise_value_to_operating_cash = model.Property(f"{FinancialSnapshot} has {Float:enterprise_value_to_operating_cash}")
model.define(FinancialSnapshot.enterprise_value_to_operating_cash(FinancialSnapshot.enterprise_value / FinancialSnapshot.net_cash_operating))

# Working Capital to Revenue evaluates working capital intensity trends.
FinancialSnapshot.working_capital_to_revenue = model.Property(f"{FinancialSnapshot} has {Float:working_capital_to_revenue}")
model.define(FinancialSnapshot.working_capital_to_revenue(FinancialSnapshot.working_capital / FinancialSnapshot.revenue))

# Free Cash Flow Quality Ratio compares cash generation to GAAP earnings.
# Rationale: Ratios below 1.0 indicate potential accrual manipulations or capital strains.
FinancialSnapshot.free_cash_flow_quality_ratio = model.Property(f"{FinancialSnapshot} has {Float:free_cash_flow_quality_ratio}")
model.define(FinancialSnapshot.free_cash_flow_quality_ratio(FinancialSnapshot.free_cash_flow_per_share / FinancialSnapshot.earnings_per_share_eps))

# Interest Expense to Operating Income evaluates debt servicing costs relative to EBIT.
FinancialSnapshot.interest_expense_to_operating_income = model.Property(f"{FinancialSnapshot} has {Float:interest_expense_to_operating_income}")
model.define(FinancialSnapshot.interest_expense_to_operating_income(FinancialSnapshot.interest_expense / FinancialSnapshot.operating_income_loss))

# Short Term Debt Rollover Ratio is current liabilities relative to total liabilities.
# Rationale: High ratios indicate refinancing pressures in rising interest rate periods.
FinancialSnapshot.short_term_debt_rollover_ratio = model.Property(f"{FinancialSnapshot} has {Float:short_term_debt_rollover_ratio}")
model.define(FinancialSnapshot.short_term_debt_rollover_ratio(FinancialSnapshot.current_liabilities / FinancialSnapshot.liabilities))

# Short Term Debt to Equity compares current liabilities directly to shareholder equity.
FinancialSnapshot.short_term_debt_to_equity = model.Property(f"{FinancialSnapshot} has {Float:short_term_debt_to_equity}")
model.define(FinancialSnapshot.short_term_debt_to_equity(FinancialSnapshot.current_liabilities / FinancialSnapshot.equity))

# Capital Expenditures to Assets tracks asset base expansion speeds.
FinancialSnapshot.capital_expenditures_to_assets = model.Property(f"{FinancialSnapshot} has {Float:capital_expenditures_to_assets}")
model.define(FinancialSnapshot.capital_expenditures_to_assets(FinancialSnapshot.capital_expenditures / FinancialSnapshot.assets))

# Maintenance Capex represents capital required to offset asset wear.
FinancialSnapshot.maintenance_capex_estimate = model.Property(f"{FinancialSnapshot} has {Float:maintenance_capex_estimate}")
model.define(FinancialSnapshot.maintenance_capex_estimate(FinancialSnapshot.depreciation_amortization * 1.0))

# Growth Capex calculates capital allocated directly to expansion plans.
FinancialSnapshot.growth_capex_estimate = model.Property(f"{FinancialSnapshot} has {Float:growth_capex_estimate}")
model.define(FinancialSnapshot.growth_capex_estimate(FinancialSnapshot.capital_expenditures - FinancialSnapshot.depreciation_amortization))
