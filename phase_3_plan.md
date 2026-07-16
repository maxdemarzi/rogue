# Rebuilding the Rogo AI Analyst - Phase 3: Advanced Reasoning Modules

This document details the software design, mathematical formulations, and execution patterns for the **Advanced Reasoning Modules** in the rebuilt Rogo AI Analyst. Rather than using external wrappers (like NetworkX, raw PyTorch Geometric, or SciPy), we leverage **Swan's native C++ reasoning engines** (`pyrel_duckdb.reasoners`) to run graph algorithms, Graph Neural Networks (GNNs), and mathematical programming directly over our DuckDB data warehouse.

---

## 📐 System Flow Overview

All reasoning modules are built as declarative layers on top of the Swan semantic model:

```mermaid
flowchart TD
    DB[(rogue_finance.duckdb)] <--> Model[Swan Relational Model]
    
    subgraph Swan Reasoners [Swan C++ Reasoning Engines]
        Graph[Graph Pathfinder & Centrality]
        GNN[Predictive GNN Serving]
        MIP[Prescriptive Solver: HiGHS]
    end
    
    subgraph Deliverables [Generative & Export Engines]
        Excel[Live Excel Modeler]
        Memo[IC Pitchbook Generator]
    end
    
    Model -->|Concept Mappings| Graph
    Graph -->|Topology & Features| GNN
    GNN -->|Served EV/Sales Predictions| MIP
    
    MIP -->|Optimal Sourced Targets| Excel
    MIP -->|Restructuring Synergy Metrics| Memo
```

---

## 🌐 1. Swan Graph Pathfinder & Contagion Simulator (`path_reasoner.py`)

This module implements value chain analysis, customer-vendor reachability, and corporate board interlocks using Swan's graph reasoning engines.

### A. Topology Construction
We instantiate a Swan `Graph` topology binding custom ontology concepts representing B2B linkages:

```python
from pyrel_duckdb.reasoners.graph import Graph

# Initialize the directed supply chain graph
supply_graph = Graph(
    model,
    directed=True,
    weighted=True,
    node_concept=Company,
    edge_concept=SupplierRelation, # supplies_to relationship mapping
    edge_src_relationship=SupplierRelation.supplier,
    edge_dst_relationship=SupplierRelation.customer,
    edge_weight_relationship=SupplierRelation.revenue_share
)
```

### B. Core Operations

#### 1. PageRank Distress Contagion (Use Case 12)
Detects central systemic nodes in the supply chain exposed to distress propagation. We invoke Swan's native PageRank:

```python
# Compute PageRank scores on the supplies graph
pagerank_scores = supply_graph.pagerank(
    damping_factor=0.85, 
    max_iter=20, 
    tolerance=1e-6
)

# Query PageRank nodes and extract to DataFrame
centrality_df = model.where(pagerank_scores).select(
    pagerank_scores["node"].id.alias("company_id"),
    pagerank_scores.score.alias("distress_influence")
).to_df()
```

#### 2. Downstream Reachability & WCC (Use Case 4 & 12)
Traces if a systemic vendor shock propagates down the supply chain to a specific customer node.
* **C++ Cache Optimization:** We pass `use_cache=True` to activate Swan's C++ transitive reachability caches (`TransitiveReachabilityCache`), bypassing expensive recursive SQL CTE processing.

```python
# Check reachability between two companies
reachable_rel = supply_graph.reachable(CompanyA, CompanyB, use_cache=True)
```

To partition the value-chain into isolated supplier clusters, we execute Weakly Connected Components:

```python
wcc_rel = supply_graph.weakly_connected_component(
    use_cache=True,
    cache_table="supplier_relation",
    cache_src="supplier_id",
    cache_tgt="customer_id"
)
```

#### 3. Board Interlock Detection (Use Case 14)
To detect interlocking directorship networks, a bipartite graph mapping `Person` nodes sitting on `Board` entities is constructed, allowing direct extraction of interlocking pathways:

```python
board_graph = Graph(
    model,
    directed=False,
    node_concept=Person,
    edge_concept=BoardMember,
    edge_src_relationship=BoardMember.director,
    edge_dst_relationship=BoardMember.company
)

# Extract degree centrality to locate high-degree directors
director_degrees = board_graph.degree(of=Person)
```

---

