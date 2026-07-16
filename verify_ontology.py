import sys
import pandas as pd
import ontology

def main():
    model = ontology.model
    print("=== VERIFYING SWAN ONTOLOGY ===")
    
    # 1. Check concept count
    num_concepts = len(model.concepts)
    print(f"Total Concepts Loaded: {num_concepts}")
    for i, c in enumerate(sorted([c.name for c in model.concepts])):
        print(f"  {i+1:2d}. {c}")
        
    if num_concepts < 50:
        print(f"[ERROR] Expected at least 50 concepts, but got {num_concepts}")
        sys.exit(1)
        
    print("\n--- Testing basic entity query ---")
    try:
        Company = model._concepts["Company"]
        df = model.where(Company.ticker == "AAPL").select(
            Company.ticker.alias("ticker"),
            Company.company_name.alias("name"),
            Company.cik.alias("cik")
        ).to_df()
        print("Query result:")
        print(df)
        if df.empty or df.loc[0, 'ticker'] != 'AAPL':
            print("[ERROR] Company query did not return expected results!")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to query Company: {e}")
        sys.exit(1)

    print("\n--- Testing SECStatement query ---")
    try:
        SECStatement = model._concepts["SECStatement"]
        df_sec = model.where(SECStatement.ticker == "AAPL").select(
            SECStatement.ticker.alias("ticker"),
            SECStatement.fiscal_year.alias("year"),
            SECStatement.total_assets.alias("assets")
        ).to_df()
        print("SECStatement Query result (first 3):")
        print(df_sec.head(3))
    except Exception as e:
        print(f"[ERROR] Failed to query SECStatement: {e}")
        sys.exit(1)

    print("\nVerification PASSED successfully!")

if __name__ == '__main__':
    main()
