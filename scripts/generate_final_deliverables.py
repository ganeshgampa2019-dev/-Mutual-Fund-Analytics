"""Generate the final 16-page PDF report and 12-slide presentation."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
SCREENSHOTS = ROOT / "bluestock_mf_dashboard_project" / "2_Exported_Reports" / "Page_Screenshots"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)
BLUE = "1261A0"
INK = "102A43"
TEAL = "00A6A6"


def load_context() -> dict[str, pd.DataFrame]:
    return {
        "aum": pd.read_csv(DATA / "cleaned_03_aum_by_fund_house.csv", parse_dates=["date"]),
        "performance": pd.read_csv(DATA / "cleaned_07_scheme_performance.csv"),
        "transactions": pd.read_csv(DATA / "cleaned_08_investor_transactions.csv", parse_dates=["transaction_date"]),
        "metrics": pd.read_csv(ROOT / "data" / "fund_metrics.csv"),
        "category": pd.read_csv(DATA / "cleaned_05_category_inflows.csv", parse_dates=["month"]),
    }


def text_page(pdf: PdfPages, title: str, paragraphs: list[str]) -> None:
    figure = plt.figure(figsize=(8.27, 11.69), facecolor="#F5F8FA")
    figure.text(0.08, 0.93, title, fontsize=24, weight="bold", color=f"#{INK}")
    y = 0.85
    for paragraph in paragraphs:
        figure.text(0.08, y, paragraph, fontsize=12, color=f"#{INK}", va="top", wrap=True)
        y -= 0.12 if len(paragraph) < 220 else 0.18
    figure.text(0.08, 0.04, "Bluestock FinTech | Mutual Fund Analytics Capstone", fontsize=9, color=f"#{BLUE}")
    pdf.savefig(figure, bbox_inches="tight")
    plt.close(figure)


def image_page(pdf: PdfPages, path: Path, title: str) -> None:
    figure = plt.figure(figsize=(16, 9), facecolor="#F5F8FA")
    figure.suptitle(title, fontsize=20, weight="bold", color=f"#{INK}")
    image = plt.imread(path)
    axis = figure.add_axes([0.04, 0.05, 0.92, 0.86])
    axis.imshow(image)
    axis.axis("off")
    pdf.savefig(figure, bbox_inches="tight")
    plt.close(figure)


def code_page(pdf: PdfPages, title: str, code: str, explanation: str) -> None:
    figure = plt.figure(figsize=(8.27, 11.69), facecolor="#F5F8FA")
    figure.text(0.08, 0.93, title, fontsize=22, weight="bold", color=f"#{INK}")
    figure.text(0.08, 0.86, explanation, fontsize=10.5, color=f"#{INK}", va="top", wrap=True)
    figure.text(0.08, 0.78, code, fontsize=8.4, color="#183B56", va="top", family="monospace", linespacing=1.35)
    figure.text(0.08, 0.04, "Bluestock FinTech | Mutual Fund Analytics Capstone", fontsize=9, color=f"#{BLUE}")
    pdf.savefig(figure, bbox_inches="tight")
    plt.close(figure)


def generate_pdf_legacy(context: dict[str, pd.DataFrame]) -> Path:
    output = REPORTS / "Final_Report.pdf"
    aum = context["aum"]
    performance = context["performance"]
    transactions = context["transactions"]
    metrics = context["metrics"]
    top_fund = performance.nlargest(1, "return_1yr_pct").iloc[0]
    top_house = aum.groupby("fund_house").aum_lakh_crore.max().idxmax()
    with PdfPages(output) as pdf:
        text_page(pdf, "Bluestock Mutual Fund Analytics", ["Final report", "A reproducible analytics workflow covering ETL, SQLite, performance measurement, investor behavior, and a four-page interactive dashboard."])
        text_page(pdf, "Executive Summary", [f"The model contains {len(performance)} schemes, {len(transactions):,} investor transactions, and daily NAV observations for performance analysis.", f"The strongest one-year return in the supplied scheme table is {top_fund.return_1yr_pct:.2f}% for {top_fund.scheme_name}.", f"The largest observed fund-house AUM is associated with {top_house}. The dashboard turns these results into four decision views."])
        text_page(pdf, "Data Sources", ["Source files cover fund master data, NAV history, fund-house AUM, monthly SIP inflows, category inflows, folios, scheme performance, investor transactions, portfolio holdings, and benchmark indices.", "All source paths are relative to the repository and are transformed into data/processed by the ETL pipeline."])
        text_page(pdf, "ETL Design", ["scripts/etl_pipeline.py validates required inputs, normalizes column names, parses date fields, removes duplicates, handles infinite numeric values, and writes deterministic cleaned CSVs.", "src/load_db.py loads every cleaned table into SQLite and creates indexes for NAV and transaction lookups. The master runner executes the workflow in order."])
        text_page(pdf, "EDA Findings: Industry", ["AUM trends are aggregated by date and fund house. The dashboard highlights industry scale, AMC concentration, SIP inflows, and folio growth.", "Units are kept explicit: lakh crore for industry AUM, crore for scheme AUM and flows, and crore folios for investor reach."])
        text_page(pdf, "EDA Findings: Investors", ["Investor transactions are segmented by state, transaction type, age group, city tier, and month.", "The most useful operational comparisons are transaction value mix, SIP amount by age group, geographic concentration, and monthly transaction volume."])
        text_page(pdf, "Performance Analysis", ["Daily NAV returns are annualized with 252 trading days. Sharpe uses a 6% annual risk-free rate. Beta uses covariance with the NIFTY50 series divided by benchmark variance.", "Maximum drawdown is calculated from the cumulative return curve. Historical 95% daily VaR is the 5th percentile of daily returns and is reported as a negative threshold."])
        text_page(pdf, "Performance Results", [f"The metrics output contains {len(metrics)} funds and {metrics.observations.min():.0f} to {metrics.observations.max():.0f} daily return observations per fund.", "The scorecard combines return, Sharpe ratio, volatility, rating, and risk grade. The recommendation logic is intentionally explainable and should not be treated as investment advice."])
        for number, name in enumerate(["Page_1_Industry_Overview.png", "Page_2_Fund_Performance.png", "Page_3_Investor_Analytics.png", "Page_4_SIP_Market_Trends.png"], 1):
            image_page(pdf, SCREENSHOTS / name, f"Dashboard Screenshot: Page {number}")
        text_page(pdf, "Limitations", ["The supplied data is historical and may be synthetic or incomplete. Historical returns, VaR, and rankings do not guarantee future performance.", "A native Power BI binary is not generated by Python. The Streamlit app is the interactive alternative; Power BI Desktop can import the cleaned CSV model for a native PBIX implementation."])
        text_page(pdf, "Recommendations", ["Use the dashboard filters to compare fund houses, categories, plans, investor cohorts, and flow periods.", "Add a scheduled production data refresh, explicit holiday calendars for live NAV ingestion, and governance review before using recommendations in an investor-facing workflow."])
        text_page(pdf, "Reproducibility", ["Run: python scripts/run_pipeline.py", "The runner rebuilds processed CSVs, metrics, SQLite, dashboard exports, and this report/deck. SQLite files are ignored by Git; sql/schema.sql is the shareable database definition."])
        text_page(pdf, "Appendix: Deliverables", ["ETL and analytics scripts are in scripts/. Notebooks are in notebooks/. SQL definitions are in sql/. Dashboard exports are in bluestock_mf_dashboard_project/. Final report and presentation are in reports/."])
    return output


def add_slide(prs: Presentation, title: str, bullets: list[str], image: Path | None = None) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    title_box = slide.shapes.add_textbox(Inches(0.55), Inches(0.35), Inches(12.2), Inches(0.6))
    title_box.text_frame.text = title
    title_box.text_frame.paragraphs[0].font.size = Pt(26)
    title_box.text_frame.paragraphs[0].font.bold = True
    title_box.text_frame.paragraphs[0].font.color.rgb = RGBColor.from_string(INK)
    if image:
        slide.shapes.add_picture(str(image), Inches(0.55), Inches(1.15), width=Inches(12.2), height=Inches(5.95))
    else:
        body = slide.shapes.add_textbox(Inches(0.85), Inches(1.35), Inches(11.4), Inches(5.3))
        body.text_frame.clear()
        for bullet in bullets:
            paragraph = body.text_frame.add_paragraph()
            paragraph.text = bullet
            paragraph.level = 0
            paragraph.font.size = Pt(20)
            paragraph.font.color.rgb = RGBColor.from_string(INK)
            paragraph.space_after = Pt(18)


def generate_pdf(context: dict[str, pd.DataFrame]) -> Path:
    output = REPORTS / "Final_Report.pdf"
    aum = context["aum"]
    performance = context["performance"]
    transactions = context["transactions"]
    metrics = context["metrics"]
    category = context["category"]
    top_fund = performance.nlargest(1, "return_1yr_pct").iloc[0]
    top_house = aum.groupby("fund_house").aum_lakh_crore.max().idxmax()
    latest_aum = aum[aum.date.eq(aum.date.max())]
    total_transactions = transactions.amount_inr.sum()
    top_state = transactions.groupby("state").amount_inr.sum().idxmax()
    top_category = category.groupby("category").net_inflow_crore.sum().idxmax()
    with PdfPages(output) as pdf:
        pages = [
            ("Bluestock Mutual Fund Analytics", ["Final project report", "A reproducible workflow covering data ingestion, cleaning, SQLite storage, exploratory analysis, risk measurement, investor segmentation, recommendations, and a four-page Streamlit dashboard.", "Reporting period: supplied 2022-2025 project data | Generated from the repository pipeline"]),
            ("Executive Summary", [f"This project converts ten raw CSV datasets into a repeatable analytical product. The supplied scheme table contains {len(performance):,} schemes, the investor table contains {len(transactions):,} transactions worth approximately Rs {total_transactions / 1_000_000_000:.2f} billion, and the NAV history supports fund-level daily return calculations.", f"The highest one-year return in the supplied performance table is {top_fund.return_1yr_pct:.2f}% for {top_fund.scheme_name}. The fund-house with the highest observed latest AUM is {top_house}. These are descriptive results, not forecasts.", "The dashboard is organized around four user questions: how large is the industry, which funds offer attractive return-risk trade-offs, how do investors transact, and how do SIP/category flows move alongside the market."]),
            ("Data Sources", ["Ten structured sources are used: fund master, NAV history, fund-house AUM, monthly SIP inflows, category inflows, industry folio count, scheme performance, investor transactions, portfolio holdings, and benchmark indices.", f"The latest AUM snapshot contains {len(latest_aum):,} fund-house records. The performance table supplies descriptors such as category, plan, rating, risk grade, and one-year return; daily NAV and NIFTY50 levels are used to independently calculate risk metrics.", "The raw layer is stored in data/raw, deterministic cleaned outputs in data/processed, and the database layer in SQLite. Units are lakh crore for industry AUM, crore for scheme AUM and flows, and rupees for transactions."]),
            ("System Design and ETL", ["The workflow is a batch pipeline: raw CSVs -> validation and normalization -> processed CSVs -> SQLite tables and analytics outputs -> dashboard exports and final report.", "The ETL contract requires every source, lower-cases and trims column names, parses recognized date fields, removes duplicate rows, replaces numeric infinity with missing values, and writes stable cleaned filenames.", "This design separates source preservation from analysis-ready data, making reruns deterministic and keeping cleaning logic out of the presentation layer."]),
            ("ETL Implementation", ["The master runner invokes cleaning, database loading, metrics, dashboard export, and report generation in sequence. Missing inputs, malformed CSVs, filesystem access errors, and invalid values are surfaced rather than silently producing partial output.", "SQLite provides a relational copy for SQL analysis and indexed lookups. The dashboard uses pandas and Plotly, while the PDF generator consumes the same processed data and calculated metrics.", "Production quality checks should include row counts, duplicate counts, date ranges, null rates, AMFI-code uniqueness, and reconciliation of headline aggregates to source totals."]),
            ("EDA Findings: Industry", [f"The latest AUM view contains {len(latest_aum):,} fund-house observations and identifies {top_house} as the largest observed house by maximum AUM. The industry page makes concentration visible with a time trend and ranked AMC chart.", "SIP inflows and folio counts are shown as separate measures because assets, contributions, and investor accounts answer different business questions.", "Compare AUM growth with folio and SIP growth over matching months. Divergence can signal ticket-size changes, market appreciation, redemptions, or acquisition effects."]),
            ("EDA Findings: Investors and Flows", [f"Transaction value is grouped by geography, transaction type, age group, city tier, and month. {top_state} contributes the largest aggregate transaction amount in the supplied investor table.", f"Category flow analysis identifies {top_category} as the category with the largest cumulative net inflow in the supplied records. The dashboard also isolates March observations as a compact FY25 comparison view.", "These are cohort-level descriptive findings. Interpret them with transaction counts, exposure period, and data completeness; aggregate rupee value alone does not measure profitability or suitability."]),
            ("Performance Methodology", ["For each AMFI code, observations are sorted by date and simple daily returns are computed as NAV_t / NAV_(t-1) - 1. Total return is converted to an annualized return using the observed return count divided by 252 trading days.", "Annualized volatility is sample standard deviation multiplied by sqrt(252). Sharpe subtracts a 6% annual risk-free rate converted to a daily rate. Beta is covariance of aligned fund and NIFTY50 returns divided by benchmark variance.", "The cumulative wealth curve produces drawdown as wealth divided by its running maximum minus one. Historical 95% daily VaR is the fifth percentile of daily returns. Observation count is retained for confidence context."]),
            ("Performance Results and Scorecard", [f"The calculated metrics table contains {len(metrics):,} funds, with {metrics.observations.min():.0f} to {metrics.observations.max():.0f} daily return observations per fund.", f"The highest one-year return in the source scorecard is {top_fund.return_1yr_pct:.2f}% for {top_fund.scheme_name}. The dashboard pairs return with annualized risk and provides a sortable table plus normalized NAV-versus-NIFTY50 drill-through.", "No single metric is treated as a winner. Return, Sharpe, volatility, drawdown, beta, rating, risk grade, and AUM should be reviewed together."]),
            ("Recommendation Algorithm", ["The recommender is a transparent ranking aid. Optional category and risk-grade filters narrow the candidate universe. Percentile ranks combine Sharpe ratio (50%), one-year return (30%), and inverse volatility (20%), then sort by score and Sharpe.", "Percentile ranking keeps component scales comparable and makes weighting easy to explain. The method is not an optimizer and does not infer suitability, cash-flow needs, taxes, or future returns.", "Governance should show component scores beside each rank, record the refresh date, apply minimum-observation rules, and require human review before investor-facing use."]),
            ("Dashboard Design", ["The Streamlit application loads processed tables through a cached loader, parses dates, and exposes sidebar filters for each analytical page. Plotly charts use consistent colors, explicit labels, and responsive containers.", "Industry Overview covers AUM, SIP inflows, folios, schemes, and AMC concentration. Fund Performance covers return-risk positioning, NAV versus NIFTY50, and a scorecard. Investor Analytics covers geography, transaction mix, age group, and monthly volume. SIP and Market Trends covers SIP/NIFTY50 movement, category heatmap, and FY25 leaders.", "The dashboard is an exploration surface; this PDF is the durable record of methods, evidence, screenshots, limitations, and recommendations."]),
        ]
        for title, paragraphs in pages:
            text_page(pdf, title, paragraphs)
        for number, name in enumerate(["Page_1_Industry_Overview.png", "Page_2_Fund_Performance.png", "Page_3_Investor_Analytics.png", "Page_4_SIP_Market_Trends.png"], 1):
            image_page(pdf, SCREENSHOTS / name, f"Dashboard Screenshot: Page {number}")
        text_page(pdf, "Limitations", ["The supplied data may be synthetic, incomplete, or snapshot-based. Missing source history, survivorship bias, stale scheme metadata, and unmodeled corporate actions can change interpretation.", "Historical VaR does not capture tail events outside the sample. Annualization assumes 252 trading days and the selected 6% risk-free rate is an analytical assumption.", "A native Power BI binary is not produced by Python. The Streamlit application and exported PNG/PDF files provide the implemented alternative; cleaned CSVs can be imported into Power BI Desktop if required."])
        text_page(pdf, "Recommendations", ["Add data quality gates for schema, date ranges, duplicates, null thresholds, benchmark coverage, and reconciliation across raw, processed, and database layers.", "Enhance the model with rolling returns, rolling volatility, benchmark-relative alpha, expense ratios, turnover, liquidity, tax treatment, and stress scenarios. Add confidence flags when history is short.", "Preserve input snapshots, version metric assumptions, expose score components, and keep recommendation output as decision support with suitability review."])
        code_page(pdf, "Appendix: Cleaning Logic", '''def clean_frame(frame):
    frame = frame.copy()
    frame.columns = [column.strip().lower() for column in frame.columns]
    for column in DATE_COLUMNS.intersection(frame.columns):
        frame[column] = pd.to_datetime(frame[column], errors="coerce")
    frame = frame.drop_duplicates().reset_index(drop=True)
    numeric = frame.select_dtypes(include="number").columns
    frame[numeric] = frame[numeric].replace([float("inf"), float("-inf")], pd.NA)
    return frame''', "This is the core cleaning function used for all ten raw sources. It keeps the processed layer deterministic and auditable.")
        code_page(pdf, "Appendix: Risk Metric Logic", """daily_returns = prices.pct_change().dropna()
