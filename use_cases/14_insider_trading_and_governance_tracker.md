# 🕵️ Use Case 14: Insider Trading & Corporate Governance Tracker

This playbook implements the **Insider Trading & Corporate Governance Anomalies Tracker**—a mind-blowing compliance and activist hedge fund workflow. It maps transaction behaviors of corporate executives and board members shortly before material corporate events (like earnings estimates revisions, patent disputes, or credit rating actions) to flag governance risks or activist targets.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **Active Trading Anomalies:** Mapping when C-Suite executives (`data/executives/`) or directors (`data/board_members/`) sell down equity positions shortly before credit downgrades (`data/corporate_credit_ratings/`) or earnings surprises (`data/earnings_estimates/`).
* **Activists Sourcing Engine:** Sourcing companies with weak alignment (such as high CEO-to-worker pay ratios in `data/ceo_salaries/` paired with net executive selling and board member overlaps).
* **Corporate Governance Auditing:** Mapping interlocking boards to identify pathways where non-public strategic information might migrate between companies.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Routes routine insider transaction listings and parses director names.
2. **Frontier Routing (Sol @ $1.26):** Resolves complex correlation patterns (e.g. cross-referencing insider selling dates with post-event news articles to assess potential governance breaches).
3. **Structured Context Ingestion:** Cross-joins local tables from `data/board_members/` and executive databases rather than reading general news feeds.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/insider_trading/](file:///home/maxdemarzi/rogue/data/insider_trading/)**: Transaction filings, dates, sizes, and executives.
2. **[data/executives/](file:///home/maxdemarzi/rogue/data/executives/)**: C-Suite listings.
3. **[data/board_members/](file:///home/maxdemarzi/rogue/data/board_members/)**: Fortune 100 director board lists.
4. **[data/ceo_salaries/](file:///home/maxdemarzi/rogue/data/ceo_salaries/)**: Executive pay and worker pay ratio databases.
5. **[data/earnings_estimates/](file:///home/maxdemarzi/rogue/data/earnings_estimates/)**: Consensus EPS numbers and beat/miss streaking.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Insider Trading Context
Link transaction actions to the executive and their firm:
```
(:Person {name: $NAME}) -[:IS_EXECUTIVE]-> (:Company {ticker: $TICKER})
  -[:HAS_INSIDER_TRADE {date: $DATE, transaction_type: $TYPE, size: $VAL}]-> (:InsiderTrade)
```

### 2. Event Proximity Alignment
Detect trades occurring in the 30-day window leading up to an earnings release:
```
(:Company {ticker: $TICKER}) -[:HAS_EARNINGS_ESTIMATE {date: $EARNINGS_DATE}]-> (:EarningsEstimate)
```

---

## 💻 Technical Solution Steps

### Step 1: Scan Insider Trade Filings
Query insider trades to isolate massive executive sell-offs:
```python
import pandas as pd

# Load insider transactions logs
trades_df = pd.read_csv('data/insider_trading/insider_trades.csv') # or equivalents
large_sales = trades_df[
    (trades_df['transaction_type'] == 'Sale') & 
    (trades_df['shares_traded'] > 100000)
]
print("=== LARGE EXECUTIVE SALES ===")
print(large_sales[['ticker', 'insider_name', 'position', 'shares_traded', 'trade_date']])
```

### Step 2: Correlate with Next Earnings Release Date
Cross-reference transaction timelines with earnings consensus estimates to flag trades close to the quiet window:
```python
estimates_df = pd.read_csv('data/earnings_estimates/earnings_features_clean (1).csv')
estimates_df['earnings_date'] = pd.to_datetime(estimates_df['earnings_date'])
large_sales['trade_date'] = pd.to_datetime(large_sales['trade_date'])

for _, trade in large_sales.head(5).iterrows():
    # Find next earnings date for this stock
    next_earnings = estimates_df[
        (estimates_df['ticker'] == trade['ticker']) & 
        (estimates_df['earnings_date'] > trade['trade_date'])
    ].sort_values('earnings_date').iloc[0]
    
    days_to_earnings = (next_earnings['earnings_date'] - trade['trade_date']).days
    print(f"Ticker: {trade['ticker']} | Trade Date: {trade['trade_date'].date()} | Earnings Date: {next_earnings['earnings_date'].date()} | Gap: {days_to_earnings} Days")
```

### Step 3: Map Board Member Interlocks
Trace if the executing insider holds seats on peer boards:
```python
board_df = pd.read_csv('data/board_members/boardmembers.csv')
director_shares = board_df[board_df['BoardMemberName'] == trade['insider_name']]
print("=== GOVERNANCE INTERLOCKS ===")
print(director_shares[['Company', 'BoardMemberName']])
```
