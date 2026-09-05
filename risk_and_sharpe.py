import numpy as np
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("mutual_funds.db")

# Fetch NAV history data
query = "SELECT amfi_code, date, nav FROM nav_history;"
df = pd.read_sql(query, conn)
df["date"] = pd.to_datetime(df["date"])

# Calculate daily returns
df["daily_return"] = df.groupby("amfi_code")["nav"].pct_change()

# Calculate Annualized Return and Volatility
metrics = (
    df.groupby("amfi_code")["daily_return"]
    .agg(
        mean_daily_return="mean",
        daily_volatility="std",
    )
    .reset_index()
)

metrics["annualized_return"] = metrics["mean_daily_return"] * 252
metrics["annualized_volatility"] = metrics["daily_volatility"] * np.sqrt(252)

# Assuming Risk-Free Rate = 6% (0.06) for Sharpe Ratio calculation
risk_free_rate = 0.06
metrics["sharpe_ratio"] = (
    metrics["annualized_return"] - risk_free_rate
) / metrics["annualized_volatility"]

print("--- ADVANCED RISK & SHARPE RATIO METRICS ---")
print(metrics.head(10))

# Save results to a new table in SQLite
metrics.to_sql("fund_risk_metrics", conn, if_exists="replace", index=False)
print("\nSaved risk metrics into database table 'fund_risk_metrics' successfully!")

conn.close()