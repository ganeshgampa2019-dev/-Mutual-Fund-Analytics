import os
import sqlite3
import pandas as pd

# SQLite connection
db_path = "mutual_funds.db"
conn = sqlite3.connect(db_path)

RAW_DIR = "data/raw/"

try:
  # 1. Fund Master table load & clean
  df_fund = pd.read_csv(os.path.join(RAW_DIR, "01_fund_master.csv"))
  df_fund.columns = df_fund.columns.str.lower().str.replace(" ", "_")
  df_fund.to_sql("fund_master", conn, if_exists="replace", index=False)

  # 2. NAV History table load & clean
  df_nav = pd.read_csv(os.path.join(RAW_DIR, "02_nav_history.csv"))
  df_nav.columns = df_nav.columns.str.lower().str.replace(" ", "_")
  df_nav.to_sql("nav_history", conn, if_exists="replace", index=False)

  print("Database tables created and data loaded successfully!")

except Exception as e:
  print("Error:", e)

finally:
  conn.close()