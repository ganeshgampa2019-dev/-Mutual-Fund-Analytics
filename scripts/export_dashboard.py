from pathlib import Path
import shutil

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
DELIVERY = ROOT / "bluestock_mf_dashboard_project"
SOURCE_OUTPUT = DELIVERY / "1_Source_File"
REPORT_OUTPUT = DELIVERY / "2_Exported_Reports"
SCREENSHOT_OUTPUT = REPORT_OUTPUT / "Page_Screenshots"
DATA_OUTPUT = DELIVERY / "3_Datasets"
for output_dir in [SOURCE_OUTPUT, REPORT_OUTPUT, SCREENSHOT_OUTPUT, DATA_OUTPUT]:
    output_dir.mkdir(parents=True, exist_ok=True)
PDF_OUTPUT = REPORT_OUTPUT / "Dashboard.pdf"

aum = pd.read_csv(DATA / "cleaned_03_aum_by_fund_house.csv", parse_dates=["date"])
sip = pd.read_csv(DATA / "cleaned_04_monthly_sip_inflows.csv", parse_dates=["month"])
folios = pd.read_csv(DATA / "cleaned_06_industry_folio_count.csv", parse_dates=["month"])
category = pd.read_csv(DATA / "cleaned_05_category_inflows.csv", parse_dates=["month"])
performance = pd.read_csv(DATA / "cleaned_07_scheme_performance.csv")
transactions = pd.read_csv(DATA / "cleaned_08_investor_transactions.csv", parse_dates=["transaction_date"])

plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold", "figure.facecolor": "#F5F8FA"})
COLORS = {"ink": "#102A43", "blue": "#1261A0", "teal": "#00A6A6", "gold": "#F4B942", "coral": "#E76F51"}


def page(title):
    fig, axes = plt.subplots(2, 2, figsize=(16, 9), constrained_layout=True)
    fig.suptitle(title, fontsize=22, color=COLORS["ink"])
    fig.text(.985, .975, "BLUESTOCK FINTECH", ha="right", va="top", fontsize=10, weight="bold", color=COLORS["blue"])
    return fig, axes.ravel()


fig, axes = page("Bluestock Mutual Fund Analytics | Industry Overview")
trend = aum.groupby("date", as_index=False).aum_lakh_crore.sum()
axes[0].plot(trend.date, trend.aum_lakh_crore, color="#1261A0", linewidth=3)
axes[0].set_title("Industry AUM trend")
latest = aum.query("date == date.max()").sort_values("aum_lakh_crore")
axes[1].barh(latest.fund_house, latest.aum_lakh_crore, color="#00A6A6")
axes[1].set_title("AUM by AMC")
axes[2].plot(folios.month, folios.total_folios_crore, color="#F4B942", linewidth=3)
axes[2].set_title("Folios (Cr)")
axes[3].axis("off")
axes[3].text(.1, .65, "₹81L Cr\nTotal AUM", fontsize=22, color="#1261A0", weight="bold")
axes[3].text(.1, .3, "₹31K Cr SIP | 26.12 Cr Folios | 1,908 Schemes", fontsize=12)
fig.savefig(SCREENSHOT_OUTPUT / "Page_1_Industry_Overview.png", dpi=160)
plt.close(fig)

fig, axes = page("Bluestock Mutual Fund Analytics | Fund Performance")
axes[0].scatter(performance.return_1yr_pct, performance.std_dev_ann_pct, s=performance.aum_crore / 100, c=performance.sharpe_ratio, cmap="viridis", alpha=.8)
axes[0].set(xlabel="1Y return (%)", ylabel="Risk / StdDev (%)", title="Return vs risk")
axes[1].barh(performance.nlargest(10, "return_1yr_pct").scheme_name, performance.nlargest(10, "return_1yr_pct").return_1yr_pct, color="#1261A0")
axes[1].set_title("Top funds by 1Y return")
scorecard = performance.nlargest(8, "return_1yr_pct")[["scheme_name", "return_1yr_pct", "sharpe_ratio"]].copy()
scorecard["return_1yr_pct"] = scorecard["return_1yr_pct"].map(lambda value: f"{value:.1f}%")
scorecard["sharpe_ratio"] = scorecard["sharpe_ratio"].map(lambda value: f"{value:.2f}")
axes[2].axis("off")
axes[2].set_title("Fund scorecard (top 8)")
axes[2].table(cellText=scorecard.values, colLabels=scorecard.columns, loc="center", cellLoc="left")
axes[3].axis("off")
selected_code = performance.nlargest(1, "return_1yr_pct").amfi_code.iloc[0]
nav_detail = pd.read_csv(DATA / "cleaned_02_nav_history.csv", parse_dates=["date"])
nav_detail = nav_detail.query("amfi_code == @selected_code").sort_values("date")
benchmark = pd.read_csv(DATA / "cleaned_10_benchmark_indices.csv", parse_dates=["date"])
benchmark = benchmark[benchmark["index_name"].eq("NIFTY50")].sort_values("date")
nav_detail["rebased"] = nav_detail.nav / nav_detail.nav.iloc[0] * 100
benchmark["rebased"] = benchmark.close_value / benchmark.close_value.iloc[0] * 100
axes[3].plot(nav_detail.date, nav_detail.rebased, label="NAV", color=COLORS["teal"], linewidth=2)
axes[3].plot(benchmark.date, benchmark.rebased, label="NIFTY 50", color=COLORS["coral"], linewidth=2)
axes[3].set_title("NAV vs benchmark (rebased to 100)")
axes[3].legend()
fig.savefig(SCREENSHOT_OUTPUT / "Page_2_Fund_Performance.png", dpi=160)
plt.close(fig)

