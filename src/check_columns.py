"""Inspect SQLite table columns for validation workflows."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


def performance_columns() -> list[str]:
	"""Return the columns in the fact_performance table."""
	with sqlite3.connect(ROOT / "database" / "bluestock_mf.db") as connection:
		return [row[1] for row in connection.execute("PRAGMA table_info(fact_performance)")]


if __name__ == "__main__":
	print(performance_columns())