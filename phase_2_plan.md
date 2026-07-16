## 🧬 Phase 2: Swan Rules & Financial Calculations

We define **240 declarative Datalog derived rules** inside `rules.py` categorized across 16 business domains:

### 1. DuPont Analysis & Profitability Rules (15 Rules)
* **`net_profit_margin`**: `net_income_loss / total_revenue`
* **`asset_turnover`**: `total_revenue / total_assets`
* **`equity_multiplier`**: `total_assets / stockholders_equity`
* **`dupont_roe`**: `net_profit_margin * asset_turnover * equity_multiplier`
* **`gross_profit_margin`**: `gross_profit / revenue`
* **`operating_profit_margin`**: `operating_income_loss / total_revenue`
* **`ebitda_margin`**: `(operating_income_loss + depreciation_amortization) / total_revenue`
* **`roa`**: `net_income_loss / total_assets`
* **`dupont_roa`**: `net_profit_margin * asset_turnover`
* **`return_on_capital_employed_roce`**: `operating_income_loss / (total_assets - current_liabilities)`
* **`return_on_invested_capital_roic`**: `operating_income_loss * (1 - tax_rate) / (equity + total_debt)`
* **`operating_return_on_assets_ora`**: `operating_income_loss / total_assets`
* **`operating_cash_flow_margin`**: `net_cash_operating / revenue`
* **`free_cash_flow_margin`**: `(net_cash_operating - capital_expenditures) / revenue`
* **`capital_intensity`**: `total_assets / total_revenue`

### 2. Solvency & Debt Diligence Rules (15 Rules)
* **`debt_to_assets`**: `total_liabilities / total_assets`
* **`debt_to_equity`**: `total_liabilities / stockholders_equity`
* **`financial_leverage`**: `total_assets / stockholders_equity`
* **`debt_to_capital`**: `total_debt / (total_debt + stockholders_equity)`
* **`interest_coverage_ratio`**: `operating_income_loss / interest_expense`
* **`cash_interest_coverage`**: `(net_cash_operating + interest_paid + taxes_paid) / interest_paid`
* **`debt_service_coverage`**: `operating_income_loss / (interest_paid + principal_payments)`
* **`leverage_multiple_ebitda`**: `total_debt / ebitda`
* **`net_debt_to_ebitda`**: `(total_debt - cash_and_equivalents) / ebitda`
* **`lt_debt_to_equity`**: `long_term_debt / stockholders_equity`
* **`cash_flow_to_debt`**: `net_cash_operating / total_liabilities`
* **`book_value_per_share`**: `stockholders_equity / common_stock_shares_issued`
* **`tangible_book_value`**: `(stockholders_equity - intangible_assets) / common_stock_shares_issued`
* **`is_leveraged_issuer`**: Unary alert relationship if `debt_to_equity > 2.0`
* **`is_speculative_bond`**: Unary alert relationship if `Bond.credit_rating` links to speculative grade (`B`, `CCC`).

### 3. Liquidity & Cash Flow Rules (15 Rules)
* **`working_capital`**: `current_assets - current_liabilities`
* **`current_ratio`**: `current_assets / current_liabilities`
* **`cash_ratio`**: `cash_and_equivalents / current_liabilities`
* **`quick_ratio`**: `(current_assets - inventories) / current_liabilities`
* **`net_working_capital_to_assets`**: `working_capital / total_assets`
* **`working_capital_turnover`**: `total_revenue / working_capital`
* **`cash_burn_rate`**: Monthly negative `net_cash_operating` run-rate.
* **`cash_runway_months`**: `cash_and_equivalents / cash_burn_rate`
* **`operating_cash_flow_to_current_liabilities`**: `net_cash_operating / current_liabilities`
* **`retained_earnings_to_assets`**: `retained_earnings / total_assets` (Altman variable)
* **`days_cash_on_hand`**: `(cash_and_equivalents * 365) / daily_operating_expenses`
* **`defensive_interval_ratio`**: `current_assets / daily_operating_expenses`
* **`cash_conversion_cycle_ccc`**: `days_inventory_outstanding + days_sales_outstanding - days_payable_outstanding`
* **`is_liquidity_distressed`**: Unary alert relationship if `current_ratio < 1.0`
* **`is_cash_constrained`**: Unary alert relationship if `cash_runway_months < 6`

