import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import logging
import sys

sns.set(style="whitegrid")

# Set page config
st.set_page_config(page_title="Business Sales Dashboard", layout="wide")

# Paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "dataset" / "dataset.csv"
REPORT_DIR = PROJECT_DIR / "report"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Logger
logging.basicConfig(
    level=logging.INFO,
    format="🔥 %(asctime)s - %(levelname)s - %(message)s",
)

# ------------------ Analysis Functions ------------------
def load_data_analysis(path: Path) -> pd.DataFrame:
    if not path.exists():
        logging.error(f"DATASET NOT FOUND: {path}")
        sys.exit(1)
    df = pd.read_csv(path, parse_dates=["OrderDate"])
    logging.info(f"Loaded dataset: {len(df)} rows")
    return df

def clean_data_analysis(df: pd.DataFrame) -> pd.DataFrame:
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

def compute_kpis_analysis(df: pd.DataFrame) -> dict:
    kpis = {
        "Total Revenue": df["Revenue"].sum(),
        "Total Orders": df["OrderID"].nunique(),
        "Average Order Value": df["Revenue"].sum() / max(df["OrderID"].nunique(), 1),
        "Total Products": df["ProductID"].nunique(),
        "Total Categories": df["Category"].nunique() if "Category" in df.columns else None,
    }
    logging.info("KPIs computed.")
    return kpis

def save_plot(filename):
    plt.tight_layout()
    outpath = REPORT_DIR / filename
    plt.savefig(outpath, dpi=300)
    plt.close()
    logging.info(f"📊 Saved visualization: {outpath}")

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

def run_analysis():
    logging.info("🚀 Starting Analysis...")
    df = load_data_analysis(DATA_PATH)
    df = clean_data_analysis(df)
    kpis = compute_kpis_analysis(df)
    plot_monthly_revenue(df)
    plot_category_revenue(df)
    plot_top_products(df)
    plot_day_heatmap(df)
    plot_correlation(df)
    plot_revenue_dist(df)
    plot_category_pie(df)
    save_insights(df, kpis)
    logging.info("✅ Analysis Complete")

# Check if reports exist, if not, run analysis
report_files = [
    "01_monthly_revenue.png",
    "02_category_contribution.png",
    "03_top_products.png",
    "04_day_heatmap.png",
    "05_correlation.png",
    "06_revenue_distribution.png",
    "07_category_pie.png",
    "INSIGHTS_PROFESSIONAL.txt"
]
if not all((REPORT_DIR / f).exists() for f in report_files):
    run_analysis()

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["OrderDate"])
    # Clean data (similar to task1_analysis.py)
    for col in ["Price", "Quantity", "Revenue"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
    df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
    df["Year"] = df["OrderDate"].dt.year
    df["Day"] = df["OrderDate"].dt.day_name()
    return df

df = load_data()

# Compute KPIs
kpis = {
    "Total Revenue": df["Revenue"].sum(),
    "Total Orders": df["OrderID"].nunique(),
    "Average Order Value": df["Revenue"].sum() / max(df["OrderID"].nunique(), 1),
    "Total Products": df["ProductID"].nunique(),
    "Total Categories": df["Category"].nunique() if "Category" in df.columns else 0,
}

# Sidebar filters
st.sidebar.header("Filters")
selected_category = st.sidebar.multiselect("Select Category", options=df["Category"].unique(), default=df["Category"].unique())
selected_year = st.sidebar.multiselect("Select Year", options=sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))

# Filter data
filtered_df = df[(df["Category"].isin(selected_category)) & (df["Year"].isin(selected_year))]

# Main title
st.title("📊 Business Sales Dashboard")

# KPIs Section
st.header("📌 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Revenue", f"${kpis['Total Revenue']:,.2f}")
with col2:
    st.metric("Total Orders", kpis["Total Orders"])
with col3:
    st.metric("Avg Order Value", f"${kpis['Average Order Value']:,.2f}")
with col4:
    st.metric("Total Products", kpis["Total Products"])
with col5:
    st.metric("Total Categories", kpis["Total Categories"])

# Visualizations Section
st.header("📈 Visualizations")

# Monthly Revenue
st.subheader("Monthly Revenue Trend")
st.image(str(REPORT_DIR / "01_monthly_revenue.png"))

# Category Contribution
st.subheader("Revenue Contribution by Category")
st.image(str(REPORT_DIR / "02_category_contribution.png"))

# Top Products
st.subheader("Top 10 Products by Revenue")
st.image(str(REPORT_DIR / "03_top_products.png"))

# Day Heatmap
st.subheader("Sales Distribution by Day & Month")
st.image(str(REPORT_DIR / "04_day_heatmap.png"))

# Correlation
st.subheader("Correlation Matrix")
st.image(str(REPORT_DIR / "05_correlation.png"))

# Revenue Distribution
st.subheader("Revenue Distribution")
st.image(str(REPORT_DIR / "06_revenue_distribution.png"))

# Category Pie
st.subheader("Category Revenue Share")
st.image(str(REPORT_DIR / "07_category_pie.png"))

# Insights Section
st.header("🧠 Insights")
insights_path = REPORT_DIR / "INSIGHTS_PROFESSIONAL.txt"
if insights_path.exists():
    with open(insights_path, "r") as f:
        insights = f.read()
    st.text_area("Business Insights", insights, height=300)
else:
    st.write("Insights file not found. Run the analysis script first.")

# Filtered Data Preview
st.header("🔍 Filtered Data Preview")
st.dataframe(filtered_df.head(100))

# Footer
st.write("Dashboard powered by Streamlit. Data from task1_analysis.py.")
