# 🌀 Use Case 22: Supply Chain Holding Cost & Inflation Squeeze Model

This playbook implements the **Supply Chain Holding Cost & Inflation Squeeze Model**—a corporate treasury and LBO target underwriting workflow. It projects how WACC and inflation shocks squeeze the margins of high-DSO / high-inventory supply chains.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **Working Capital Squeeze Mapping:** Projects how WACC increases input holding costs based on DSO durations and inventory cycles.
* **Inflation Margin Stress-Testing:** Simulates gross margin degradation when local CPI increases procurement costs.
* **LBO Debt Capacity Adjustments:** Subtracts working capital squeeze losses from projected cash flows to adjust debt payoffs.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/business_network/](file:///home/maxdemarzi/rogue/data/business_network/)**: Domain supply linkages.
2. **[data/trade_credit/](file:///home/maxdemarzi/rogue/data/trade_credit/)**: Days Sales Outstanding (DSO) values and financing costs.
3. **[data/global_inflation/](file:///home/maxdemarzi/rogue/data/global_inflation/)**: National CPI rates.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Supply Chain Squeeze
Link supplier domains to trade credit terms and local inflation:
```
(:Company {name: $COMPANY}) -[:APPLIES_TO_TRADE]-> (:TradeCredit {dso_value: $DSO})
  -[:DOMICILED_IN]-> (:Country) -[:HAS_CPI]-> (:Inflation {rate: $CPI})
```

---

## 💻 Technical Solution Steps

### Step 1: Trace Trade Credit Terms
Identify high-DSO sectors susceptible to cash-flow squeeze:
```python
import pandas as pd

trade_df = pd.read_excel('data/trade_credit/Trade_Credit_and_Financing_Costs.xlsx', sheet_name='Combined')
high_dso_sectors = trade_df[trade_df['DATA_DETAIL'] == 'DSO_value'].sort_values('2017', ascending=False)

print("=== HIGH DSO WORKING CAPITAL SECTORS ===")
print(high_dso_sectors[['COUNTRY', 'SECTOR', '2017']].head(5))
```
