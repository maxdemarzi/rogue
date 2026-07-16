# 🛢️ Use Case 24: Corporate Input Commodity Hedging Solver

This playbook implements the **Corporate Input Commodity Hedging Solver**—an industrial corporate treasury and commodity risk management workflow. It uses Swan's prescriptive HiGHS solver to optimize derivative hedging cover ratios across crude oil, gold, silver, and copper spot price timelines.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **Commodity Cost Volatility Audits:** Analyzes daily price changes for key raw materials (oil, metals) to identify input margin risks.
* **Derivative Portfolio Allocation:** Formulates linear constraints to minimize procurement cost variance under corporate treasury budgets.
* **Margin Impact Stress-Testing:** Simulates gross margin improvements when procurement contracts are fully covered by derivatives.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/commodity_prices/](file:///home/maxdemarzi/rogue/data/commodity_prices/)**: Daily commodity prices (gold, crude oil, copper, silver).
2. **[data/fundamentals/](file:///home/maxdemarzi/rogue/data/fundamentals/)**: Cost of goods sold (COGS) and inventory asset holdings.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Commodity Exposure
Link industrial companies to their input raw materials:
```
(:Company {name: $COMPANY}) -[:PROCURES]-> (:Commodity {commodity_name: $COMMODITY})
  -[:HAS_PRICE_SERIES]-> (:OHLCV {close_val: $VAL})
```

---

## 💻 Technical Solution Steps

### Step 1: Trace Daily Commodity Spot Prices
Identify price fluctuations for base commodities:
```python
import pandas as pd

gold_df = pd.read_csv('data/gold_prices/final_uso.csv')
gold_df['Date'] = pd.to_datetime(gold_df['Date'])
latest_prices = gold_df.sort_values('Date').tail(5)

print("=== LATEST COMMODITY PRICE TIMELINE ===")
print(latest_prices[['Date', 'Close', 'Volume']])
```
