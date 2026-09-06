QUERY_TOP_ASSETS = """
SELECT scheme_name, aum_amount
FROM fact_performance
ORDER BY aum_amount DESC
LIMIT 5;
"""

QUERY_AVG_NAV = """
SELECT scheme_name, AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY scheme_name;
"""

QUERY_TRANSACTION_SUMMARY = """
SELECT transaction_type, COUNT(*) AS total_count, SUM(amount) AS total_volume
FROM fact_transactions
GROUP BY transaction_type;
"""

QUERY_TOP_RETURNS = """
SELECT scheme_name, returns_1yr
FROM fact_performance
ORDER BY returns_1yr DESC
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
