# 📊 Use Case 11: Auditable, Live-Formula Excel Financial Modeler

This playbook implements the **"Last Mile" Excel Modeler** (similar to Rogo's *Subset* acquisition, which integrates smart spreadsheet agents directly into core banking platforms). It automates generating Excel files (`.xlsx`) pre-loaded with live, dynamic formulas rather than static values, allowing analysts to trace Free Cash Flow (FCF) projections and LBO schedules back to their inputs.

---

## 🎯 The "Last Mile" Analyst Needs Solved
* **Dynamic Spreadsheet Generation:** Creating forecast sheets pre-loaded with active Excel formulas (e.g. `SUM`, `AVERAGE`, CAGR formulas) rather than hardcoded numbers.
* **Audit-Trail Calculations:** Generating tracing chains so that analysts can click a projected Free Cash Flow cell and see the exact formula path leading back to historical EBITDA and working capital.
* **Comps Rollovers:** Swapping comparable companies in a sheet and having all multiple calculations update instantly.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Routes straightforward calculation scripts and aggregates daily closing stock prices.
2. **Frontier Routing (Sol @ $1.26):** Resolves non-recurring items or extraordinary adjustments to standardize peer EBITDAs.
3. **Structured Context Ingestion:** Bypasses web scraping by feeding directly from standard fundamental lines in `data/fundamentals/` and `data/simfin/`.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/fundamentals/](file:///home/maxdemarzi/rogue/data/fundamentals/)**: Balance sheet items, earnings rows, and capital parameters.
2. **[data/simfin/](file:///home/maxdemarzi/rogue/data/simfin/)**: Meta-details and company descriptors.
3. **[data/sec_financials/](file:///home/maxdemarzi/rogue/data/sec_financials/)**: Pre-structured Balance Sheets and Income Statements.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. The Model Driver Link
Connect historical variables to their forecast formula drivers:
```
(:Company {ticker: $TICKER}) -[:HAS_MODEL_DRIVER {metric: $METRIC}]-> (:ModelDriver {
  historical_avg_growth: $AVG_GROWTH,
  forecast_formula: $FORMULA
})
```

---

## 💻 Technical Solution Steps

### Step 1: Query Historical Variables
Load the historical financials to serve as the baseline for our forecast sheet:
```python
import pandas as pd

fundamentals_df = pd.read_csv('data/fundamentals/AAPL_fundamentals.csv')
revenue_hist = fundamentals_df[fundamentals_df['metric'] == 'total_revenue'].iloc[-3:]['value'].tolist()
print(f"Historical Revenues (Last 3 Years): {revenue_hist}")
```

### Step 2: Generate an Excel File with Live Formulas
Use `openpyxl` to build an Excel sheet containing active formulas for projections:
```python
import openpyxl

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Financial Forecast"

# Write headers
ws['A1'] = "Metric"
ws['B1'] = "2024 (A)"
ws['C1'] = "2025 (A)"
ws['D1'] = "2026 (A)"
ws['E1'] = "2027 (E)"
ws['F1'] = "2028 (E)"

# Write historical values
ws['A2'] = "Total Revenue"
ws['B2'] = revenue_hist[0]
ws['C2'] = revenue_hist[1]
ws['D2'] = revenue_hist[2]

# Write active Excel formulas for projections (assuming a 5% year-over-year growth rate)
ws['E2'] = "=D2*1.05"
ws['F2'] = "=E2*1.05"

# Save workbook
wb.save("AAPL_Financial_Model.xlsx")
print("Saved AAPL_Financial_Model.xlsx with live projection formulas!")
```

### Step 3: Audit Formula Integrity
Verify that the output sheet contains live string formulas rather than hardcoded floats:
```python
wb_loaded = openpyxl.load_workbook("AAPL_Financial_Model.xlsx", data_only=False)
ws_loaded = wb_loaded.active
print(f"Projected 2027 Revenue Formula: {ws_loaded['E2'].value}")
print(f"Projected 2028 Revenue Formula: {ws_loaded['F2'].value}")
```
