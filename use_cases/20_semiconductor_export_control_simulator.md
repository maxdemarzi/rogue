# 🔌 Use Case 20: Semiconductor Fab Capacity & Export Control Restriction Simulator

This playbook implements the **Semiconductor Fab Capacity & Export Control Restriction Simulator**—a geopolitical and sector-specialty buy-side due diligence workflow. It simulates customer revenue blockages, chip spot prices, and fab capacity utilization under international entity list actions.

---

## 🎯 The Mind-Blowing Analyst Capabilities
* **Geopolitical Trade Shock Modeling:** Projects revenue contraction if a semiconductor target is blocked from selling to restricted customer domains.
* **Fab Capacity Optimization:** Simulates in-database fab utilization constraints based on nodes sizes and facility locations.
* **Chip Spot Price Sensitivity:** Simulates gross margin volatility across historical chip pricing shifts.

---

## 🛠️ Datasets Utilized in this Workspace
1. **[data/semiconductor_industry/](file:///home/maxdemarzi/rogue/data/semiconductor_industry/)**: Fab capacity, spot prices, export restrictions, and market segment sizes.
2. **[data/fundamentals/](file:///home/maxdemarzi/rogue/data/fundamentals/)**: R&D spending and operating revenues.

---

## 🔗 Knowledge Graph Resolution Paths

### 1. Export Control Exposure
Link chipmakers to export restrictions and fab operations:
```
(:Company {name: $COMPANY}) -[:OPERATES_FAB]-> (:FabCapacity {location: $LOC, capacity_wspm: $VAL})
  <-[:RESTRICTED_BY]- (:ExportControl {restricted_entity: $ENTITY})
```

---

## 💻 Technical Solution Steps

### Step 1: Trace Export Blockages
Identify export control restrictions active on targeted companies:
```python
import pandas as pd

export_df = pd.read_csv('data/semiconductor_industry/export_controls.csv')
print("=== ACTIVE SEMICONDUCTOR EXPORT CONTROLS ===")
print(export_df[['restricted_entity', 'controlling_country', 'restriction_type']])
```
