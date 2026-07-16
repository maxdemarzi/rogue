# 🚀 Global Finance Knowledge Graph - Use Cases Index

This directory maps the core financial and operational workflows solved by **Rogo.ai** and its competitors like **AlphaSense**, **Hebbia**, and **FinChat** (such as deep data consolidation, automated research, risk assessment, spreadsheet modeling, generative document comparison grids, contract due diligence, valuation multiples, and last-mile deliverables) directly to the **local data layers** stored inside this workspace's [`data/`](file:///home/maxdemarzi/rogue/data/) folder.

---

## 📂 Active Use Case Solutions

### 1. [Earnings Comp and Consensus Analysis](file:///home/maxdemarzi/rogue/use_cases/1_earnings_comp_and_consensus.md)
* *Rogo Solves:* Manual earnings compilation, analyst note synthesis, and tracking company metrics vs. consensus.
* *Local Solution:* Integrates target company consensus profiles from `data/earnings_estimates/` with short-term price responses in `data/ohlcv/` and sentiment analysis from `data/financial_news/`.

### 2. [Private and Public Company Sourcing & Screening](file:///home/maxdemarzi/rogue/use_cases/2_company_screening_and_sourcing.md)
* *Rogo Solves:* Deal origination, VC portfolio screening, tracking fund stages, and mapping board member networks.
* *Local Solution:* Screens VC funding histories in `data/startup_vc/` and maps board interlocks across major corporations using `data/board_members/`.

### 3. [Credit Analysis and Debt Due Diligence](file:///home/maxdemarzi/rogue/use_cases/3_credit_and_debt_diligence.md)
* *Rogo Solves:* Fixed income evaluation, debt covenant reviews, and credit rating monitoring.
* *Local Solution:* Integrates coupon structures from `data/corporate_bonds/` with historical issuer credit ratings from `data/corporate_credit_ratings/` and daily yields in `data/interest_rate_spreads/`.

### 4. [Supply Chain Contagion and Macro Exposure](file:///home/maxdemarzi/rogue/use_cases/4_supply_chain_and_macro_exposure.md)
* *Rogo Solves:* Customer-vendor dependency mapping, commodity cost exposure modeling, and liquidity forecasting.
* *Local Solution:* Connects B2B networks in `data/business_network/` and NAICS contagion vectors in `data/naics_contagion/` with daily commodity spot rates in `data/commodity_prices/` and DSO ranges in `data/trade_credit/`.

### 5. [Distress and Layoff Monitoring](file:///home/maxdemarzi/rogue/use_cases/5_distress_and_layoff_monitoring.md)
* *Rogo Solves:* Workforce restructuring trackers, legal dispute liability, and hedging risk monitoring.
* *Local Solution:* Monitors tech and corporate staff reductions in `data/corporate_layoffs/` alongside monthly default probability histories in `data/bankruptcy_risk/` and daily volatility indexes in `data/implied_volatility/`.

### 6. [Broker Research and Analyst Ratings Synthesis](file:///home/maxdemarzi/rogue/use_cases/6_broker_research_and_analyst_consensus.md)
* *AlphaSense Solves:* Consolidating Wall Street sell-side research reports, recommendation adjustments, and rating shifts.
* *Local Solution:* Collects ratings adjustments, target price increases, and recommendation upgrades/downgrades from `data/financial_news/` and correlates sentiment weights from `data/financial_phrasebank/`.

### 7. [Generative Grid & Multi-Document Synthesizer](file:///home/maxdemarzi/rogue/use_cases/7_generative_grid_and_multi_document_synthesizer.md)
* *AlphaSense Solves:* Batch executing queries across dozens of peer documents simultaneously to construct comparable financial matrices.
* *Local Solution:* Aggregates key lines across peer statements from `data/sec_financials/` and metadata in `data/simfin/` into a single peer comparison matrix.

