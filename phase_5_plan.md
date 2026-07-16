# Rebuilding the Rogo AI Analyst - Phase 5: Glassmorphic Web App Interface

This document details the frontend visual design, interactive visualizers, backend web server routes, and competitor-beating user interfaces for the **Glassmorphic Web App** (`web_app/`). We design a terminal interface that rivals Bloomberg, Koyfin, and Hebbia, combining rich styling with neuro-symbolic reasoning outputs.

---

## 📐 1. Premium Visual Design System (`styles.css`)

To establish a premium, state-of-the-art console interface that wows institutional financial clients, we implement a cohesive glassmorphic design system:

### A. Color Palette & Neon Glows
* **Base Canvas:** Deepest obsidian-violet (`#080414`).
* **Panels & Cards:** Translucent slate-glass (`rgba(17, 10, 36, 0.65)`) with a `backdrop-filter: blur(20px)` and a thin border border (`1px solid rgba(255, 255, 255, 0.08)`).
* **Primary Accent:** Cyber-purple (`#bd00ff`) for highlights and glows.
* **Secondary Accent:** Neon-teal (`#00f0ff`) representing Swan C++ reasoner paths and optimal variables.
* **Alert Status:** High-conviction buy/long signals in mint green (`#00ffaa`), risk/default warnings in hot pink (`#ff0055`).

### B. Typography
* We import Google Fonts **Outfit** (for headers and metrics) and **Inter** (for text blocks and data cells) to replace standard system fonts:
  ```css
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@400;600;800&display=swap');
  ```

---

## 💻 2. The Interactive Workspace Layout (`index.html`)

We structure a multi-pane split workspace allowing analysts to run comparative research without tab switching:

```
+-----------------------------------------------------------------------------------+
|  [Logo] ROGO NEXUS ANALYST TERMINAL                            [Status: Connected]|
+-----------------------------------------------------------------------------------+
|  Left Pane: Chat & Prompt Controller     | Right Pane: Interactive Visualization   |
|                                          |                                         |
|  > Input query...                        |  [ Hebbia Grid | Cytoscape Board Graph ]|
|  [Run Sourcing Optimizer]                |  [ Koyfin Chart | AlphaSense Redliner  ]|
|                                          |                                         |
|  +------------------------------------+  |  +-----------------------------------+  |
|  | Nexus Agent Chat Output            |  |  | Active Visualization Canvas       |  |
|  | - Predict EV/Sales multiples       |  |  |                                   |  |
|  | - Sourced portfolio optimization   |  |  |   (Interactive graph/comps grid)  |  |
|  | - Excel target links generated     |  |  |                                   |  |
|  +------------------------------------+  |  +-----------------------------------+  |
+-----------------------------------------------------------------------------------+
|  Bottom Pane: SEC Source Citation Card Info & Row-Index Audit Trails              |
+-----------------------------------------------------------------------------------+
```

---

## ⚡ 3. Competitor-Beating Interactive Components (`app.js`)

To surpass specialized tools, the web terminal renders tailored components based on the query route:

### A. Hebbia-Style Comparable Covenant Matrix
* **How it beats competitors:** Clickable cell values link directly to the **SEC Source Citation Cards**.
* **Interactivity:** Hovering over an M&A covenant metric (e.g. change-of-control threshold) displays a tooltip containing the exact SEC statement paragraph. Clicking the metric opens the document viewer scrolled directly to the source row index in DuckDB.

### B. AlphaSense-Style Risk Disclosure Redliner
* **How it beats competitors:** Split-screen comparison window highlighting deleted, modified, or added risk paragraphs.
* **Interactivity:** Deleted paragraphs are highlighted in hot-pink redlines, and newly inserted risk factors are highlighted in neon-green. A divergence indicator flags if the company added litigation risks that were unmentioned in prior files.

### C. PitchBook-Style Interactive Board Pathfinder
* **How it beats competitors:** Computes and visualizes warm executive pathways using `Cytoscape.js`.
* **Interactivity:** Rendered nodes represent corporate executives and company boards:
  * Acquirer executive ($A$) is highlighted in teal.
  * Target founder ($F$) is highlighted in purple.
  * Intermediate connectors are colored by connection strength ($\text{PathStrength}_p$).
  * Users can hover over intermediate nodes to view board seats and degree values.

### D. Koyfin-Style Multi-Axis Multiples Charting
* **How it beats competitors:** Interactive mean-reversion analysis overlays ($Z < -2.0$) computed by the Koyfin Multiple Solver.
* **Interactivity:** Built using Chart.js, rendering multi-axis timelines:
  * **Y1 Axis:** EV/Sales multiple (GNN prediction vs. historical).
  * **Y2 Axis:** Quarterly Revenue Growth %.
  * Plots a dotted green line representing the 5-year historical mean, highlighting undervalued arbitrage zones.

