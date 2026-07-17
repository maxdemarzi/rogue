CELL_MAPPING = {
    "B5": {"table": "fundamentals_snapshots", "column": "revenue", "label": "Revenue"},
    "B6": {"table": "fundamentals_snapshots", "column": "cogs", "label": "COGS"},
    "B7": {"table": "fundamentals_snapshots", "column": "operating_income_loss", "label": "Operating Income"},
    "B8": {"table": "fundamentals_snapshots", "column": "ebitda", "label": "EBITDA"},
    "B9": {"table": "fundamentals_snapshots", "column": "interest_expense", "label": "Interest Expense"},
    "B10": {"table": "fundamentals_snapshots", "column": "total_debt", "label": "Total Debt"},
    "B11": {"table": "fundamentals_snapshots", "column": "assets", "label": "Total Assets"},
    "B12": {"table": "fundamentals_snapshots", "column": "liabilities", "label": "Total Liabilities"},
    "B13": {"table": "fundamentals_snapshots", "column": "working_capital", "label": "Working Capital"},
    "B14": {"table": "fundamentals_snapshots", "column": "retained_earnings", "label": "Retained Earnings"},
    "B15": {"table": "fundamentals_snapshots", "column": "market_capitalization", "label": "Market Capitalization"},
    "B16": {"table": "fundamentals_snapshots", "column": "accounts_receivable", "label": "Accounts Receivable"},
}

FORMULA_MAPPING = {
    "E3": {"formula": "=B5-B6", "label": "Gross Profit", "dependencies": ["B5", "B6"]},
    "E4": {"formula": "=E3/B5", "label": "Gross Profit Margin (%)", "dependencies": ["B5", "E3"]},
    "E5": {"formula": "=B8/B5", "label": "EBITDA Margin (%)", "dependencies": ["B8", "B5"]},
    "E6": {"formula": "=B10/B14", "label": "Debt-to-Equity (%)", "dependencies": ["B10", "B14"]},
    "E7": {"formula": "=B7/B9", "label": "Interest Coverage (x)", "dependencies": ["B7", "B9"]},
    "E8": {"formula": "=365*B16/B5", "label": "Days Sales Outstanding (DSO)", "dependencies": ["B16", "B5"]},
    "E9": {"formula": "=1.2*(B13/B11) + 1.4*(B14/B11) + 3.3*(B7/B11) + 0.6*(B15/B12) + 0.999*(B5/B11)", "label": "Altman Z-Score", "dependencies": ["B13", "B11", "B14", "B7", "B15", "B12", "B5"]}
}

def locate_source_row(cell_ref, ticker="AIR", year=2012):
    """
    Locates the physical SQL source table, column, and row query for any audited
    Excel cell in the generated spreadsheet model.
    """
    cell_ref = cell_ref.upper().strip()
    
    # 1. Check if it's a formula cell
    if cell_ref in FORMULA_MAPPING:
        f_info = FORMULA_MAPPING[cell_ref]
        deps_info = {dep: locate_source_row(dep, ticker, year) for dep in f_info["dependencies"]}
        return {
            "cell": cell_ref,
            "type": "derived_formula",
            "label": f_info["label"],
            "formula": f_info["formula"],
            "dependencies": deps_info
        }
        
    # 2. Check if it's a hardcoded database cell
    if cell_ref in CELL_MAPPING:
        m_info = CELL_MAPPING[cell_ref]
        sql_query = (
            f"SELECT {m_info['column']} "
            f"FROM {m_info['table']} "
            f"WHERE ticker = '{ticker}' AND fiscal_year = {year};"
        )
        return {
            "cell": cell_ref,
            "type": "database_row_locator",
            "label": m_info["label"],
            "table": m_info["table"],
            "column": m_info["column"],
            "ticker_filter": ticker,
            "year_filter": year,
            "sql_query": sql_query
        }
        
    return {
        "cell": cell_ref,
        "type": "unknown",
        "message": "Cell is not mapped to the active financial model variables."
    }

if __name__ == "__main__":
    import json
    
    # Audit a database-backed cell
    print("Auditing Cell B5 (Revenue):")
    print(json.dumps(locate_source_row("B5"), indent=2))
    
    # Audit a formula-backed cell
    print("\nAuditing Cell E9 (Altman Z-Score):")
    print(json.dumps(locate_source_row("E9"), indent=2))