### 4. Efficiency & Capital Return Rules (15 Rules)
* **`asset_turnover_snapshot`**: `revenue / assets`
* **`receivables_turnover`**: `total_revenue / accounts_receivable`
* **`days_sales_outstanding_dso`**: `(accounts_receivable / total_revenue) * 365`
* **`inventory_turnover`**: `cogs / inventory`
* **`days_inventory_outstanding_dio`**: `(inventory / cogs) * 365`
* **`payables_turnover`**: `cogs / accounts_payable`
* **`days_payable_outstanding_dpo`**: `(accounts_payable / cogs) * 365`
* **`revenue_per_employee`**: `revenue / employees`
* **`net_income_per_employee`**: `earnings / employees`
* **`capital_returned_ratio`**: `(share_repurchase_amount + dividends_paid) / net_income_loss`
* **`dividend_payout_ratio`**: `dividends_paid / net_income_loss`
* **`buyback_yield`**: `share_repurchase_amount / market_capitalization`
* **`worker_pay_ratio_dispersion`**: `ceo_compensation / median_worker_pay`
* **`rnd_intensity_pharma`**: `rnd_expenses / revenue`
* **`rnd_intensity_hardware`**: `rnd_spending / revenue`

### 5. Governance & Interlock Risk Rules (10 Rules)
* **`is_governance_risk`**: Alert if `worker_pay_ratio > 300` and `InsiderTransaction.conviction_score > 0.8`
* **`is_interlocked_director`**: Alert if `BoardMemberName` sits on $>2$ Fortune 100 boards.
* **`is_insider_quiet_window_trade`**: Alert if `InsiderTransaction` date falls within 30 days before `EarningsEstimate.earnings_date`.
* **`insider_sell_ratio`**: `total_disposed_shares / (total_acquired_shares + total_disposed_shares)`
* **`is_insider_panic_selling`**: Alert if `insider_sell_ratio > 0.9` and `BankruptcyRisk.probability > 0.05`.
* **`board_independence_ratio`**: `independent_directors / total_board_members`
* **`is_entrenched_board`**: Alert if board members' average tenure $>12$ years.
* **`compensation_growth_vs_net_income`**: `ceo_pay_growth_pct / net_income_growth_pct`
* **`dilution_risk`**: `executive_stock_dilution / share_repurchase_amount`
* **`is_governance_outlier`**: Alert if `is_governance_risk` and `is_entrenched_board` are both true.

### 6. B2B Value-Chain & Contagion Risk Rules (15 Rules)
* **`is_distressed_supplier`**: Alert if `Company.supplies_to(Customer)` and `Customer.bankruptcy_risk_probability > 0.10`.
* **`downstream_revenue_exposure`**: Sum of revenue shares from distressed clients.
* **`is_systemic_supplier`**: Alert if a company supplies products to $>5$ public companies.
* **`upstream_supply_concentration`**: Percent of products sourced from a single supplier.
* **`write_off_credit_exposure`**: Estimated trade credit default = `downstream_revenue_exposure * customer_default_probability`
* **`naics_contagion_factor`**: Sector-level default risk weight based on NAICS links.
* **`days_sales_outstanding_mismatch`**: `Supplier.dso - Customer.dpo`
* **`value_chain_liquidity_gap`**: Gap in days sales outstanding across multi-hop supplier chains.
* **`contagion_risk_score`**: Bipartite PageRank multiplier over the supplier graph.
* **`is_single_point_of_failure`**: Alert if a company is the sole vendor of a critical NAICS component.
* **`supplier_insolvency_alert`**: Alert if `is_distressed_supplier` and `supplier_debt_to_equity > 2.0`.
* **`customer_concentration_risk`**: Alert if any single customer represents $>20\%$ of revenues.
* **`working_capital_squeeze`**: Alert if DSO is rising while DPO is falling.
* **`supply_chain_lead_time_cost`**: manufacturing costs normalized by shipping routes.
* **`value_chain_restructuring_threat`**: Aggregate default probability of all linked domain nodes.

