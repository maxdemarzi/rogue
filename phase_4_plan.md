# Rebuilding the Rogo AI Analyst - Phase 4: Nexus Agent Coordinator & Playbook Orchestrator

This document details the software design, routing mechanics, sandboxed execution rules, and playbook integration schemes for the **Nexus Agent Coordinator** (`agent_pipeline.py`). Nexus coordinates incoming user questions, compiles them into executable Swan and Python pipelines, enforces security sandboxing, and synthesizes output deliverables for all **24 financial due diligence use cases**.

---

## 📐 1. Nexus Coordinator Architecture

Nexus acts as the central cognitive router. It bridges the natural language interface (Chat UI) with the local reasoning solvers:

```mermaid
graph TD
    User[User Prompt / Chat UI] --> Router{Nexus Cognitive Router}
    
    subgraph Model Broker Routing
        Router -->|Simple queries| Luna[Luna/Terra: Tag Extraction]
        Router -->|Complex models| Sol[Sol: Code Synthesis & Synthesis]
    end
    
    Sol -->|Generated Python Code| Sandbox[Secure AST Sandbox]
    Sandbox -->|Approved AST| Executor[Python Execution Engine]
    
    subgraph Solver Modules
        Executor -->|pyrel_duckdb| Swan[Swan Semantic & Rules Engine]
        Executor -->|openpyxl| Solvers[Merton / Excel Modeler]
    end
    
    Executor -->|JSON Output & Diffs| Visualizer[Dashboard UI Render]
```

---

## 🔒 2. Secure AST Python Sandbox (`sandbox.py`)

To prevent arbitrary execution risks (XSS, remote code execution, database corruption), all generated Python blocks are checked using an Abstract Syntax Tree (AST) validator before execution.

### A. Deny-List and Allow-List Checks
The validator audits the code's parsed nodes against a whitelist:
* **Approved Modules:** `pyrel_duckdb`, `pandas`, `numpy`, `openpyxl`, `json`, `math`, `datetime`.
* **Prohibited Imports:** `os`, `sys`, `shutil`, `subprocess`, `requests`, `urllib`, `socket`, `builtins.eval`, `builtins.exec`, `sqlite3`, `duckdb` (raw connections bypassed; only Swan `Model` references allowed).

### B. Validation Code Skeleton
```python
import ast

class SecureASTValidator(ast.NodeVisitor):
    def __init__(self):
        self.allowed_imports = {'pandas', 'numpy', 'openpyxl', 'pyrel_duckdb', 'json', 'math', 'datetime'}
        
    def visit_Import(self, node):
        for alias in node.names:
            base_module = alias.name.split('.')[0]
            if base_module not in self.allowed_imports:
                raise PermissionError(f"AST Error: Import of '{alias.name}' is prohibited in the sandbox.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        base_module = node.module.split('.')[0]
        if base_module not in self.allowed_imports:
            raise PermissionError(f"AST Error: Import from '{node.module}' is prohibited in the sandbox.")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Prevent calls to built-in eval/exec or open
        if isinstance(node.func, ast.Name):
            if node.func.id in {'eval', 'exec', 'open', 'compile'}:
                raise PermissionError(f"AST Error: Call to built-in function '{node.func.id}' is prohibited.")
        self.generic_visit(node)
```

---

## 💼 3. The Playbook Orchestrator (Solving the 24 Use Cases)

Nexus compiles incoming queries into specific playbook pipelines, querying the DuckDB/Swan layer and outputting target spreadsheets, IC memos, or graph visualizations. The playbooks are categorized and structured below:

### 1. Earnings Comp & Consensus Analysis
* **Business Case & Rationale:**
  Public equity analysts need to monitor consensus estimates (EPS, Revenue) and quickly cross-reference them with actual performance and short-term price reactions to spot earnings surprises and sentiment shifts.
* **Pipeline Mechanics:**
  1. Queries target consensus parameters from `earnings_estimates`.
  2. Joins estimates with actual values from SimFin fundamentals and daily closing prices in `ohlcv`.
  3. Computes the post-earnings stock price drift over a 5-day trading window.
* **Output:**
  A tabular summary detailing consensus estimates vs. actual results, surprise percentages, and a timeline plot of post-earnings volatility.

### 2. Public & Private Company Sourcing & Screening
* **Business Case & Rationale:**
  Private equity and VC associates screen target databases to map funding histories and executive board interlocks to find deal sourcing candidates.
