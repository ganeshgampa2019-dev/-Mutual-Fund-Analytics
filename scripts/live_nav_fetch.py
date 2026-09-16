"""Optional weekday NAV refresh helper for mfapi.in.

Usage: python scripts/live_nav_fetch.py --scheme 119551
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def fetch_nav(scheme_code: str) -> pd.DataFrame:
    response = requests.get(f"https://api.mfapi.in/mf/{scheme_code}", timeout=30)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "SUCCESS" or not payload.get("data"):
        raise ValueError(f"No NAV data returned for scheme {scheme_code}")
    return pd.DataFrame(payload["data"]).rename(columns={"date": "date", "nav": "nav"})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheme", required=True)
    args = parser.parse_args()
    output = RAW / f"nav_{args.scheme}.csv"
    frame = fetch_nav(args.scheme)
    frame.to_csv(output, index=False)
    print(f"Saved {len(frame)} NAV observations to {output}")


if __name__ == "__main__":
    main()
