import sys
import pandas as pd
import rules
from rules import model, FinancialSnapshot

def main():
    print("\n=== VERIFYING SWAN DERIVED RULES ===")
    
    # 1. Check if model exists
    print(f"Model Name: {model.name}")
    
    # 2. Select a subset of the 240 rules to query
    print("Executing query on derived financial ratios for AIR...")
    try:
        df = model.where(FinancialSnapshot.ticker == "AIR").select(
            FinancialSnapshot.ticker.alias("ticker"),
            FinancialSnapshot.fiscal_year.alias("year"),
            FinancialSnapshot.net_profit_margin.alias("net_profit_margin"),
            FinancialSnapshot.dupont_roe.alias("dupont_roe"),
            FinancialSnapshot.current_ratio.alias("current_ratio"),
            FinancialSnapshot.altman_z_score.alias("altman_z_score"),
            FinancialSnapshot.ebitda.alias("ebitda"),
            FinancialSnapshot.pe_multiple.alias("pe_multiple")
        ).to_df()
        
        print("\nQuery results (first 5 rows):")
        print(df.head(5))
        
        if df.empty:
            print("[ERROR] Derived rules query returned empty DataFrame!")
            sys.exit(1)
            
        print("\nChecking computed values...")
        row = df.iloc[0]
        print(f"  Year: {row['year']}")
        print(f"  Net Profit Margin: {row['net_profit_margin']:.4f}")
        print(f"  DuPont ROE: {row['dupont_roe']:.4f}")
        print(f"  Current Ratio: {row['current_ratio']:.4f}")
        print(f"  Altman Z-Score: {row['altman_z_score']:.4f}")
        print(f"  EBITDA: {row['ebitda']:.4f}")
        print(f"  P/E Multiple: {row['pe_multiple']:.4f}")
        
    except Exception as e:
        print(f"[ERROR] Failed to query derived rules: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nRules verification PASSED successfully!")

if __name__ == '__main__':
    main()
