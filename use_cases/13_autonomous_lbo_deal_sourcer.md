# 🤖 Use Case 13: Autonomous PE/LBO Target Deal Hunter & Valuator

This playbook implements the **Autonomous PE/LBO Target Deal Hunter**—a mind-blowing automation workflow that does the sourcing work of an entire team of private equity associates. It screens companies using multiple operational dimensions, checks litigation risk, calculates LBO debt capacity, and builds a forecast sheet with live formulas.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **Autonomous Multidimensional Screening:** Sifting public and private companies to locate LBO targets with low valuation multiples (`data/fundamentals/`), high startup VC traction (`data/startup_vc/`), and minimal litigation risk (`data/patent_litigation/`).
* **Governance Quality Auditing:** Reviewing CEO salaries and pay-to-worker ratios (`data/ceo_salaries/`) to flag bloated cost structures that can be optimized post-acquisition.
* **Automatic LBO Debt Capacity Modeler:** Calculating how much debt (Senior, Mezzanine) the target’s Free Cash Flows can support, and generating a spreadsheet loaded with active Excel formulas.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Filters companies based on simple revenue and sector tags.
2. **Frontier Routing (Sol @ $1.26):** Resolves LBO structures, runs the optimization formulas, and builds the investment committee thesis.
3. **Structured Context Ingestion:** Bypasses manual searches by direct joins across local datasets like `data/fundamentals/` and `data/ceo_salaries/`.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/startup_vc/](file:///home/maxdemarzi/rogue/data/startup_vc/)**: Private company funding milestones and statuses.
2. **[data/fundamentals/](file:///home/maxdemarzi/rogue/data/fundamentals/)**: Income sheets and debt metrics.
3. **[data/patent_litigation/](file:///home/maxdemarzi/rogue/data/patent_litigation/)**: Active litigation histories.
4. **[data/ceo_salaries/](file:///home/maxdemarzi/rogue/data/ceo_salaries/)**: Executive pay and governance ratios.
5. **[data/ohlcv/](file:///home/maxdemarzi/rogue/data/ohlcv/)**: Daily prices to track current trading valuation multiples.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. The Deal Sourcing Join
Locate target companies matching PE criteria:
```
(:Company {ticker: $TICKER}) -[:HAS_METRICS]-> (:FilingMetrics {revenue: $REV, debt: $DEBT})
  -[:HAS_GOVERNANCE]-> (:CEOPay {pay_ratio: $RATIO})
```

### 2. Litigation Risk Check
Verify target does not face active structural patent disputes:
```
(:Company {name: $TARGET}) -[:DEFENDANT_IN]-> (:LitigationCase {status: $STATUS})
```

---

## 💻 Technical Solution Steps

### Step 1: Run Multi-Criteria Target Sourcing
Filter companies with stable revenues, reasonable debt loads, and high executive overhead:
```python
import pandas as pd

ceo_df = pd.read_csv('data/ceo_salaries/ceo_data_pay_merged_sp500.csv')
# Screen for companies with high executive pay overhead (potential restructuring targets)
targets = ceo_df[
    (ceo_df['total_ceo_pay'] > 15000000) & 
    (ceo_df['pay_ratio'] > 300)
]
print("=== SOURCED RESTRUCTURING CANDIDATES ===")
print(targets[['company_name', 'ceo_name', 'total_ceo_pay', 'pay_ratio']].head(5))
```

### Step 2: Audit Intellectual Property Litigation Exposure
Verify that target candidates do not have active legal disputes:
```python
litigation_df = pd.read_csv('data/patent_litigation/Patent_Data.csv')
target_names = targets['company_name'].tolist()

# Find any lawsuits matching our targets
active_suits = litigation_df[litigation_df['parent_company'].isin(target_names)]
print("=== ACTIVE LITIGATION OVERLAPS ===")
print(active_suits[['parent_company', 'plaintiff', 'defendant']])
```

### Step 3: Compute Debt Capacity & Generate LBO Sheet
Build the debt payoff schedule sheet with dynamic formulas:
```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "LBO Model"

# Write headers and assumptions
ws['A1'] = "Parameter"
ws['B1'] = "Value"
ws['A2'] = "Purchase Price"
ws['B2'] = 1000000000  # $1B Purchase price
ws['A3'] = "Equity Contribution (40%)"
ws['B3'] = "=B2*0.40"
ws['A4'] = "Debt Contribution (60%)"
ws['B4'] = "=B2*0.60"

# Save workbook
wb.save("Target_LBO_Model.xlsx")
print("Saved Target_LBO_Model.xlsx with live LBO debt capacity formulas!")
```
