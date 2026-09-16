"""Simple transparent fund recommender using risk-adjusted score."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def recommend(category: str | None = None, risk_grade: str | None = None, limit: int = 5) -> pd.DataFrame:
    performance = pd.read_csv(PROCESSED / "cleaned_07_scheme_performance.csv")
    view = performance.copy()
    if category:
        view = view[view["category"].eq(category)]
    if risk_grade:
        view = view[view["risk_grade"].eq(risk_grade)]
    view["recommendation_score"] = view["sharpe_ratio"].rank(pct=True) * 0.5 + view["return_1yr_pct"].rank(pct=True) * 0.3 + (1 - view["std_dev_ann_pct"].rank(pct=True)) * 0.2
    return view.sort_values(["recommendation_score", "sharpe_ratio"], ascending=False).head(limit)


if __name__ == "__main__":
    print(recommend().to_string(index=False))