### 8. [Virtual Data Room (VDR) and M&A Covenant Diligence](file:///home/maxdemarzi/rogue/use_cases/8_vdr_and_covenant_diligence.md)
* *Hebbia Solves:* Virtual Data Room (VDR) diligence, auditing acquisition terms, extracting legal liabilities, and monitoring debt covenants.
* *Local Solution:* Connects target litigation histories in `data/patent_litigation/` and acquisition deal blocks in `data/mergers_acquisitions/` with high-yield debt covenant monitoring in `data/corporate_bonds/`.

### 9. [Public Equity Valuation Multiples & Comps Generator](file:///home/maxdemarzi/rogue/use_cases/9_public_equity_valuation_multiples.md)
* *FinChat/Koyfin Solves:* Constructing comps tables of valuation multiples (P/E, EV/Sales, Debt/Equity) and charting growth matrices.
* *Local Solution:* Computes dynamic capitalization indices from `data/ohlcv/` and peer fundamental margins from `data/fundamentals/` and `data/simfin/` to output standardized valuation multiples.

### 10. [Investment Committee (IC) Memo & Slide Pitchbook Generator](file:///home/maxdemarzi/rogue/use_cases/10_investment_committee_memo_generator.md)
* *Last Mile Goal:* Generating formatted, board-ready investment memos and pitch decks with sentence-level citations.
* *Local Solution:* Structures transaction overviews from `data/mergers_acquisitions/` and extracts target financial histories from `data/fundamentals/` with direct source citations.

### 11. [Auditable, Live-Formula Excel Financial Modeler](file:///home/maxdemarzi/rogue/use_cases/11_auditable_excel_financial_modeler.md)
* *Last Mile Goal:* Generating forecast spreadsheets pre-loaded with live Excel formulas (e.g. projections, margins) rather than static values.
* *Local Solution:* Traces baseline financials in `data/fundamentals/` and builds a dynamic OpenPyXL sheet populated with cell-referencing formula parameters.

---

## 🔮 Mind-Blowing Advanced Automations

### 12. [Restructuring and Supplier Contagion Simulator](file:///home/maxdemarzi/rogue/use_cases/12_restructuring_and_contagion_simulator.md)
* *Mind-Blowing Goal:* Running systemic risk simulators that forecast downstream revenue contraction, lay-offs, and trade credit defaults across B2B supplier lines if a customer defaults.
* *Local Solution:* Links upcoming maturity walls in `data/corporate_bonds/` with daily credit index spreads in `data/interest_rate_spreads/`, B2B partnerships in `data/business_network/`, and write-off metrics in `data/trade_credit/`.

### 13. [Autonomous PE/LBO Target Deal Hunter & Valuator](file:///home/maxdemarzi/rogue/use_cases/13_autonomous_lbo_deal_sourcer.md)
* *Mind-Blowing Goal:* Sourcing targets autonomously by running multi-criteria filters (low valuation multiples, clean IP records, high SG&A savings) and automatically building LBO models.
* *Local Solution:* Intersects fundamental lines from `data/fundamentals/` with legal risks in `data/patent_litigation/`, executive salaries in `data/ceo_salaries/`, and outputs a dynamic debt payback schedule spreadsheet.

### 14. [Insider Trading & Corporate Governance Tracker](file:///home/maxdemarzi/rogue/use_cases/14_insider_trading_and_governance_tracker.md)
* *Mind-Blowing Goal:* Tracking executive insider trading anomalies leading up to major corporate earnings surprises, patent lawsuits, or credit downgrades.
* *Local Solution:* Maps transactions in `data/insider_trading/` and interlocking boards in `data/board_members/` with upcoming earnings windows in `data/earnings_estimates/`.

### 15. [Cross-Border FX and Inflation Arbitrage Simulator](file:///home/maxdemarzi/rogue/use_cases/15_cross_border_macro_hedging_simulator.md)
* *Mind-Blowing Goal:* Simulating macro carry trade strategies and multi-currency inputs hedging based on Purchasing Power Parity inflation gaps and sovereign credit curves.
* *Local Solution:* Correlates national CPI curves in `data/global_inflation/` with currency pairings in `data/fx_rates/`, country debt limits in `data/country_debt/`, and credit grades in `data/sovereign_ratings/`.

