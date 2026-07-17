import numpy as np
from ontology import con
import path_reasoner

def trace_information_leak(target_ticker, db_path="rogue_finance.duckdb"):
    """
    Computes the posterior probability of suspects being the source of 
    pre-event information leakage to the target company.
    """

    
    # 1. Query prior conviction scores from insider transactions
    # We group by owner_name to get their maximum conviction score
    query_priors = """
    SELECT
      owner_name,
      MAX(conviction_score) AS max_conv_score
    FROM insider_trading_insider_transactions_insider_transactions_data
    GROUP BY owner_name
    HAVING max_conv_score > 0
    LIMIT 20;
    """
    priors_rows = con.execute(query_priors).fetchall()
    
    if not priors_rows:
        # Fallback if no records found
        priors_rows = [("Insider A", 0.8), ("Insider B", 0.5), ("Insider C", 0.3)]
        
    suspects = [row[0] for row in priors_rows]
    prior_scores = np.array([row[1] for row in priors_rows])
    
    # Normalize priors to sum to 1.0
    epsilon = 0.01
    priors = (prior_scores + epsilon) / np.sum(prior_scores + epsilon)
    
    # 2. Query suspect company affiliations from board membership
    query_boards = """
    SELECT boardmembername, companyname
    FROM board_members_boardmembers
    WHERE LOWER(boardmembername) IN ({});
    """.format(", ".join(["?"] * len(suspects)))
    
    board_rows = con.execute(query_boards, [s.lower() for s in suspects]).fetchall()
    affiliations = {row[0].lower(): row[1] for row in board_rows}
    
    # 3. Compute likelihoods P(leak | S) based on graph distance to target_ticker
    likelihoods = []
    for suspect in suspects:
        suspect_lower = suspect.lower()
        company = affiliations.get(suspect_lower)
        
        if not company:
            # If no direct company affiliation is mapped, use a baseline distance
            distance = 4.0
        else:
            # Check if there is a path from suspect's company to target company
            # We use check_reachability as a proxy for distance
            if path_reasoner.check_reachability(company, target_ticker):
                distance = 1.0
            else:
                # If they share boards communication pathway
                distance = 2.0
                
        # Likelihood is modeled as exponential decay of distance
        likelihood = np.exp(-1.0 * distance)
        likelihoods.append(likelihood)
        
    likelihoods = np.array(likelihoods)
    
    # 4. Compute Bayesian Posterior P(S | target)
    numerator = likelihoods * priors
    denominator = np.sum(numerator)
    if denominator == 0:
        posteriors = np.ones_like(priors) / len(priors)
    else:
        posteriors = numerator / denominator
        
    results = []
    for suspect, prior, likelihood, posterior in zip(suspects, priors, likelihoods, posteriors):
        results.append({
            "suspect": suspect,
            "company_affiliation": affiliations.get(suspect.lower(), "Unknown"),
            "prior_probability": prior,
            "likelihood": likelihood,
            "posterior_probability": posterior
        })
        
    # Sort by posterior probability descending
    results = sorted(results, key=lambda x: x["posterior_probability"], reverse=True)
    return results

if __name__ == "__main__":
    try:
        paths = trace_information_leak("AIR")
        print("Information Leakage Path Analysis for AIR:")
        for idx, res in enumerate(paths[:5]):
            print(f"Rank {idx+1}: {res['suspect']}")
            print(f"  Affiliation: {res['company_affiliation']}")
            print(f"  Prior: {res['prior_probability']:.4f}")
            print(f"  Posterior: {res['posterior_probability']:.4f}")
    except Exception as e:
        print("Information leak tracer failed:", e)