years = len(daily_returns) / 252
total_return = prices.iloc[-1] / prices.iloc[0] - 1
annual_return = (1 + total_return) ** (1 / years) - 1
volatility = daily_returns.std() * sqrt(252)
excess = daily_returns - 0.06 / 252
sharpe = excess.mean() / daily_returns.std() * sqrt(252)
cumulative = (1 + daily_returns).cumprod()
drawdown = cumulative / cumulative.cummax() - 1
var_95 = daily_returns.quantile(0.05)""", "This implementation pattern makes the algorithms inspectable. Benchmark alignment is performed before beta; drawdown and VaR use observed daily returns.")
        text_page(pdf, "Reproducibility and Deliverables", ["Run `python scripts/run_pipeline.py` from the repository root to rebuild processed CSVs, fund metrics, SQLite, dashboard exports, this PDF, and the presentation.", "Notebooks are in notebooks/. ETL and analytics scripts are in scripts/. SQL definitions are in sql/. Dashboard code is in app.py and exported screenshots are in bluestock_mf_dashboard_project/2_Exported_Reports/Page_Screenshots/.", "The report documents what was measured, how it was computed, what the dashboard shows, and where additional controls are needed before production or investor-facing use."])
    return output


def generate_presentation(context: dict[str, pd.DataFrame]) -> Path:
    output = REPORTS / "Bluestock_MF_Presentation.pptx"
    performance = context["performance"]
    metrics = context["metrics"]
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slides = [
        ("Bluestock Mutual Fund Analytics", ["Final capstone presentation", "ETL, performance analytics, investor behavior, and BI dashboard"]),
        ("Problem and Objective", ["Create a reliable mutual fund analytics workflow", "Measure scale, returns, risk, flows, and investor activity", "Deliver a decision-ready four-page dashboard"]),
        ("Data Sources", ["10 raw CSV datasets covering funds, NAV, benchmarks, flows, holdings, and transactions", "40 schemes and 32,778 investor transactions in the supplied data", "Cleaned outputs are stored in data/processed/"]),
        ("Architecture and ETL", ["Raw CSVs -> pathlib ETL -> cleaned CSVs -> SQLite star-style tables", "Metrics layer computes annualized return, Sharpe, Beta, drawdown, and VaR", "Streamlit and exported PDF/PNG dashboard consume the same model"]),
        ("EDA Highlights: Industry", ["AUM trend and AMC concentration", "SIP inflow and folio growth context", "Explicit units distinguish lakh crore, crore, and folios"]),
        ("EDA Highlights: Investors", ["Transaction value split by SIP, lumpsum, and redemption", "State, age-group, city-tier, and monthly volume comparisons", "Cohort table supports operational segmentation"]),
        ("Performance Metrics", ["Annualization uses 252 trading days", "Sharpe uses a 6% annual risk-free rate", "Beta is aligned to the NIFTY50 benchmark series"]),
        ("Performance Insights", [f"Top one-year return: {performance.nlargest(1, 'return_1yr_pct').scheme_name.iloc[0]}", f"Metrics computed for {len(metrics)} funds", "Scorecard balances return, risk-adjusted return, and volatility"]),
        ("Dashboard: Industry and Performance", [], SCREENSHOTS / "Page_1_Industry_Overview.png"),
        ("Dashboard: Investors and Market Trends", [], SCREENSHOTS / "Page_3_Investor_Analytics.png"),
        ("Key Findings and Recommendations", ["Use filters to compare fund houses, categories, plans, and investor cohorts", "Treat historical risk metrics and recommender scores as decision support", "Schedule controlled data refreshes before production use"]),
        ("Thank You", ["Bluestock FinTech Mutual Fund Analytics Capstone", "Repository includes scripts, notebooks, SQL, dashboard exports, and documentation"]),
    ]
    for item in slides:
        if len(item) == 3:
            add_slide(prs, item[0], item[1], item[2])
        else:
            add_slide(prs, item[0], item[1])
    prs.save(output)
    return output


def generate() -> tuple[Path, Path]:
    context = load_context()
    return generate_pdf(context), generate_presentation(context)


if __name__ == "__main__":
    for artifact in generate():
        print(f"Created {artifact}")
