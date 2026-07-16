# 📉 Use Case 5: Distress and Layoff Monitoring

This use case automates corporate distress tracking, employee layoffs monitoring, litigation liability monitoring, and market panic/hedging indicators alignment.

---

## 🎯 Rogo.ai Problem Framings Solved
* **Corporate Layoffs & Restructuring Tracking:** Monitoring headcount reductions to identify operational distress, structural shifts, or cost-cutting cycles.
* **Corporate Default & Bankruptcy Probabilities:** Processing credit parameters and monthly default timelines to compute corporate health indices.
* **Litigation & Lawsuits Liability:** Tracking patent lawsuits, plaintiffs, and defendants to quantify legal liabilities.
* **Implied Volatility & Fear Gauges:** Standardizing CBOE VIX daily benchmarks to analyze macro-hedging demands and general market panic levels.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Extracts daily VIX closes or identifies basic layoff counts.
2. **Frontier Routing (Sol @ $1.26):** Analyzes multidimensional risk correlations (e.g. comparing how a sudden spike in patent litigation aligns with an increase in default probability and staffing cuts).
3. **Structured Context Ingestion:** Queries are routed over pre-configured indexes containing `data/corporate_layoffs/` and `data/bankruptcy_risk/` rather than reading raw news feeds.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/corporate_layoffs/](file:///home/maxdemarzi/rogue/data/corporate_layoffs/)**: Corporate layoffs histories, headcount cuts, and funding stages.
2. **[data/bankruptcy_risk/](file:///home/maxdemarzi/rogue/data/bankruptcy_risk/)**: Monthly defaults and distress probability timelines.
3. **[data/patent_litigation/](file:///home/maxdemarzi/rogue/data/patent_litigation/)**: Legal litigation mapping plaintiffs, defendants, and case numbers.
4. **[data/implied_volatility/](file:///home/maxdemarzi/rogue/data/implied_volatility/)**: Daily CBOE VIX levels.
5. **[data/financial_news/](file:///home/maxdemarzi/rogue/data/financial_news/)**: Labeled news headlines and analyst ratings.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Corporate Layoffs Edge
Link headcount cuts directly to corporate nodes:
```
(:Company {name: $COMPANY}) -[:DECLARED_LAYOFF]-> (:LayoffEvent {
  date: $DATE,
  count: total_laid_off,
  pct: percentage_laid_off,
  stage: funding_stage
})
```

### 2. Legal Distress Bridges
Map litigation risks between plaintiffs and defendants:
```
(:Company {name: $PLAINTIFF}) -[:LITIGATED {case_no: $CASE, date: $DATE}]-> (:Company {name: $DEFENDANT})
```

### 3. Volatility Panic Correlation
Align daily VIX peaks with corporate layoff announcements and distress probabilities:
```
(:VolatilityIndex {date: $DATE, vix: $VIX_CLOSE}) -[:MARKET_VOLATILITY]-> (:MarketIndex)
```

---

## 💻 Technical Solution Steps

### Step 1: Track Corporate Layoffs and Scale
Query the layoffs database to identify recent downsizings and the scale of staffing reductions:
```python
import pandas as pd

layoffs_df = pd.read_csv('data/corporate_layoffs/layoffs.csv')
layoffs_df['date'] = pd.to_datetime(layoffs_df['date'])
# Find largest headcount reductions in a given period
large_layoffs = layoffs_df.sort_values('total_laid_off', ascending=False)
print("=== LARGE CORPORATE LAYOFFS ===")
print(large_layoffs[['company', 'location', 'total_laid_off', 'percentage_laid_off', 'date', 'stage']].head(5))
```

### Step 2: Track Legal Litigation Risks
Query lawsuit logs to list legal exposure for public and private corporations:
```python
litigation_df = pd.read_csv('data/patent_litigation/Patent_Data.csv')
print("=== CORPORATE LITIGATION RECORDS ===")
print(litigation_df[['patent_id', 'plaintiff', 'parent_company', 'defendant']].head(5))
```

### Step 3: Align with Daily VIX Fear Gauge
Monitor daily VIX close levels to measure broader market fear and hedging trends:
```python
vix_df = pd.read_csv('data/implied_volatility/vix.csv')
vix_df['DATE'] = pd.to_datetime(vix_df['DATE'])
# Locate major volatility spikes
vix_spikes = vix_df[vix_df['CLOSE'] > 30].sort_values('DATE')
print("=== VIX SPIKES (>30 CLOSE) ===")
print(vix_spikes[['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE']].tail(5))
```
