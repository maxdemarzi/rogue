# 🌀 Use Case 12: Restructuring and Supplier Contagion Simulator

This playbook implements the **Systemic Restructuring & Supplier Contagion Simulator**—a mind-blowing capability that goes beyond document reading or simple Q&A. It maps what happens to a company's entire value chain if it experiences a distress event or debt restructuring, tracking downstream contagion and trade credit losses.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **Dynamic Maturity Wall Shock:** Simulating what happens when a company's upcoming debt maturity (`data/corporate_bonds/`) is forced to refinance at current macro interest rate spreads (`data/interest_rate_spreads/`).
* **Multi-Hop Supply Chain Contagion:** Tracing downstream domains (`data/business_network/`) to flag which partner companies will suffer revenue losses or trade credit write-offs (`data/trade_credit/`) if the parent company defaults.
* **Macro Distress Aggregators:** Estimating how a cluster of defaults or layoffs (`data/corporate_layoffs/`) in a specific NAICS code affects adjacent sectors (`data/naics_contagion/`).

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Sweeps daily interest rate indices and parses basic vendor connections.
2. **Frontier Routing (Sol @ $1.26):** Executes the multi-hop systemic risk model, calculates projected cash shortfalls, and drafts the distress warning report.
3. **Structured Context Ingestion:** Operates directly over pre-constructed graph edges (`Company -> SUPPLIES_TO -> Customer`) rather than attempting to discover connections by reading raw news feeds.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/bankruptcy_risk/](file:///home/maxdemarzi/rogue/data/bankruptcy_risk/)**: Monthly quantitative default probability timelines.
2. **[data/corporate_bonds/](file:///home/maxdemarzi/rogue/data/corporate_bonds/)**: Debt maturities, coupons, and credit grades.
3. **[data/interest_rate_spreads/](file:///home/maxdemarzi/rogue/data/interest_rate_spreads/)**: BAA/AAA corporate yield spreads over Treasuries.
4. **[data/business_network/](file:///home/maxdemarzi/rogue/data/business_network/)**: Domain-to-domain supplier linkages.
5. **[data/trade_credit/](file:///home/maxdemarzi/rogue/data/trade_credit/)**: Accounts receivable cycles and DSO terms.
6. **[data/corporate_layoffs/](file:///home/maxdemarzi/rogue/data/corporate_layoffs/)**: Headcount cuts.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Distress Contagion Chain
Trace how a company's distress spreads to its suppliers:
```
(:Company {name: $DISTRESSED_CO}) -[:HAS_BANKRUPTCY_RISK {date: $DATE, probability: $PROB}]-> (:BankruptcyRisk)
  <-[:SUPPLIES_TO {revenue_share: $SHARE}]- (:Company {name: $SUPPLIER_CO})
```

### 2. Trade Credit Risk Intersection
Estimate trade credit losses for exposed suppliers:
```
(:Company {name: $SUPPLIER_CO}) -[:HAS_TRADE_CREDIT]-> (:TradeCredit {dso_range: $DSO})
```

---

## 💻 Technical Solution Steps

### Step 1: Detect Distressed Debt Maturity Walls
Identify companies with deteriorating credit ratings and debt maturities coming due:
```python
import pandas as pd

bonds_df = pd.read_excel('data/corporate_bonds/CompanyBonds.xlsx')
# Filter for high maturity risk debt with speculative ratings
distressed_issuers = bonds_df[
    (bonds_df['CREDIT RATING'].isin(['B', 'CCC'])) & 
    (pd.to_datetime(bonds_df['MATURITY DATE']).dt.year <= 2027)
]
print("=== DISTRESSED ISSUERS MATURITY Risk ===")
print(distressed_issuers[['SYMBOL', 'BOND TYPE', 'CREDIT RATING', 'MATURITY DATE']])
```

### Step 2: Map the Supplier Contagion Network
Trace vendors connected to these distressed corporate domains:
```python
net_df = pd.read_csv('data/business_network/domain_partnerships.csv')
# Assuming Apple was the distressed domain, list exposed suppliers
exposed_partners = net_df[net_df['link_domain'] == 'apple.com']
print("=== EXPOSED SUPPLIER NETWORK ===")
print(exposed_partners[['home_domain', 'link_domain', 'partnership_type']])
```

### Step 3: Estimate Trade Credit Delinquency Impact
Cross-reference these exposed suppliers with sector trade credit Terms:
```python
trade_df = pd.read_excel('data/trade_credit/Trade_Credit_and_Financing_Costs.xlsx', sheet_name='Combined')
# Pull default probabilities and DSO lengths for exposed manufacturing/tech partners
print("=== TRADE CREDIT WRITE-OFF PROJECTIONS ===")
print(trade_df[['COUNTRY', 'SECTOR', 'DATA_DETAIL', '2017']].head(5))
```