## 🤖 2. Swan Predictive GNN Servicer (`gnn_model.py`)

This module uses Swan's GNN predictive reasoning engine to forecast company valuation multiples (EV/Sales and EV/EBITDA) directly inside DuckDB.

### A. Feature Ingestion & Normalization (`PropertyTransformer`)
We define a property transformer to standardize categorical sectors, continuous financial ratios, and news sentiment headlines into tensor representations:

```python
from pyrel_duckdb.reasoners.predictive import PropertyTransformer

pt = PropertyTransformer(
    category=[Company.sector, Company.credit_rating],
    continuous=[
        Company.revenue, 
        Company.ebitda_margin, 
        Company.debt_to_equity, 
        Company.altman_z_score,
        Company.free_cash_flow_quality_ratio
    ],
    text=[Company.latest_headline] # Normalized via local sentence-transformers
)
```

### B. GNN Configuration & Servicing
We partition our historical fundamentals datasets into train/validation queries:

```python
from pyrel_duckdb.semantics.reasoners.predictive import GNN

# Define query splits
TrainQuery = select(Company.id, Company.target_multiple).where(Company.is_train == True)
ValQuery = select(Company.id, Company.target_multiple).where(Company.is_val == True)

# Build the GNN
gnn = GNN(
    graph=supply_graph,
    property_transformer=pt,
    train=TrainQuery,
    validation=ValQuery,
    task_type="regression", # Predict continuous multiples
    hidden_channels=16,
    n_epochs=50,
    lr=0.01
)

# Train GNN locally (PyG back-end) and compile to native C++ ONNX model
gnn.fit()
```

### C. Native In-Database Inference (C++ ONNX Runtime)
Once trained, the GNN weights are saved as an ONNX artifact. Serve predictions natively inside DuckDB queries to bypass Python transfer overhead:

```python
# Serving predictions on target PE screening candidates
Company.predicted_multiples = gnn.predictions(domain=ScreeningTestQuery)

# Select GNN projections in-place
valuation_df = select(
    Company.id,
    Company.predicted_multiples.probs.alias("predicted_multiple")
).where(Company.predicted_multiples).to_df()
```

### D. Model Explainability Views
For investment diligence reporting (Use Case 10), we query Swan's C++ GNN explainability metrics (`ExplainNode` and `ExplainEdge`) to audit what features drove a specific valuation:

```python
ExplainNode, ExplainEdge = gnn.explain(target_id="AAPL", top_k=5)

# Query most important feature contributions
node_attributions = select(ExplainNode.node, ExplainNode.weight).to_df()
edge_attributions = select(ExplainEdge.src, ExplainEdge.dst, ExplainEdge.weight).to_df()
```

---

## 🎯 3. Swan Prescriptive Target Optimizer (`optimizer.py`)

This module uses Swan's prescriptive solver wrapper (`pyrel_duckdb.reasoners.prescriptive`) to compile Linear Programs (LP) and Mixed-Integer Programs (MIP) directly over the DuckDB engine, solving them using the local C++ **HiGHS** solver.

### A. Problem Context & Variable Declarations
We instantiate a prescriptive context and define binary variables indicating whether target firms are selected for acquisition:

```python
from pyrel_duckdb.reasoners.prescriptive import Problem, implies
from pyrel_duckdb.std import aggregates as aggs

problem = Problem(model, Float)

# Declare binary decision variables (populate=True writes output back to database)
x_acquire = problem.solve_for(Company.x_acquire, type="bin", populate=True)
```

### B. Objective Function
Maximize the aggregate projected portfolio Net Income, including cost savings generated by optimizing executive pay overhead:

```python
problem.maximize(
    aggs.sum(
        Company.x_acquire * (Company.net_income_loss + Company.ceo_compensation * 0.3)
    )
)
```

### C. Sourcing Constraints & Big-M Implications
Swan compiles these constraints directly into HiGHS matrices:

