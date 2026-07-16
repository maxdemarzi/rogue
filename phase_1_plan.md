# Rebuilding the Rogo AI Analyst - Comprehensive Global Ontology Plan

This plan details the full implementation plan to rebuild the **Rogo AI Analyst** using our **229-table DuckDB data warehouse** and the **Swan reasoning engine**, mapping all financial, regulatory, and specialized industry datasets.

Based on database structure, cardinality checks, and comprehensive **Use Case Playbook alignment**, we have promoted dimensions (such as Ticker, CIK, Domain, Industry, Sector, Rating, and Date) and key industry-specific tables (Aviation, Pharma, Semiconductors, and M&A Deals) to first-class **Concepts** in the Swan ontology.

---

## 📐 Rebuild Phase Roadmap

* **Phase 1 (Active): Complete Swan Ontology mapping all 50 datasets (`ontology.py`)**
* **Phase 2:** Advanced Reasoning Modules (`path_reasoner.py`, `gnn_model.py`, `optimizer.py`)
* **Phase 3: Swan Rules & Financial Calculations (`rules.py`)**
  * *Purpose:* Write declarative Datalog rules to automate **240 financial, leverage sensitivity, capital allocation, cash flow conversion, and market valuation multiples** bridging the gap between raw data and frontier intelligence.
* **Phase 4:** Nexus Agent Coordinator & Sandboxed Execution (`agent_pipeline.py`)

* **Phase 5:** Web Server & Glassmorphic Dashboard UI (`web_server.py` & `web_app/`)

---

## 🧬 Phase 1: Entity-First Swan Ontology Schema

We define **51 core concepts** and map relationships across our 229 DuckDB tables.

### 1. Linking & Dimension Concepts (First-Class Entities)

1. **`Ticker`** (Identifier: `symbol`: String)
   * Source Tables: `companies.ticker`, `ohlcv.ticker`, `earnings_estimates_earnings_features_clean_1.ticker`, `ticker_mapping_ticker_mapping.mapped_ticker`
2. **`CIK`** (Identifier: `number`: String)
   * Source Tables: `companies.cik`, `fundamentals_snapshots.cik`, `insider_trading_insider_transactions_insider_transactions_data.cik`
3. **`Domain`** (Identifier: `name`: String)
   * Source Tables: `business_network_companies.domain`, `business_network_links.home_domain`
4. **`Industry`** (Identifier: `name`: String)
   * Source Tables: `companies.industry`, `naics_contagion_naics_contagion_nodes_github.industry_name`
5. **`Sector`** (Identifier: `name`: String)
   * Source Tables: `companies.sector`
6. **`Rating`** (Identifier: `grade`: String)
   * Source Tables: `corporate_credit_ratings_morningstar_corporate_credit_ratings_2019.rating`, `sovereign_ratings_sovereign_credit_ratings.rating_foreign`, `sovereign_ratings_sovereign_short_term_ratings.rating_foreign`
7. **`Date`** (Identifier: `date_str`: String)
   * Source Tables: `ohlcv.date_time`, `fundamentals_snapshots.date`, `insider_trading_insider_transactions_insider_transactions_data.transaction_date`, `corporate_layoffs_layoffs.date`
8. **`Publisher`** (Identifier: `name`: String)
   * Source Tables: `financial_news_raw_partner_headlines.publisher`
9. **`FundingStage`** (Identifier: `name`: String)
   * Source Tables: `corporate_layoffs_layoffs.stage`

---

### 2. General & Industry Vertical Concepts

#### A. Corporate & Fundamental Metrics (Unified Global SimFin)
10. **`Company`** (Identifier: `company_id`: String)
    * Properties: `company_name`
    * Source Tables: `companies`, `countries`
11. **`LegalEntity`** (Identifier: `lei`: String)
    * Properties: `isin`
    * Source Table: `isin_lei_mapping_isin_lei`
12. **`FinancialSnapshot`** (Identifier: `snapshot`: String)
    * Properties: `revenue`, `earnings`, `assets`, `equity`, `liabilities`, `cogs`, `gross_profit`, `net_cash_operating`, `net_cash_financing`, `shares_outstanding`, `public_float`, `employees`, `country_code`
    * Source Tables: `fundamentals_snapshots`, `simfin_simfin_data_*_balance_annual`, `simfin_simfin_data_*_income_annual`, `simfin_simfin_data_*_cashflow_annual`