* **Pipeline Mechanics:**
  1. Queries start-up funding rounds in `startup_vc` by round size, valuation, and funding stage.
  2. Maps Fortune 100 interlocking board directors from `board_members` sitting on peer boards.
  3. Visualizes director co-membership paths using Swan Graph degree tracking.
* **Output:**
  An interactive director interlock network diagram linking PE/VC investors to target company founders.

### 3. Credit Analysis & Debt Due Diligence
* **Business Case & Rationale:**
  Credit research analysts stress-test corporate debt structures, coupon rates, and ratings to predict impending default risks or maturity wall refinancing constraints.
* **Pipeline Mechanics:**
  1. Extracts bond coupon structures and maturity dates from `corporate_bonds`.
  2. Correlates issuers with historical corporate rating paths in `corporate_credit_ratings`.
  3. Groups debt profiles by maturity years to locate credit walls.
* **Output:**
  A structured maturity wall timeline chart highlighting outstanding debt volumes segmented by credit quality.

### 4. Supply Chain Contagion & Macro Exposure
* **Business Case & Rationale:**
  Firms with high customer concentration or commodity dependency face margin compression if their supply chains break. Risk managers map these upstream supply lines to quantify exposure.
* **Pipeline Mechanics:**
  1. Joins the domain linkages in `business_network_links` with daily commodity spot rates in `commodity_prices`.
  2. Traces multi-hop B2B supplies to isolate supplier dependency ratios.
  3. Maps cost shocks from raw commodities to finished product cost structures.
* **Output:**
  A value-chain risk report displaying direct exposure to commodity price shocks across suppliers.

### 5. Distress & Layoff Monitoring
* **Business Case & Rationale:**
  Early indicators of operational distress (headcount reductions, layoff events) precede formal default filings. Credit desks monitor these layoff curves to hedge loan portfolios.
* **Pipeline Mechanics:**
  1. Aggregates monthly layoff counts and percentages from `corporate_layoffs`.
  2. Cross-references headcount cuts with default probability changes in `bankruptcy_risk`.
  3. Plats daily volatility changes from `implied_volatility` around layoff events.
* **Output:**
  A distress dashboard displaying layoff timelines correlated with default probability curves.

### 6. Broker Research & Ratings Synthesis
* **Business Case & Rationale:**
  Buy-side PMs compile sell-side consensus ratings (Buy/Hold/Sell) and broker research price targets to identify market sentiment anomalies.
* **Pipeline Mechanics:**
  1. Extracts ratings adjustments and recommendation dates from `financial_news`.
  2. Performs sentiment weight scoring using `financial_phrasebank` sentiment models.
  3. Computes the consensus target price spread relative to the actual spot trading price.
* **Output:**
  A broker ratings summary chart detailing target price spreads and sentiment distributions.

### 7. Generative Grid & Multi-Document Comparison
* **Business Case & Rationale:**
  PE associates compare dozens of peer SEC filings (10-K, 10-Q) side-by-side to benchmark operational metrics (operating margins, working capital cycles).
* **Pipeline Mechanics:**
  1. Compiles SEC balance sheet and income metrics from `sec_financials` across peer tickers.
  2. Normalizes financial variables (standardizing concept keys like `net_income` or `total_assets`).
  3. Formulates a comparable comparables grid in-memory.
* **Output:**
  An interactive side-by-side comparable grid (Generative Grid) displaying margins, leverage, and liquidity metrics.

### 8. Virtual Data Room (VDR) & M&A Covenant Diligence
* **Business Case & Rationale:**
  During M&A diligence, deal teams audit target litigation histories and high-yield covenants to assess technical default triggers.
* **Pipeline Mechanics:**
  1. Scans target litigation histories and outstanding damages in `patent_litigation`.
  2. Compiles high-yield covenant limits from `corporate_bonds` credit structures.
  3. Computes leverage ratios to flags potential covenant violations.
* **Output:**
  A covenant compliance checklist highlighting outstanding liabilities and covenant breach flags.

### 9. Public Equity Valuation Multiples Comps Generator
* **Business Case & Rationale:**
  Public equity PMs build comparable valuation models (comps tables) plotting trading multiples (P/E, EV/Sales, EV/EBITDA) against revenue growth to find arbitrage targets.
