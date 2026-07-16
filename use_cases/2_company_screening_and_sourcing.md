# 🔍 Use Case 2: Private and Public Company Sourcing & Screening

This use case automates corporate sourcing, private company deal screening, VC investment history tracking, M&A advisory preparation, and board interlocks mapping.

---

## 🎯 Rogo.ai Problem Framings Solved
* **Private Company Screening & Sourcing:** Aggregating VC rounds, funding directories, and ownership structures to screen potential acquisition targets.
* **Deterministic Screening (March Update Style):** Performing deterministic filters across structured company facts to isolate target investments at scale.
* **Corporate Governance & Board Networks:** Mapping director relationships and board interlocks to discover pathways of executive influence and board connectivity.
* **CEO vs. Worker Pay Benchmarking:** Comparing corporate executive compensation profiles to evaluate governance and capital allocation.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Handles basic profile aggregation, company background lookup, and formatting bios.
2. **Frontier Routing (Sol @ $1.26):** Evaluates complex board-interlock relationships (e.g. comparing overlapping corporate governance risks or finding strategic influence pathways).
3. **Structured Context Ingestion:** Models feed on structured directories from `data/startup_vc/` and `data/board_members/`, skipping the massive raw web searches to run on highly localized database mappings.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/startup_vc/](file:///home/maxdemarzi/rogue/data/startup_vc/)**: VC investment rounds, company categories, and funding paths (Crunchbase-equivalent database).
2. **[data/mergers_acquisitions/](file:///home/maxdemarzi/rogue/data/mergers_acquisitions/)**: Historical records of corporate acquisitions valued at $20B+.
3. **[data/executives/](file:///home/maxdemarzi/rogue/data/executives/)**: Corporate leadership directory mapping CEOs, CFOs, and board profiles.
4. **[data/board_members/](file:///home/maxdemarzi/rogue/data/board_members/)**: Board director list for Fortune 100 corporations.
5. **[data/ceo_salaries/](file:///home/maxdemarzi/rogue/data/ceo_salaries/)**: Corporate CEO compensation metrics and pay ratios.
6. **[data/business_network/](file:///home/maxdemarzi/rogue/data/business_network/)**: Domain-to-domain partner linkages to map corporate relationships.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Board Interlock Connections
Discover shared directors connecting different corporate boards:
```
(:Company {name: $COMPANY_A}) <-[:SITS_ON_BOARD]- (:Person) -[:SITS_ON_BOARD]-> (:Company {name: $COMPANY_B})
```

### 2. Venture Capital Sourcing
Trace private funding stages and corporate lineage:
```
(:Company {name: $STARTUP}) <-[:INVESTED_IN {rounds: $ROUNDS, amount: $AMOUNT}]- (:Company {name: $PE_VC_FIRM})
```

### 3. Executive Migration & Compensation
Map corporate roles and executive governance metrics:
```
(:Person {name: $CEO}) -[:IS_EXECUTIVE {total_pay: $PAY, pay_ratio: $RATIO}]-> (:Company {ticker: $TICKER})
```

---

## 💻 Technical Solution Steps

### Step 1: Map Board Director Interlocks
Query the board directory to locate individuals holding multiple seats across Fortune 100 boards:
```python
import pandas as pd

board_df = pd.read_csv('data/board_members/boardmembers.csv')
# Identify directors sitting on multiple boards
interlocks = board_df.groupby('BoardMemberName').filter(lambda x: len(x) > 1)
print(interlocks.sort_values('BoardMemberName').head(10))
```

### Step 2: Screen Private Funding Targets by Category
Filter VC databases for high-growth tech or biotech startups to populate target screening pools:
```python
vc_companies = pd.read_csv('data/startup_vc/apps_VC.csv') # or investments_VC.csv depending on file structures
# Filter by category and funding thresholds
target_pool = vc_companies[
    (vc_companies['market'].str.contains('Software|Biotechnology', na=False)) & 
    (vc_companies['funding_total_usd'] > 10000000)
]
print(target_pool[['name', 'market', 'funding_total_usd', 'status']].head(5))
```

### Step 3: Analyze CEO Pay Ratios
Benchmark executive compensation stats against peer companies:
```python
ceo_df = pd.read_csv('data/ceo_salaries/ceo_data_pay_merged_sp500.csv')
high_pay_ratios = ceo_df.sort_values('pay_ratio', ascending=False)
print(high_pay_ratios[['company_name', 'ceo_name', 'total_ceo_pay', 'pay_ratio']].head(5))
```
