import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("mutual_funds.db")

print("--- EXPLORATORY DATA ANALYSIS (EDA) ---")

# 1. Check total number of funds in fund_master
query_funds = "SELECT COUNT(*) AS total_funds FROM fund_master;"
df_funds = pd.read_sql(query_funds, conn)
print(f"Total Funds: {df_funds['total_funds'].iloc[0]}")

# 2. Check sample records from nav_history
query_nav = "SELECT * FROM nav_history LIMIT 5;"
df_nav_sample = pd.read_sql(query_nav, conn)
print("\nSample NAV History Records:")
print(df_nav_sample)

conn.close()