### 7. Macro, Carry Trade & Arbitrage Rules (15 Rules)
* **`sovereign_debt_to_gdp`**: sovereign debt ratio / GDP.
* **`is_speculative_grade`**: Alert if rating foreign currency grade is speculative (`B`, `CCC`).
* **`interest_rate_spread`**: `BAA10Y - AAA10Y` (corporate default risk premium).
* **`yield_curve_inversion`**: `T10Y2Y < 0.0` (recession predictor).
* **`inflation_momentum`**: Annual rate change in national consumer price index.
* **`purchasing_power_parity_gap`**: `local_inflation_rate - us_inflation_rate`
* **`carry_trade_spread`**: `local_policy_rate - fed_funds_rate`
* **`sovereign_rating_momentum`**: Numeric shift in credit grade actions (upgrades vs downgrades).
* **`real_yield_premium`**: `carry_trade_spread - purchasing_power_parity_gap`
* **`sovereign_debt_service_ratio`**: Government debt payments / GDP.
* **`economic_freedom_rank`**: Sorted score of economic freedom indicators.
* **`is_capital_flight_risk`**: Alert if currency depreciation $>10\%$ paired with negative yield spreads.
* **`arbitrage_index`**: Cross-border valuation differences for identical ISIN/LEI listings.
* **`uk_cost_of_living_stress`**: longitudinal difference between average wages and CPI.
* **`sweden_interest_inflation_spread`**: Swedish Riksbank policy rate minus CPI.

### 8. Sector Specialty Ratios (Aviation, Pharma, Semiconductor) (15 Rules)
* **`airline_passenger_mile_yield`**: `passenger_revenue / passenger_count`
* **`airline_capacity_utilization`**: Passenger traffic load factor.
* **`airline_fuel_efficiency`**: passenger count divided by fuel cost share.
* **`is_high_incident_airline`**: Alert if fatalities in `AviationIncident` $>50$.
* **`airline_operating_efficiency`**: passenger revenue divided by route operating cost.
* **`biotech_trial_success_rate_phase_3`**: FDA approvals / clinical phase 3 trials count.
* **`biotech_rnd_efficiency`**: FDA approvals / R&D intensity ratio.
* **`is_pharma_acquisition_target`**: Alert if R&D intensity $>0.20$ and approvals count is zero.
* **`disease_burden_market_opportunity`**: global cases divided by total phase 3 trials.
* **`semiconductor_fab_utilization`**: `capacity_wspm / total_fab_capacity`
* **`semiconductor_rnd_leverage`**: semiconductor revenue / R&D spending.
* **`semiconductor_price_momentum`**: year-over-year shift in chip spot prices.
* **`semiconductor_export_exposure`**: count of export restricted entities linked to a chip firm.
* **`semiconductor_distress_alert`**: Alert if spot prices drop $>20\%$ paired with fab capacity reductions.
* **`vertical_integration_multiple`**: M&A value divided by target R&D spend.

### 9. Growth, Valuation Drivers & Per-Share Metrics (16 Rules)
* **`revenue_growth_yoy`**: `(total_revenue_t - total_revenue_t_minus_1) / total_revenue_t_minus_1`
* **`net_income_growth_yoy`**: `(net_income_loss_t - net_income_loss_t_minus_1) / net_income_loss_t_minus_1`
* **`operating_income_growth_yoy`**: `(operating_income_t - operating_income_t_minus_1) / operating_income_t_minus_1`
* **`earnings_per_share_eps`**: `net_income_loss / common_stock_shares_issued`
* **`revenue_per_share`**: `total_revenue / common_stock_shares_issued`
* **`free_cash_flow_per_share`**: `(net_cash_operating - capital_expenditures) / common_stock_shares_issued`
* **`operating_cash_flow_per_share`**: `net_cash_operating / common_stock_shares_issued`
* **`net_debt`**: `total_liabilities - cash_and_equivalents`
* **`net_debt_to_equity`**: `net_debt / stockholders_equity`
* **`tangible_assets`**: `total_assets - intangible_assets`
* **`tangible_equity`**: `stockholders_equity - intangible_assets`
* **`tangible_debt_to_equity`**: `total_liabilities / tangible_equity`
* **`cogs_margin`**: `cogs / total_revenue`
* **`effective_tax_rate`**: `income_tax_expense / operating_income_loss`
* **`real_interest_rate`**: `macro_indicator_value - country_inflation_rate`
* **`insider_net_buying_usd`**: `sum(acquired_shares * transaction_price) - sum(disposed_shares * transaction_price)`

