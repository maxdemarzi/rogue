# 🏛️ Use Case 16: Federal Contracting Backlog & Revenue Shock Simulator

This playbook implements the **Federal Contracting Backlog & Revenue Shock Simulator**—a buy-side deal due diligence and valuation stress-testing workflow. It integrates federal contract awards and expiration dates to model revenue concentration risks under policy changes or spending freezes.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **Contract Backlog Decay Modeling:** Simulates how a target contractor's revenue backlog rolls off over time based on award values and elapsed periods.
* **Fiscal Spending Shock Stress-Testing:** Projects net operating margin contraction if government agencies delay or cancel pending defense/AI contracts.
* **Inductive Target Valuation Adjustment:** Adjusts GNN predicted valuation multiples downwards based on government dependency concentration ratios.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/federal_contracts/](file:///home/maxdemarzi/rogue/data/federal_contracts/)**: US federal AI contract awards, agencies, and values.
2. **[data/fundamentals/](file:///home/maxdemarzi/rogue/data/fundamentals/)**: Income sheets and cash margins.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Federal Contract Dependency
Link target companies to federal award streams:
```
(:Company {name: $COMPANY}) -[:RECIPIENT_OF]-> (:FederalContract {award_amount: $VAL, elapsed: $M1, duration: $M2})
```

---

## 💻 Technical Solution Steps

### Step 1: Calculate Contract Backlog Decay
Compute monthly contract backlog curves:
```python
import pandas as pd

contracts_df = pd.read_excel('data/federal_contracts/US_Fed_AI_Contracts_Sample.xlsx')
# Calculate remaining contract value based on elapsed durations
contracts_df['elapsed_months'] = (pd.to_datetime('today') - pd.to_datetime(contracts_df['Start Date'])).dt.days // 30
contracts_df['remaining_value'] = contracts_df['Award Amount'] * (1 - contracts_df['elapsed_months'] / contracts_df['Duration Months'])
contracts_df.loc[contracts_df['remaining_value'] < 0, 'remaining_value'] = 0

print("=== REMAINING CONTRACT BACKLOG ===")
print(contracts_df[['Recipient Name', 'Award Amount', 'remaining_value', 'Agency Name']])
```
