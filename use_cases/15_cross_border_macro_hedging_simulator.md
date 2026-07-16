# 🌍 Use Case 15: Cross-Border FX and Inflation Arbitrage Simulator

This playbook implements the **Cross-Border FX and Inflation Arbitrage Simulator**—a mind-blowing global macro hedge fund and corporate treasury workflow. It simulates currency volatility, inflation curves, and sovereign rating trajectories to recommend corporate hedging or macro carry trade allocations.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **FX Inflation Arbitrage:** Modeling how divergence in country-level inflation rates (`data/global_inflation/`) affects bilateral foreign exchange rates (`data/fx_rates/`) over time (Purchasing Power Parity shocks).
* **Sovereign Debt Risk Simulator:** Mapping sovereign debt-to-GDP levels (`data/country_debt/`, `data/country_gdp_employment/`) and economic liberty metrics (`data/economic_freedom/`) to forecast credit upgrades/downgrades (`data/sovereign_ratings/`).
* **Commodity Hedging Modeler:** Determining optimal input cost hedges by standardizing raw material pricing trends (`data/commodity_prices/`) with currency exchange volatility.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Fetches daily currency pairings and lists yearly inflation values.
2. **Frontier Routing (Sol @ $1.26):** Resolves complex sovereign default probability models and drafts structural carry trade strategies.
3. **Structured Context Ingestion:** Bypasses manual searches by directly indexing macro timelines from FRED, UK costs indices, and Swedish macro files.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/global_inflation/](file:///home/maxdemarzi/rogue/data/global_inflation/)**: National yearly CPI inflation rates.
2. **[data/fx_rates/](file:///home/maxdemarzi/rogue/data/fx_rates/)**: Daily foreign exchange rates.
3. **[data/sovereign_ratings/](file:///home/maxdemarzi/rogue/data/sovereign_ratings/)**: National government credit rating histories.
4. **[data/country_debt/](file:///home/maxdemarzi/rogue/data/country_debt/)**: Central government debt ratios.
5. **[data/economic_freedom/](file:///home/maxdemarzi/rogue/data/economic_freedom/)**: National regulatory and trade freedom indexes.
6. **[data/commodity_prices/](file:///home/maxdemarzi/rogue/data/commodity_prices/)**: Daily crude oil, gold, silver, and copper spot prices.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Macro Economic Exposure Node
Link country profiles to their inflation rates and credit ratings:
```
(:Country {name: $COUNTRY}) -[:HAS_INFLATION_RECORD {date: $DATE}]-> (:Inflation {rate: $RATE})
  -[:HAS_SOVEREIGN_RATING]-> (:SovereignRating {grade: $GRADE})
```

### 2. Cross-Border FX Pairings
Map daily exchange rates between two national nodes:
```
(:Country {name: $COUNTRY_A}) -[:FX_PAIR {ticker: $TICKER}]-> (:FXRate {date: $DATE, value: $RATE})
  <-[:FX_PAIR]- (:Country {name: $COUNTRY_B})
```

---

## 💻 Technical Solution Steps

### Step 1: Trace Global Inflation Levels
Load country-level consumer price inflation timelines to identify macro divergence:
```python
import pandas as pd

inflation_df = pd.read_csv('data/global_inflation/global_inflation.csv') # or equivalents
# Filter for countries experiencing elevated CPI (>10%)
high_inflation = inflation_df[inflation_df['CPI_Rate'] > 10.0].sort_values('Year')
print("=== ELEVATED GLOBAL CPI RECORDS ===")
print(high_inflation[['Country', 'Year', 'CPI_Rate']].tail(5))
```

### Step 2: Correlate with Bilateral FX Rates
Analyze how inflation gaps match up with daily foreign exchange fluctuations:
```python
fx_df = pd.read_csv('data/fx_rates/daily_fx_rates.csv') # or equivalents
fx_df['Date'] = pd.to_datetime(fx_df['Date'])
# Select historical USD/EUR or USD/SEK pairing
sek_rates = fx_df.sort_values('Date').tail(5)
print("=== DAILY FX TIMELINE ===")
print(sek_rates[['Date', 'USD_SEK', 'USD_EUR']])
```

### Step 3: Audit Sovereign Credit Ratings
Evaluate national credit rating trajectories alongside economic freedom scores:
```python
ratings_df = pd.read_csv('data/sovereign_ratings/sovereign_ratings.csv')
freedom_df = pd.read_csv('data/economic_freedom/economic_freedom.csv')

# Merge rating updates with economic liberty scores to forecast country risk shifts
country_risk = pd.merge(ratings_df, freedom_df, on='Country')
print("=== SOVEREIGN COUNTRY Risk INDEX ===")
print(country_risk[['Country', 'Credit_Rating', 'Freedom_Score']].head(5))
```
