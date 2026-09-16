"""Reproducible ETL pipeline for the Bluestock mutual fund project."""
from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOGGER = logging.getLogger(__name__)

FILES = {
    "01_fund_master.csv": "cleaned_01_fund_master.csv",
    "02_nav_history.csv": "cleaned_02_nav_history.csv",
    "03_aum_by_fund_house.csv": "cleaned_03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv": "cleaned_04_monthly_sip_inflows.csv",
    "05_category_inflows.csv": "cleaned_05_category_inflows.csv",
    "06_industry_folio_count.csv": "cleaned_06_industry_folio_count.csv",
    "07_scheme_performance.csv": "cleaned_07_scheme_performance.csv",
    "08_investor_transactions.csv": "cleaned_08_investor_transactions.csv",
    "09_portfolio_holdings.csv": "cleaned_09_portfolio_holdings.csv",
    "10_benchmark_indices.csv": "cleaned_10_benchmark_indices.csv",
}

DATE_COLUMNS = {"date", "month", "transaction_date", "launch_date"}


def clean_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names, dates, duplicate rows, and numeric nulls."""
    frame = frame.copy()
    frame.columns = [column.strip().lower() for column in frame.columns]
    for column in DATE_COLUMNS.intersection(frame.columns):
        frame[column] = pd.to_datetime(frame[column], errors="coerce")
    frame = frame.drop_duplicates().reset_index(drop=True)
    numeric_columns = frame.select_dtypes(include="number").columns
    frame[numeric_columns] = frame[numeric_columns].replace([float("inf"), float("-inf")], pd.NA)
    return frame


def run() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for raw_name, processed_name in FILES.items():
        source = RAW / raw_name
        if not source.exists():
            raise FileNotFoundError(f"Missing required source file: {source}")
        try:
            cleaned = clean_frame(pd.read_csv(source))
            cleaned.to_csv(PROCESSED / processed_name, index=False, date_format="%Y-%m-%d")
            LOGGER.info("%s: %s rows", processed_name, len(cleaned))
        except (pd.errors.ParserError, OSError, ValueError) as error:
            raise RuntimeError(f"Could not process {source}: {error}") from error


if __name__ == "__main__":
    run()
