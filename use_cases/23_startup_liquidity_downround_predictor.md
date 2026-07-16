# 💸 Use Case 23: Startup Liquidity Runway & VC Down-Round Predictor

This playbook implements the **Startup Liquidity Runway & VC Down-Round Predictor**—a late-stage venture capital and private equity secondary market sourcing workflow. It estimates private startup burn rates and runways to predict down-round funding probabilities.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **Startup Burn Rate Forecasting:** Estimates monthly cash burn based on employee headcounts and regional compensation averages.
* **Down-Round Insolvency Predictor:** Predicts the probability of down-round refinancing or default based on runway limits and macro yield spreads.
* **Secondary Market Sourcing:** Filters highly motivated venture sellers facing upcoming cash cliffs.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/startup_vc/](file:///home/maxdemarzi/rogue/data/startup_vc/)**: Startup investments, round sizes, and funding totals.
2. **[data/corporate_layoffs/](file:///home/maxdemarzi/rogue/data/corporate_layoffs/)**: Headcount reductions and funding stages.
3. **[data/interest_rate_spreads/](file:///home/maxdemarzi/rogue/data/interest_rate_spreads/)**: Daily corporate bond spreads.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Burn Rate Runway
Link startups to funding milestones and layoff headcount cuts:
```
(:Company {name: $STARTUP}) -[:FUNDED_BY]-> (:VCInvestment {funding_total_usd: $TOTAL})
  <-[:LAYOFF_AT]- (:LayoffEvent {total_laid_off: $CUTS})
```

---

## 💻 Technical Solution Steps

### Step 1: Trace Startup VC Rounds
List late-stage private startups with venture track records:
```python
import pandas as pd

vc_df = pd.read_csv('data/startup_vc/vc.csv')
late_stage_vc = vc_df[vc_df['funding_total_usd'] > 50000000]

print("=== LATE STAGE VC STARTUPS ===")
print(late_stage_vc[['name', 'funding_total_usd', 'funding_rounds', 'status']].head(5))
```
