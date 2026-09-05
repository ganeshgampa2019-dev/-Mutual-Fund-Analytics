import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("mutual_funds.db")

print("--- TESTING SQL QUERIES ON DATABASE ---")

# 1. Database lo unna table names chuddam
query_tables = (
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE"
    " 'sqlite_%';"
)
tables = pd.read_sql(query_tables, conn)
print("\nAvailable Tables in Database:")
print(tables)

# 2. Fund Master table nundi first 5 records chuddam
query_fund_sample = "SELECT * FROM fund_master LIMIT 5;"
df_funds = pd.read_sql(query_fund_sample, conn)
print("\nSample Rows from fund_master:")
print(df_funds)

conn.close()