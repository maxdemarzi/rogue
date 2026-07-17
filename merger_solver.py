from ontology import con

def solve_merger_accretion(
    acquirer_ticker,
    target_ticker,
    offer_price,
    cash_fraction=0.5,
    synergies=10_000_000.0,
    debt_rate=0.06,
    tax_rate=0.21,
    db_path="rogue_finance.duckdb"
):
    """
    Computes post-merger combined EPS and accretion/dilution percentage.
    """
    # Query fundamental inputs for acquirer and target for 2012 (latest full year in snapshots)
    query = """
    SELECT
      ticker,
      earnings AS net_income,
      shares AS shares_outstanding,
      stock_price AS current_stock_price
    FROM fundamentals_snapshots
    WHERE ticker IN (?, ?) AND fiscal_year = 2012;
    """
    rows = con.execute(query, [acquirer_ticker, target_ticker]).fetchall()

    
    data = {row[0]: {"net_income": row[1], "shares": row[2], "price": row[3]} for row in rows}
    
    if acquirer_ticker not in data or target_ticker not in data:
        raise ValueError("Missing fundamental snapshots data for acquirer or target company.")
        
    acq = data[acquirer_ticker]
    tgt = data[target_ticker]
    
    # 1. Acquirer standalone EPS
    eps_acq = acq["net_income"] / acq["shares"]
    
    # 2. Merger Exchange Ratio and funding math
    er = offer_price / acq["price"]
    
    # Cash needed to fund the cash portion of the transaction
    cash_needed = offer_price * tgt["shares"] * cash_fraction
    
    # Post-tax interest expense on debt funding the cash portion
    post_tax_interest = cash_needed * debt_rate * (1.0 - tax_rate)
    
    # New shares issued for the stock portion
    shares_issued = tgt["shares"] * (1.0 - cash_fraction) * er
    
    # 3. Combined financials
    combined_net_income = acq["net_income"] + tgt["net_income"] + synergies - post_tax_interest
    combined_shares = acq["shares"] + shares_issued
    combined_eps = combined_net_income / combined_shares
    
    # 4. Accretion/Dilution Percentage
    accretion_dilution = (combined_eps - eps_acq) / eps_acq
    
    return {
        "acquirer_ticker": acquirer_ticker,
        "target_ticker": target_ticker,
        "acquirer_standalone_eps": eps_acq,
        "combined_eps": combined_eps,
        "accretion_dilution_pct": accretion_dilution,
        "cash_needed": cash_needed,
        "shares_issued": shares_issued,
        "exchange_ratio": er
    }

if __name__ == "__main__":
    # Test with AIR and another ticker (or mock tickers if only AIR exists)
    try:
        res = solve_merger_accretion(
            acquirer_ticker="AIR",
            target_ticker="AIR",  # self-merger test or proxy
            offer_price=25.0,
            cash_fraction=0.4,
            synergies=5_000_000.0
        )
        print("Merger Accretion Results:")
        for k, v in res.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print("Merger simulation failed:", e)