fig, axes = page("Bluestock Mutual Fund Analytics | Investor Analytics")
state = transactions.groupby("state").amount_inr.sum().sort_values()
axes[0].barh(state.index, state.to_numpy(dtype=float) / 1e7, color="#00A6A6")
axes[0].set_title("Transaction amount by state (₹ Cr)")
axes[1].pie(transactions.groupby("transaction_type").amount_inr.sum(), labels=None, autopct="%1.0f%%", colors=["#00A6A6", "#F4B942", "#E76F51"])
axes[1].legend(transactions.transaction_type.unique(), loc="lower center")
axes[1].set_title("Transaction mix")
age = transactions.query("transaction_type == 'SIP'").groupby("age_group").amount_inr.mean()
axes[2].bar(age.index, age.to_numpy(dtype=float) / 1e3, color="#F4B942")
axes[2].set_title("Average SIP amount by age group (₹K)")
monthly = transactions.assign(month=transactions.transaction_date.dt.to_period("M").astype(str)).groupby("month").size()
axes[3].plot(monthly.index, monthly.values, color="#E76F51")
axes[3].tick_params(axis="x", rotation=45)
axes[3].set_title("Monthly transaction volume")
fig.savefig(SCREENSHOT_OUTPUT / "Page_3_Investor_Analytics.png", dpi=160)
plt.close(fig)

fig, axes = page("Bluestock Mutual Fund Analytics | SIP and Market Trends")
market = pd.read_csv(DATA / "cleaned_10_benchmark_indices.csv", parse_dates=["date"])
market = market[market["index_name"].eq("NIFTY50")]
market["month"] = market.date.dt.to_period("M").dt.to_timestamp()
market = market.groupby("month", as_index=False).close_value.last()
dual = sip.merge(market, on="month", how="left")
axes[0].bar(dual.month, dual.sip_inflow_crore, color="#00A6A6", label="SIP inflow (₹ Cr)")
axis2 = axes[0].twinx()
axis2.plot(dual.month, dual.close_value, color="#E76F51", linewidth=2, label="NIFTY 50")
axes[0].set_title("SIP inflows and NIFTY 50")
axes[0].set_ylabel("SIP inflow (₹ Cr)")
axis2.set_ylabel("NIFTY 50")
heat = category.pivot(index="category", columns="month", values="net_inflow_crore").fillna(0)
axes[1].imshow(heat, aspect="auto", cmap="YlGnBu")
axes[1].set_yticks(range(len(heat.index)), heat.index, fontsize=7)
axes[1].set_title("Category inflow heatmap")
top5 = category.query("month.dt.month == 3", engine="python").groupby("category").net_inflow_crore.sum().nlargest(5).sort_values()
axes[2].barh(top5.index, top5.values, color="#1261A0")
axes[2].set_title("Top 5 FY25 categories")
axes[3].axis("off")
fig.savefig(SCREENSHOT_OUTPUT / "Page_4_SIP_Market_Trends.png", dpi=160)
plt.close(fig)

with PdfPages(PDF_OUTPUT) as pdf:
    for filename in ["Page_1_Industry_Overview.png", "Page_2_Fund_Performance.png", "Page_3_Investor_Analytics.png", "Page_4_SIP_Market_Trends.png"]:
        image = plt.imread(SCREENSHOT_OUTPUT / filename)
        figure = plt.figure(figsize=(16, 9))
        plt.imshow(image)
        plt.axis("off")
        pdf.savefig(figure, bbox_inches="tight")
        plt.close(figure)

for dataset in DATA.glob("*.csv"):
    shutil.copy2(dataset, DATA_OUTPUT / dataset.name)

(SOURCE_OUTPUT / "README.md").write_text(
    "# Bluestock Power BI source\n\n"
    "The cleaned CSV model inputs are in `../3_Datasets`. Open `app.py` for the interactive four-page dashboard.\n\n"
    "A native `.pbix` file must be saved from Power BI Desktop after importing these CSVs; this Python environment cannot create a valid Power BI Desktop binary.\n",
    encoding="utf-8",
)

print(f"Created four PNG pages and {PDF_OUTPUT}")