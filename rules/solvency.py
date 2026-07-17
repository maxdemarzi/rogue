import ontology
from ontology import model, FinancialSnapshot, Company, Bond
from pyrel_duckdb import Float, Integer, String, Boolean

# --- 2. Solvency & Debt Diligence Rules ---

# Debt to Assets calculates total debt relative to total assets.
# Rationale: Measures what percentage of assets are funded via debt obligations.
FinancialSnapshot.debt_to_assets = model.Property(f"{FinancialSnapshot} has {Float:debt_to_assets}")
model.define(FinancialSnapshot.debt_to_assets(FinancialSnapshot.total_debt / FinancialSnapshot.assets))

# Debt to Equity compares total debt directly to shareholder equity.
# Rationale: Identifies corporate leverage profiles and balance sheet safety boundaries.
FinancialSnapshot.debt_to_equity = model.Property(f"{FinancialSnapshot} has {Float:debt_to_equity}")
model.define(FinancialSnapshot.debt_to_equity(FinancialSnapshot.total_debt / FinancialSnapshot.equity))

# Financial Leverage is total assets divided by equity.
# Rationale: Measures asset amplification driven by all liabilities.
FinancialSnapshot.financial_leverage = model.Property(f"{FinancialSnapshot} has {Float:financial_leverage}")
model.define(FinancialSnapshot.financial_leverage(FinancialSnapshot.assets / FinancialSnapshot.equity))

# Debt to Capital is total debt divided by total capital (debt + equity).
# Rationale: Provides a standardized ratio of capital structure debt mix.
FinancialSnapshot.debt_to_capital = model.Property(f"{FinancialSnapshot} has {Float:debt_to_capital}")
model.define(FinancialSnapshot.debt_to_capital(FinancialSnapshot.total_debt / (FinancialSnapshot.total_debt + FinancialSnapshot.equity)))

# Interest Coverage Ratio is operating profit divided by interest expense.
# Rationale: Measures capability to meet debt servicing costs from current operating profits.
FinancialSnapshot.interest_coverage_ratio = model.Property(f"{FinancialSnapshot} has {Float:interest_coverage_ratio}")
model.define(FinancialSnapshot.interest_coverage_ratio(FinancialSnapshot.operating_income_loss / FinancialSnapshot.interest_expense))

# Cash Interest Coverage is operating cash inflows relative to interest paid.
# Rationale: Provides cash-flow level safety check on capability to meet debt costs.
FinancialSnapshot.cash_interest_coverage = model.Property(f"{FinancialSnapshot} has {Float:cash_interest_coverage}")
model.define(FinancialSnapshot.cash_interest_coverage((FinancialSnapshot.net_cash_operating + FinancialSnapshot.interest_paid + FinancialSnapshot.taxes_paid) / FinancialSnapshot.interest_paid))

# Debt Service Coverage Ratio is operating income divided by total debt service obligations (interest + principal).
# Rationale: Primary metric used by lenders to assess credit safety headroom.
FinancialSnapshot.debt_service_coverage = model.Property(f"{FinancialSnapshot} has {Float:debt_service_coverage}")
model.define(FinancialSnapshot.debt_service_coverage(FinancialSnapshot.operating_income_loss / (FinancialSnapshot.interest_paid + FinancialSnapshot.principal_payments)))

# Leverage Multiple (Debt to EBITDA) calculates total debt divided by operating cash profits (EBITDA).
# Rationale: Standard leverage metric indicating how many years of EBITDA are required to repay outstanding debt.
FinancialSnapshot.leverage_multiple_ebitda = model.Property(f"{FinancialSnapshot} has {Float:leverage_multiple_ebitda}")
model.define(FinancialSnapshot.leverage_multiple_ebitda(FinancialSnapshot.total_debt / (FinancialSnapshot.operating_income_loss + FinancialSnapshot.depreciation_amortization)))

# Net Debt to EBITDA is total debt minus cash, divided by EBITDA.
# Rationale: Focuses on net debt obligations assuming cash reserves could be used to repay debt immediately.
FinancialSnapshot.net_debt_to_ebitda = model.Property(f"{FinancialSnapshot} has {Float:net_debt_to_ebitda}")
model.define(FinancialSnapshot.net_debt_to_ebitda((FinancialSnapshot.total_debt - FinancialSnapshot.cash_and_equivalents) / (FinancialSnapshot.operating_income_loss + FinancialSnapshot.depreciation_amortization)))

