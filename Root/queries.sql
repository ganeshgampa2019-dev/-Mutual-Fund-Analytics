-- 10 Analytical SQL Queries for Mutual Fund Analytics

-- 1. Top 5 funds by AUM
SELECT scheme_name, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month for each scheme
SELECT amfi_code, SUBSTR(date, 1, 7) AS nav_month, AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, nav_month
ORDER BY nav_month;

-- 3. SIP Year-over-Year (or overall monthly) transaction growth
SELECT SUBSTR(transaction_date, 1, 7) AS txn_month, COUNT(*) AS sip_count, SUM(amount_inr) AS total_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY txn_month
ORDER BY txn_month;

-- 4. Total transactions and volume by State
SELECT state, COUNT(*) AS total_transactions, SUM(amount_inr) AS total_volume
FROM fact_transactions
GROUP BY state
ORDER BY total_volume DESC;

-- 5. Funds with expense ratio less than 1%
SELECT scheme_name, expense_ratio_pct, fund_house
FROM fact_performance
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- 6. Top 5 schemes by 1-year returns percentage
SELECT scheme_name, return_1yr_pct
FROM fact_performance
ORDER BY return_1yr_pct DESC
LIMIT 5;

-- 7. Transaction summary by type (Lumpsum, SIP, Redemption)
SELECT transaction_type, COUNT(*) AS total_count, SUM(amount_inr) AS total_volume
FROM fact_transactions
GROUP BY transaction_type;

-- 8. Average annual income of investors grouped by city tier
SELECT city_tier, AVG(annual_income_lakh) AS avg_annual_income_lakh
FROM fact_transactions
GROUP BY city_tier;

-- 9. Top 5 funds with highest Sharpe Ratio
SELECT scheme_name, sharpe_ratio, category
FROM fact_performance
WHERE sharpe_ratio IS NOT NULL
ORDER BY sharpe_ratio DESC
LIMIT 5;

-- 10. Monthly total transaction count across all types
SELECT SUBSTR(transaction_date, 1, 7) AS txn_month, COUNT(*) AS txn_count
FROM fact_transactions
GROUP BY txn_month
ORDER BY txn_month;