```python
# 1. Sourcing Quantity (Select exactly K targets)
problem.satisfy(aggs.sum(Company.x_acquire) == K)

# 2. Capital Allocation Limit (Total Cost <= Budget)
problem.satisfy(
    aggs.sum(Company.x_acquire * Company.predicted_multiples.probs * Company.revenue) <= Budget
)

# 3. Sector Concentration Constraints (Max 2 acquisitions per sector)
problem.satisfy(
    aggs.sum(Company.x_acquire).per(Company.sector) <= 2
)

# 4. Solvency Exclusion (Exclude Altman Distress candidates)
problem.satisfy(
    model.require(implies(Company.altman_z_score < 1.81, Company.x_acquire == 0))
)

# 5. Litigation Exclusions (Exclude defendants)
problem.satisfy(
    model.require(implies(Company.is_litigation_defendant == True, Company.x_acquire == 0))
)
```

### D. Solving & Value Retrieval
We execute the solver locally:

```python
# Run the local C++ HiGHS solve
problem.solve()

# Check solver results
solve_stats = problem.solve_info()
print("Solve Termination:", solve_stats.termination_status) # e.g. Optimal
print("Optimal Objective:", solve_stats.objective_value)
```

---

## 📈 4. Live Formula Excel Modeler (`live_modeler.py`)

Generates living Excel spreadsheet outputs (Use Cases 11 & 13) using `openpyxl`.
* **Zero Hardcoding Rule:** Projection cells must refer to formula equations in uppercase string parameters (e.g. `=B2*0.60`) rather than injecting static float results.
* **Dependency Tree:** Traces inputs dynamically:

| Output Row | Cell Label | Excel Formula |
| :--- | :--- | :--- |
| **Row 2** | `Purchase Price` | `B2` (Base value sourced from GNN prediction) |
| **Row 3** | `Debt Contribution` | `=B2 * 0.60` (60% LBO Debt capacity) |
| **Row 4** | `Sponsor Equity` | `=B2 - B3` (Remaining Equity financing) |
| **Row 5** | `Year 1 Revenue` | `=PriorYearSales * (1 + GrowthRate)` |
| **Row 6** | `Year 1 EBITDA` | `=B5 * EBITDA_Margin` |
| **Row 7** | `Year 1 Debt Payment` | `=PMT(InterestRate, 5, -B3)` (Amortization schedule) |

---

## 🔗 5. Source Citation Engine (`citation_engine.py`)

Binds cell data in web grids and pitchbooks to row indexes inside DuckDB:

```json
{
  "citation_id": "CIT_SEC_2026_091",
  "symbol": "AAPL",
  "period": "FY2026",
  "concept": "operating_income_loss",
  "val": 114500000000.0,
  "source_table": "sec_financials_short_financials_df",
  "source_row_index": 9482,
  "sql_locator": "SELECT operating_income_loss FROM sec_financials_short_financials_df WHERE ticker='AAPL' AND fiscal_year=2026"
}
```

---

## 🌍 6. Macro Hedging & Sovereign Rating Simulator (`macro_simulator.py`)

This module simulates Purchasing Power Parity (PPP) adjustments and carry trade exposures across national borders (Use Case 15).

### A. Purchasing Power Parity (PPP) Valuation Gaps
We calculate the PPP spot rate differential over a year horizon:

$$\text{FX\_PPP}_{t} = \text{FX\_Spot}_{t-1} \times \left( \frac{1 + \text{Inflation}_{\text{Country B}}}{1 + \text{Inflation}_{\text{Country A}}} \right)$$

If $\text{FX\_Spot}_t > \text{FX\_PPP}_t$, the currency is flagged as overvalued.

### B. Carry Trade Arbitrage Yields
Estimates the net carry spread adjusting for sovereign credit risk and inflation differentials:

$$\text{Net Carry Yield} = \left(\text{Rate}_{\text{Local}} - \text{Rate}_{\text{Fed}}\right) - \left( \text{SovereignSpread}_{\text{Local}} + \text{PPP\_Gap} \right)$$

If the net carry yield remains above a threshold (e.g. 200 bps), the simulator triggers a carry trade allocation model.

---

## 🧪 Phase 3 Verification Plan

The test suite `verify_reasoning.py` verifies the Swan solvers:
1. **Graph Pathfinder Isolation:** Verifies that reachability checks compile correctly and yield expected binary paths.
2. **GNN Serving check:** Asserts that predictions return valid float arrays via local ONNX runtime.
3. **MIP Convergence test:** Formulates a mock subset allocation and verifies that HiGHS returns the global optimum matching hand-computed bounds.
4. **Excel live formula check:** Validates that generated LBO sheets do not contain static numeric values in formula fields.