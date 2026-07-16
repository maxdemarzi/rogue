# 🌐 Use Case 4: Supply Chain Contagion and Macro Exposure

This use case automates supply chain dependency mapping, inter-industry contagion analysis, corporate input commodity exposure monitoring, and trade credit liquidity risk modeling.

---

## 🎯 Rogo.ai Problem Framings Solved
* **Supply Chain Dependency & Contagion:** Mapping partner and supplier networks to trace systemic risks (e.g., if a supplier goes bankrupt or raises prices, which customers are exposed?).
* **Commodity Price Exposure:** Tracking daily gold, oil, silver, copper, and agricultural prices to evaluate input cost (COGS) shocks for exposed sectors.
* **Trade Credit & Accounts Receivable Liquidity:** Modeling Days Sales Outstanding (DSO) and accounts receivable risk profiles across sectors and countries.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Sweeps daily commodity price levels or pulls country inflation metrics.
2. **Frontier Routing (Sol @ $1.26):** Evaluates multi-hop contagion risks (e.g., tracing a price spike in raw copper through intermediate suppliers to downstream companies).
3. **Structured Context Ingestion:** Utilizes sector revenue tables from `data/naics_contagion/` and B2B linkages from `data/business_network/` to provide structured context, reducing token overhead.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/business_network/](file:///home/maxdemarzi/rogue/data/business_network/)**: Domain-to-domain partner and vendor connections.
2. **[data/supply_chain/](file:///home/maxdemarzi/rogue/data/supply_chain/)**: SKU logistics, supplier pricing, and manufacturing costs.
3. **[data/trade_credit/](file:///home/maxdemarzi/rogue/data/trade_credit/)**: Accounts receivable cycles (DSO) and financing costs.
4. **[data/naics_contagion/](file:///home/maxdemarzi/rogue/data/naics_contagion/)**: Sector-to-sector revenue share dependency matrices.
5. **[data/commodity_prices/](file:///home/maxdemarzi/rogue/data/commodity_prices/)**: Daily global gold, silver, crude oil, and copper prices.
6. **[data/global_inflation/](file:///home/maxdemarzi/rogue/data/global_inflation/)**: National yearly CPI inflation rates.
7. **[data/fx_rates/](file:///home/maxdemarzi/rogue/data/fx_rates/)**: Daily foreign exchange rates to standardize multinational financials.
8. **[data/macroeconomics/](file:///home/maxdemarzi/rogue/data/macroeconomics/)**: Daily Fed interest rates and treasury indexes.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Corporate Supply Network
Trace corporate partnerships and customer-vendor exposure:
```
(:Company {domain: $VENDOR}) -[:SUPPLIES_TO {revenue_share: $SHARE}]-> (:Company {domain: $CUSTOMER})
```

### 2. Commodity Cost Exposure
Map raw material dependencies from industries to pricing indexes:
```
(:Industry {name: $SECTOR}) -[:USES_COMMODITY]-> (:Commodity {ticker: $TICKER})
```
Assess profit margin compression when daily commodity pricing surges.

### 3. Sector Liquidity Risk
Track trade credit delinquency speeds per sector and country:
```
(:Industry {name: $SECTOR}) -[:HAS_TRADE_CREDIT]-> (:TradeCredit {country: $COUNTRY, dso_range: $DSO})
```

---

## 💻 Technical Solution Steps

### Step 1: Trace Customer-Vendor B2B Links
Query the business network file using web domains to map public-private supplier linkages:
```python
import pandas as pd

net_df = pd.read_csv('data/business_network/domain_partnerships.csv') # or relevant CSV inside the folder
# Find key partners for a specific corporate domain
company_partners = net_df[net_df['home_domain'] == 'apple.com']
print("=== CORPORATE B2B PARTNERS ===")
print(company_partners[['home_domain', 'link_domain', 'partnership_type']].head(5))
```

### Step 2: Track Daily Commodity Spot Prices
Analyze daily crude oil benchmark spot pricing (WTI & Brent) to calculate input cost inflation rates:
```python
# Note: openpyxl supports reading Excel sheets for crude prices
oil_df = pd.read_excel('data/crude_oil_prices/Crude oil and Sustainable Indices - US and India.xlsx')
oil_df['Date'] = pd.to_datetime(oil_df['Date'])
recent_oil = oil_df.sort_values('Date').tail(5)
print("=== OIL PRICE TIMELINE ===")
print(recent_oil[['Date', 'WTI', 'Brent']])
```

### Step 3: Monitor Sector Trade Credit DSO Ranges
Evaluate Days Sales Outstanding (DSO) to model cash conversion cycles:
```python
trade_df = pd.read_excel('data/trade_credit/Trade_Credit_and_Financing_Costs.xlsx', sheet_name='Combined')
# Filter for Manufacturing sectors with slow DSO payment terms (>60 days or high ranges)
slow_payers = trade_df[
    (trade_df['SECTOR'] == 'Manufacturing') & 
    (trade_df['DATA_DETAIL'].str.contains('DSO >= 60', na=False))
]
print("=== MANUFACTURING DSO STRESS ===")
print(slow_payers[['COUNTRY', 'DATA_DETAIL', '2017', 'SIZE']].head(5))
```
