import ontology
from ontology import model, FinancialSnapshot, SECStatement, Company
from pyrel_duckdb import Float, Integer, String, Boolean




# --- 1. DuPont Analysis & Profitability Rules ---

# Net Profit Margin measures the percentage of revenue remaining as net income after all expenses are paid.
# Rationale: Indication of pricing power and overall cost-control efficiency.
FinancialSnapshot.net_profit_margin = model.Property(f"{FinancialSnapshot} has {Float:net_profit_margin}")
model.define(FinancialSnapshot.net_profit_margin(FinancialSnapshot.earnings / FinancialSnapshot.revenue))

# Asset Turnover calculates revenue generated per dollar of assets.
# Rationale: Measures how efficiently a firm uses its asset base to drive sales.
FinancialSnapshot.asset_turnover = model.Property(f"{FinancialSnapshot} has {Float:asset_turnover}")
model.define(FinancialSnapshot.asset_turnover(FinancialSnapshot.revenue / FinancialSnapshot.assets))

# Equity Multiplier represents total assets divided by equity, measuring financial leverage.
# Rationale: Identifies how much debt is used to finance the asset base.
FinancialSnapshot.equity_multiplier = model.Property(f"{FinancialSnapshot} has {Float:equity_multiplier}")
model.define(FinancialSnapshot.equity_multiplier(FinancialSnapshot.assets / FinancialSnapshot.equity))

# DuPont Return on Equity (ROE) decomposes ROE into Profit Margin * Asset Turnover * Financial Leverage.
# Rationale: Helps pinpoint whether ROE is driven by profitability, operational efficiency, or high leverage.
FinancialSnapshot.dupont_roe = model.Property(f"{FinancialSnapshot} has {Float:dupont_roe}")
model.define(FinancialSnapshot.dupont_roe(FinancialSnapshot.net_profit_margin * FinancialSnapshot.asset_turnover * FinancialSnapshot.equity_multiplier))

# Gross Profit Margin measures profit relative to direct cost of goods sold.
# Rationale: Shows pricing markup capability and core manufacturing or service efficiency.
FinancialSnapshot.gross_profit_margin = model.Property(f"{FinancialSnapshot} has {Float:gross_profit_margin}")
model.define(FinancialSnapshot.gross_profit_margin(FinancialSnapshot.gross_profit / FinancialSnapshot.revenue))

# Operating Profit Margin measures operating income relative to net sales.
# Rationale: Evaluates profitability derived from core business activities, ignoring taxes and interest.
FinancialSnapshot.operating_profit_margin = model.Property(f"{FinancialSnapshot} has {Float:operating_profit_margin}")
model.define(FinancialSnapshot.operating_profit_margin(FinancialSnapshot.operating_income_loss / FinancialSnapshot.revenue))

# EBITDA Margin measures operating profitability before depreciation and amortization.
# Rationale: Standardizes operating cash profit capability across companies with different asset structures.
FinancialSnapshot.ebitda_margin = model.Property(f"{FinancialSnapshot} has {Float:ebitda_margin}")
model.define(FinancialSnapshot.ebitda_margin((FinancialSnapshot.operating_income_loss + FinancialSnapshot.depreciation_amortization) / FinancialSnapshot.revenue))

# Return on Assets (ROA) measures profit generated per unit of total assets.
# Rationale: A generic metric of overall capital efficiency.
FinancialSnapshot.roa = model.Property(f"{FinancialSnapshot} has {Float:roa}")
model.define(FinancialSnapshot.roa(FinancialSnapshot.earnings / FinancialSnapshot.assets))

# DuPont ROA decomposes ROA into profit margin multiplied by asset turnover.
# Rationale: Isolates operational drivers from financing structures.
FinancialSnapshot.dupont_roa = model.Property(f"{FinancialSnapshot} has {Float:dupont_roa}")
model.define(FinancialSnapshot.dupont_roa(FinancialSnapshot.net_profit_margin * FinancialSnapshot.asset_turnover))

# Return on Capital Employed (ROCE) is operating profit divided by total assets minus current liabilities.
# Rationale: Evaluates profitability comparing operating profits against long-term capital investments.
FinancialSnapshot.return_on_capital_employed_roce = model.Property(f"{FinancialSnapshot} has {Float:return_on_capital_employed_roce}")
model.define(FinancialSnapshot.return_on_capital_employed_roce(FinancialSnapshot.operating_income_loss / (FinancialSnapshot.assets - FinancialSnapshot.current_liabilities)))

# Tax Rate represents income tax expense relative to operating income.
# Rationale: Used to analyze corporate tax structures and net profit conversion.
FinancialSnapshot.tax_rate = model.Property(f"{FinancialSnapshot} has {Float:tax_rate}")
model.define(FinancialSnapshot.tax_rate(FinancialSnapshot.income_tax_expense / FinancialSnapshot.operating_income_loss))

