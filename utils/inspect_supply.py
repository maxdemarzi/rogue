import pandas as pd

df = pd.read_csv('data/supply_chain/supply_chain_data.csv', nrows=2)
print("=== SUPPLY CHAIN DATA ===")
print(df.columns.tolist())
print(df.head(2))
