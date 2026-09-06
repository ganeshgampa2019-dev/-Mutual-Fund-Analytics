import sqlite3

# Updated queries using exact database column names
QUERY_TOP_ASSETS = """
SELECT scheme_name, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;
"""

QUERY_AVG_NAV = """
SELECT amfi_code, AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY amfi_code
LIMIT 5;
"""

QUERY_TRANSACTION_SUMMARY = """
SELECT transaction_type, COUNT(*) AS total_count, SUM(amount_inr) AS total_volume
FROM fact_transactions
GROUP BY transaction_type;
"""

QUERY_TOP_RETURNS = """
SELECT scheme_name, return_1yr_pct
FROM fact_performance
ORDER BY return_1yr_pct DESC
LIMIT 5;
"""

QUERY_MONTHLY_TXN_COUNT = """
SELECT SUBSTR(transaction_date, 1, 7) AS txn_month, COUNT(*) AS txn_count
FROM fact_transactions
GROUP BY txn_month
ORDER BY txn_month;
"""

SQL_QUERIES = [
    QUERY_TOP_ASSETS,
    QUERY_AVG_NAV,
    QUERY_TRANSACTION_SUMMARY,
    QUERY_TOP_RETURNS,
    QUERY_MONTHLY_TXN_COUNT,
]

# Database connection
conn = sqlite3.connect('database/bluestock_mf.db')
cursor = conn.cursor()

print("Executing corrected SQL queries...\n")
for i, query in enumerate(SQL_QUERIES, 1):
    print(f"--- Running Query {i} ---")
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results[:3]:  # Print top 3 rows for preview
            print(row)
    except Exception as e:
        print(f"Error executing query {i}: {e}")
    print("\n")

conn.close()