# Long-term Debt to Equity compares only non-current debt to shareholder equity.
# Rationale: Focuses on long-term funding leverage risks.
FinancialSnapshot.lt_debt_to_equity = model.Property(f"{FinancialSnapshot} has {Float:lt_debt_to_equity}")
model.define(FinancialSnapshot.lt_debt_to_equity(FinancialSnapshot.long_term_debt / FinancialSnapshot.equity))

# Cash Flow to Debt divides operating cash flow by total debt.
# Rationale: High percentages indicate strong organic capability to pay off debt obligations.
FinancialSnapshot.cash_flow_to_debt = model.Property(f"{FinancialSnapshot} has {Float:cash_flow_to_debt}")
model.define(FinancialSnapshot.cash_flow_to_debt(FinancialSnapshot.net_cash_operating / FinancialSnapshot.total_debt))

# Book Value per Share is total equity divided by shares outstanding.
# Rationale: Represents the theoretical value of equity if assets are liquidated.
FinancialSnapshot.book_value_per_share = model.Property(f"{FinancialSnapshot} has {Float:book_value_per_share}")
model.define(FinancialSnapshot.book_value_per_share(FinancialSnapshot.equity / FinancialSnapshot.shares_outstanding))

# Tangible Book Value per Share excludes intangibles from equity.
# Rationale: Strict valuation metric focusing only on physical and liquid net asset structures.
FinancialSnapshot.tangible_book_value = model.Property(f"{FinancialSnapshot} has {Float:tangible_book_value}")
model.define(FinancialSnapshot.tangible_book_value((FinancialSnapshot.equity - FinancialSnapshot.intangible_assets) / FinancialSnapshot.shares_outstanding))

# Leveraged Issuer flags companies with debt-to-equity ratios above 2.0.
# Rationale: High leverage alert for corporate credit assessments.
Company.is_leveraged_issuer = model.Property(f"{Company} is leveraged issuer {Boolean:is_leveraged_issuer}")
model.define(Company.is_leveraged_issuer(True)).where(
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.debt_to_equity > 2.0
)

# Speculative Bond flags bonds with credit ratings B or CCC.
# Rationale: High risk bond asset indicators.
Bond.is_speculative_bond = model.Property(f"{Bond} is speculative bond {Boolean:is_speculative_bond}")
model.define(Bond.is_speculative_bond(True)).where(Bond.credit_rating == "B")
model.define(Bond.is_speculative_bond(True)).where(Bond.credit_rating == "CCC")


# --- 3. Liquidity & Cash Flow Rules ---

# Working Capital is current assets minus current liabilities.
# Rationale: Measures short-term operating capital headroom.
FinancialSnapshot.working_capital = model.Property(f"{FinancialSnapshot} has {Float:working_capital}")
model.define(FinancialSnapshot.working_capital(FinancialSnapshot.current_assets - FinancialSnapshot.current_liabilities))

# Current Ratio is current assets divided by current liabilities.
# Rationale: Essential indicator of capability to meet short-term liabilities.
FinancialSnapshot.current_ratio = model.Property(f"{FinancialSnapshot} has {Float:current_ratio}")
model.define(FinancialSnapshot.current_ratio(FinancialSnapshot.current_assets / FinancialSnapshot.current_liabilities))

# Cash Ratio compares only cash and cash equivalents to current liabilities.
# Rationale: Strictest measure of short-term cash coverage.
FinancialSnapshot.cash_ratio = model.Property(f"{FinancialSnapshot} has {Float:cash_ratio}")
model.define(FinancialSnapshot.cash_ratio(FinancialSnapshot.cash_and_equivalents / FinancialSnapshot.current_liabilities))

# Quick Ratio (Acid-Test) excludes inventory from current assets before dividing by current liabilities.
# Rationale: Focuses on quick-liquid assets, ignoring potentially slow-moving inventory.
FinancialSnapshot.quick_ratio = model.Property(f"{FinancialSnapshot} has {Float:quick_ratio}")
model.define(FinancialSnapshot.quick_ratio((FinancialSnapshot.current_assets - FinancialSnapshot.inventories) / FinancialSnapshot.current_liabilities))

