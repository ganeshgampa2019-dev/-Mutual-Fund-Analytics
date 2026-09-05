import os
import pandas as pd

# Files unna path
RAW_DIR = "data/raw/"

# Check a few key files
files = ["01_fund_master.csv", "02_nav_history.csv", "03_aum_by_fund_house.csv"]

for file in files:
  path = os.path.join(RAW_DIR, file)
  if os.path.exists(path):
    df = pd.read_csv(path)
    print(f"Loaded {file} Successfully! Shape: {df.shape}")
  else:
    print(f"File missing: {file}")