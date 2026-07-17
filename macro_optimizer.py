from pyrel_duckdb.reasoners.prescriptive import Problem
from ontology import model, Currency
from pyrel_duckdb.std import aggregates as aggs
from pyrel_duckdb import select

def optimize_carry_trade(max_single_exposure=0.40, max_high_inflation_exposure=0.20):
    """
    Formulates and solves the Macro Currency Carry Trade allocation optimization.
    """
    # 1. Initialize prescriptive problem context
    problem = Problem(model)
    
    # 2. Declare decision variables (populate=True updates database allocation column)
    allocation = problem.solve_for(
        Currency.allocation,
        type="cont",
        lower=0.0,
        upper=max_single_exposure,
        populate=True
    )
    
    # 3. Add constraints
    # Fully invested: Sum(allocation) == 1.0
    problem.satisfy(aggs.sum(Currency.allocation) == 1.0)
    
    # High inflation limit: Sum(allocation) where inflation > 5.0% <= 20%
    problem.satisfy(
        aggs.sum(Currency.allocation).where(Currency.inflation > 0.05) <= max_high_inflation_exposure
    )
    
    # 4. Objective: Maximize carry rate spread
    problem.maximize(aggs.sum(Currency.spread * Currency.allocation))
    
    # 5. Solve using HiGHS
    print("Solving Macro Carry Trade Optimizer...")
    problem.solve()
    
    # 6. Extract solve information
    si = problem.solve_info()
    print("Optimization complete.")
    print("Status:", si.termination_status)
    print("Objective Value (Portfolio Carry Rate):", si.objective_value)
    
    # 7. Query and return allocations
    allocations = select(
        Currency.code,
        Currency.spread,
        Currency.inflation,
        Currency.allocation
    ).to_df()
    
    return allocations, si

if __name__ == "__main__":
    try:
        allocations, info = optimize_carry_trade()
        print("\nOptimal Currency Carry Allocations:")
        print(allocations)
    except Exception as e:
        print("Macro optimization failed:", e)
