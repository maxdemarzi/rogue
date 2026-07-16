import duckdb

db_path = '/home/maxdemarzi/rogue/rogue_finance.duckdb'
print(f"Connecting to DuckDB at {db_path}...")
con = duckdb.connect(db_path)

# 1. Show all tables
tables = con.execute("SHOW TABLES").fetchall()
print(f"\nTotal Tables Ingested: {len(tables)}")
print("Table list sample (first 15):")
for t in sorted([r[0] for r in tables])[:15]:
    print(f"  - {t}")

# 2. Check row counts for master dimensions and sample tables
sample_tables = [
    'companies',
    'countries',
    'ohlcv',
    'index_constituents',
    'sec_financials_short_financials_df',
    'earnings_estimates_earnings_features_clean_1'
]

print("\n=== ROW COUNTS FOR CRITICAL TABLES ===")
for t in sample_tables:
    try:
        cnt = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  Table: {t:45} | Rows: {cnt:,}")
    except Exception as e:
        print(f"  Table: {t:45} | Error: {e}")

# 3. Test joining across tables
print("\n=== TESTING CROSS-TABLE JOIN QUERY ===")
join_query = """
    SELECT 
      c.ticker,
      c.company_name,
      e.earnings_date,
      e.beat,
      o.close_val,
      o.volume
    FROM companies c
    JOIN earnings_estimates_earnings_features_clean_1 e ON c.ticker = e.ticker
    JOIN ohlcv o ON c.ticker = o.ticker AND e.earnings_date::DATE = o.date_time::DATE
    WHERE c.ticker = 'AAPL'
    ORDER BY e.earnings_date::DATE DESC
    LIMIT 5;
"""
try:
    res = con.execute(join_query).fetchdf()
    print(res)
except Exception as e:
    print("Join query error:", e)

# 4. Check schema and constraints of a sample table
print("\n=== CHECKING SCHEMA CONSTRAINTS (companies) ===")
schema_info = con.execute("PRAGMA table_info(companies)").fetchall()
for col in schema_info:
    print(f"  Col: {col[1]:15} | Type: {col[2]:10} | Nullable: {'NO' if col[3] else 'YES'} | PK: {'YES' if col[5] else 'NO'}")

con.close()