# Return on Invested Capital (ROIC) calculates net operating profit after tax relative to total equity and debt.
# Rationale: Evaluates how efficiently a firm allocates capital under its control to profitable investments.
FinancialSnapshot.return_on_invested_capital_roic = model.Property(f"{FinancialSnapshot} has {Float:return_on_invested_capital_roic}")
model.define(FinancialSnapshot.return_on_invested_capital_roic(FinancialSnapshot.operating_income_loss * (1.0 - FinancialSnapshot.tax_rate) / (FinancialSnapshot.equity + FinancialSnapshot.total_debt)))

# Operating Return on Assets (ORA) is operating income divided by total assets.
# Rationale: Measures asset productivity before tax and financing costs.
FinancialSnapshot.operating_return_on_assets_ora = model.Property(f"{FinancialSnapshot} has {Float:operating_return_on_assets_ora}")
model.define(FinancialSnapshot.operating_return_on_assets_ora(FinancialSnapshot.operating_income_loss / FinancialSnapshot.assets))

# Operating Cash Flow Margin measures cash from operations relative to sales.
# Rationale: Confirms if revenue is converting to actual cash flow.
FinancialSnapshot.operating_cash_flow_margin = model.Property(f"{FinancialSnapshot} has {Float:operating_cash_flow_margin}")
model.define(FinancialSnapshot.operating_cash_flow_margin(FinancialSnapshot.net_cash_operating / FinancialSnapshot.revenue))

# Free Cash Flow Margin is free cash flow divided by revenue.
# Rationale: Assesses net cash flow left for equity holders relative to sales.
FinancialSnapshot.free_cash_flow_margin = model.Property(f"{FinancialSnapshot} has {Float:free_cash_flow_margin}")
model.define(FinancialSnapshot.free_cash_flow_margin((FinancialSnapshot.net_cash_operating - FinancialSnapshot.capital_expenditures) / FinancialSnapshot.revenue))

# Capital Intensity represents assets divided by revenue.
# Rationale: Measures the asset footprint required to generate a dollar of sales.
FinancialSnapshot.capital_intensity = model.Property(f"{FinancialSnapshot} has {Float:capital_intensity}")
model.define(FinancialSnapshot.capital_intensity(FinancialSnapshot.assets / FinancialSnapshot.revenue))


# --- 4. Efficiency & Capital Return Rules ---

# Asset Turnover Snapshot is a local alias for asset efficiency analysis.
FinancialSnapshot.asset_turnover_snapshot = model.Property(f"{FinancialSnapshot} has {Float:asset_turnover_snapshot}")
model.define(FinancialSnapshot.asset_turnover_snapshot(FinancialSnapshot.revenue / FinancialSnapshot.assets))

# Receivables Turnover measures how quickly a company collects outstanding credit sales.
# Rationale: High turnover indicates efficient collections and credit policies.
FinancialSnapshot.receivables_turnover = model.Property(f"{FinancialSnapshot} has {Float:receivables_turnover}")
model.define(FinancialSnapshot.receivables_turnover(FinancialSnapshot.revenue / FinancialSnapshot.accounts_receivable))

# Days Sales Outstanding (DSO) represents the average number of days it takes to collect cash from customers.
# Rationale: Higher days sales indicate worsening collections and potentially high client defaults.
FinancialSnapshot.days_sales_outstanding_dso = model.Property(f"{FinancialSnapshot} has {Float:days_sales_outstanding_dso}")
model.define(FinancialSnapshot.days_sales_outstanding_dso((FinancialSnapshot.accounts_receivable / FinancialSnapshot.revenue) * 365.0))

# Inventory Turnover calculates how many times inventory is sold and replaced over a year.
# Rationale: Evaluates storage costs and inventory demand.
FinancialSnapshot.inventory_turnover = model.Property(f"{FinancialSnapshot} has {Float:inventory_turnover}")
model.define(FinancialSnapshot.inventory_turnover(FinancialSnapshot.cogs / FinancialSnapshot.inventories))

# Days Inventory Outstanding (DIO) represents the average days inventory sits on shelves.
# Rationale: Worsening DIO indicates slow sales or over-purchasing.
FinancialSnapshot.days_inventory_outstanding_dio = model.Property(f"{FinancialSnapshot} has {Float:days_inventory_outstanding_dio}")
model.define(FinancialSnapshot.days_inventory_outstanding_dio((FinancialSnapshot.inventories / FinancialSnapshot.cogs) * 365.0))

