from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Bluestock Mutual Fund Analytics", page_icon="📈", layout="wide")

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "processed"
COLORS = {"ink": "#102A43", "blue": "#1261A0", "teal": "#00A6A6", "gold": "#F4B942", "coral": "#E76F51"}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: #102A43; }
[data-testid="stMetricValue"] { color: #1261A0; }
.hero { background: linear-gradient(120deg, #102A43, #1261A0); color: white; padding: 1.5rem 2rem; border-radius: 12px; margin-bottom: 1rem; }
.hero h1 { color: white; margin: 0; }
.hero p { color: #D9F0F0; margin: .35rem 0 0; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    names = {
        "funds": "cleaned_01_fund_master.csv", "nav": "cleaned_02_nav_history.csv",
        "aum": "cleaned_03_aum_by_fund_house.csv", "sip": "cleaned_04_monthly_sip_inflows.csv",
        "category": "cleaned_05_category_inflows.csv", "folios": "cleaned_06_industry_folio_count.csv",
        "performance": "cleaned_07_scheme_performance.csv", "transactions": "cleaned_08_investor_transactions.csv",
        "holdings": "cleaned_09_portfolio_holdings.csv", "benchmark": "cleaned_10_benchmark_indices.csv",
    }
    tables = {key: pd.read_csv(DATA / value) for key, value in names.items()}
    for key in ["nav", "aum", "benchmark"]:
        tables[key]["date"] = pd.to_datetime(tables[key]["date"])
    tables["transactions"]["transaction_date"] = pd.to_datetime(tables["transactions"]["transaction_date"])
    for key in ["sip", "category", "folios"]:
        tables[key]["month"] = pd.to_datetime(tables[key]["month"])
    return tables


def chart_layout(fig, title=None):
    fig.update_layout(title=title, height=360, margin=dict(l=12, r=12, t=48, b=12), template="plotly_white", font=dict(color=COLORS["ink"]))
    return fig


def filters(data, fields):
    selected = {}
    for field, label in fields:
        values = sorted(data[field].dropna().unique().tolist())
        selected[field] = st.sidebar.multiselect(label, values, default=values)
    return selected


def apply_filters(frame, selected):
    for field, values in selected.items():
        frame = frame[frame[field].isin(values)]
    return frame


tables = load_data()
funds = tables["funds"]
performance = tables["performance"].merge(funds[["amfi_code", "sub_category", "benchmark"]], on="amfi_code", how="left")
transactions = tables["transactions"]

st.markdown('<div class="hero"><h1>Bluestock Mutual Fund Analytics</h1><p>Four views of scale, performance, investor behavior, and market momentum | 2022-2025</p></div>', unsafe_allow_html=True)
page = st.sidebar.radio("Dashboard page", ["Industry Overview", "Fund Performance", "Investor Analytics", "SIP & Market Trends"])
st.sidebar.caption("Bluestock Fintech | AMFI-aligned analytics")

if page == "Industry Overview":
    st.header("Industry overview")
    selected = filters(tables["aum"], [("fund_house", "Fund house"), ("date", "AUM date")])
    industry_aum = apply_filters(tables["aum"], selected)
    latest_aum = tables["aum"].query("date == date.max()")
    latest_sip = tables["sip"].iloc[-1]
    latest_folios = tables["folios"].iloc[-1]
    kpis = st.columns(4)
    kpis[0].metric("Total AUM", "₹81L Cr")
    kpis[1].metric("SIP inflows", f"₹{latest_sip.sip_inflow_crore / 1000:.0f}K Cr")
    kpis[2].metric("Folios", f"{latest_folios.total_folios_crore:.2f} Cr")
    kpis[3].metric("Schemes", "1,908")
    left, right = st.columns(2)
    with left:
        aum_trend = industry_aum.groupby("date", as_index=False)["aum_lakh_crore"].sum()
        st.plotly_chart(chart_layout(px.line(aum_trend, x="date", y="aum_lakh_crore", markers=True, labels={"aum_lakh_crore": "AUM (₹ lakh crore)", "date": "Date"}), "Industry AUM trend"), use_container_width=True)
    with right:
        latest_aum = industry_aum.sort_values("aum_lakh_crore", ascending=True).tail(10)
        st.plotly_chart(chart_layout(px.bar(latest_aum, x="aum_lakh_crore", y="fund_house", orientation="h", color="aum_lakh_crore", color_continuous_scale="Teal"), "AUM by AMC (latest)"), use_container_width=True)
    st.caption("Headline KPIs follow the project brief; trend charts use the supplied source tables.")

elif page == "Fund Performance":
    st.header("Fund performance")
    selected = filters(performance, [("fund_house", "Fund house"), ("category", "Category"), ("plan", "Plan")])
    view = apply_filters(performance, selected)
    left, right = st.columns(2)
    with left:
        fig = px.scatter(view, x="return_1yr_pct", y="std_dev_ann_pct", size="aum_crore", color="category", hover_name="scheme_name", hover_data=["fund_house", "sharpe_ratio", "risk_grade"], labels={"return_1yr_pct": "1Y return (%)", "std_dev_ann_pct": "Annualized risk (%)"})
        st.plotly_chart(chart_layout(fig, "Return vs risk"), use_container_width=True)
    with right:
        selected_code = st.selectbox("Drill through to NAV detail", view.amfi_code.tolist(), format_func=lambda code: view.loc[view.amfi_code.eq(code), "scheme_name"].iloc[0])
        nav = tables["nav"].query("amfi_code == @selected_code").sort_values("date")
        benchmark = tables["benchmark"].query("index_name == 'NIFTY50'").sort_values("date")
        nav = nav.assign(normalized=nav.nav / nav.nav.iloc[0] * 100)
        benchmark = benchmark.assign(normalized=benchmark.close_value / benchmark.close_value.iloc[0] * 100)
        fig = go.Figure([go.Scatter(x=nav.date, y=nav.normalized, name="NAV", line=dict(color=COLORS["teal"])), go.Scatter(x=benchmark.date, y=benchmark.normalized, name="NIFTY 50", line=dict(color=COLORS["coral"]))])
        st.plotly_chart(chart_layout(fig, "NAV vs NIFTY 50 (rebased to 100)"), use_container_width=True)
    scorecard = view[["scheme_name", "fund_house", "category", "plan", "return_1yr_pct", "sharpe_ratio", "std_dev_ann_pct", "aum_crore", "morningstar_rating", "risk_grade"]].sort_values("return_1yr_pct", ascending=False)
    st.dataframe(scorecard, use_container_width=True, hide_index=True)

elif page == "Investor Analytics":
    st.header("Investor analytics")
    selected = filters(transactions, [("state", "State"), ("age_group", "Age group"), ("city_tier", "City tier")])
    view = apply_filters(transactions, selected).copy()
    left, right = st.columns(2)
    with left:
        state = view.groupby("state")["amount_inr"].sum().sort_values().rename_axis("state").reset_index(name="amount_inr")
        st.plotly_chart(chart_layout(px.bar(state, x="amount_inr", y="state", orientation="h", labels={"amount_inr": "Amount (₹)", "state": "State"}), "Transaction amount by state"), use_container_width=True)
    with right:
        split = view.groupby("transaction_type", as_index=False)["amount_inr"].sum()
        st.plotly_chart(chart_layout(px.pie(split, names="transaction_type", values="amount_inr", hole=.52, color_discrete_sequence=[COLORS["teal"], COLORS["gold"], COLORS["coral"]]), "Transaction mix"), use_container_width=True)
    left, right = st.columns(2)
    with left:
        age = view.groupby("age_group", as_index=False)["amount_inr"].mean()
        st.plotly_chart(chart_layout(px.bar(age, x="age_group", y="amount_inr", labels={"amount_inr": "Average transaction (₹)"}), "Average amount by age group"), use_container_width=True)
    with right:
        monthly = view.assign(month=view.transaction_date.dt.to_period("M").astype(str)).groupby("month", as_index=False).size()
        st.plotly_chart(chart_layout(px.line(monthly, x="month", y="size", markers=True, labels={"size": "Transactions"}), "Monthly transaction volume"), use_container_width=True)

else:
    st.header("SIP and market trends")
    selected = filters(tables["category"], [("category", "Category"), ("month", "Flow month")])
    sip = tables["sip"].copy()
    category_view = apply_filters(tables["category"], selected)
    nifty = tables["benchmark"].query("index_name == 'NIFTY50'").copy()
    nifty["month"] = nifty.date.dt.to_period("M").dt.to_timestamp()
    nifty = nifty.groupby("month", as_index=False).close_value.last()
    trend = sip.merge(nifty, on="month", how="left")
    fig = go.Figure([go.Bar(x=trend.month, y=trend.sip_inflow_crore, name="SIP inflow (₹ Cr)", marker_color=COLORS["teal"]), go.Scatter(x=trend.month, y=trend.close_value, name="NIFTY 50", yaxis="y2", line=dict(color=COLORS["coral"], width=3))])
    fig.update_layout(yaxis=dict(title="SIP inflow (₹ Cr)"), yaxis2=dict(title="NIFTY 50", overlaying="y", side="right"))
    st.plotly_chart(chart_layout(fig, "SIP inflows and NIFTY 50"), use_container_width=True)
    heat = category_view.pivot(index="category", columns="month", values="net_inflow_crore").fillna(0)
    st.plotly_chart(chart_layout(px.imshow(heat, color_continuous_scale="Tealgrn", aspect="auto", labels={"color": "₹ Cr"}), "Category inflow heatmap"), use_container_width=True)
    top5 = category_view.query("month.dt.month == 3", engine="python").groupby("category")["net_inflow_crore"].sum().nlargest(5).rename_axis("category").reset_index(name="net_inflow_crore")
    st.plotly_chart(chart_layout(px.bar(top5.sort_values(by="net_inflow_crore"), x="net_inflow_crore", y="category", orientation="h", labels={"net_inflow_crore": "Net inflow (₹ Cr)"}), "Top 5 categories by FY25 inflow"), use_container_width=True)