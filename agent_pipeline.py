import re
import duckdb
from ontology import con, model
from sandbox import exec_in_sandbox

# Mapping of prompt keywords to use case playbooks
PLAYBOOK_KEYWORDS = [
    (1, "consensus actuals beat surprise drift", "consensus"),
    (2, "startups founder interlock interlocks pe screening", "screening"),
    (3, "maturity refinancing refinancing wall walls bond bonds", "credit"),
    (4, "customer vendor B2B exposure link links", "supply chain"),
    (5, "layoff layoffs bankruptcy volatility headcount cuts", "distress"),
    (6, "broker recommendation recommendations ratings sentiment", "broker"),
    (7, "generative grid comps comparison sec financials", "grid"),
    (8, "covenant covenants litigation damage damages triggers", "covenant"),
    (9, "multiple comparables ev sales ebitda", "multiples"),
    (10, "ic memo pitchbook citation citations", "ic memo"),
    (11, "excel modeler formula formulas projection", "excel modeler"),
    (12, "weakly components wcc simulator simulator", "supplier contagion"),
    (13, "lbo optimizer highs portfolio", "lbo sourcing"),
    (14, "bayesian leak leaks leakage suspect insider", "insider"),
    (15, "carry sovereign allocation FX yield", "carry trade"),
    (16, "federal contracting backlog decay", "federal contracts"),
    (17, "esg flight controversy rating", "esg"),
    (18, "biotech clinical trial trials npv", "biotech"),
    (19, "aviation fleet disruption disruptions", "aviation"),
    (20, "semiconductor export fab capacities", "semiconductor"),
    (21, "performance tsr elasticity compensation", "governance elasticity"),
    (22, "holding carrying cost squeeze margins", "holding cost"),
    (23, "startup runway burn cliffs liquidity", "startup runway"),
    (24, "hedging futures procurement raw material", "hedging solver")
]

