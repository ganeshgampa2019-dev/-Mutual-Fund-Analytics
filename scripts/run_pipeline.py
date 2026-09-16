"""Run the complete Bluestock capstone pipeline in dependency order."""
from __future__ import annotations

import subprocess

from compute_metrics import compute_metrics
from etl_pipeline import run as run_etl
from generate_final_deliverables import generate
from recommender import recommend

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from load_db import load_database


def run_pipeline() -> None:
    """Build cleaned data, analytics, database, dashboard, report, and slides."""
    run_etl()
    metrics = compute_metrics()
    load_database()
    subprocess.run([sys.executable, str(Path(__file__).with_name("export_dashboard.py"))], check=True)
    report, presentation = generate()
    print(f"Pipeline complete: {len(metrics)} fund metric rows")
    print(f"Report: {report}")
    print(f"Presentation: {presentation}")
    print(f"Recommendations available: {len(recommend())}")


if __name__ == "__main__":
    run_pipeline()
