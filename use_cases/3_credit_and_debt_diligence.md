# 💳 Use Case 3: Credit Analysis and Debt Due Diligence

This use case automates fixed income analysis, corporate bond diligence, issuer credit rating history tracking, bankruptcy risk monitoring, and interest rate spread monitoring.

---

## 🎯 Rogo.ai Problem Framings Solved
* **Fixed Income & Bond Diligence:** Pulling bond coupon rates, maturities, face values, and issuer rating metrics to evaluate risk-return profiles.
* **Credit Rating & Default Risk Tracking:** Synthesizing rating upgrades, downgrades, and defaults across agencies (Moody's, S&P, Fitch, Fitch Solutions, CreditSights) for corporate and sovereign debt.
* **The AI Spreadsheet Agent (Subset Style):** Interrogating complex financial sheets to identify anomalies. For example, trace formulas to answer: *"Why is Free Cash Flow negative in 2027?"* or roll forward debt repayment schedules automatically.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Extracts bond coupon structures and maps basic issuer rating levels.
2. **Frontier Routing (Sol @ $1.26):** Audits negative metrics, executes Excel modeling logic, and traces formulas across multiple sheets to verify default risk indicators.
3. **Reasoning Reductions:** Integrates directly with pre-structured Excel parameters in `data/corporate_bonds/CompanyBonds.xlsx` to prevent token consumption on parsing raw tabular documents.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/corporate_bonds/](file:///home/maxdemarzi/rogue/data/corporate_bonds/)**: Corporate bond details including coupon rates, maturities, and ratings.
2. **[data/corporate_credit_ratings/](file:///home/maxdemarzi/rogue/data/corporate_credit_ratings/)**: Issuer rating history and rating action updates.
3. **[data/sovereign_ratings/](file:///home/maxdemarzi/rogue/data/sovereign_ratings/)**: National government credit rating history.
4. **[data/bankruptcy_risk/](file:///home/maxdemarzi/rogue/data/bankruptcy_risk/)**: Monthly quantitative default probability timelines.
5. **[data/interest_rate_spreads/](file:///home/maxdemarzi/rogue/data/interest_rate_spreads/)**: Daily macro spreads (10Y-2Y, AAA/BAA corporate yield differentials).
6. **[data/treasury_yields/](file:///home/maxdemarzi/rogue/data/treasury_yields/)**: Daily constant maturity yield curve profiles.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Bond Issuance & Credit Risk
Map corporate bond issues to their credit ratings:
```
(:Company {ticker: $TICKER}) -[:ISSUED_BOND]-> (:Bond {sku: $SKU}) -[:HAS_BOND_RATING]-> (:CreditRating)
```

### 2. Time-Series Default Risks
Align monthly default probability metrics with rating actions:
```
(:Company {name: $NAME}) -[:HAS_BANKRUPTCY_RISK]-> (:BankruptcyRisk {date: $DATE, probability: $PROB})
```

### 3. Yield Curve Alignment
Track macro credit spreads against specific rating buckets:
```
(:MacroIndicator {date: $DATE}) -[:AFFECTS]-> (:Company {ticker: $TICKER})
```
Compare `BAA10Y` spread changes to the pricing volatility of BAA-rated bonds.

---

## 💻 Technical Solution Steps

### Step 1: Ingest Corporate Bonds & Ratings
Load bond listings, maturities, and credit grades:
```python
import pandas as pd

# Note: openpyxl is installed to support reading Excel files
bonds_df = pd.read_excel('data/corporate_bonds/CompanyBonds.xlsx')
print("=== CORPORATE BOND LISTINGS ===")
print(bonds_df[['SYMBOL', 'BOND TYPE', 'COUPON RATE', 'CREDIT RATING', 'MATURITY DATE']].head(5))
```

### Step 2: Track Corporate Credit Rating Actions
Evaluate upgrades and downgrades to flag deteriorating credit risks:
```python
ratings_df = pd.read_csv('data/corporate_credit_ratings/Morningstar Corporate Credit Ratings - 2019.csv')
print("=== RATING ACTIONS LOG ===")
print(ratings_df[['obligor_name', 'rating', 'rating_agency_name', 'rating_action_date']].head(5))
```

### Step 3: Monitor Macro Interest Spreads
Load daily credit risk spreads (e.g. BAA-rated corporate bonds yield vs 10Y US Treasury) to monitor market stress levels:
```python
spreads_df = pd.read_csv('data/interest_rate_spreads/FRED_InterestRate_Data.csv')
spreads_df['Date'] = pd.to_datetime(spreads_df['Date'])
# Filter recent dates where default spreads are elevated
stressed_periods = spreads_df[spreads_df['BAA10Y'] > 3.0].sort_values('Date')
print("=== ELEVATED CREDIT SPREAD PERIODS ===")
print(stressed_periods[['Date', 'T10Y2Y', 'BAA10Y', 'AAA10Y']].tail(5))
```