* **Pipeline Mechanics:**
  1. Queries daily capitalization weights (StockPrice * SharesOutstanding) from `ohlcv`.
  2. Divides capitalization weights by fundamental EBITDA and sales margins in SimFin.
  3. Compares multiples against peer sector medians.
* **Output:**
  A standard comparables comps table detailing P/E, P/S, EV/EBITDA, and gross margin trends.

### 10. IC Memo & Pitchbook Generator
* **Business Case & Rationale:**
  Deal teams generate formatted, board-ready investment committee memos containing sentence-level citations to back up target acquisition metrics.
* **Pipeline Mechanics:**
  1. Extracts transaction variables from `mergers_acquisitions` and target financials in SimFin.
  2. Formulates a structured document layout utilizing preset paragraphs and tables.
  3. Injects citation tags referencing the exact table row index inside `rogue_finance.duckdb`.
* **Output:**
  A downloadable Word/PDF Investment Committee pitchbook containing inline source citations.

### 11. Auditable Live-Formula Excel Modeler
* **Business Case & Rationale:**
  Investment analysts require spreadsheets containing live, audit-ready cell formulas (e.g. projecting future cash flows and margins) rather than static, hardcoded numbers.
* **Pipeline Mechanics:**
  1. Queries target historical balance sheet and income lines.
  2. Scribes baseline values into an OpenPyXL workbook structure.
  3. Injects uppercase referencing formulas (e.g., `=B5*(1+C5)`) across forecast columns.
* **Output:**
  A downloadable `.xlsx` model pre-loaded with dynamic projection formulas.

---

### 🔮 12. Restructuring & Supplier Contagion Simulator
* **Business Case & Rationale:**
  A credit default or restructuring event at a major corporate node (e.g., Apple, Boeing) can trigger systemic insolvency across its entire supplier base. Credit officers and distressed debt analysts need to stress-test this contagion risk to avoid cascading trade-credit losses.
* **Pipeline Mechanics:**
  1. Identifies spec-grade bonds with upcoming maturity walls (`corporate_bonds`).
  2. Queries the B2B supplies graph (`business_network_links`) to locate all supplier connections.
  3. Projects multi-hop supplier losses based on target default probabilities and supplier Days Sales Outstanding (DSO) metrics in `trade_credit`.
* **Output:**
  An interactive Cytoscape network graph highlighting distressed source nodes and color-coding suppliers by projected credit loss exposure (low, medium, critical).

### 🤖 13. Autonomous PE/LBO Target Deal Sourcing
* **Business Case & Rationale:**
  Private equity associates spend hundreds of hours manually screening databases for leveraged buyout candidates. This playbook automates deal sourcing by locating undervalued target firms with optimized post-restructuring cash flows.
* **Pipeline Mechanics:**
  1. Screens target companies with low EV/Sales and EV/EBITDA multiples.
  2. Filters out active patent litigation defendants (`patent_litigation`).
  3. Employs Swan's prescriptive solver to select the optimal portfolio of targets that maximizes projected net income under fixed budget limits.
* **Output:**
  A downloadable OpenPyXL spreadsheet detailing a 5-year debt paydown amortization schedule and projected equity returns (IRR) with cell-level referencing formulas.

### 🕵️ 14. Insider Trading & Governance Audit
* **Business Case & Rationale:**
  Hedge funds and compliance officers look for corporate governance red flags, such as executive panic-selling shortly before bad news (earnings misses, rating downgrades, product delays).
* **Pipeline Mechanics:**
  1. Matches executive transactions in `insider_trading` with upcoming consensus earnings announcement dates in `earnings_estimates`.
  2. Traces interlocking directors across peer boards using Swan Graph reachability pathfinders to identify potential information leakage routes.
* **Output:**
  A compliance dashboard registry flagging trades executed in quiet-windows, rated by a Bayesian leakage probability score.

### 🌍 15. Cross-Border FX Carry Trade & Arbitrage Simulator
* **Business Case & Rationale:**
  Macro hedge funds leverage divergence in sovereign yield curves, inflation, and currency pairings to structure FX carry trades while hedging currency downside.
* **Pipeline Mechanics:**
  1. Correlates national CPI curves (`global_inflation`) with currency spot rates in `fx_rates`.
  2. Computes Purchasing Power Parity (PPP) differentials to flag overvalued currencies.
  3. Executes Swan's prescriptive solver to find optimal allocation weights ($w_j$) across international yield curves that minimize portfolio volatility under minimum spread targets.
