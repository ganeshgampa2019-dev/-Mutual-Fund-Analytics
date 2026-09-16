"""Create a compact fund dimension from loaded performance data."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


def create_dimension() -> None:
    """Rebuild dim_fund from the fact_performance table."""
    with sqlite3.connect(ROOT / "database" / "bluestock_mf.db") as connection:
        connection.executescript("""
        DROP TABLE IF EXISTS dim_fund;
        CREATE TABLE dim_fund (amfi_code TEXT PRIMARY KEY, scheme_name TEXT, fund_house TEXT, category TEXT, plan TEXT);
        INSERT OR IGNORE INTO dim_fund
        SELECT DISTINCT amfi_code, scheme_name, fund_house, category, plan
        FROM fact_performance WHERE amfi_code IS NOT NULL;
        """)


if __name__ == "__main__":
    create_dimension()