import sqlite3
import pandas as pd

conn = sqlite3.connect('database/bluestock_mf.db')

for table in ['fact_nav', 'fact_performance', 'fact_transactions']:
    print(f"\n--- Columns in {table} ---")
    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 1;", conn)
    print(list(df.columns))

conn.close()