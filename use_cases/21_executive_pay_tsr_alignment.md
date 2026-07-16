# ⚖️ Use Case 21: Executive Pay-for-Performance & TSR Alignment Elasticity Solver

This playbook implements the **Executive Pay-for-Performance & TSR Alignment Elasticity Solver**—an activist hedge fund and corporate governance due diligence workflow. It calculates the elasticity of CEO compensation relative to historical Total Shareholder Return (TSR) to flag misaligned boards.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **TSR-Compensation Elasticity Solver:** Computes pay-performance mismatch ratios to highlight activist targets.
* **CEO Pay Dispersion Audits:** Benchmarks CEO pay vs. median worker pay dispersion across peer sectors.
* **Activist Sourcing Filters:** Auto-scores target companies where CEO salaries rise while shareholder returns contract.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/ceo_salaries/](file:///home/maxdemarzi/rogue/data/ceo_salaries/)**: Executive salaries, CEO compensation, and CEO-to-worker pay ratios.
2. **[data/ohlcv/](file:///home/maxdemarzi/rogue/data/ohlcv/)**: Daily prices to compute total shareholder returns.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Pay-Performance Alignment
Link C-Suite compensation to historical price returns:
```
(:Company {symbol: $SYMBOL}) -[:HAS_PRICE_SERIES]-> (:OHLCV {close_val: $VAL})
  <-[:EXECUTIVE_OF]- (:Person {ceo_compensation: $COMP, worker_pay_ratio: $RATIO})
```

---

## 💻 Technical Solution Steps

### Step 1: Trace CEO Pay Overhead
List target companies with high executive pay dispersion metrics:
```python
import pandas as pd

ceo_df = pd.read_csv('data/ceo_salaries/ceo_data_pay_merged_r3000.csv')
bloated_boards = ceo_df[ceo_df['pay_ratio'] > 500]

print("=== BLOATED CORPORATE BOARDS ===")
print(bloated_boards[['company_name', 'ceo_name', 'total_ceo_pay', 'pay_ratio']].head(5))
```
