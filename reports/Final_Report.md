# Bluestock Mutual Fund Analytics Report

## Executive summary
This project creates a reproducible mutual fund analytics workflow from raw industry, scheme, NAV, benchmark, and investor transaction data. The dashboard presents scale, performance, investor behavior, and SIP/market trends.

## Data and method
Raw CSV files are normalized by `scripts/etl_pipeline.py`. The SQLite loader imports all cleaned tables. Fund metrics use daily NAV returns, 252 trading days, a 6% annual risk-free rate, aligned benchmark returns, maximum drawdown, and historical 95% daily VaR.

## Key analysis areas
- Industry AUM, SIP inflows, folios, and AMC concentration.
- Fund return versus risk, risk-adjusted scorecard, and NAV versus NIFTY 50.
- Transaction mix, state distribution, age-group SIP behavior, and monthly volume.
- Category flows, FY25 leaders, and SIP inflow versus NIFTY 50.

## Caveats
The recommender is an explainable ranking aid, not investment advice. Historical returns and VaR do not guarantee future performance. A native Power BI `.pbix` requires Power BI Desktop; the supplied Streamlit app is the interactive alternative and the exporter produces PDF/PNG deliverables.

## Deliverables
See `notebooks/`, `data/fund_metrics.csv`, `database/bluestock_mf.db`, `bluestock_mf_dashboard_project/`, and `app.py`.
