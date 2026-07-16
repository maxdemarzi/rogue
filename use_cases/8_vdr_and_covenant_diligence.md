# 📂 Use Case 8: Virtual Data Room (VDR) and M&A Covenant Diligence

This use case automates buy-side and sell-side transaction due diligence, analyzing unstructured filings, debt covenants, IP patent litigations, and mergers & acquisitions records to flag liability exposures.

---

## 🎯 Hebbia & Rogo Problem Framings Solved
* **VDR Document Diligence:** Sifting through thousands of pages of private placement memos, acquisition terms, legal disputes, and corporate agreements to extract deal conditions.
* **Debt Covenants & Restructuring Restrictions:** Extracting legal limits (such as leverage covenants, change of control clauses, dividend restrictions) from bond indentures.
* **Litigation Liability Quantification:** Mapping patent lawsuits and open claims to assess target risk parameters before deal closure.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s and Hebbia’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Sweeps filings to extract metadata, list parties involved in litigation, or trace deal dates.
2. **Frontier Routing (Sol @ $1.26):** Audits complex covenant clauses (e.g. evaluating if a specific restructuring proposal violates negative covenants or debt-incurrence restrictions).
3. **Structured Context Ingestion:** Integrates target legal records from `data/patent_litigation/Patent_Data.csv` and deal lists in `data/mergers_acquisitions/` to isolate target entities and minimize search inputs.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/mergers_acquisitions/](file:///home/maxdemarzi/rogue/data/mergers_acquisitions/)**: Historical records of large-scale corporate mergers, acquirers, targets, and valuations.
2. **[data/patent_litigation/](file:///home/maxdemarzi/rogue/data/patent_litigation/)**: Intellectual property disputes, plaintiffs, and parent companies.
3. **[data/corporate_bonds/](file:///home/maxdemarzi/rogue/data/corporate_bonds/)**: Bond structures, coupon terms, and ratings.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Merger Target Intersect
Trace acquirer-target networks to flag overlapping legal dependencies:
```
(:Company {name: $ACQUIRER}) -[:ACQUIRED {valuation: $VAL}]-> (:Company {name: $TARGET})
```

### 2. Intellectual Property Risk Bridge
Connect patent litigation defendants to acquisition target profiles:
```
(:Company {name: $TARGET}) <-[:DEFENDANT_IN]- (:LitigationCase {id: $CASE_ID})
```

### 3. Bond Covenants
Map debt agreements and leverage ratios directly to issuer entities:
```
(:Company {ticker: $TICKER}) -[:ISSUED_DEBT]-> (:Bond {coupon: $COUPON}) -[:HAS_COVENANT]-> (:Covenant {leverage_limit: $LIMIT})
```

---

## 💻 Technical Solution Steps

### Step 1: Scan Target Corporate Litigation History
Evaluate outstanding litigation exposure for target companies:
```python
import pandas as pd

litigation_df = pd.read_csv('data/patent_litigation/Patent_Data.csv')
# Search for targets involved in active disputes as defendants
target_disputes = litigation_df[litigation_df['defendant'].str.contains('Apple|Samsung', na=False, case=False)]
print("=== OUTSTANDING LITIGATION EXPOSURE ===")
print(target_disputes[['patent_id', 'plaintiff', 'defendant', 'parent_company']])
```

### Step 2: Ingest Historical Deal Benchmarks
Load mergers and acquisitions benchmarks to value target companies:
```python
ma_df = pd.read_csv('data/mergers_acquisitions/M&A Transactions.csv')
# List acquisitions in tech or software sectors
tech_deals = ma_df[ma_df['Target'].str.contains('Tech|Software|Data', na=False, case=False)]
print("=== HISTORICAL M&A BENCHMARKS ===")
print(tech_deals[['Acquirer', 'Target', 'Value (USD)', 'Status']].head(5))
```

### Step 3: Extract Restrictive Bond Covenants
Track bond rating actions and maturity terms to forecast capital structure changes:
```python
bonds_df = pd.read_excel('data/corporate_bonds/CompanyBonds.xlsx')
# Filter target high-yield bonds to audit interest coverage covenant thresholds
high_yield_debt = bonds_df[bonds_df['CREDIT RATING'].isin(['BB+', 'BB', 'B'])]
print("=== HIGH-YIELD COVENANT AUDIT LIST ===")
print(high_yield_debt[['SYMBOL', 'BOND TYPE', 'COUPON RATE', 'CREDIT RATING', 'MATURITY DATE']])
```