### E. Bloomberg Credit Default CDSD Interface
* **How it beats competitors:** Compares credit rating agency defaults against Merton options models and CDS market-implied default curves.
* **Interactivity:** Renders dual credit curves. Analysts can slider-adjust recovery rate assumptions to stress-test implied default probabilities dynamically.

---

## 🌐 4. Custom Python HTTP Server (`web_server.py`)

A light, fast Web Server exposes the terminal api directly inside our python framework:

### Exposed Endpoints
1. **`GET /`**: Serves the main glassmorphic HTML terminal dashboard.
2. **`POST /api/chat`**:
   * Receives: `{"message": "user query prompt", "session_id": "GUID"}`.
   * Execution flow:
     1. Passes the query to the **Nexus Router** to identify the route.
     2. Validates safety constraints inside the **AST Sandbox** if code generation is triggered.
     3. Queries `rogue_finance.duckdb` via Swan.
     4. Resolves citations and formats JSON return packets.
   * Returns:
     ```json
     {
       "answer_text": "Markdown response text detailing targets...",
       "route": "ROUTE_PREDICT",
       "data_payload": { ... },
       "citations": [
         {
           "citation_id": "CIT_SEC_2026_091",
           "val": 114500000000.0,
           "sql_locator": "SELECT ... FROM ..."
         }
       ]
     }
     ```

---

## 🔬 5. Audit Trail & Filing Source Citation Cards

To maintain auditability, when an analyst hovers over any metrics in the comps grids, a **Citation Card** renders at the bottom of the interface:

```
+---------------------------------------------------------------------------------+
| CITATION CARD [CIT_SEC_2026_091]                                               |
| Issuer: Apple Inc. (AAPL) | Filing: 10-K (FY2026) | Period Ending: 2026-09-26  |
| Concept: operating_income_loss | Sourced Value: $114,500,000,000.00             |
| Confidence: 1.00 (Audited)                                                      |
| SQL Locator: SELECT operating_income_loss FROM sec_financials_df WHERE row=9482 |
+---------------------------------------------------------------------------------+
```

---

## 🚀 6. Premium "Wow Factor" Interactive Features

To fully capture institutional buy-side interest, we implement four highly responsive interactive visualizers that demonstrate the real-time reasoning of our neuro-symbolic backend:

### A. Dynamic "What-If" LBO & M&A Sensitivity Sliders
* **How it works:** Directly in the comps grid or deal evaluation pane, analysts can adjust core transaction assumptions via sliders:
  * *Purchase Multiple (EV/EBITDA)*
  * *Leverage Percentage (LBO Debt %)*
  * *Interest Rate (Cost of Debt)*
  * *Synergy Realization Rate %*
* **Real-time Recalculation:** Adjusting these sliders triggers a client-side recalculation of the LBO debt amortization schedule and expected sponsor IRR. It sends socket requests to Swan's prescriptive solver to re-solve the HiGHS optimization target portfolio under the modified capital budgets in real-time.

### B. Supply Chain Distress Contagion Particle Heatmap
* **How it works:** Visualizes the supplies path network as a particle flow field using HTML5 Canvas or Cytoscape overlays:
  * Users can select a supplier node and adjust its *Merton Default Probability* via a slider.
  * Raising the default probability triggers a real-time cascade animation where red pulse waves flow down the supply graph edges, indicating distress propagation.
  * Downstream customer nodes change color and raise alerts as their *Attributed Supplier Default Exposure (ASDE)* limits are breached.

### C. Black-Litterman Portfolio Frontier Curve visualizer (Bloomberg PORT style)
* **How it works:** Renders the Markowitz Efficient Frontier curve for the global macro carry trade optimizer:
  * Displays a curved plot with expected carry yield on the Y-axis and portfolio covariance risk on the X-axis.
  * Toggle checkboxes allow analysts to add/remove sovereign yield curves (US, EU, JP, UK, etc.).
  * Drag-and-drop handles let analysts visually position custom currency views, instantly recalculating the Black-Litterman allocations and shifting the frontier curve dynamically.

### D. Hands-Free Speech-to-Query Dictation Interface
* **How it works:** Integrates a glassmorphic microphone button in the central input console utilizing the native browser Web Speech API:
  * Analysts can dictate complex questions (e.g., *"Find undervalued semiconductor fabs and show me the warm introductions to their board members"*).
  * Synthesizes audio commands into formatted prompt text for the Nexus Router, showing active voice-waveform animations.

---

## 🧪 Phase 5 Verification Plan

The test script `verify_web_app.py` executes these frontend validation checks:
1. **Endpoint Integrity:** Simulates chat requests to `/api/chat` and asserts response code `200` with correctly structured JSON payload fields.
2. **Citation Resolution:** Asserts that every numeric metric in the comps payload matches a valid citation object.
3. **HTML5 Tag Validation:** Audits `index.html` to confirm that CSS grids, Cytoscape containers, and Chart selectors use valid and unique HTML IDs.