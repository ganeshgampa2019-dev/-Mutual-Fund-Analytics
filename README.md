# Bluestock Mutual Fund Capstone

This project is a reproducible mutual fund analytics workflow covering ETL, SQLite, exploratory analysis, risk metrics, investor cohorts, recommendations, and a four-page interactive dashboard.

## Setup

```powershell
python -m pip install -r requirements.txt
python scripts/run_pipeline.py
```

The master runner rebuilds cleaned CSVs, `data/fund_metrics.csv`, `database/bluestock_mf.db`, dashboard PNG/PDF exports, `reports/Final_Report.pdf`, and `reports/Bluestock_MF_Presentation.pptx`.

## Open the dashboard

```powershell
streamlit run app.py
```

Pages include Industry Overview, Fund Performance, Investor Analytics, and SIP & Market Trends. Each page has interactive filters; Fund Performance includes NAV versus NIFTY50 and a scorecard.

## Dataset descriptions

| Dataset | Description |
| --- | --- |
| `01_fund_master` | Scheme identity, AMC, category, plan, benchmark, and fund metadata |
| `02_nav_history` | Daily NAV observations by AMFI code |
| `03_aum_by_fund_house` | Fund-house AUM trend in lakh crore |
| `04_monthly_sip_inflows` | Monthly SIP inflow in crore |
| `05_category_inflows` | Category-level monthly net inflow in crore |
| `06_industry_folio_count` | Monthly industry folio count in crore |
| `07_scheme_performance` | Scheme returns, risk, Sharpe, Beta, AUM, and ratings |
| `08_investor_transactions` | Investor transaction amount, type, geography, age, and city tier |
| `09_portfolio_holdings` | Scheme holdings and portfolio weights |
| `10_benchmark_indices` | Daily benchmark index levels, including NIFTY50 |

## Project map

- ETL and analytics: `scripts/`
- Notebooks: `notebooks/01_data_ingestion.ipynb` through `05_advanced_analytics.ipynb`
- Database: `database/bluestock_mf.db`, `sql/schema.sql`, `sql/queries.sql`
- Dashboard: `app.py` and `bluestock_mf_dashboard_project/`
- Final report and slides: `reports/Final_Report.pdf`, `reports/Bluestock_MF_Presentation.pptx`

SQLite files are ignored by Git; `sql/schema.sql` is the shareable database definition. The recommender is analytical decision support, not financial advice.
