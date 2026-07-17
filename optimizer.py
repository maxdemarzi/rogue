from pyrel_duckdb.reasoners.prescriptive import Problem
from ontology import model, Company
from pyrel_duckdb.std import aggregates as aggs
from pyrel_duckdb import select

def run_lbo_optimization(budget_limit=5_000_000_000.0, target_count=3):
    """
    Formulates and solves the LBO target acquisition problem.
    """
    # 1. Initialize prescriptive problem context
    problem = Problem(model)
    
    # 2. Declare binary decision variables scoped to viable, non-distressed, 
    # and GNN-approved target candidates.
    acquire = problem.solve_for(
        Company.acquire,
        type="bin",
        populate=True,
        where=[
            Company.enterprise_value > 0.0,
            Company.ebitda > -1e9,
            Company.altman_z_score > 1.81,
            Company.predicted_ebitda_margin >= 0.0,
            Company.is_sp500 == 1
        ]
    )
    
    # 3. Add constraints
    # Budget constraint: Sum(EV * acquire) <= budget_limit
    problem.satisfy(aggs.sum(Company.enterprise_value * Company.acquire) <= budget_limit)
    
    # Selection constraint: Sum(acquire) == target_count
    problem.satisfy(aggs.sum(Company.acquire) == target_count)
    
    # 4. Objective: Maximize total EBITDA acquired
    problem.maximize(aggs.sum(Company.ebitda * Company.acquire))
    
    # 5. Solve using HiGHS
    print(f"Solving LBO MIP Optimizer (Budget: ${budget_limit/1e9:.2f}B, Targets: {target_count})...")
    problem.solve()
    
    # 6. Extract solve information
    si = problem.solve_info()
    print("Optimization complete.")
    print("Status:", si.termination_status)
    print("Objective Value (EBITDA Acquired):", si.objective_value)
    
    # 7. Query and return chosen companies
    chosen_companies = select(
        Company.ticker,
        Company.company_name,
        Company.enterprise_value,
        Company.ebitda
    ).where(Company.acquire == 1).to_df()
    
    return chosen_companies, si

if __name__ == "__main__":
    try:
        companies, info = run_lbo_optimization()
        print("\nAcquisition Targets Selected:")
        print(companies)
    except Exception as e:
        print("Optimization failed:", e)
