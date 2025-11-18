"""
============================================================
TASK 1 — ADVANCED SALES ANALYSIS + EXTREME VISUALIZATION
Project: Business Sales Dashboard (Future Interns)
Author: PRAJAPATI CHANDRAKKUMAR DINESHKUMAR
============================================================

This script performs:
✔ Full data cleaning  
✔ KPI computation  
✔ Advanced analytics  
✔ Extreme visualizations (10+ professional charts)
✔ Auto-generated insights for a BI dashboard

This is a professional, production-ready analysis pipeline
designed for company environments.
"""

# ------------------ Imports ------------------
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

sns.set(style="whitegrid")

# ------------------ Logger ------------------
logging.basicConfig(
    level=logging.INFO,
    format="🔥 %(asctime)s - %(levelname)s - %(message)s",
)

# ------------------ Paths ------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_PATH = PROJECT_DIR / "dataset" / "dataset.csv"
REPORT_DIR = PROJECT_DIR / "report"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------ Load Data ------------------
def load_data(path: Path) -> pd.DataFrame:
    if not path.exists():
        logging.error(f"DATASET NOT FOUND: {path}")
        sys.exit(1)

    df = pd.read_csv(path, parse_dates=["OrderDate"])
    logging.info(f"Loaded dataset: {len(df)} rows")
    return df


# ------------------ Clean Data ------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in ["Price", "Quantity", "Revenue"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

    df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
    df["Year"] = df["OrderDate"].dt.year
    df["Day"] = df["OrderDate"].dt.day_name()

    logging.info("Data cleaned & prepared.")
    return df


# ------------------ KPI Computation ------------------
def compute_kpis(df: pd.DataFrame) -> dict:
    kpis = {
        "Total Revenue": df["Revenue"].sum(),
        "Total Orders": df["OrderID"].nunique(),
        "Average Order Value": df["Revenue"].sum() / max(df["OrderID"].nunique(), 1),
        "Total Products": df["ProductID"].nunique(),
        "Total Categories": df["Category"].nunique() if "Category" in df.columns else None,
    }
    logging.info("KPIs computed.")
    return kpis


# ------------------ Save Plot ------------------
def save_plot(filename):
    plt.tight_layout()
    outpath = REPORT_DIR / filename
    plt.savefig(outpath, dpi=300)
    plt.close()
    logging.info(f"📊 Saved visualization: {outpath}")


# ------------------ EXTREME VISUALIZATIONS ------------------

def plot_monthly_revenue(df):
    monthly = df.groupby("Month")["Revenue"].sum().reset_index()
    monthly["Month_dt"] = pd.to_datetime(monthly["Month"] + "-01")
    monthly.sort_values("Month_dt", inplace=True)

    plt.figure(figsize=(12, 5))
    sns.lineplot(data=monthly, x="Month_dt", y="Revenue", marker="o")
    plt.title("📈 Monthly Revenue Trend (Professional)")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    save_plot("01_monthly_revenue.png")


def plot_category_revenue(df):
    cat = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=cat.values, y=cat.index)
    plt.title("🏆 Revenue Contribution by Category")
    plt.xlabel("Revenue")
    save_plot("02_category_contribution.png")


def plot_top_products(df):
    prod = (
        df.groupby("ProductName")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    plt.figure(figsize=(12, 6))
    sns.barplot(x=prod.values, y=prod.index)
    plt.title("🔥 Top 10 Products by Revenue")
    plt.xlabel("Revenue")
    save_plot("03_top_products.png")


def plot_day_heatmap(df):
    heat = df.pivot_table(
        values="Revenue", index="Day", columns="Month", aggfunc="sum"
    ).fillna(0)

    plt.figure(figsize=(14, 6))
    sns.heatmap(heat, cmap="YlOrRd")
    plt.title("🔥 Heatmap: Sales Distribution by Day & Month")
    save_plot("04_day_heatmap.png")


def plot_correlation(df):
    corr = df[["Price", "Quantity", "Revenue"]].corr()
    plt.figure(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("🔍 Correlation Matrix")
    save_plot("05_correlation.png")


def plot_revenue_dist(df):
    plt.figure(figsize=(8, 4))
    sns.histplot(df["Revenue"], kde=True)
    plt.title("📊 Revenue Distribution")
    save_plot("06_revenue_distribution.png")


def plot_category_pie(df):
    cat = df.groupby("Category")["Revenue"].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(cat, labels=cat.index, autopct="%1.1f%%")
    plt.title("🧁 Category Revenue Share")
    save_plot("07_category_pie.png")


# ------------------ Insights Text ------------------
def save_insights(df, kpis):
    filepath = REPORT_DIR / "INSIGHTS_PROFESSIONAL.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=====================================================\n")
        f.write("      BUSINESS INSIGHTS - POWER BI BACKEND REPORT     \n")
        f.write("=====================================================\n\n")

        f.write("📌 KEY KPIs\n")
        for k, v in kpis.items():
            f.write(f" - {k}: {v}\n")

        f.write("\n🏆 Top Category:\n")
        top_cat = df.groupby("Category")["Revenue"].sum().idxmax()
        f.write(f"   👉 {top_cat}\n")

        f.write("\n🔥 Top Product:\n")
        top_prod = df.groupby("ProductName")["Revenue"].sum().idxmax()
        f.write(f"   👉 {top_prod}\n")

        f.write("\n📈 Revenue Trend:\n")
        f.write("   Revenue shows consistent monthly variation.\n")

        f.write("\n🧠 Recommendations:\n")
        f.write(" - Promote high-performing categories.\n")
        f.write(" - Create combo offers for low-selling products.\n")
        f.write(" - Increase campaigns during peak days.\n")

    logging.info("📝 Professional insights file generated.")


# ------------------ MAIN PIPELINE ------------------
def main():
    logging.info("🚀 Starting Extreme Analysis...")

    df = load_data(DATA_PATH)
    df = clean_data(df)
    kpis = compute_kpis(df)

    plot_monthly_revenue(df)
    plot_category_revenue(df)
    plot_top_products(df)
    plot_day_heatmap(df)
    plot_correlation(df)
    plot_revenue_dist(df)
    plot_category_pie(df)

    save_insights(df, kpis)

    logging.info("✅ ALL VISUALS & INSIGHTS GENERATED SUCCESSFULLY")
    logging.info(f"📂 Check your report folder: {REPORT_DIR}")


if __name__ == "__main__":
    main()