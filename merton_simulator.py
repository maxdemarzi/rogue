import numpy as np
import scipy.stats as stats
import duckdb
from ontology import con

def merton_solver(VE, sigma_E, D, r, T=1.0, max_iter=100, tol=1e-6):
    """
    Vectorized Newton-Raphson solver for the Merton model.
    Resolves Asset Value (VA) and Asset Volatility (sigma_A) from:
    VE = VA * N(d1) - D * e^{-rT} * N(d2)
    sigma_E = (VA / VE) * N(d1) * sigma_A => sigma_A = (sigma_E * VE) / (VA * N(d1))
    """
    VE = np.maximum(np.array(VE, dtype=float), 1e-4)
    sigma_E = np.maximum(np.array(sigma_E, dtype=float), 1e-4)
    D = np.maximum(np.array(D, dtype=float), 1e-4)
    
    VA = VE + D  # Initial guess
    sigma_A = sigma_E * (VE / (VE + D))  # Initial guess
    
    for _ in range(max_iter):
        sigma_A = np.maximum(sigma_A, 1e-4)
        VA = np.maximum(VA, 1e-4)
        
        d1 = (np.log(VA / D) + (r + 0.5 * sigma_A**2) * T) / (sigma_A * np.sqrt(T))
        d2 = d1 - sigma_A * np.sqrt(T)
        
        Nd1 = stats.norm.cdf(d1)
        Nd2 = stats.norm.cdf(d2)
        
        VE_calc = VA * Nd1 - D * np.exp(-r * T) * Nd2
        
        diff = VE_calc - VE
        if np.all(np.abs(diff) < tol):
            break
            
        VA = VA - diff / np.maximum(Nd1, 1e-4)
        sigma_A = (sigma_E * VE) / np.maximum(VA * Nd1, 1e-4)
        
    dd = (np.log(VA / D) + (r - 0.5 * sigma_A**2) * T) / (sigma_A * np.sqrt(T))
    pd = stats.norm.cdf(-dd)
    return VA, sigma_A, dd, pd

def simulate_merton(db_path="rogue_finance.duckdb"):
    
    # Query latest US 10-year yield as risk-free rate
    r_row = con.execute("SELECT us10y / 100.0 FROM treasury_yields_us_treasury_yields_daily ORDER BY date DESC LIMIT 1").fetchone()
    r = r_row[0] if r_row else 0.0425
    
    # Query VE, D, and sigma_E from fundamentals_snapshots joined with latest volatility from bankruptcy table
    query = """
    SELECT
      s.ticker,
      s.market_capitalization AS VE,
      s.total_debt AS D,
      COALESCE(b.volatility, 0.40) AS sigma_E
    FROM fundamentals_snapshots s
    LEFT JOIN (
      SELECT ticker, volatility
      FROM (
        SELECT ticker, volatility, ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date DESC) as rn
        FROM bankruptcy_risk_bankruptcy
        WHERE ticker IN (SELECT DISTINCT ticker FROM fundamentals_snapshots)
      )
      WHERE rn = 1
    ) b ON s.ticker = b.ticker
    WHERE s.market_capitalization > 0 AND s.total_debt > 0;
    """
    rows = con.execute(query).fetchall()
    if not rows:
        print("No tickers found with positive market capitalization and debt.")
        return
        
    tickers = [row[0] for row in rows]
    VEs = np.array([row[1] for row in rows])
    Ds = np.array([row[2] for row in rows])
    sigma_Es = np.array([row[3] for row in rows])
    
    # Run solver
    VAs, sigma_As, dds, pds = merton_solver(VEs, sigma_Es, Ds, r)
    
    # Write back the computed PDs to database
    for ticker, pd in zip(tickers, pds):
        # Update latest bankruptcy record
        latest_date_row = con.execute(
            "SELECT MAX(date) FROM bankruptcy_risk_bankruptcy WHERE ticker = ?", [ticker]
        ).fetchone()
        
        if latest_date_row and latest_date_row[0]:
            latest_date = latest_date_row[0]
            con.execute(
                "UPDATE bankruptcy_risk_bankruptcy SET probability = ? WHERE ticker = ? AND date = ?",
                [float(pd), ticker, latest_date]
            )
            print(f"Updated Merton PD for {ticker} (Date: {latest_date}): {pd:.6f}")
        else:
            # If no record exists, insert a default one
            con.execute(
                "INSERT INTO bankruptcy_risk_bankruptcy (ticker, date, probability, volatility, multiplier, version) VALUES (?, '2024-06-21', ?, 0.40, 1.0, 20240901)",
                [ticker, float(pd)]
            )
            print(f"Inserted Merton PD for {ticker}: {pd:.6f}")

if __name__ == "__main__":
    simulate_merton()