* **Output:**
  An asset allocation table detailing target currency weights, hedged risk ratios, and sovereign credit default protection spreads.

### 🏛️ 16. Federal Contracting Backlog & Revenue Shock Simulator
* **Business Case & Rationale:**
  Defense and government-tech contractors depend heavily on federal agency funding. A budget freeze or government shutdown can cause immediate cash flow shocks. Equity analysts need to stress-test contract backlog decay curves.
* **Pipeline Mechanics:**
  1. Compiles contract start dates, values, and durations from `federal_contracts`.
  2. Computes the contract backlog roll-off curve:
     $$\text{Backlog}_{t} = \sum \text{AwardAmount} \times (1 - \text{ElapsedTime}/\text{Duration})$$
  3. Projects operating margin contraction if pending awards are delayed.
* **Output:**
  A line chart plotting contract backlog roll-off timelines and valuation multiple adjustments.

### 🍃 17. ESG Capital Flight & Controversy Discount Engine
* **Business Case & Rationale:**
  Institutional LPs frequently enforce strict ESG exclusion mandates. A major controversy spike can trigger rapid capital divestment, compressing a target's valuation multiple. Buy-side PMs need to quantify this valuation penalty.
* **Pipeline Mechanics:**
  1. Merges controversy ratings in `esg_ratings` with institutional holdings in `insider_trading`.
  2. Projects LP divestment probabilities ($P_{flight}$) based on controversy severity and institutional weights.
  3. Adjusts the GNN's predicted EV/Sales multiples downward.
* **Output:**
  A valuation multiple discount matrix showing the GNN valuation adjusted for LP capital flight risk.

### 🧬 18. Biotech Binary Clinical Trial Valuation Jump Simulator
* **Business Case & Rationale:**
  Venture capital and biotech equity investors face binary risk profiles when clinical trials are released. This model maps candidate pipeline probability curves to project post-event equity jumps.
* **Pipeline Mechanics:**
  1. Traces clinical trial stages in `pharma_trials` and maps indications to disease global case sizes in `disease_burden`.
  2. Compiles historical trial success rates by phase to estimate the approval probability ($P_{success}$).
  3. Simulates expected post-event equity values compared to liquidation boundaries.
* **Output:**
  A decision-tree scenario matrix detailing risk-adjusted valuations and NPV curves under trial success vs. fail scenarios.

### ✈️ 19. Aviation Fleet Disruption & Route Capacity Optimizer
* **Business Case & Rationale:**
  Airlines face margin squeeze when aircraft orders are delayed or safety incidents occur, dragging down route capacity. Sector analysts need to stress-test these operational parameters.
* **Pipeline Mechanics:**
  1. Traces fleet orders and delivery schedules in `aviation_industry/fleet_orders`.
  2. Adjusts passenger load factors based on safety incident fatalities and delivery delays.
  3. Projects route-by-route operating margin degradation.
* **Output:**
  A comparable route capacity table displaying load factor shocks and expected operational cost-per-passenger increases.

### 🔌 20. Semiconductor Fab Capacity & Export Control Simulator
* **Business Case & Rationale:**
  Geopolitical export controls directly impact semiconductor chipmakers by blocking sales to specific regions or entity lists. Analysts need to calculate customer-level revenue blockages and fab capacity write-downs.
* **Pipeline Mechanics:**
  1. Maps fab sizes and locations in `semiconductor_industry/fab_capacity`.
  2. Flags sales blockages to restricted clients linked via export controls.
  3. Restricts fab utilization capacities dynamically inside Swan Datalog rules.
* **Output:**
  A global trade risk map detailing customer revenue blockages and unutilized fab capacity costs.

### ⚖️ 21. Executive Pay-for-Performance & TSR Alignment Elasticity Solver
* **Business Case & Rationale:**
  Activist hedge funds look for corporate governance targets where board members approve massive executive pay packages despite declining total shareholder returns (TSR).
* **Pipeline Mechanics:**
  1. Compiles CEO compensation in `ceo_salaries` and daily price series in `ohlcv`.
  2. Calculates the TSR-Compensation elasticity ratio ($\epsilon_{pay}$).
  3. Scores and ranks targets where compensation growth diverges from shareholder returns.
