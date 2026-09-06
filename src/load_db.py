import os
import pandas as pd
from sqlalchemy import create_engine

os.makedirs('database', exist_ok=True)
db_path = os.path.abspath('database/bluestock_mf.db')
engine = create_engine(f'sqlite:///{db_path}')

print(f"Connecting to database at: {db_path}")

# Load and explicitly check if files exist and have rows
nav_file = 'data/processed/clean_nav_history.csv'
if os.path.exists(nav_file):
    df_nav = pd.read_csv(nav_file)
    print(f"NAV rows loaded: {len(df_nav)}")
    df_nav.to_sql('fact_nav', engine, if_exists='replace', index=False)
else:
    print(f"Error: {nav_file} not found!")

perf_file = 'data/processed/clean_scheme_performance.csv'
if os.path.exists(perf_file):
    df_perf = pd.read_csv(perf_file)
    print(f"Performance rows loaded: {len(df_perf)}")
    df_perf.to_sql('fact_performance', engine, if_exists='replace', index=False)
else:
    print(f"Error: {perf_file} not found!")

trans_file = 'data/processed/clean_investor_transactions.csv'
if os.path.exists(trans_file):
    df_trans = pd.read_csv(trans_file)
    print(f"Transaction rows loaded: {len(df_trans)}")
    df_trans.to_sql('fact_transactions', engine, if_exists='replace', index=False)
else:
    print(f"Error: {trans_file} not found!")

# Verify tables inside database
with engine.connect() as conn:
    result = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    print("\nTables currently in database:")
    print(result)

print("\nDatabase loading script finished!")