-- Reusable validation and reporting queries
SELECT COUNT(*) AS schemes FROM dim_fund;
SELECT transaction_type, COUNT(*) AS transactions, SUM(amount_inr) AS amount_inr FROM fact_transactions GROUP BY transaction_type;
SELECT scheme_name, return_1yr_pct, sharpe_ratio, beta FROM fact_performance ORDER BY sharpe_ratio DESC LIMIT 10;
SELECT substr(transaction_date, 1, 7) AS month, COUNT(*) AS transaction_count FROM fact_transactions GROUP BY month ORDER BY month;