### 10. Advanced Financial Strength & Predictive Analytics (19 Rules)
* **`altman_z_score`**: Solvency credit check: `1.2 * X1 + 1.4 * X2 + 3.3 * X3 + 0.6 * X4 + 0.999 * X5`
* **`is_altman_distress_zone`**: Unary alert relationship if `altman_z_score < 1.81`
* **`is_altman_gray_zone`**: Unary alert relationship if `1.81 <= altman_z_score <= 2.99`
* **`is_altman_safe_zone`**: Unary alert relationship if `altman_z_score > 2.99`
* **`piotroski_f_score`**: Integer (0 to 9) measuring firm fundamental quality based on margins, leverage, and cash flow.
* **`is_high_piotroski_score`**: Unary classification relationship if `piotroski_f_score >= 8`
* **`is_low_piotroski_score`**: Unary alert relationship if `piotroski_f_score <= 2`
* **`beneish_m_score`**: Probability index identifying earnings manipulation.
* **`is_earnings_manipulator`**: Unary alert relationship if `beneish_m_score > -1.78`
* **`capex_to_depreciation`**: `CapitalExpenditures / Depreciation`
* **`reinvestment_rate`**: `(CapitalExpenditures + RndExpenses - Depreciation) / OperatingIncome`
* **`pe_multiple`**: `StockPrice / EarningsPerShare`
* **`ps_multiple`**: `StockPrice / RevenuePerShare`
* **`pb_multiple`**: `StockPrice / BookValuePerShare`
* **`market_capitalization`**: `StockPrice * common_stock_shares_issued`
* **`enterprise_value`**: `market_capitalization + total_debt - cash_and_equivalents`
* **`ev_to_revenue`**: `enterprise_value / total_revenue`
* **`ev_to_ebitda`**: `enterprise_value / ebitda`
* **`price_to_fcf`**: `StockPrice / free_cash_flow_per_share`

### 11. Advanced Leverage Coverage & Value Metrics (15 Rules)
* **`fixed_charge_coverage_ratio_fccr`**: `(operating_income_loss + lease_payments) / (interest_expense + lease_payments)`
* **`times_interest_earned`**: `operating_income_loss / interest_expense`
* **`ebitda_growth_yoy`**: `(ebitda_t - ebitda_t_minus_1) / ebitda_t_minus_1`
* **`capex_growth_yoy`**: `(capex_t - capex_t_minus_1) / capex_t_minus_1`
* **`free_cash_flow_growth_yoy`**: `(fcf_t - fcf_t_minus_1) / fcf_t_minus_1`
* **`operating_profit_margin_post_tax`**: `operating_income_loss * (1 - effective_tax_rate) / total_revenue`
* **`invested_capital_turnover`**: `total_revenue / (stockholders_equity + total_debt - cash_and_equivalents)`
* **`dupont_roic`**: `operating_profit_margin_post_tax * invested_capital_turnover`
* **`fcf_yield`**: `free_cash_flow_per_share / StockPrice`
* **`earnings_yield`**: `1 / pe_multiple`
* **`peg_ratio`**: `pe_multiple / net_income_growth_yoy`
* **`sustainable_growth_rate`**: `roe * (1 - dividend_payout_ratio)`
* **`aviation_operating_cost_per_passenger`**: `operating_expenses / passenger_count`
* **`semiconductor_rnd_to_capex`**: `rnd_spending / capital_expenditures`
* **`biotech_pipeline_density`**: `clinical_trial_count / total_employees`