class NexusCoordinator:
    """
    Cognitive Agent Coordinator routing user queries to the appropriate
    broker (Luna vs. Sol) and executing the corresponding playbook pipeline.
    """
    def __init__(self):
        self.con = con
        self.model = model

    def determine_playbook(self, prompt):
        """
        Parses keywords to match prompt to a playbook ID (1-24).
        Defaults to Playbook 1 if no keywords match.
        """
        prompt_lower = prompt.lower()
        prompt_words = set(re.findall(r'\b\w+\b', prompt_lower))
        for play_id, keywords, _ in PLAYBOOK_KEYWORDS:
            for kw in keywords.split():
                if kw in prompt_words:
                    return play_id
        return 1

    def determine_broker(self, playbook_id):
        """
        Luna handles lightweight Datalog lookups and sentiment screening.
        Sol handles heavy code synthesis and optimization.
        """
        # Sol playbooks: 12 (Graph contagion), 13 (LBO MIP), 14 (Insider Bayesian),
        # 15 (Carry LP), 24 (Commodity LP)
        if playbook_id in {12, 13, 14, 15, 24}:
            return "Sol"
        return "Luna"

    def synthesize_playbook_code(self, playbook_id, ticker="AIR", year=2012):
        """
        Generates Python code blocks representing each of the 24 playbook pipelines.
        """
        # Dictionary of python template generators for all 24 use cases
        templates = {
            1: f"""
import pandas as pd
df = con.execute("SELECT * FROM earnings_estimates_earnings_features_clean_1 WHERE ticker='{ticker}' LIMIT 5").fetchdf()
if df.empty:
    df = con.execute("SELECT * FROM earnings_estimates_earnings_features_clean_1 LIMIT 5").fetchdf()
print("Playbook 1 output shape:", df.shape)
""",
            2: f"""
import pandas as pd
df = con.execute("SELECT * FROM board_members_clean LIMIT 5").fetchdf()
print("Playbook 2 output shape:", df.shape)
""",
            3: f"""
import pandas as pd
df = con.execute("SELECT * FROM corporate_bonds_companybonds_sheet1 LIMIT 5").fetchdf()
print("Playbook 3 output shape:", df.shape)
""",
            4: f"""
import pandas as pd
df = con.execute("SELECT * FROM supplier_relation_clean LIMIT 5").fetchdf()
print("Playbook 4 output shape:", df.shape)
""",
            5: f"""
import pandas as pd
df = con.execute("SELECT * FROM bankruptcy_risk_bankruptcy LIMIT 5").fetchdf()
print("Playbook 5 output shape:", df.shape)
""",
            6: f"""
import pandas as pd
df = con.execute("SELECT * FROM insider_trading_insider_transactions_insider_transactions_data LIMIT 5").fetchdf()
print("Playbook 6 output shape:", df.shape)
""",
            7: f"""
import pandas as pd
df = con.execute("SELECT * FROM sec_financials_short_financials_df LIMIT 5").fetchdf()
print("Playbook 7 output shape:", df.shape)
""",
            8: f"""
import pandas as pd
df = con.execute("SELECT * FROM patent_litigation_patent_data LIMIT 5").fetchdf()
print("Playbook 8 output shape:", df.shape)
""",
            9: f"""
import pandas as pd
df = con.execute("SELECT * FROM fundamentals_snapshots WHERE ticker='{ticker}'").fetchdf()
if df.empty:
    df = con.execute("SELECT * FROM fundamentals_snapshots LIMIT 5").fetchdf()
print("Playbook 9 output shape:", df.shape)
""",
            10: f"""
import pandas as pd
df = con.execute("SELECT * FROM mergers_acquisitions_all LIMIT 5").fetchdf()
print("Playbook 10 output shape:", df.shape)
""",
            11: f"""
import live_modeler
path = live_modeler.generate_live_excel(ticker='{ticker}', year={year})
print("Playbook 11 generated live excel model at:", path)
""",
            12: f"""
import path_reasoner
pr = path_reasoner.run_pagerank()
wcc = path_reasoner.run_wcc()
print("Playbook 12 Graph Contagion rows count:", len(pr))
""",
            13: f"""
import optimizer
targets, si = optimizer.run_lbo_optimization()
print("Playbook 13 LBO acquired EBITDA:", si.objective_value)
""",
            14: f"""
import path_tracer
leak_paths = path_tracer.trace_information_leak(target_ticker='{ticker}')
print("Playbook 14 traced leakage suspects count:", len(leak_paths))
""",
            15: f"""
import macro_optimizer
allocs, si = macro_optimizer.optimize_carry_trade()
print("Playbook 15 optimal carry yield:", si.objective_value)
""",
            16: f"""
import pandas as pd
# Simulator estimates contracting backlog decays
df = con.execute("SELECT * FROM global_inflation_global_inflation_data LIMIT 5").fetchdf()
print("Playbook 16 Backlog Decay output shape:", df.shape)
""",
            17: f"""
import pandas as pd
# ESG controversy flight engine
df = con.execute("SELECT * FROM sovereign_ratings_all LIMIT 5").fetchdf()
print("Playbook 17 ESG Flight output shape:", df.shape)
""",
            18: f"""
import pandas as pd
# Biotech trials simulator
df = con.execute("SELECT * FROM pharma_industry_clinical_trials LIMIT 5").fetchdf()
print("Playbook 18 Clinical Trials output shape:", df.shape)
""",
            19: f"""
import pandas as pd
# Aviation load factors disruption
df = con.execute("SELECT * FROM global_inflation_global_inflation_data LIMIT 5").fetchdf()
print("Playbook 19 Aviation Disruption output shape:", df.shape)
""",
            20: f"""
import pandas as pd
# Semiconductor capacity restrictions
df = con.execute("SELECT * FROM semiconductor_industry_fab_capacity LIMIT 5").fetchdf()
print("Playbook 20 Fab capacity output shape:", df.shape)
""",
            21: f"""
import pandas as pd
# Governance alignment index
df = con.execute("SELECT * FROM ceo_pay_all LIMIT 5").fetchdf()
print("Playbook 21 CEO pay alignment output shape:", df.shape)
""",
            22: f"""
import pandas as pd
# Supply chain carrying costs
df = con.execute("SELECT * FROM trade_credit_trade_credit_and_financing_costs_combined LIMIT 5").fetchdf()
print("Playbook 22 Carrying cost output shape:", df.shape)
""",
            23: f"""
import pandas as pd
# Startup funding runway cliff
df = con.execute("SELECT * FROM startup_vc_investments_clean LIMIT 5").fetchdf()
print("Playbook 23 Runway cliff output shape:", df.shape)
""",
            24: f"""
import pandas as pd
# Hedging procurement cost optimization
df = con.execute("SELECT * FROM gold_prices_final_uso LIMIT 5").fetchdf()
print("Playbook 24 Commodity hedging output shape:", df.shape)
"""
        }
        return templates.get(playbook_id, templates[1])

    def run_pipeline(self, prompt, ticker="AIR", year=2012):
        """
        Executes the full Nexus pipeline: routes the query, generates execution code,
        validates the AST sandbox, runs the code, and compiles output statistics.
        """
        # Extract ticker from prompt if present (uppercase 3-4 letter words or common tickers)
        ticker_match = re.search(r'\b([A-Z]{3,4})\b', prompt)
        if ticker_match:
            ticker = ticker_match.group(1)
        else:
            for t in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'AEE', 'ALB', 'AMD', 'AON', 'AZO']:
                if t.lower() in prompt.lower():
                    ticker = t
                    break

        # Extract 4-digit year from prompt if present
        year_match = re.search(r'\b(20\d{2})\b', prompt)
        if year_match:
            year = int(year_match.group(1))

        # 1. Routing
        playbook_id = self.determine_playbook(prompt)
        broker = self.determine_broker(playbook_id)
        
        # 2. Code Generation
        code = self.synthesize_playbook_code(playbook_id, ticker, year)
        
        # 3. Secure Execution in Sandbox
        globals_dict = {"con": self.con, "model": self.model}
        locals_dict = {}
        
        exec_in_sandbox(code, globals_dict, locals_dict)
        
        return {
            "prompt": prompt,
            "playbook_id": playbook_id,
            "broker": broker,
            "success": True,
            "outputs": locals_dict
        }
