# Rogo AI Analyst — Development Summary

This document provides a comprehensive overview of the design, implementation, and verification of the **Rogo AI Analyst** built in the `swan-rogo` workspace copy. The Rogo AI Analyst is a neuro-symbolic financial intelligence coordinator running on top of Swan (a Datalog + GNN + MILP optimizer framework bound to DuckDB).

---

## Project Overview

The Rogo AI Analyst replicates the capabilities of a modern financial analyst terminal ("Bloomberg + ChatGPT") by combining:
1.  **Structured Financial Knowledge**: Recursive parent-subsidiary Datalog lookups and SEC filing records.
2.  **AI-Native Reasoning**: Isolated Python execution sandboxes and anti-hallucination citation trails.
3.  **Predictive Modeling**: Graph Neural Networks (GNN) to forecast valuation multiples.
4.  **Prescriptive Optimization**: Mixed-Integer Linear Programming (MILP) solvers to select optimal corporate acquisition targets.
5.  **User UI Frontend**: A responsive, dark-mode glassmorphic web console interface.

---

## Detailed Development Phases

### Phase 1: Ingestion & Relational Datalog Pipeline
*   **Seed Data Generation**: [seed_data.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/nlq/app/seed_data.py) seeds six mock CSV tables under `/data/` representing GLEIF legal entities, OpenFIGI securities, SEC 10-K filings, and SEC Form 4 insider transactions, loading them into DuckDB.
*   **Ontology Mapping**: [ontology.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/nlq/app/ontology.py) defines the PyRel concepts, properties, and direct-parent relationships.
*   **Recursive Parent-Subsidiary Rules**: Implemented recursive Datalog rules to trace the ultimate parents (top-most corporate ancestors) of any legal entity.
    *   *Base Case*: If an entity has no parent, its ultimate parent is itself.
    *   *Recursive Case*: If entity `A` has parent `B`, and `B` has ultimate parent `C`, then `A` has ultimate parent `C`.
*   **Datalog Safe Negation Fix**: The initial base case `not_(p1.direct_parent(p2))` introduced an unsafe free variable `p2`. We resolved this by introducing a helper relation `has_parent("YES")` and negating it (`not_(p1.has_parent("YES"))`), which binds all variables safely and ensures unique ultimate parentage resolution.

### Phase 2: State Memory, Routing & Secure Sandboxing
*   **State Manager**: [state_manager.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/nlq/app/state_manager.py) serializes short-term history, active target tickers, and comps sheets config into a local JSON file (`session_memory.json`).
*   **Nexus Query Router**: [router.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/nlq/app/router.py) checks keywords and historical context to route user questions to three backends:
    1.  `ROUTE_NLQ`: Standard tabular database queries.
    2.  `ROUTE_GRAPH`: Relational pathfinding and centrality.
    3.  `ROUTE_PREDICT`: GNN multiple predictions and MILP target portfolios.
*   **Secure Sandbox**: [sandbox.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/nlq/app/sandbox.py) uses Python AST and limited execution namespaces to block unsafe calls (preventing filesystem, subprocess, and network socket access).
*   **Filing Citations Trail**: Generates a verifiable audit trail mapping returned financial values back to their source SEC EDGAR accession number and filing date with a confidence score of `1.0` (100% confidence).

### Phase 3: Relational GNNs & Graph Reasoners
*   **PyG HeteroData Graph Load**: [gnn_model.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/nlq/app/gnn_model.py) queries DuckDB to build a PyTorch Geometric `HeteroData` graph mapping `company` nodes, `legal_entity` nodes, and their edges.
    *   *Normalization*: Company features (revenue and net income) are scaled down by `1e9` (scaled to billions) to avoid floating-point overflow and prevent ReLU saturation.
*   **HeteroGNN Architecture**: Implements a two-layer HeteroGNN utilizing `HeteroConv` and `SAGEConv` to propagate features across bipartite channels and predict positive EV/Sales multiples.
*   **Neuro-Symbolic Soft Logic Loss**: Formulates a soft-logic sector bounds loss function based on the Łukasiewicz t-norm, penalizing software multiple predictions that fall outside the industry bounds `[2.0x, 40.0x]`.
*   **Path Reasoner**: [path_reasoner.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/nlq/app/path_reasoner.py) utilizes NetworkX to find shortest path hops and compute PageRank node importance centralities.
    *   *Namespace Suffixing*: Suffixes company node IDs with `" (Company)"` to prevent namespace collisions when companies and legal entities share identical names.