13. **`SECStatement`** (Identifier: `id`: String)
    * Properties: `fiscal_year`, `stock_price_at_filing`, `total_assets`, `current_assets`, `cash_and_equivalents`, `common_stock_shares_issued`, `common_stock_value`, `income_tax_expense`, `current_liabilities`, `operating_income_loss`, `stockholders_equity`, `net_income_loss`, `total_liabilities`
    * Source Table: `sec_financials_short_financials_df`
14. **`CreditRating`** (Identifier: `id`: String)
    * Properties: `obligor_name`, `agency_name`
    * Source Table: `corporate_credit_ratings_morningstar_corporate_credit_ratings_2019`
15. **`Bond`** (Identifier: `id`: String)
    * Properties: `bond_type`, `coupon_rate`, `face_value`, `maturity_date`
    * Source Table: `corporate_bonds_companybonds_sheet1`
16. **`EarningsEstimate`** (Identifier: `id`: String)
    * Properties: `beat`, `beat_streak`, `historical_beat_rate`, `avg_surprise_4q`
    * Source Table: `earnings_estimates_earnings_features_clean_1`
17. **`BankruptcyRisk`** (Identifier: `id`: String)
    * Properties: `probability`, `sans_market`, `volatility`
    * Source Table: `bankruptcy_risk_bankruptcy`
18. **`ESGRating`** (Identifier: `id`: String)
    * Properties: `total_score`, `environment_score`, `social_score`, `governance_score`, `controversy_level`
    * Source Tables: `esg_ratings_data`, `esg_ratings_sp_500_esg_risk_ratings`
19. **`IndexConstituent`** (Identifier: `id`: String)
    * Properties: `ticker_symbol`, `company_name`, `weight`, `year`
    * Source Table: `index_constituents`

#### B. Leadership & Corporate Governance Networks
20. **`Person`** (Identifier: `id`: String)
    * Properties: `first_name`, `last_name`, `linkedin_url`, `net_worth_usd`, `ceo_compensation`, `median_worker_pay`, `worker_pay_ratio`
    * Source Tables: `executives_global_ceo_and_cfo_leadership_c_level_executives_dataset`, `billionaire_wealth_forbes_billionaires`, `ceo_salaries_ceo_data_pay_merged_r3000`, `ceo_salaries_ceo_data_pay_merged_sp500`, `ceo_salaries_ceo_data_pay_r3000`, `ceo_salaries_ceo_data_pay_sp500`
21. **`BoardMember`** (Identifier: `id`: String)
    * Properties: `member_name`, `company_name`, `source`
    * Source Table: `board_members_boardmembers`
22. **`InsiderTransaction`** (Identifier: `id`: String)
    * Properties: `owner_name`, `shares_amount`, `transaction_price`, `acquired_disposed_code`, `conviction_score`, `is_director`, `is_officer`, `officer_title`
    * Source Tables: `insider_trading_insider_transactions_insider_transactions_data`, `insider_trading_master_data_enriched`, `insider_trading_premium_cross_market_signals`
23. **`InstitutionalHolding`** (Identifier: `id`: String)
    * Properties: `institution_name`, `shares_amount`, `value_usd`
    * Source Table: `insider_trading_institutional_holdings_institutional_holdings_data`

#### C. Operational & Supply Chain Metrics
24. **`Product`** (Identifier: `sku`: String)
    * Properties: `product_type`, `price`, `revenue_generated`, `supplier_name`, `manufacturing_costs`, `defect_rate`
    * Source Table: `supply_chain_supply_chain_data`
25. **`Patent`** (Identifier: `case_no`: String)
    * Properties: `plaintiff`, `defendant`, `asserted_patents`
    * Source Table: `patent_litigation_patent_data`
26. **`VCInvestment`** (Identifier: `permalink`: String)
    * Properties: `name`, `funding_total_usd`, `seed_funding`, `venture_funding`, `angel_funding`
    * Source Table: `startup_vc_investments_vc`
27. **`FederalContract`** (Identifier: `award_key`: String)
    * Properties: `recipient_name`, `agency_name`, `award_amount`
    * Source Table: `federal_contracts_us_fed_ai_contracts_sample`
28. **`LayoffEvent`** (Identifier: `id`: String)
    * Properties: `company_name`, `location`, `total_laid_off`, `percentage_laid_off`, `funds_raised`
    * Source Table: `corporate_layoffs_layoffs`
