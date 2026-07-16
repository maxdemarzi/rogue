# 📊 Use Case 9: Public Equity Valuation Multiples & Comps Generator

This use case implements the **Public Equity Comps & Valuation Multiples** modeling workflow (similar to FinChat and Koyfin). It automates calculating P/E, EV/Revenue, and Debt/Equity multiples and charting growth parameters across peer groups.

---

## 🎯 FinChat & Rogo Problem Framings Solved
* **Valuation Multiples Generator:** Scraping peer filings to compile Price-to-Earnings (P/E), Enterprise Value-to-Sales (EV/Sales), and Debt-to-Equity ratios.
* **Financial Charting & Metrics Visualizer:** Mapping quarterly revenue growth profiles and operating margins against daily stock valuation changes.
* **Capital Structure Auditing:** Calculating leverage multiples (Debt/EBITDA) and returns on invested capital (ROIC) across peer universes.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s and FinChat’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Routes straightforward calculation scripts and aggregates daily closing stock prices.
2. **Frontier Routing (Sol @ $1.26):** Resolves non-recurring items or extraordinary adjustments to standardize peer EBITDAs.
3. **Structured Context Ingestion:** Bypasses web scraping by feeding directly from standard fundamental lines in `data/fundamentals/` and `data/simfin/`.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/fundamentals/](file:///home/maxdemarzi/rogue/data/fundamentals/)**: Balance sheet items, earnings rows, and capital parameters.
2. **[data/simfin/](file:///home/maxdemarzi/rogue/data/simfin/)**: Meta-details and company descriptors.
3. **[data/ohlcv/](file:///home/maxdemarzi/rogue/data/ohlcv/)**: Daily price and volume histories (to calculate current Market Caps).
4. **[data/sec_financials/](file:///home/maxdemarzi/rogue/data/sec_financials/)**: Pre-structured Balance Sheets and Income Statements.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Market Capitalization Integration
Map daily stock prices to shares outstanding to compute dynamic Market Caps:
```
(:Company {ticker: $TICKER}) -[:HAS_PRICE_SERIES]-> (:OHLCV {date: $DATE, close: $CLOSE})
```

### 2. Multiples Resolution
Link dynamic valuation multiples directly to the company profiles:
```
(:Company {ticker: $TICKER}) -[:HAS_VALUATION_MULTIPLE {date: $DATE}]-> (:ValuationMultiple {
  pe_ratio: pe,
  ev_revenue: ev_rev,
  debt_equity: de
})
```

---

## 💻 Technical Solution Steps

### Step 1: Calculate Dynamic Market Caps
Calculate recent market capitalization values using shares outstanding and daily closing stock prices:
```python
import pandas as pd

# Load shares outstanding from metadata
shares_df = pd.read_csv('data/simfin/companies.csv') # or relevant file containing metadata
shares_outstanding = 16000000000 # Example shares outstanding for AAPL

# Fetch daily closing price
price_df = pd.read_csv('data/ohlcv/stocks_us/1d/AAPL.csv')
price_df['Date'] = pd.to_datetime(price_df['Date'])
latest_price = price_df.sort_values('Date').iloc[-1]['Close']

market_cap = latest_price * shares_outstanding
print(f"Latest Stock Price: ${latest_price:.2f} | Market Capitalization: ${market_cap:,.2f}")
```

### Step 2: Extract Key Financial Metrics
Retrieve Revenue, Net Income, and Total Debt figures to prepare multiples:
```python
fundamentals_df = pd.read_csv('data/fundamentals/AAPL_fundamentals.csv') # or equivalent path
revenue = fundamentals_df[fundamentals_df['metric'] == 'total_revenue'].iloc[-1]['value']
net_income = fundamentals_df[fundamentals_df['metric'] == 'net_income'].iloc[-1]['value']
total_debt = fundamentals_df[fundamentals_df['metric'] == 'total_debt'].iloc[-1]['value']

print(f"Revenue: ${revenue:,.2f} | Net Income: ${net_income:,.2f} | Total Debt: ${total_debt:,.2f}")
```

### Step 3: Compute Valuation Multiples
Calculate standard financial multiples:
```python
pe_ratio = market_cap / net_income
ev_revenue = (market_cap + total_debt) / revenue
debt_equity = total_debt / (revenue - net_income) # proxy book equity

print(f"=== VALUATION MULTIPLES ===")
print(f"P/E Ratio: {pe_ratio:.2f}x")
print(f"EV / Revenue: {ev_revenue:.2f}x")
print(f"Debt / Equity: {debt_equity:.2f}x")
```