# Net Working Capital to Assets is working capital divided by assets.
# Rationale: Indicates capital liquidity relative to company size.
FinancialSnapshot.net_working_capital_to_assets = model.Property(f"{FinancialSnapshot} has {Float:net_working_capital_to_assets}")
model.define(FinancialSnapshot.net_working_capital_to_assets(FinancialSnapshot.working_capital / FinancialSnapshot.assets))

# Working Capital Turnover is revenue divided by working capital.
# Rationale: Measures how efficiently working capital generates sales volume.
FinancialSnapshot.working_capital_turnover = model.Property(f"{FinancialSnapshot} has {Float:working_capital_turnover}")
model.define(FinancialSnapshot.working_capital_turnover(FinancialSnapshot.revenue / FinancialSnapshot.working_capital))

# Cash Burn Rate is negative operating cash flow divided by 12.
# Rationale: Monthly operating cash deficit estimation for distressed entities.
FinancialSnapshot.cash_burn_rate = model.Property(f"{FinancialSnapshot} has {Float:cash_burn_rate}")
model.define(FinancialSnapshot.cash_burn_rate((0.0 - FinancialSnapshot.net_cash_operating) / 12.0))

# Cash Runway calculates how many months cash reserves will last based on burn rate.
# Rationale: Vital metric for distressed and pre-revenue startups.
FinancialSnapshot.cash_runway_months = model.Property(f"{FinancialSnapshot} has {Float:cash_runway_months}")
model.define(FinancialSnapshot.cash_runway_months(FinancialSnapshot.cash_and_equivalents / FinancialSnapshot.cash_burn_rate))

# Operating Cash Flow to Current Liabilities compares annual operating cash to short-term liabilities.
# Rationale: Measures short-term obligations coverage directly from core operations cash flows.
FinancialSnapshot.operating_cash_flow_to_current_liabilities = model.Property(f"{FinancialSnapshot} has {Float:operating_cash_flow_to_current_liabilities}")
model.define(FinancialSnapshot.operating_cash_flow_to_current_liabilities(FinancialSnapshot.net_cash_operating / FinancialSnapshot.current_liabilities))


# Liquidity Distressed flags companies with current ratios below 1.0 and quick ratios below 0.8.
# Rationale: Builds on current_ratio and quick_ratio to identify near-term default risks.
FinancialSnapshot.is_liquidity_distressed = model.Property(f"{FinancialSnapshot} is liquidity distressed {Boolean:is_liquidity_distressed}")
model.define(FinancialSnapshot.is_liquidity_distressed(True)).where(
    FinancialSnapshot.current_ratio < 1.0,
    FinancialSnapshot.quick_ratio < 0.8
)

# Solvency Distressed flags companies with long-term debt-to-equity exceeding 2.0 and interest coverage below 1.5.
# Rationale: Builds on lt_debt_to_equity and interest_coverage_ratio to identify structural funding distress.
FinancialSnapshot.is_solvency_distressed = model.Property(f"{FinancialSnapshot} is solvency distressed {Boolean:is_solvency_distressed}")
model.define(FinancialSnapshot.is_solvency_distressed(True)).where(
    FinancialSnapshot.lt_debt_to_equity > 2.0,
    FinancialSnapshot.interest_coverage_ratio < 1.5
)

# Financial Distressed flags companies suffering from both liquidity constraints and solvency issues.
# Rationale: Builds on top of is_liquidity_distressed and is_solvency_distressed to identify critical defaults.
FinancialSnapshot.is_financial_distressed = model.Property(f"{FinancialSnapshot} is financially distressed {Boolean:is_financial_distressed}")
model.define(FinancialSnapshot.is_financial_distressed(True)).where(
    FinancialSnapshot.is_liquidity_distressed == True,
    FinancialSnapshot.is_solvency_distressed == True
)


# Retained Earnings to Assets is retained earnings divided by assets.
# Rationale: Analyzes how much of the assets have been built using retained earnings rather than debt or share issuances.
FinancialSnapshot.retained_earnings_to_assets = model.Property(f"{FinancialSnapshot} has {Float:retained_earnings_to_assets}")
model.define(FinancialSnapshot.retained_earnings_to_assets(FinancialSnapshot.retained_earnings / FinancialSnapshot.assets))

# Daily Operating Expenses represents daily corporate running costs.
# Rationale: Daily cash outflow metric.
FinancialSnapshot.daily_operating_expenses = model.Property(f"{FinancialSnapshot} has {Float:daily_operating_expenses}")
model.define(FinancialSnapshot.daily_operating_expenses((FinancialSnapshot.revenue - FinancialSnapshot.operating_income_loss) / 365.0))

