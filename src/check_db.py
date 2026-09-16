"""Inspect the tables available in the project SQLite database."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


def table_names() -> list[str]:
	"""Return SQLite table names in creation order."""
	with sqlite3.connect(ROOT / "database" / "bluestock_mf.db") as connection:
		return [row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]


if __name__ == "__main__":
	print(table_names())