# 🍃 Use Case 17: ESG Capital Flight & Controversy Valuation Discount Engine

This playbook implements the **ESG Capital Flight & Controversy Valuation Discount Engine**—an institutional risk-arbitrage and target screening workflow. It models probability curves for LP fund divestment and applies valuation discounts to targets suffering ESG controversies.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **Controversy Divestment Forecasting:** Predicts capital outflows ($P_{flight}$) based on controversy severity levels and institutional ownership concentrations.
* **Valuation Multiple Adjustments:** Quantifies the "ESG Discount Factor" to adjust GNN multiples before portfolio optimization.
* **Activist Sourcing:** Identifies high-quality firms suffering from temporary controversy discounts that can be unlocked via governance restructuring.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/esg_ratings/](file:///home/maxdemarzi/rogue/data/esg_ratings/)**: ESG scores, risk segments, and controversy indicators.
2. **[data/insider_trading/](file:///home/maxdemarzi/rogue/data/insider_trading/)**: Institutional ownership weights and shares held.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Controversy Risk Mapping
Link ESG controversy indicators to company ownership:
```
(:Company {ticker: $TICKER}) -[:HAS_ESG_RATING]-> (:ESGRating {controversy_level: $VAL})
  <-[:HOLDS_SHARES {weight: $WEIGHT}]- (:InstitutionalHolder)
```

---

## 💻 Technical Solution Steps

### Step 1: Filter High Controversy Outliers
Filter firms experiencing high ESG controversy levels:
```python
import pandas as pd

esg_df = pd.read_csv('data/esg_ratings/esg_ratings_sp_500_esg_risk_ratings.csv')
controversy_outliers = esg_df[esg_df['Controversy Level'] >= 4]

print("=== ESG CONTROVERSY RISK TARGETS ===")
print(controversy_outliers[['Company Name', 'Ticker', 'Total ESG Score', 'Controversy Level']])
```