### 12. Cost of Capital (WACC), Margin Expansion & Dividend Security (15 Rules)
* **`cost_of_equity_capm`**: `risk_free_rate + beta * market_risk_premium`
* **`cost_of_debt`**: `interest_expense / total_debt`
* **`wacc`**: `(equity_weight * cost_of_equity_capm) + (debt_weight * cost_of_debt * (1 - effective_tax_rate))`
* **`ev_to_fcf`**: `enterprise_value / free_cash_flow`
* **`ev_to_invested_capital`**: `enterprise_value / (stockholders_equity + total_debt - cash_and_equivalents)`
* **`merton_default_distance_proxy`**: `(total_assets - total_liabilities) / volatility`
* **`equity_value_headroom`**: `market_capitalization / total_liabilities`
* **`accounts_receivable_pct_revenue`**: `accounts_receivable / total_revenue`
* **`inventory_pct_cogs`**: `inventory / cogs`
* **`accounts_payable_pct_cogs`**: `accounts_payable / cogs`
* **`working_capital_intensity`**: `working_capital / total_revenue`
* **`ebitda_margin_expansion`**: `ebitda_margin_t - ebitda_margin_t_minus_1`
* **`gross_margin_expansion`**: `gross_margin_t - gross_margin_t_minus_1`
* **`dividend_coverage_ratio`**: `net_income_loss / dividends_paid`
* **`fcf_dividend_coverage_ratio`**: `free_cash_flow / dividends_paid`

### 13. Capital Allocation Integrity, Operating Leverage & Cash Flow Conversion (15 Rules)
* **`plowback_ratio`**: `1 - dividend_payout_ratio`
* **`share_buyback_dilution_offset`**: `share_repurchase_amount / executive_stock_dilution`
* **`capital_return_to_ebitda`**: `(share_repurchase_amount + dividends_paid) / ebitda`
* **`degree_of_operating_leverage_dol`**: `% change in operating_income / % change in total_revenue`
* **`degree_of_financial_leverage_dfl`**: `% change in earnings_per_share / % change in operating_income`
* **`degree_of_total_leverage_dtl`**: `degree_of_operating_leverage_dol * degree_of_financial_leverage_dfl`
* **`tax_shield_usd`**: `interest_expense * effective_tax_rate`
* **`adjusted_ebitda`**: `operating_income_loss + depreciation_amortization`
* **`free_cash_flow_to_firm_fcff`**: `operating_income_loss * (1 - effective_tax_rate) + depreciation_amortization - capital_expenditures - change_in_working_capital`
* **`free_cash_flow_to_equity_fcfe`**: `free_cash_flow_to_firm_fcff + net_borrowings - interest_expense * (1 - effective_tax_rate)`
* **`fcf_conversion_ratio`**: `free_cash_flow / ebitda`
* **`risk_premium_over_risk_free`**: `earnings_yield - US10Y_bond_yield`
* **`tobin_q_proxy`**: `(market_capitalization + total_liabilities) / total_assets`
* **`reinvestment_rate_post_tax`**: `(capital_expenditures - depreciation_amortization + rnd_expenses) / (operating_income_loss * (1 - effective_tax_rate))`
* **`return_on_incremental_invested_capital_roiic`**: `change_in_operating_income_post_tax / prior_year_reinvestment`

### 14. Growth Quality Trends, Payout Yields & Economic Differentials (15 Rules)
* **`interest_expense_to_debt_ratio`**: `interest_expense / total_debt`
* **`fixed_charge_coverage_ratio_post_tax`**: `(operating_income_loss * (1 - effective_tax_rate) + lease_payments) / (interest_expense + lease_payments)`
* **`gross_profit_growth_yoy`**: `(gross_profit_t - gross_profit_t_minus_1) / gross_profit_t_minus_1`
* **`operating_cash_flow_growth_yoy`**: `(net_cash_operating_t - net_cash_operating_t_minus_1) / net_cash_operating_t_minus_1`
* **`reinvestment_growth_yoy`**: `(reinvestment_rate_t - reinvestment_rate_t_minus_1) / reinvestment_rate_t_minus_1`
* **`is_growth_decelerating`**: Unary alert flagging slower revenue growth compared to prior year.
* **`equity_risk_premium`**: `cost_of_equity_capm - risk_free_rate`
* **`spread_earnings_yield_to_bond_yield`**: `earnings_yield - cost_of_debt`
* **`days_working_capital_outstanding`**: `(working_capital * 365) / total_revenue`
* **`cash_conversion_cycle_expansion`**: `cash_conversion_cycle_ccc_t - cash_conversion_cycle_ccc_t_minus_1`
* **`shareholder_payout_yield`**: `(dividends_paid + share_repurchase_amount) / market_capitalization`
* **`reinvestment_efficiency_index`**: `change_in_operating_income_post_tax / capital_expenditures_t_minus_1`
* **`inflation_differential`**: `local_inflation_rate - macro_indicator_inflation_rate`
* **`sovereign_spread_premium`**: `sovereign_yield - risk_free_rate`
* **`real_sovereign_yield`**: `sovereign_yield - local_inflation_rate`

