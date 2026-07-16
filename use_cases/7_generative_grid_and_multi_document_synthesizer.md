# 📊 Use Case 7: Generative Grid & Multi-Document Synthesizer

This use case implements the **Generative Grid** capability (similar to AlphaSense’s Generative Grid and Rogo's deterministic agentic tables). It runs batch prompts across multiple corporate documents simultaneously to extract, verify, and compile financial metrics into comparative tables.

---

## 🎯 Rogo.ai & AlphaSense Problem Framings Solved
* **The Generative Grid:** Sifting through 10-20 different corporate filings simultaneously to extract specific parameters (e.g. Net income, Operating cash flows, R&D expense, and segment performance) and arranging them into a consolidated table.
* **Comp Table Generator:** Constructing financial comparison sheets across industry peers with direct source-hyperlink tags for each cell.
* **Multi-Document Discrepancy Auditing:** Detecting anomalies or revisions between consecutive reports (e.g. comparing restated historical figures).

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Extracts simple metrics from pre-indexed document sections (e.g. finding the value of "Total Assets" on the Balance Sheet).
2. **Frontier Routing (Sol @ $1.26):** Audits complex disclosures (e.g. tracing tax rate explanations or restructuring liabilities across footnotes).
3. **Structured Context Ingestion:** Document parsing pipelines pre-extract specific forms from `data/sec_financials/` and metadata from `data/simfin/` to target only the relevant financial tables, saving up to 90% in token consumption compared to reading full raw filings.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/sec_financials/](file:///home/maxdemarzi/rogue/data/sec_financials/)**: Pre-structured tables and statements from SEC reports.
2. **[data/simfin/](file:///home/maxdemarzi/rogue/data/simfin/)**: Meta-details and statement summaries for public companies.
3. **[data/fundamentals/](file:///home/maxdemarzi/rogue/data/fundamentals/)**: Key financial metrics, balance sheets, and cash flow items.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Document Extraction Nodes
Link structured filings to their parent companies and specific tables:
```
(:Company {ticker: $TICKER}) -[:FILED]-> (:Filing {form: $FORM, period: $PERIOD}) -[:CONTAINS_TABLE]-> (:FinancialTable {type: $TABLE_TYPE})
```

### 2. Multi-Company Grid Matrix
Aggregate metrics across peers for a single period:
```
(:FinancialTable {period: $PERIOD}) -[:HAS_METRIC {name: $METRIC}]-> (:MetricValue {value: $VAL})
```

---

## 💻 Technical Solution Steps

### Step 1: Batch Load Peer Filings
Query financial parameters across peer companies for a given period:
```python
import pandas as pd
import glob

# Load company details
companies = pd.read_csv('data/simfin/companies.csv') # or equivalents

# Batch load key indicators
fundamentals_files = glob.glob('data/fundamentals/*.csv')
peer_metrics = []

for file_path in fundamentals_files:
    df = pd.read_csv(file_path)
    # Extract specific rows (e.g. Net Income, Total Assets)
    key_metrics = df[df['metric'].isin(['net_income', 'total_revenue', 'operating_cash_flow'])]
    peer_metrics.append(key_metrics)

grid_df = pd.concat(peer_metrics)
print("=== BATCH PEER DATASET ===")
print(grid_df.head(10))
```

### Step 2: Compile the Generative Comparison Grid
Build a pivot table that aggregates these parameters into a structured comparison grid:
```python
# Pivot to format like a Generative Grid comparison table
pivot_grid = grid_df.pivot_table(
    index='ticker', 
    columns='metric', 
    values='value', 
    aggfunc='first'
)
print("=== PEER COMPARISON GRID ===")
print(pivot_grid)
```

### Step 3: Audit Footnote Revisions
Compare original values with restated values to flag reporting discrepancies:
```python
# Check for differences between reports
revisions = grid_df[grid_df['restated'] == True]
print("=== REPORTED REVISIONS ===")
print(revisions[['ticker', 'metric', 'original_value', 'restated_value', 'filing_date']])
```