29. **`BuybackRecord`** (Identifier: `id`: String)
    * Properties: `company_name`, `share_repurchase_amount`, `executive_stock_dilution`, `capital_returned_ratio`
    * Source Table: `corporate_buybacks_financial_truth_dataset`
30. **`TradeCredit`** (Identifier: `id`: String)
    * Properties: `country_name`, `industry_sector`, `dso_value`, `finance_cost_pct`
    * Source Table: `trade_credit_trade_credit_and_financing_costs_combined`

#### D. Industry Verticals & Corporate Transactions (M&A)
31. **`MADeal`** (Identifier: `id`: String)
    * Properties: `year`, `purchaser_name`, `purchased_name`, `value_billions`
    * Source Tables: `mergers_acquisitions_top_30_m_a_deals_...`, `mergers_acquisitions_top_m_a_deals_20_billion_or_larger_...`, `mergers_acquisitions_top_ma_deals_...`
32. **`AviationIncident`** (Identifier: `id`: String)
    * Properties: `aircraft_type`, `fatalities`, `incident_description`
    * Source Table: `aviation_industry_aviation_incidents`
33. **`AviationFleetOrder`** (Identifier: `id`: String)
    * Properties: `aircraft_type`, `order_year`, `quantity`, `delivery_status`
    * Source Table: `aviation_industry_fleet_orders`
34. **`AviationPassengerTraffic`** (Identifier: `id`: String)
    * Properties: `passenger_count`, `load_factor`, `passenger_revenue`
    * Source Tables: `aviation_industry_passenger_traffic`, `aviation_industry_airline_financials`
35. **`AviationRoutePerformance`** (Identifier: `id`: String)
    * Properties: `route_name`, `revenue_per_passenger`, `operating_margin`
    * Source Table: `aviation_industry_route_performance`
36. **`BiotechFunding`** (Identifier: `id`: String)
    * Properties: `funding_amount_usd`, `funding_round`
    * Source Table: `pharma_industry_biotech_funding`
37. **`ClinicalTrial`** (Identifier: `id`: String)
    * Properties: `trial_id`, `drug_name`, `phase`, `status`
    * Source Table: `pharma_industry_clinical_trials`
38. **`DiseaseBurden`** (Identifier: `id`: String)
    * Properties: `disease_name`, `global_cases`, `yearly_mortality_rate`
    * Source Table: `pharma_industry_disease_burden`
39. **`DrugApproval`** (Identifier: `id`: String)
    * Properties: `drug_name`, `indication`
    * Source Table: `pharma_industry_drug_approvals`
40. **`PharmaFinancials`** (Identifier: `id`: String)
    * Properties: `rnd_intensity`, `fda_approvals`
    * Source Table: `pharma_industry_pharma_companies_financials`
41. **`ChipMarketMetric`** (Identifier: `id`: String)
    * Properties: `segment_name`, `market_size_usd`, `growth_rate_pct`, `year`
    * Source Table: `semiconductor_industry_ai_chip_market`
42. **`SemiconductorFinancials`** (Identifier: `id`: String)
    * Properties: `revenue`, `rnd_spending`
    * Source Table: `semiconductor_industry_chip_companies_financials`
43. **`ChipPrice`** (Identifier: `id`: String)
    * Properties: `chip_type`, `spot_price_usd`
    * Source Table: `semiconductor_industry_chip_prices`
44. **`SemiconductorExportControl`** (Identifier: `id`: String)
    * Properties: `restricted_entity`, `controlling_country`, `restriction_type`
    * Source Table: `semiconductor_industry_export_controls`
45. **`SemiconductorFabCapacity`** (Identifier: `id`: String)
    * Properties: `facility_name`, `location`, `capacity_wspm`, `node_size_nm`
    * Source Table: `semiconductor_industry_fab_capacity`

#### E. Sentiment & External Factors
46. **`NewsHeadline`** (Identifier: `id`: String)
    * Source Tables: `financial_news_raw_partner_headlines`, `financial_news_analyst_ratings_processed`, `financial_news_raw_analyst_ratings`
47. **`SentimentRecord`** (Identifier: `id`: String)
    * Properties: `sentence`, `sentiment`
    * Source Table: `financial_phrasebank_all_data`
