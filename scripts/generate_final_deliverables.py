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


def generate_pdf(context: dict[str, pd.DataFrame]) -> Path:
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
