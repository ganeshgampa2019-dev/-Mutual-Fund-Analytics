import numpy as np
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("mutual_funds.db")

print("--- CALCULATING RISK METRICS (Volatility & Returns) ---")

# NAV history lo daily returns calculate chesi volatility (standard deviation) kanukkundam
query = "SELECT amfi_code, date, nav FROM nav_history;"
df = pd.read_sql(query, conn)

# Date column ni datetime lo ki convert cheyali
df["date"] = pd.to_datetime(df["date"])

# Prati fund ki daily percentage returns calculate cheyadam
df["daily_return"] = df.groupby("amfi_code")["nav"].pct_change()

# Volatility (Standard Deviation of returns) and Annualized Volatility (approx sqrt(252))
risk_df = (
    df.groupby("amfi_code")["daily_return"]
    .agg(
        daily_volatility="std",
        mean_daily_return="mean",
    )
    .reset_index()
)

risk_df["annualized_volatility"] = risk_df["daily_volatility"] * np.sqrt(252)
risk_df["annualized_return"] = risk_df["mean_daily_return"] * 252

print("\nTop 5 Funds Risk & Return Summary:")
print(risk_df.head())

conn.close()