# Days Cash on Hand represents cash reserves divided by daily operating costs.
# Rationale: Days a company could survive without any new revenues.
FinancialSnapshot.days_cash_on_hand = model.Property(f"{FinancialSnapshot} has {Float:days_cash_on_hand}")
model.define(FinancialSnapshot.days_cash_on_hand((FinancialSnapshot.cash_and_equivalents * 365.0) / FinancialSnapshot.daily_operating_expenses))

# Defensive Interval Ratio is current assets divided by daily operating expenses.
# Rationale: Standard metric representing how long current assets can fund operations before new financing is needed.
FinancialSnapshot.defensive_interval_ratio = model.Property(f"{FinancialSnapshot} has {Float:defensive_interval_ratio}")
model.define(FinancialSnapshot.defensive_interval_ratio(FinancialSnapshot.current_assets / FinancialSnapshot.daily_operating_expenses))

# Liquidity Distressed flags firms with current ratios below 1.0.
# Rationale: Early alert for short-term working capital distress.
Company.is_liquidity_distressed = model.Property(f"{Company} is liquidity distressed {Boolean:is_liquidity_distressed}")
model.define(Company.is_liquidity_distressed(True)).where(
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.current_ratio < 1.0
)

# Cash Constrained flags firms with cash runway under 6 months.
# Rationale: Immediate warning for fundraising or cash saving needs.
Company.is_cash_constrained = model.Property(f"{Company} is cash constrained {Boolean:is_cash_constrained}")
model.define(Company.is_cash_constrained(True)).where(
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.cash_runway_months < 6.0
)


# --- 11. Advanced Leverage Coverage & Value Metrics ---

# Lease Payments represent contract obligations.
# Rationale: Used in fixed charge coverage calculations.
FinancialSnapshot.lease_payments = model.Property(f"{FinancialSnapshot} has {Float:lease_payments}")
model.define(FinancialSnapshot.lease_payments(0.0 * 1.0))

# Fixed Charge Coverage Ratio (FCCR) is (EBIT + Leases) / (Interest + Leases).
# Rationale: Stricter coverage ratio analyzing capability to service fixed lease agreements as well as interest.
FinancialSnapshot.fixed_charge_coverage_ratio_fccr = model.Property(f"{FinancialSnapshot} has {Float:fixed_charge_coverage_ratio_fccr}")
model.define(FinancialSnapshot.fixed_charge_coverage_ratio_fccr((FinancialSnapshot.operating_income_loss + FinancialSnapshot.lease_payments) / (FinancialSnapshot.interest_expense + FinancialSnapshot.lease_payments)))

# Times Interest Earned (TIE) is EBIT / Interest Expense.
# Rationale: Standard solvency metric for corporate credit analysis.
FinancialSnapshot.times_interest_earned = model.Property(f"{FinancialSnapshot} has {Float:times_interest_earned}")
model.define(FinancialSnapshot.times_interest_earned(FinancialSnapshot.operating_income_loss / FinancialSnapshot.interest_expense))


# Operating Profit Margin Post-Tax is net operating profit after tax relative to revenue.
# Rationale: Tracks real corporate profit margins from core business segments.
FinancialSnapshot.operating_profit_margin_post_tax = model.Property(f"{FinancialSnapshot} has {Float:operating_profit_margin_post_tax}")
model.define(FinancialSnapshot.operating_profit_margin_post_tax(FinancialSnapshot.operating_income_loss * (1.0 - FinancialSnapshot.tax_rate) / FinancialSnapshot.revenue))

# Invested Capital Turnover is revenue divided by invested capital.
# Rationale: Measures sales efficiency of the capital invested.
FinancialSnapshot.invested_capital_turnover = model.Property(f"{FinancialSnapshot} has {Float:invested_capital_turnover}")
model.define(FinancialSnapshot.invested_capital_turnover(FinancialSnapshot.revenue / (FinancialSnapshot.equity + FinancialSnapshot.total_debt - FinancialSnapshot.cash_and_equivalents)))

