"""Export the top funds by one-year return from SQLite."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def analyze_fund_performance() -> pd.DataFrame:
    """Return and save the top ten schemes by one-year return."""
    query = """
    SELECT amfi_code, scheme_name, category, fund_house, return_1yr_pct,
           return_3yr_pct, return_5yr_pct, sharpe_ratio, risk_grade
    FROM fact_performance ORDER BY return_1yr_pct DESC LIMIT 10
    """
    with sqlite3.connect(ROOT / "database" / "bluestock_mf.db") as connection:
        result = pd.read_sql_query(query, connection)
    result.to_csv(ROOT / "data" / "fund_performance_output.csv", index=False)
    return result

if __name__ == '__main__':
    analyze_fund_performance()