# 📊 Capstone Project I - Mutual Fund Analytics: Final Report

## 1. Project Overview
This project focuses on analyzing mutual fund performance, risk metrics, and historical Net Asset Value (NAV) trends using Python, SQLite, and Streamlit. The dataset contains 40 mutual funds across Equity and Debt categories.

---

## 2. Methodology & Tech Stack
* **Language:** Python
* **Database:** SQLite (`mutual_funds.db`)
* **Libraries Used:** Pandas, NumPy, Matplotlib, Seaborn, Streamlit
* **Core Pipeline:**
  1. **Data Ingestion & Cleaning:** Raw CSV datasets cleaned and loaded into relational database tables (`fund_master`, `nav_history`).
  2. **Exploratory Data Analysis (EDA):** Category distributions and NAV range analysis.
  3. **Advanced Risk Analytics:** Daily returns calculation, annualized volatility, annualized returns, and Sharpe Ratio computation.
  4. **Dashboard Development:** Interactive local web application built using Streamlit.

---

## 3. Key Findings & Analytics Summary
* **Category Breakdown:** The dataset consists of **34 Equity Funds** and **6 Debt Funds** (Total: 40 funds).
* **Risk & Return Performance:** 
  * High-growth equity funds exhibited higher annualized returns accompanied by higher volatility.
  * Sharpe ratios were computed assuming a risk-free rate of **6% (0.06)** to evaluate risk-adjusted returns, stored successfully in the `fund_risk_metrics` database table.

---

## 4. Conclusion & Deliverables
All core requirements—from ETL pipelines and SQL storage to automated risk metrics and interactive UI dashboards—have been successfully implemented and tested locally.