* **Output:**
  An activist sourcing dashboard listing governance targets sorted by pay-for-performance mismatch.

### 🌀 22. Supply Chain Holding Cost & Inflation Squeeze Model
* **Business Case & Rationale:**
  Macroeconomic inflation and rising interest rates squeeze supplier margins by increasing the carrying costs of raw materials and inventory. Corporate treasurers use this model to hedge working capital lines.
* **Pipeline Mechanics:**
  1. Queries B2B supply links and trade credit DSO terms in `trade_credit`.
  2. Shocks supplier inventory holding costs based on local CPI inflation and WACC rates.
  3. Projects gross operating margin contraction.
* **Output:**
  A margin sensitivity table detailing how inflation shocks compress gross profits across high-DSO sectors.

### 💸 23. Startup Liquidity Runway & VC Down-Round Predictor
* **Business Case & Rationale:**
  Late-stage secondary market buyers and PE funds look for cash-strapped private startups facing upcoming funding cliffs to negotiate discounts.
* **Pipeline Mechanics:**
  1. Extracts startup fundraising records in `startup_vc` and headcount cuts in `layoffs`.
  2. Projects monthly cash burn rates and runway months.
  3. Calculates down-round refinancing probabilities ($P_{down}$) under elevated macro spreads.
* **Output:**
  A venture screening registry flagging startups with less than 6 months of runway and high refinancing risk.

### 🛢️ 24. Corporate Input Commodity Hedging Solver
* **Business Case & Rationale:**
  Manufacturing and industrial firms suffer margin volatility when commodity input prices (oil, metals) spike. Corporate treasurers use mathematical programming to minimize procurement cost variances.
* **Pipeline Mechanics:**
  1. Queries historical spot price series in `commodity_prices` (gold, crude oil, copper, silver).
  2. Minimizes total inventory procurement cost variance using Swan's prescriptive solver.
  3. Computes the optimal futures hedging allocations under fixed premium budgets.
* **Output:**
  A treasury hedging schedule table detailing optimal commodity coverage ratios and cost savings projections.

---

## 🏁 10. Competitor Alignment: Hebbia Credit Matrices & AlphaSense Document Diffing

To match the core generative products of specialized tools (like Hebbia’s document-to-matrix query and AlphaSense’s MD&A redline diffs), we define the final reasoning engines:

### A. Hebbia Change-of-Control & Covenant Creditor Matrix Extractor
* **Business Case & Rationale:**
  Credit analysts reviewing complex debt agreements need to compare restrictive covenants and change-of-control thresholds across peers to assess technical default triggers.
* **Pipeline Mechanics:**
  Pulls covenant attributes across credit agreements (`data/corporate_bonds/`) and evaluates if combined transaction debt volumes trigger covenant breach flags.
* **Output:**
  A comparative matrix listing change-of-control covenants, debt maturity walls, and interest rate margins.

### B. AlphaSense MD&A Risk Redliner
* **Business Case & Rationale:**
  Corporate lawyers and buy-side analysts compare subsequent annual reports to find subtle wording changes in risk disclosures, indicating upcoming legal or operational liabilities.
* **Pipeline Mechanics:**
  Redline-diffs MD&A risk disclosure sections across consecutive SEC filings (`SECStatement_t` vs `SECStatement_t-1`) in DuckDB.
* **Output:**
  A redline text viewer highlighting deleted, added, or modified risk factors rated by a sentiment severity score.

### C. PitchBook Warm Introduction Connection Pathfinder
* **Business Case & Rationale:**
  Deal origination teams look for pathways of warm introductions to startup founders through mutual directors or interlocking board members.
* **Pipeline Mechanics:**
  Runs reachability checks on the interlocking `BoardMember` graph to locate the shortest connectivity path between an acquirer executive and a target founder, ranking pathways by network degrees.
* **Output:**
  A relationship graph visualizing the board interlocks linking the two executives.

### D. S&P Capital IQ LP Commitment Allocation Optimizer
* **Business Case & Rationale:**
  Pension funds and institutional LPs allocate capital commitments across multiple private equity fund managers to maximize long-term IRR while adhering to dry powder liquidity bounds.
* **Pipeline Mechanics:**
  Formulates a prescriptive optimization problem in Swan to solve for optimal commitment weights ($w_f$) across fund managers, constrained by dry powder exposure and vintage limits.
