# 📈 Use Case 6: Broker Research and Analyst Ratings Synthesis

This use case automates the collection, structuring, and sentiment synthesis of Wall Street broker research (sell-side analyst reports) and rating changes.

---

## 🎯 Rogo.ai & AlphaSense Problem Framings Solved
* **Aftermarket Broker Research Consolidation:** Consolidating and comparing ratings, recommendation shifts (Upgrades/Downgrades), and price targets across major research desks.
* **Semantic Sentiment & Tone Analysis:** Scanning research text to extract positive, negative, or neutral sentiment scores and detecting shifts in analyst confidence.
* **Synonym-Expanded Search:** Searching across reports using synonym expansion (e.g. searching "revenue growth" automatically pulls "top-line expansion", "sales increase", or "turnover acceleration").

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Sweeps daily ratings logs to isolate target upgrades/downgrades and standardizes price targets.
2. **Frontier Routing (Sol @ $1.26):** Resolves contradictions between different broker reports (e.g. if Morgan Stanley is bullish on a company but Goldman Sachs is bearish, summarizing the core points of debate).
3. **Structured Context Ingestion:** Extracts tables from `data/financial_news/analyst_ratings_processed.csv` to serve as clean structured templates, preventing token wastage on raw text parsing.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/financial_news/](file:///home/maxdemarzi/rogue/data/financial_news/)**: Labeled analyst ratings log, price targets, and recommendation actions.
2. **[data/financial_phrasebank/](file:///home/maxdemarzi/rogue/data/financial_phrasebank/)**: Sentiment annotated sentences to train sentiment mapping engines.
3. **[data/earnings_estimates/](file:///home/maxdemarzi/rogue/data/earnings_estimates/)**: Historical quarterly consensus figures.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. The Broker Rating Edge
Link broker recommendations directly to corporate nodes:
```
(:Broker {name: $BROKER}) -[:ISSUED_RATING {
  action: rating_action,
  old_rating: prev_rating,
  new_rating: current_rating,
  target_price: target_val,
  date: $DATE
}]-> (:Company {ticker: $TICKER})
```

### 2. Consensus Sentiment Alignment
Map aggregate analyst sentiment to historical performance changes:
```
(:Company {ticker: $TICKER}) -[:HAS_CONSENSUS_SENTIMENT]-> (:ConsensusSentiment {
  bullish_ratio: bull_pct,
  bearish_ratio: bear_pct,
  date: $DATE
})
```

---

## 💻 Technical Solution Steps

### Step 1: Ingest Analyst Rating Changes
Load analyst recommendation logs to identify upgrades, downgrades, and price targets:
```python
import pandas as pd

ratings_df = pd.read_csv('data/financial_news/analyst_ratings_processed.csv')
ratings_df['date'] = pd.to_datetime(ratings_df['date'])

# Filter for a specific stock (e.g., Apple) to see recent rating actions
company_ratings = ratings_df[ratings_df['stock'] == 'AAPL'].sort_values('date', ascending=False)
print("=== ANALYST RATINGS TIMELINE ===")
print(company_ratings[['date', 'title', 'stock']].head(10))
```

### Step 2: Extract Price Targets and Actions
Process the unstructured headline field to parse upgrades, downgrades, and price targets:
```python
# Helper to extract price targets and actions from titles
def parse_rating_details(title):
    action = "Neutral"
    target = None
    if "Upgrade" in title:
        action = "Upgrade"
    elif "Downgrade" in title:
        action = "Downgrade"
    
    # Extract numeric target values
    targets = re.findall(r'\$(\d+)', title)
    if targets:
        target = float(targets[0])
    return pd.Series([action, target])

import re
company_ratings[['action', 'price_target']] = company_ratings['title'].apply(parse_rating_details)
print(company_ratings[['date', 'title', 'action', 'price_target']].head(5))
```

### Step 3: Run Semantic Sentiment Scoring
Run a sentiment analyzer on analyst commentary to flag bullish/bearish signals:
```python
# Load phrasebank sentiment markers
phrasebank = pd.read_csv('data/financial_phrasebank/Sentiment_Clean.csv')
# Mapping rating announcements to sentiment weights
print("=== SENTIMENT SEEDS ===")
print(phrasebank.head(5))
```
