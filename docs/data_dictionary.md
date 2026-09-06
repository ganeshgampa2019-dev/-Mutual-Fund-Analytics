# Data Dictionary - Mutual Fund Analytics

This document provides detailed descriptions of all tables, columns, data types, and business definitions used in the SQLite star schema (`bluestock_mf.db`).

---

## 1. dim_fund
Stores dimension details for each mutual fund scheme.

| Column Name | Data Type | Description | Source / Reference |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER (PK) | Unique AMFI identification code for the scheme | AMFI Master |
| `scheme_name` | TEXT | Full official name of the mutual fund scheme | Scheme Master |
| `fund_house` | TEXT | Asset Management Company (AMC) name | Fund House Master |
| `category` | TEXT | Fund category (e.g., Small Cap, Large Cap, Hybrid) | SEBI Categorization |
| `plan` | TEXT | Investment plan type (e.g., Regular, Direct) | Scheme Master |

---

## 2. dim_date
Stores date attributes for time-series analysis and aggregations.

| Column Name | Data Type | Description | Source / Reference |
| :--- | :--- | :--- | :--- |
| `date` | TEXT (PK) | Calendar date in `YYYY-MM-DD` format | Standard Calendar |
| `year` | INTEGER | Calendar year extracted from date | Derived |
| `month` | INTEGER | Calendar month (1–12) | Derived |
| `day` | INTEGER | Day of the month (1–31) | Derived |
| `quarter` | INTEGER | Financial/Calendar quarter (1–4) | Derived |

---

## 3. fact_nav
Stores daily Net Asset Value (NAV) records for all schemes.

| Column Name | Data Type | Description | Source / Reference |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER (FK) | Reference to `dim_fund(amfi_code)` | NAV Feed |
| `date` | TEXT (FK) | Reference to `dim_date(date)` | NAV Feed |
| `nav` | REAL | Net Asset Value amount in INR (> 0) | NAV Feed |

---

## 4. fact_performance
Stores scheme performance metrics, risk ratios, and asset under management.

| Column Name | Data Type | Description | Source / Reference |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER (PK/FK) | Reference to `dim_fund(amfi_code)` | Performance Sheet |
| `scheme_name` | TEXT | Name of the scheme | Performance Sheet |
| `fund_house` | TEXT | AMC name | Performance Sheet |
| `category` | TEXT | Scheme category | Performance Sheet |
| `plan` | TEXT | Scheme plan type | Performance Sheet |
| `return_1yr_pct` | REAL | 1-Year trailing annualized return percentage | Calculated |
| `return_3yr_pct` | REAL | 3-Year trailing annualized return percentage | Calculated |
| `return_5yr_pct` | REAL | 5-Year trailing annualized return percentage | Calculated |
| `benchmark_3yr_pct`| REAL | Benchmark 3-year return percentage | Benchmark Feed |
| `alpha` | REAL | Scheme alpha (excess return over benchmark) | Risk Metrics |
| `beta` | REAL | Scheme beta (volatility relative to market) | Risk Metrics |
| `sharpe_ratio` | REAL | Risk-adjusted return metric | Risk Metrics |
| `sortino_ratio` | REAL | Downside risk-adjusted return metric | Risk Metrics |
| `std_dev_ann_pct` | REAL | Annualized standard deviation percentage | Risk Metrics |
| `max_drawdown_pct` | REAL | Maximum peak-to-trough decline percentage | Risk Metrics |
| `aum_crore` | REAL | Assets Under Management in Crores INR | Fund House Data |
| `expense_ratio_pct`| REAL | Annual scheme expense ratio percentage (0.1% – 2.5%) | Financial Reports |
| `morningstar_rating`| INTEGER | Morningstar rating (1 to 5 stars) | Morningstar |
| `risk_grade` | TEXT | Assigned risk level (e.g., Moderately High, High) | Risk Analysis |

---

## 5. fact_transactions
Stores investor-level transaction history.

| Column Name | Data Type | Description | Source / Reference |
| :--- | :--- | :--- | :--- |
| `transaction_id` | INTEGER (PK) | Auto-increment unique identifier for each transaction | Transaction Log |
| `investor_id` | TEXT | Unique identifier of the investor | Investor Database |
| `transaction_date`| TEXT | Date when the transaction took place (`YYYY-MM-DD`) | Transaction Log |
| `amfi_code` | INTEGER (FK) | Reference to `dim_fund(amfi_code)` | Transaction Log |
| `transaction_type`| TEXT | Type of transaction (`SIP`, `Lumpsum`, `Redemption`) | Standardized Enum |
| `amount_inr` | REAL | Total transaction amount in INR (> 0) | Transaction Log |
| `state` | TEXT | Indian state of the investor | Investor Profile |
| `city` | TEXT | City of the investor | Investor Profile |
| `city_tier` | TEXT | Classification of city tier (Tier 1, Tier 2, Tier 3) | Demographic Data |
| `age_group` | TEXT | Age bracket of the investor (e.g., 25-35, 36-50) | Investor Profile |
| `gender` | TEXT | Gender of the investor | Investor Profile |
| `annual_income_lakh`| REAL | Annual income of the investor in Lakhs INR | Investor Profile |
| `payment_mode` | TEXT | Payment method used (e.g., UPI, NetBanking, Mandate)| Transaction Log |
| `kyc_status` | TEXT | KYC verification status (`Verified`, `Pending`) | Compliance System |

---

## 6. fact_aum
Stores monthly asset under management history for trend analysis.

| Column Name | Data Type | Description | Source / Reference |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER (FK) | Reference to `dim_fund(amfi_code)` | AUM Records |
| `month` | TEXT | Month string in `YYYY-MM` format | AUM Records |
| `aum_crore` | REAL | Total AUM amount in Crores INR | AUM Records |