48. **`Commodity`** (Identifier: `id`: String)
    * Properties: `commodity_name`, `open_val`, `close_val`
    * Source Tables: `commodity_prices_global_commodity_prices_2000_2026`, `crude_oil_prices_crude_oil_and_sustainable_indices_us_and_india_oil_and_sus_index_us_and_india`, `gold_prices_final_uso`

#### F. Domicile, Macroeconomics & Price Series Cross-walk
49. **`PriceSeries`** (Identifier: `series_id`: String)
    * Source Tables: `crypto_holdings_*_price`, `fx_rates_foreign_exchange_rates_rates`
50. **`Country`** (Identifier: `country_name`: String)
    * Properties: `property_rights`, `tax_burden`, `government_spending`, `business_freedom`
    * Source Table: `economic_freedom_economic_freedom_index2019_data`
51. **`SovereignRating`** (Identifier: `country_name`: String)
    * Properties: `rating_foreign`, `rating_local`
    * Source Tables: `sovereign_ratings_sovereign_credit_ratings`, `sovereign_ratings_sovereign_short_term_ratings`, `sovereign_ratings_supranational_issuers`
52. **`CountryMacro`** (Identifier: `id`: String)
    * Properties: `year`, `gdp_usd`, `unemployment_rate`, `debt_indicator_name`, `debt_ratio_1950_2022`
    * Source Tables: `country_gdp_employment_employment_unemployment_gdp_data`, `country_debt_central_government_debt`
53. **`MacroIndicator`** (Identifier: `id`: String)
    * Properties: `indicator_name`, `value`
    * Source Tables: `macroeconomics_index`, `global_inflation_global_inflation_data`, `sweden_macro_interestrate_and_inflation_sweden_1908_2001`, `uk_cost_of_living_uk_col_salary_longitudinal_2010_2024`, `interest_rate_spreads_fred_interestrate_data`, `treasury_yields_us_treasury_yields_daily`, `fx_rates_foreign_exchange_rates`, `eu_inflation_eurostat_table_hicpv2`
54. **`SectorReturn`** (Identifier: `id`: String)
    * Properties: `sector_name`, `return_pct`, `year`
    * Source Tables: `sector_returns_stock_market_daily`, `sector_returns_sector_annual_summary`, `sector_returns_ticker_monthly_returns`

---

### 3. Entity-Relationship Schema

We define the structural relationships linking every concept back to its key dimensions:

#### Company & Corporate Identity
* `Company.has_ticker -> Ticker.lookup(symbol)`
* `Company.has_cik -> CIK.lookup(number)`
* `Company.has_domain -> Domain.lookup(name)`
* `Company.belongs_to_industry -> Industry.lookup(name)`
* `Company.resolves_to -> LegalEntity.lookup(lei)`
* `Company.domiciled_in -> Country.lookup(country_name)`
* `PriceSeries.for_ticker -> Ticker.lookup(symbol)`

#### Categorization Hierarchies
* `Industry.belongs_to_sector -> Sector.lookup(name)`
* `Domain.linked_to -> Domain` (B2B vendor linkages)
* `Industry.contagion_threat -> Industry` (NAICS contagion links)

#### Securities, Debt & Credit Ratings
* `SECStatement.for_ticker -> Ticker.lookup(symbol)`
* `SECStatement.filed_on -> Date.lookup(date_str)`
* `SECStatement.price_on -> Date.lookup(date_str)`
* `SECStatement.report_on -> Date.lookup(date_str)`
* `CreditRating.for_company -> Company.lookup(company_name=obligor_name)`
* `CreditRating.has_rating -> Rating.lookup(grade=rating)`
* `Bond.for_ticker -> Ticker.lookup(symbol)`
* `Bond.has_rating -> Rating.lookup(grade=credit_rating)`
* `SovereignRating.for_country -> Country.lookup(country_name=sovereign)`
* `SovereignRating.foreign_rating -> Rating.lookup(grade=rating_foreign)`
* `SovereignRating.local_rating -> Rating.lookup(grade=rating_local)`
* `IndexConstituent.has_ticker -> Ticker.lookup(symbol=ticker_symbol)`