# Payables Turnover measures the rate at which a company pays off suppliers.
# Rationale: Evaluates creditworthiness and supplier payment management.
FinancialSnapshot.payables_turnover = model.Property(f"{FinancialSnapshot} has {Float:payables_turnover}")
model.define(FinancialSnapshot.payables_turnover(FinancialSnapshot.cogs / FinancialSnapshot.accounts_payable))

# Days Payable Outstanding (DPO) represents average days taken to pay invoices.
# Rationale: Increasing DPO acts as short-term liquidity, but might damage supplier relationships.
FinancialSnapshot.days_payable_outstanding_dpo = model.Property(f"{FinancialSnapshot} has {Float:days_payable_outstanding_dpo}")
model.define(FinancialSnapshot.days_payable_outstanding_dpo((FinancialSnapshot.accounts_payable / FinancialSnapshot.cogs) * 365.0))

# Revenue per Employee divides sales by workforce count.
# Rationale: Evaluates overall workforce productivity.
FinancialSnapshot.revenue_per_employee = model.Property(f"{FinancialSnapshot} has {Float:revenue_per_employee}")
model.define(FinancialSnapshot.revenue_per_employee(FinancialSnapshot.revenue / FinancialSnapshot.employees))

# Net Income per Employee divides earnings by employee count.
# Rationale: Measures bottom-line worker productivity.
FinancialSnapshot.net_income_per_employee = model.Property(f"{FinancialSnapshot} has {Float:net_income_per_employee}")
model.define(FinancialSnapshot.net_income_per_employee(FinancialSnapshot.earnings / FinancialSnapshot.employees))

# Capital Returned Ratio is the total of buybacks and dividends divided by earnings.
# Rationale: Rationale tracks payout policy aggressiveness.
FinancialSnapshot.capital_returned_ratio = model.Property(f"{FinancialSnapshot} has {Float:capital_returned_ratio}")
model.define(FinancialSnapshot.capital_returned_ratio((FinancialSnapshot.share_repurchase_amount + FinancialSnapshot.dividends_paid) / FinancialSnapshot.earnings))

# Dividend Payout Ratio is dividends paid divided by earnings.
# Rationale: Assesses profit reinvestment vs distribution.
FinancialSnapshot.dividend_payout_ratio = model.Property(f"{FinancialSnapshot} has {Float:dividend_payout_ratio}")
model.define(FinancialSnapshot.dividend_payout_ratio(FinancialSnapshot.dividends_paid / FinancialSnapshot.earnings))

# Stock Price represents share value at statement filing.
FinancialSnapshot.stock_price = model.Property(f"{FinancialSnapshot} has {Float:stock_price}")
model.define(FinancialSnapshot.stock_price(SECStatement.stock_price_at_filing * 1.0)).where(
    FinancialSnapshot.ticker == SECStatement.ticker,
    FinancialSnapshot.fiscal_year == SECStatement.fiscal_year
)

# Market Capitalization is share price times shares outstanding.
FinancialSnapshot.market_capitalization = model.Property(f"{FinancialSnapshot} has {Float:market_capitalization}")
model.define(FinancialSnapshot.market_capitalization(FinancialSnapshot.stock_price * FinancialSnapshot.shares_outstanding))

# Buyback Yield is share buybacks divided by market capitalization.
# Rationale: Measures capital return yields generated through share buybacks.
FinancialSnapshot.buyback_yield = model.Property(f"{FinancialSnapshot} has {Float:buyback_yield}")
model.define(FinancialSnapshot.buyback_yield(FinancialSnapshot.share_repurchase_amount / FinancialSnapshot.market_capitalization))

# Worker Pay Ratio Dispersion compares CEO pay to median workers.
# Rationale: Used to analyze social governance pay ratios.
FinancialSnapshot.worker_pay_ratio_dispersion = model.Property(f"{FinancialSnapshot} has {Float:worker_pay_ratio_dispersion}")
model.define(FinancialSnapshot.worker_pay_ratio_dispersion(FinancialSnapshot.ceo_compensation / FinancialSnapshot.median_worker_pay))

# R&D Intensity (Pharma) is R&D expense divided by revenue.
# Rationale: Measures research spending aggressiveness in biotech/pharma sectors.
FinancialSnapshot.rnd_intensity_pharma = model.Property(f"{FinancialSnapshot} has {Float:rnd_intensity_pharma}")
model.define(FinancialSnapshot.rnd_intensity_pharma(FinancialSnapshot.rnd_expenses / FinancialSnapshot.revenue))

# R&D Intensity (Hardware) is hardware-focused R&D spending divided by revenue.
FinancialSnapshot.rnd_intensity_hardware = model.Property(f"{FinancialSnapshot} has {Float:rnd_intensity_hardware}")
model.define(FinancialSnapshot.rnd_intensity_hardware(FinancialSnapshot.rnd_spending / FinancialSnapshot.revenue))
