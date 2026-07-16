import duckdb
con = duckdb.connect('rogue_finance.duckdb')
tables = [t[0] for t in con.execute("SHOW TABLES").fetchall()]
print("Matching tables:")
for t in sorted(tables):
    if any(k in t.lower() for k in ['gleif', 'link', 'partner', 'relat', 'network', 'company', 'sec_fin', 'corporate_layoffs', 'bankruptcy_risk']):
        print(f"  - {t}")
con.close()
