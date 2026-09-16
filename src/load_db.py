"""Load every cleaned project table into a reproducible SQLite database."""
from pathlib import Path
import sqlite3

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
DATABASE = ROOT / "database" / "bluestock_mf.db"
TABLES = {
    "cleaned_01_fund_master.csv": "dim_fund",
    "cleaned_02_nav_history.csv": "fact_nav",
    "cleaned_03_aum_by_fund_house.csv": "fact_aum_by_fund_house",
    "cleaned_04_monthly_sip_inflows.csv": "fact_sip_inflows",
    "cleaned_05_category_inflows.csv": "fact_category_inflows",
    "cleaned_06_industry_folio_count.csv": "fact_folios",
    "cleaned_07_scheme_performance.csv": "fact_performance",
    "cleaned_08_investor_transactions.csv": "fact_transactions",
    "cleaned_09_portfolio_holdings.csv": "fact_holdings",
    "cleaned_10_benchmark_indices.csv": "fact_benchmark_indices",
}


def load_database() -> Path:
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE) as connection:
        for filename, table in TABLES.items():
            source = PROCESSED / filename
            if not source.exists():
                raise FileNotFoundError(f"Missing processed input: {source}")
            frame = pd.read_csv(source)
            frame.to_sql(table, connection, if_exists="replace", index=False)
            if frame.empty:
                raise ValueError(f"Loaded table is empty: {table}")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_nav_code_date ON fact_nav(amfi_code, date)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON fact_transactions(transaction_date)")
    return DATABASE


if __name__ == "__main__":
    print(f"Loaded SQLite database: {load_database()}")