#### Operational & Governance Metrics
* `Product.supplied_by -> Company.lookup(company_name=supplier_name)`
* `Patent.owned_by -> Company.lookup(company_name=parent_company)`
* `Company.litigated_against -> Company` (Plaintiff ↔ Defendant)
* `VCInvestment.funded_company -> Company.lookup(company_name=name)`
* `FederalContract.recipient -> Company.lookup(company_name=recipient_name)`
* `FederalContract.parent_ticker -> Ticker.lookup(symbol=parent_recipient_ticker)`
* `FederalContract.started_on -> Date.lookup(date_str=start_date)`
* `LayoffEvent.for_company -> Company.lookup(company_name=company)`
* `LayoffEvent.occurred_on -> Date.lookup(date_str=date)`
* `LayoffEvent.has_funding_stage -> FundingStage.lookup(name=stage)`
* `BuybackRecord.for_ticker -> Ticker.lookup(symbol)`
* `BoardMember.sits_on_board_of -> Company.lookup(company_name)`
* `Person.executive_of -> Company.lookup(company_name)`
* `InsiderTransaction.for_ticker -> Ticker.lookup(symbol)`
* `InsiderTransaction.occurred_on -> Date.lookup(date_str)`
* `InstitutionalHolding.for_ticker -> Ticker.lookup(symbol)`
* `InstitutionalHolding.reported_on -> Date.lookup(date_str)`
* `TradeCredit.applies_to_sector -> Sector.lookup(name=industry_sector)`
* `Company.supplies_to -> Company` (B2B value-chain edges)

#### Industry Verticals & Deals
* `MADeal.purchaser -> Company.lookup(company_name=purchaser_name)`
* `MADeal.target -> Company.lookup(company_name=purchased_name)`
* `AviationIncident.involves_airline -> Company.lookup(company_name=airline)`
* `AviationIncident.occurred_on -> Date.lookup(date_str=date)`
* `AviationFleetOrder.ordered_by -> Company.lookup(company_name=airline)`
* `AviationPassengerTraffic.for_airline -> Company.lookup(company_name=airline)`
* `AviationRoutePerformance.operated_by -> Company.lookup(company_name=airline)`
* `BiotechFunding.funded_company -> Company.lookup(company_name=company_name)`
* `BiotechFunding.funded_on -> Date.lookup(date_str=date)`
* `ClinicalTrial.conducted_by -> Company.lookup(company_name=company)`
* `ClinicalTrial.started_on -> Date.lookup(date_str=start_date)`
* `DrugApproval.approved_for -> Company.lookup(company_name=company)`
* `DrugApproval.approved_on -> Date.lookup(date_str=approval_date)`
* `PharmaFinancials.for_company -> Company.lookup(company_name=company_name)`
* `SemiconductorFinancials.for_company -> Company.lookup(company_name=company_name)`
* `ChipPrice.pricing_date -> Date.lookup(date_str=date)`
* `SemiconductorExportControl.restricted_company -> Company.lookup(company_name=restricted_entity)`
* `SemiconductorExportControl.effective_on -> Date.lookup(date_str=effective_date)`
* `SemiconductorFabCapacity.operated_by -> Company.lookup(company_name=company)`

#### Sentiment, Macro, and Timelines
* `NewsHeadline.mentions_ticker -> Ticker.lookup(symbol=stock)`
* `NewsHeadline.published_on -> Date.lookup(date_str=date)`
* `NewsHeadline.published_by -> Publisher.lookup(name=publisher)`
* `Commodity.pricing_date -> Date.lookup(date_str)`
* `Country.has_sovereign_rating -> SovereignRating.lookup(country_name)`
* `Country.has_macro_data -> CountryMacro`
* `MacroIndicator.measured_on -> Date.lookup(date_str)`
* `SectorReturn.for_sector -> Sector.lookup(name=sector_name)`
* `SectorReturn.recorded_on -> Date.lookup(date_str)`

---


---

## 🧪 Phase 1 Verification Plan

### Automated Verification
The test runner `verify_ontology.py` will assert:
1. Clean compilation of all 54 concepts.
2. Ingestion count checks of all 229 tables.
3. Ingestion speeds remain **under 5 seconds** (raw daily pricing timelines excluded).

### B. Dynamic Catalog & Schema Drift Validator (`validate_schema.py`)
To prevent silent runtime ingestion failures when DuckDB tables undergo changes:
1. A dynamic schema validator queries the DuckDB catalog schema (`information_schema.columns` and `information_schema.tables`).
2. It loops through all Concept and Property declarations in `ontology.py` and verifies they exist physically in the catalog.
3. Any column type mismatch or missing attribute triggers a build-blocking exception, alerting developers to schema drift.