### 15. Quality of Earnings, Rollover Risk & Growth Capital Efficacy (15 Rules)
* **`sustainable_reinvestment_rate`**: `reinvestment_rate_post_tax * return_on_invested_capital_roic`
* **`net_debt_to_capital`**: `net_debt / (net_debt + stockholders_equity)`
* **`enterprise_value_to_operating_cash`**: `enterprise_value / net_cash_operating`
* **`working_capital_to_revenue`**: `working_capital / total_revenue`
* **`free_cash_flow_quality_ratio`**: `free_cash_flow_per_share / earnings_per_share_eps`
* **`interest_expense_to_operating_income`**: `interest_expense / operating_income_loss`
* **`short_term_debt_rollover_ratio`**: `current_liabilities / total_liabilities`
* **`short_term_debt_to_equity`**: `current_liabilities / stockholders_equity`
* **`capital_expenditures_to_assets`**: `capital_expenditures / total_assets`
* **`maintenance_capex_estimate`**: `depreciation_amortization`
* **`growth_capex_estimate`**: `capital_expenditures - depreciation_amortization`
* **`country_equity_risk_premium`**: `equity_risk_premium + sovereign_spread_premium`
* **`real_corporate_borrowing_rate`**: `cost_of_debt - local_inflation_rate`
* **`economic_freedom_trade_freedom_premium`**: `economic_freedom_rank - SovereignRating.local_rating`
* **`retained_earnings_growth_yoy`**: `(retained_earnings_t - retained_earnings_t_minus_1) / retained_earnings_t_minus_1`

### 16. Economic Value Added (EVA), Asset Quality & Impairment Alerting (15 Rules)
* **`roic_wacc_spread`**: `return_on_invested_capital_roic - wacc`
* **`economic_value_added_eva_estimate`**: `roic_wacc_spread * (stockholders_equity + total_debt - cash_and_equivalents)`
* **`goodwill_to_assets`**: `goodwill / total_assets`
* **`intangibles_to_assets`**: `intangible_assets / total_assets`
* **`is_goodwill_impairment_threat`**: Unary alert flagging post-acquisition companies facing earnings deceleration alongside heavy goodwill density.
* **`dividend_yield_to_wacc_ratio`**: `dividend_yield / wacc`
* **`fcf_yield_to_cost_of_equity_spread`**: `fcf_yield - cost_of_equity_capm`
* **`operating_cash_to_working_capital`**: `net_cash_operating / working_capital`
* **`retained_earnings_to_total_liabilities`**: `retained_earnings / total_liabilities`
* **`cash_to_total_assets`**: `cash_and_equivalents / total_assets`
* **`real_risk_free_rate`**: `risk_free_rate - macro_indicator_inflation_rate`
* **`default_risk_premium_spread`**: `corporate_bond_spread - sovereign_spread_premium`
* **`tangible_assets_to_total_liabilities`**: `(total_assets - intangible_assets) / total_liabilities`
* **`cash_flow_to_reinvestment_ratio`**: `net_cash_operating / capital_expenditures`
* **`sustainable_reinvestment_spread`**: `sustainable_reinvestment_rate - wacc`

---

## 🧪 Phase 1 Verification Plan

### Automated Verification
The test runner `verify_rules.py` will assert:
1. Verification of derived rules (e.g. asserting computed values for ROE/Current Ratios match manually calculated values from raw SQL table data).
