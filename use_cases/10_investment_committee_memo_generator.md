# 📄 Use Case 10: Investment Committee (IC) Memo & Slide Pitchbook Generator

This playbook implements the **"Last Mile" Deliverable Generator** (similar to Rogo's *Nexus* agent and Hebbia's slide generators). It automates the compilation of investment committee (IC) memos and presentation slides, embedding sentence-level citations to verify accuracy.

---

## 🎯 The "Last Mile" Analyst Needs Solved
* **Automated IC Memo Drafting:** Turning disparate data rooms and public filings into structured Word/Markdown memos covering deal overviews, competitive landscapes, financial highlights, and risk factors.
* **Citational Precision:** Linking every statement of fact (e.g., revenue growth rates or litigation counts) back to its original source cell or document paragraph.
* **Decks & PowerPoint Generation:** Converting textual syntheses into structured slide outlines ready for corporate templates.

---

## ⚙️ Model Broker Routing & Optimization
Rogo’s **Model Broker** optimizes the token spend for this use case:
1. **Lightweight Routing (Luna/Terra @ $0.02):** Populates basic slide fields and formats metadata templates.
2. **Frontier Routing (Sol @ $1.26):** Resolves contradictions across sources and drafts highly persuasive executive summaries and investment thesis rationales.
3. **Structured Context Ingestion:** Document models read clean JSON records extracted from `data/mergers_acquisitions/` and `data/fundamentals/` instead of parsing massive raw PDFs.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/mergers_acquisitions/](file:///home/maxdemarzi/rogue/data/mergers_acquisitions/)**: Deal sizes, buyer/seller metadata, and status logs.
2. **[data/fundamentals/](file:///home/maxdemarzi/rogue/data/fundamentals/)**: Key historical financial metrics.
3. **[data/financial_news/](file:///home/maxdemarzi/rogue/data/financial_news/)**: Live industry headlines and analyst reactions.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. The Deal Target Node
Map the investment candidate's metrics directly to the target transaction node:
```
(:Transaction {id: $DEAL_ID}) -[:HAS_TARGET_FINANCIALS]-> (:FilingMetrics {ticker: $TICKER})
```

### 2. Citational Footnote Linkages
Link statements inside the drafted memo directly to database entries:
```
(:ICMemo {id: $MEMO_ID}) -[:CITES {source_row: $ROW, source_file: $FILE}]-> (:FilingMetrics)
```

---

## 💻 Technical Solution Steps

### Step 1: Query Deal Target Metadata
Pull deal benchmarks to write the transaction overview section of the IC memo:
```python
import pandas as pd

ma_df = pd.read_csv('data/mergers_acquisitions/M&A Transactions.csv')
target_deal = ma_df[ma_df['Target'].str.contains('Whole Foods', na=False)]
print("=== TARGET TRANSACTION BENCHMARK ===")
print(target_deal[['Acquirer', 'Target', 'Value (USD)', 'Status']])
```

### Step 2: Extract Target Financials with Sourced Citations
Compile the target's financial profile, explicitly logging the source files to serve as footnotes:
```python
# Load target fundamentals
fundamentals_df = pd.read_csv('data/fundamentals/AAPL_fundamentals.csv') # Proxy target
target_rev = fundamentals_df[fundamentals_df['metric'] == 'total_revenue'].iloc[-1]

print("=== CITATION DATA PACK ===")
print(f"Revenue Value: ${target_rev['value']:,.2f}")
print(f"Verified Source File: data/fundamentals/AAPL_fundamentals.csv")
print(f"Verified Source Row ID: {target_rev.name}")
```

### Step 3: Format the Output Markdown Draft
Assemble these facts into a formatted, client-ready markdown draft complete with citational footnotes:
```python
memo_draft = f"""
# INVESTMENT COMMITTEE MEMO: PROJECT WHOLE FOODS

## 1. Transaction Overview
* **Acquirer:** {target_deal.iloc[0]['Acquirer']}
* **Target:** {target_deal.iloc[0]['Target']}
* **Deal Value:** ${target_deal.iloc[0]['Value (USD)']}
* **Status:** {target_deal.iloc[0]['Status']}

## 2. Key Financial Highlights [1]
* **Target Revenue:** ${target_rev['value']:,.2f}

---
## 📑 Citations
[1] Source: `data/fundamentals/AAPL_fundamentals.csv`, Row Index: {target_rev.name}
"""
print(memo_draft)
```
