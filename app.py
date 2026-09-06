import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Mutual Fund Analytics Dashboard", layout="wide")

st.title("📊 Capstone Project I - Mutual Fund Analytics")
st.markdown("Bluestock Fintech - Mutual Fund Data Insights & Portfolio Dashboard")

# Connect to database
conn = sqlite3.connect('database/bluestock_mf.db')

# Sidebar selection
st.sidebar.header("Navigation")
option = st.sidebar.selectbox("Choose View", ["Top Assets by AUM", "Transaction Summary", "Monthly Trends", "Top Returns"])

if option == "Top Assets by AUM":
    st.subheader("Top 5 Funds by AUM (Crores)")
    query = """
    SELECT scheme_name, aum_crore
    FROM fact_performance
    ORDER BY aum_crore DESC
    LIMIT 5;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index('scheme_name')['aum_crore'])

elif option == "Transaction Summary":
    st.subheader("Investor Transactions Overview")
    query = """
    SELECT transaction_type, COUNT(*) AS total_count, SUM(amount_inr) AS total_volume
    FROM fact_transactions
    GROUP BY transaction_type;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index('transaction_type')['total_volume'])

elif option == "Monthly Trends":
    st.subheader("Monthly Transaction Volume Trends")
    query = """
    SELECT SUBSTR(transaction_date, 1, 7) AS txn_month, COUNT(*) AS txn_count
    FROM fact_transactions
    GROUP BY txn_month
    ORDER BY txn_month;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df, use_container_width=True)
    st.line_chart(df.set_index('txn_month')['txn_count'])

elif option == "Top Returns":
    st.subheader("Top Schemes by 1-Year Returns (%)")
    query = """
    SELECT scheme_name, return_1yr_pct
    FROM fact_performance
    ORDER BY return_1yr_pct DESC
    LIMIT 5;
    """
    df = pd.read_sql(query, conn)
    st.dataframe(df, use_container_width=True)

conn.close()