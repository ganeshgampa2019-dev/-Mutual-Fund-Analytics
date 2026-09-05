import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("mutual_funds.db")

print("--- ADVANCED EXPLORATORY DATA ANALYSIS ---")

# 1. Check max and min NAV for each fund to see volatility
query_nav_range = """
    SELECT amfi_code, MIN(nav) as min_nav, MAX(nav) as max_nav, AVG(nav) as avg_nav
    FROM nav_history
    GROUP BY amfi_code
    LIMIT 5;
"""
df_range = pd.read_sql(query_nav_range, conn)
print("\nNAV Range (Min, Max, Avg) per Fund:")
print(df_range)

# 2. Check fund master details category-wise count
query_cat = """
    SELECT category, COUNT(*) as fund_count
    FROM fund_master
    GROUP BY category;
"""
df_cat = pd.read_sql(query_cat, conn)
print("\nFunds Count by Category:")
print(df_cat)

conn.close()