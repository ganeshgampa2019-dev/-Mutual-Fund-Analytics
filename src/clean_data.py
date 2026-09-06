import os
import pandas as pd

# Directories create cheyadam
os.makedirs('data/processed', exist_ok=True)

print("Starting Data Cleaning process...")

# 1. Cleaning NAV History
nav_path = 'data/raw/02_nav_history.csv'
if os.path.exists(nav_path):
    df_nav = pd.read_csv(nav_path)
    df_nav['date'] = pd.to_datetime(df_nav['date'], errors='coerce')
    df_nav = df_nav.dropna(subset=['date', 'nav'])
    df_nav = df_nav[df_nav['nav'] > 0]
    df_nav = df_nav.drop_duplicates()
    df_nav.to_csv('data/processed/clean_nav_history.csv', index=False)
    print("NAV history cleaned successfully.")

# 2. Cleaning Scheme Performance
perf_path = 'data/raw/07_scheme_performance.csv'
if os.path.exists(perf_path):
    df_perf = pd.read_csv(perf_path)
    df_perf = df_perf.drop_duplicates()
    df_perf.to_csv('data/processed/clean_scheme_performance.csv', index=False)
    print("Scheme performance cleaned successfully.")

# 3. Cleaning Investor Transactions
trans_path = 'data/raw/08_investor_transactions.csv'
if os.path.exists(trans_path):
    df_trans = pd.read_csv(trans_path)
    df_trans['transaction_date'] = pd.to_datetime(df_trans['transaction_date'], errors='coerce')
    df_trans = df_trans.dropna(subset=['transaction_date'])
    df_trans = df_trans.drop_duplicates()
    df_trans.to_csv('data/processed/clean_investor_transactions.csv', index=False)
    print("Investor transactions cleaned successfully.")

print("Data cleaning completed! Processed files are saved in data/processed/")