### Phase 4: Target Optimization & Orchestration Pipeline
*   **Prescriptive MILP Solver**: [optimizer.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/nlq/app/optimizer.py) uses Swan's native prescriptive solver wrapper (`pyrel_duckdb.reasoners.prescriptive.Problem`) to select optimal acquisition targets.
    *   *Objective*: Maximize aggregate net income.
    *   *Constraints*: Select exactly $K$ targets, limit total GNN-predicted multiple cost below a budget limit, and enforce sector diversity (at most $M$ targets per industry).
*   **Nexus Agent Pipeline**: [agent_pipeline.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/nlq/app/agent_pipeline.py) connects the router, state manager, sandbox compiler, pathfinder, GNN, and MILP optimizer into a single unified `NexusAgent` class.

---

## Swan Engine Core Bug Remediations

During development, we diagnosed and fixed a bug in the core Swan compiler SQL generation:
*   **Location**: [loader_helpers.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/loader_helpers.py#L125-L170)
*   *Bug*: The SQL insertion builder hardcoded `"id"` as the lookup primary key column name in SQL subqueries (e.g. `SELECT id FROM ...`). This crashed ingestion for concepts identified by custom keys (like `Company` using `ticker` and `LegalEntity` using `lei`).
*   *Fix*: Modified the subquery builder to dynamically retrieve the primary key column name of the target concept using its `identify_by` schema configuration:
    ```python
    target_pk = list(val_expr.concept.identify_by.keys())[0] if val_expr.concept.identify_by else "id"
    ```

---

## Web Application UI Frontend

To deliver a premium financial terminal experience, we built a custom web console interface located under [web_app/](file:///home/maxdemarzi/swan-rogo/web_app/):
1.  **Frontend**:
    *   [index.html](file:///home/maxdemarzi/swan-rogo/web_app/index.html): Standard HTML5 layout.
    *   [styles.css](file:///home/maxdemarzi/swan-rogo/web_app/styles.css): Premium, glassmorphic dark-mode CSS theme utilizing Outfit/Inter Google Fonts and purple neon glows.
    *   [app.js](file:///home/maxdemarzi/swan-rogo/web_app/app.js): Asynchronous JS engine that sends chat requests, renders tabular results, draws graph paths, displays predicted multiples, and structures citation cards.
2.  **Backend Web Server**:
    *   [web_server.py](file:///home/maxdemarzi/swan-rogo/python/pyrel_duckdb/nlq/app/web_server.py): A custom Python HTTP server exposing `/api/chat` that pipes JSON requests directly to the `NexusAgent` pipeline without external dependencies.
    *   [run_web_app.sh](file:///home/maxdemarzi/swan-rogo/run_web_app.sh): Launcher script preloading the correct standard libraries under ASan debug environments.

---

## Verification & testing Commands

### 1. Run Automated Unit Tests (21/21 Pass)
Run the complete pytest test suites verifying all ingestion logic, sandbox isolation rules, PageRank traversals, GNN predictions, and target solver:
```bash
LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libasan.so.8:/usr/lib/x86_64-linux-gnu/libstdc++.so.6" ASAN_OPTIONS=detect_leaks=0 PYTHONPATH=python pytest test/python/test_rogo_agent.py test/python/test_rogo_sandbox.py test/python/test_rogo_gnn.py test/python/test_rogo_agent_pipeline.py -v
```

### 2. Run Terminal-Based Interactive Demo
Run a quick demo showcasing routing, sandbox citation trails, pathfinding, and target optimizations directly on the command line:
```bash
LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libasan.so.8:/usr/lib/x86_64-linux-gnu/libstdc++.so.6" ASAN_OPTIONS=detect_leaks=0 PYTHONPATH=python python3 run_agent_demo.py
```

### 3. Launch Web Application Interface
Start the background server listening on port 8000:
```bash
./run_web_app.sh
```
*(If on a remote server, establish an SSH tunnel on your local machine: `ssh -N -L 8080:localhost:8000 maxdemarzi@<server_ip>` and browse to `http://localhost:8080`)*
