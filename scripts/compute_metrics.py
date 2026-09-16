"""Compute reproducible fund risk and return metrics from NAV history."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "data" / "fund_metrics.csv"
TRADING_DAYS = 252


def compute_metrics() -> pd.DataFrame:
    nav = pd.read_csv(PROCESSED / "cleaned_02_nav_history.csv", parse_dates=["date"])
    benchmark = pd.read_csv(PROCESSED / "cleaned_10_benchmark_indices.csv", parse_dates=["date"])
    nav = nav.sort_values(["amfi_code", "date"])
    benchmark = benchmark.sort_values("date")
    benchmark = benchmark[benchmark["index_name"].eq("NIFTY50")]
    benchmark_series = benchmark.drop_duplicates("date").set_index("date")["close_value"].pct_change()
    rows = []
    for amfi_code, frame in nav.groupby("amfi_code", sort=False):
        prices = frame.set_index("date")["nav"].sort_index()
        daily_returns = prices.pct_change().dropna()
        aligned = daily_returns.to_frame("fund").join(benchmark_series.rename("benchmark"), how="inner").dropna()
        if daily_returns.empty:
            continue
        years = len(daily_returns) / TRADING_DAYS
        total_return = prices.iloc[-1] / prices.iloc[0] - 1
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else np.nan
        volatility = daily_returns.std(ddof=1) * np.sqrt(TRADING_DAYS)
        downside = daily_returns.where(daily_returns < 0, 0).std(ddof=1) * np.sqrt(TRADING_DAYS)
        excess = daily_returns - 0.06 / TRADING_DAYS
        sharpe = excess.mean() / daily_returns.std(ddof=1) * np.sqrt(TRADING_DAYS) if daily_returns.std(ddof=1) else np.nan
        beta = aligned["fund"].cov(aligned["benchmark"]) / aligned["benchmark"].var() if len(aligned) > 1 else np.nan
        cumulative = (1 + daily_returns).cumprod()
        drawdown = cumulative / cumulative.cummax() - 1
        var_95 = daily_returns.quantile(0.05)
        rows.append({"amfi_code": amfi_code, "annualized_return_pct": annual_return * 100, "volatility_pct": volatility * 100, "downside_deviation_pct": downside * 100, "sharpe_ratio": sharpe, "beta": beta, "max_drawdown_pct": drawdown.min() * 100, "var_95_daily_pct": var_95 * 100, "observations": len(daily_returns)})
    result = pd.DataFrame(rows)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT, index=False)
    return result


if __name__ == "__main__":
    print(compute_metrics().head().to_string(index=False))
