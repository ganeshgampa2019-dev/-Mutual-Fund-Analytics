"""Backward-compatible entry point for the canonical ETL pipeline."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
from scripts.etl_pipeline import run


if __name__ == "__main__":
    run()