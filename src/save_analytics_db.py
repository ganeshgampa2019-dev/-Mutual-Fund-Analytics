"""Persist a joined fund performance analytics table in SQLite."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def save_to_db() -> None:
    """Create or replace the analytics_fund_performance table."""
    query = """
    SELECT f.amfi_code, f.scheme_name, f.category, f.fund_house,
           p.return_1yr_pct, p.return_3yr_pct, p.return_5yr_pct,
           p.sharpe_ratio, p.risk_grade
    FROM dim_fund f JOIN fact_performance p ON f.amfi_code = p.amfi_code
    """
    with sqlite3.connect(ROOT / "database" / "bluestock_mf.db") as connection:
        result = pd.read_sql_query(query, connection)
        result.to_sql("analytics_fund_performance", connection, if_exists="replace", index=False)

if __name__ == '__main__':
    save_to_db()