* **Output:**
  An allocation table detailing target fund weights, vintage distributions, and liquidity ratios.

### E. Tegus Expert Transcript Sentiment Divergence Tracker
* **Business Case & Rationale:**
  Hedge funds look for long/short ideas by identifying where expert network interview sentiment (Tegus) diverges from public Wall Street broker consensus ratings.
* **Pipeline Mechanics:**
  Traces sentiment shifts across executive news headlines and phrasebanks, benchmarking them against analyst EPS consensus beat streams.
* **Output:**
  A divergence dashboard flagging long/short candidates based on consensus mismatches.

### F. Koyfin Multiples Mean-Reversion Solver
* **Business Case & Rationale:**
  Value investors look for mean-reverting valuation anomalies by tracking how far current trading multiples deviate from historical averages.
* **Pipeline Mechanics:**
  Calculates the Z-score of the current trading multiple relative to its 5-year historical distribution.
* **Output:**
  A comps table highlighting targets trading at more than 2.0 standard deviations below their historical mean.

### G. Bloomberg Covered Interest Rate Parity (CIP) Basis Spread Arbitrage Solver
* **Business Case & Rationale:**
  Global macro desks and FX traders search for riskless cross-currency basis arbitrage opportunities resulting from Covered Interest Parity (CIP) violations.
* **Pipeline Mechanics:**
  Formulates the CIP swap arbitrage equation across daily FX rates and macro yield curves, calculating the basis spread mismatch.
* **Output:**
  A basis spread table flagging swap opportunities where the arbitrage spread exceeds 10 bps.

### H. Diligent Board Poison Pill Defensive Dilution Simulator
* **Business Case & Rationale:**
  Activist hedge funds need to know their maximum share accumulation threshold before triggering defensive board poison pill share issues that dilute their stake.
* **Pipeline Mechanics:**
  Models the expected dilution curve to an activist's ownership stake if a target board deploys a Shareholder Rights Trigger.
* **Output:**
  A dilution curve plot displaying activist ownership share vs. total outstanding shares issued under rights triggers.

### I. Bloomberg CDS Market-Implied Probability of Default Solver
* **Business Case & Rationale:**
  Fixed-income PMs look for discrepancies between rating-agency credit metrics and real-time market pricing of credit risk by extracting default probabilities from CDS spreads.
* **Pipeline Mechanics:**
  Calculates continuous default probabilities directly from Credit Default Swap (CDS) spreads and recovery rates.
* **Output:**
  A credit risk dashboard comparing fundamentals-based default risk (Merton) against CDS-implied default curves.

### J. PitchBook Co-Investment Syndicate Pathfinder
* **Business Case & Rationale:**
  Deal sourcing teams co-investing in private startups analyze syndicate networks to target co-investment leads or find friendly co-investors.
* **Pipeline Mechanics:**
  Calculates the Jaccard similarity index ($J$) of co-investments between VC funds over historical funding rounds:
  $$J(A, B) = \frac{|\text{Portfolio}_A \cap \text{Portfolio}_B|}{|\text{Portfolio}_A \cup \text{Portfolio}_B|}$$
* **Output:**
  A VC co-investment cluster map displaying high-similarity syndicate partners.

### K. Bloomberg Black-Litterman Sovereign Portfolio Allocation Optimizer
* **Business Case & Rationale:**
  Sovereign wealth funds and global macro treasuries optimize foreign sovereign bond allocations by combining baseline yield variances with active macro views.
* **Pipeline Mechanics:**
  Solves the Black-Litterman asset estimation algorithm inside Swan's prescriptive solver, applying yield covariance matrices and linear FX return constraints.
* **Output:**
  An optimal sovereign asset weights table displaying allocation adjustments and expected portfolio return metrics.

---

## 🧪 Phase 4 Verification Plan

The test suite `verify_coordinator.py` verifies the Nexus coordinator:
1. **Sandbox Prohibitions:** Verifies that importing `os` or calling `eval` triggers a `PermissionError` inside the AST sandbox.
2. **Playbook Compilation:** Simulates user prompts for each of the 24 use cases and asserts that Nexus builds the correct PyRel/SQL execution queries.
3. **Model Broker Routing:** Verifies that simple query strings compile using Luna, while complex optimization prompts route to Sol.