import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Mutual Fund Analytics Dashboard", layout="wide"
)

st.title("📊 Mutual Fund Analytics & Risk Dashboard")
st.markdown("Capstone Project Dashboard built with Streamlit and SQLite.")

# Connect to database
conn = sqlite3.connect("mutual_funds.db")

# 1. Load Fund Master summary
df_fund = pd.read_sql("SELECT * FROM fund_master;", conn)
df_risk = pd.read_sql("SELECT * FROM fund_risk_metrics;", conn)

conn.close()

# Sidebar filters
st.sidebar.header("Filter Options")
selected_category = st.sidebar.selectbox(
    "Select Category", df_fund["category"].unique()
)

filtered_funds = df_fund[df_fund["category"] == selected_category]

st.subheader(f"Funds in Category: {selected_category}")
st.dataframe(filtered_funds[["amfi_code", "fund_house", "scheme_name"]])

# Display Risk Metrics Summary
st.subheader("📈 Risk & Sharpe Ratio Metrics Overview")
st.dataframe(df_risk.head(10))