# DuPont ROIC decomposes ROIC into post-tax profit margin and invested capital turnover.
# Rationale: Pinpoints efficiency drivers of invested capital return metrics.
FinancialSnapshot.dupont_roic = model.Property(f"{FinancialSnapshot} has {Float:dupont_roic}")
model.define(FinancialSnapshot.dupont_roic(FinancialSnapshot.operating_profit_margin_post_tax * FinancialSnapshot.invested_capital_turnover))

# Free Cash Flow Yield is FCF per share divided by stock price.
# Rationale: Equity valuation tool comparing cash flow generated directly to valuation pricing.
FinancialSnapshot.fcf_yield = model.Property(f"{FinancialSnapshot} has {Float:fcf_yield}")
model.define(FinancialSnapshot.fcf_yield(FinancialSnapshot.free_cash_flow_per_share / FinancialSnapshot.stock_price))

# Earnings Yield is the inverse of the PE ratio.
# Rationale: Standardizes equity yields to compare directly with bond yields.
FinancialSnapshot.earnings_yield = model.Property(f"{FinancialSnapshot} has {Float:earnings_yield}")
model.define(FinancialSnapshot.earnings_yield(1.0 / FinancialSnapshot.pe_multiple))


# Sustainable Growth Rate is ROE multiplied by retention ratio (1 - Payout Ratio).
# Rationale: Estimates max organic growth rate without raising additional debt or equity.
FinancialSnapshot.sustainable_growth_rate = model.Property(f"{FinancialSnapshot} has {Float:sustainable_growth_rate}")
model.define(FinancialSnapshot.sustainable_growth_rate(FinancialSnapshot.dupont_roe * (1.0 - FinancialSnapshot.dividend_payout_ratio)))

# Has Outstanding Bonds flags issuers with active debt obligations in corporate bond markets.
# Rationale: Identifies companies utilizing public bond markets for capital.
Company.has_outstanding_bonds = model.Property(f"{Company} has outstanding bonds {Boolean:has_outstanding_bonds}")
model.define(Company.has_outstanding_bonds(True)).where(
    Bond.symbol == Company.ticker
)

# Has High Yield Bonds flags issuers paying high coupon rates on their active bonds.
# Rationale: Key indicator of high borrowing costs in public credit markets.
Company.has_high_yield_bonds = model.Property(f"{Company} has high yield bonds {Boolean:has_high_yield_bonds}")
model.define(Company.has_high_yield_bonds(True)).where(
    Bond.symbol == Company.ticker,
    Bond.coupon_rate > 0.06
)

# Investment Grade Bond Issuer flags companies with outstanding bonds holding AAA, AA, A, or BBB ratings.
# Rationale: Indicates institutional-grade credit safety profiles.
Company.is_investment_grade_bond_issuer = model.Property(f"{Company} is investment grade bond issuer {Boolean:is_investment_grade_bond_issuer}")
model.define(Company.is_investment_grade_bond_issuer(True)).where(
    Bond.symbol == Company.ticker,
    Bond.credit_rating == "AAA"
)
model.define(Company.is_investment_grade_bond_issuer(True)).where(
    Bond.symbol == Company.ticker,
    Bond.credit_rating == "AA"
)
model.define(Company.is_investment_grade_bond_issuer(True)).where(
    Bond.symbol == Company.ticker,
    Bond.credit_rating == "A"
)
model.define(Company.is_investment_grade_bond_issuer(True)).where(
    Bond.symbol == Company.ticker,
    Bond.credit_rating == "BBB"
)

# Junk Bond Issuer flags companies issuing high-risk speculative grade bonds.
# Rationale: Higher-tier nested rule building on is_speculative_bond.
Company.is_junk_bond_issuer = model.Property(f"{Company} is junk bond issuer {Boolean:is_junk_bond_issuer}")
model.define(Company.is_junk_bond_issuer(True)).where(
    Bond.symbol == Company.ticker,
    Bond.is_speculative_bond == True
)

# Bond Refinancing Stress flags junk bond issuers who are also facing overall balance sheet solvency strains.
# Rationale: Higher-tier nested rule building on is_junk_bond_issuer and is_solvency_distressed.
Company.bond_refinancing_stress = model.Property(f"{Company} has bond refinancing stress {Boolean:bond_refinancing_stress}")
model.define(Company.bond_refinancing_stress(True)).where(
    Company.is_junk_bond_issuer == True,
    FinancialSnapshot.ticker == Company.ticker,
    FinancialSnapshot.is_solvency_distressed == True
)