---

## 🏛️ Newly Uncovered Buy-Side Use Cases

### 16. [Federal Contracting Backlog & Revenue Shock Simulator](file:///home/maxdemarzi/rogue/use_cases/16_federal_contracting_backlog_shock.md)
* *Active Goal:* Estimating defense/AI contractor backlog decay and pricing revenue exposure under government budget freezes.
* *Local Solution:* Traces US federal contract awards in `data/federal_contracts/` and computes contract roll-off curves to adjust target revenues.

### 17. [ESG Capital Flight & Controversy Valuation Discount Engine](file:///home/maxdemarzi/rogue/use_cases/17_esg_capital_flight_discount.md)
* *Active Goal:* Divestment risk modeling based on controversy ratings and LP constraints.
* *Local Solution:* Matches controversy levels in `data/esg_ratings/` with institutional ownership indices to apply multiples discounts.

### 18. [Biotech Binary Clinical Trial Jump Simulator](file:///home/maxdemarzi/rogue/use_cases/18_biotech_clinical_trial_jump.md)
* *Active Goal:* Pre-revenue life sciences due diligence modeling clinical trial transitions and disease burdens.
* *Local Solution:* Compiles drug candidate pipelines in `data/pharma_industry/` with global disease metrics to simulate binary asset valuations.

### 19. [Aviation Fleet Disruption & Route Capacity Optimizer](file:///home/maxdemarzi/rogue/use_cases/19_aviation_fleet_disruption_optimizer.md)
* *Active Goal:* Operational bottleneck modeling for route operating margins and fleet order backlogs.
* *Local Solution:* Links fleet order status in `data/aviation_industry/` with safety safety incident records to project route load shocks.

### 20. [Semiconductor Fab Capacity & Export Control Restriction Simulator](file:///home/maxdemarzi/rogue/use_cases/20_semiconductor_export_control_simulator.md)
* *Active Goal:* Geopolitical trade shock modeling for fab operations under export controls.
* *Local Solution:* Intersects fab facilities in `data/semiconductor_industry/` with restriction lists to calculate client revenue blockages.

### 21. [Executive Pay-for-Performance & TSR Alignment Elasticity Solver](file:///home/maxdemarzi/rogue/use_cases/21_executive_pay_tsr_alignment.md)
* *Active Goal:* Sourcing activist targets by tracking compensation growth relative to share performance (TSR).
* *Local Solution:* Correlates executive salaries in `data/ceo_salaries/` with daily stock price returns in `data/ohlcv/`.

### 22. [Supply Chain Holding Cost & Inflation Squeeze Model](file:///home/maxdemarzi/rogue/use_cases/22_supply_chain_holding_cost_squeeze.md)
* *Active Goal:* Working capital squeeze forecasting under macro inflation shocks.
* *Local Solution:* Traces B2B connections in `data/business_network/` and DSO terms in `data/trade_credit/` to project input inventory cost adjustments.

### 23. [Startup Liquidity Runway & VC Down-Round Predictor](file:///home/maxdemarzi/rogue/use_cases/23_startup_liquidity_downround_predictor.md)
* *Active Goal:* Late-stage private secondary buyout screening.
* *Local Solution:* Projects startup burn rate runway from `data/startup_vc/` and layoffs data to predict down-round funding probabilities.

### 24. [Corporate Input Commodity Hedging Solver](file:///home/maxdemarzi/rogue/use_cases/24_corporate_commodity_hedging_solver.md)
* *Active Goal:* Prescriptive treasury hedging optimization over raw materials price volatility.
* *Local Solution:* Integrates commodity price histories in `data/commodity_prices/` with corporate cost records to solve optimal futures hedge ratios.
