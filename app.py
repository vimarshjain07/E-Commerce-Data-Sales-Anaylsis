import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

st.title("📊 E-Commerce Sales Analytics Dashboard")

# ---------------------------
# Custom CSS (smaller KPI font)
# ---------------------------
st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Load Data
# ---------------------------
df = pd.read_csv("Ecommerce_Sales_Data_2024_2025.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("🔎 Filters")

region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique()
)

payment = st.sidebar.multiselect(
    "Payment Mode",
    options=df["Payment Mode"].unique()
)

filtered_df = df.copy()

if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]

if category:
    filtered_df = filtered_df[filtered_df["Category"].isin(category)]

if payment:
    filtered_df = filtered_df[filtered_df["Payment Mode"].isin(payment)]

# ---------------------------
# If no data after filters
# ---------------------------
if filtered_df.empty:

    st.warning("⚠️ No data for selected filters. Showing overall insights instead.")

    # Overview charts
    colA, colB = st.columns(2)

    with colA:
        region_sales = df.groupby("Region")["Sales"].sum().reset_index()

        fig = px.bar(
            region_sales,
            x="Region",
            y="Sales",
            color="Sales",
            title="Overall Region Sales"
        )

        st.plotly_chart(fig, use_container_width=True)

    with colB:
        category_sales = df.groupby("Category")["Sales"].sum().reset_index()

        fig2 = px.pie(
            category_sales,
            names="Category",
            values="Sales",
            hole=0.4,
            title="Overall Category Sales"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.stop()

# ---------------------------
# KPIs
# ---------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_order = filtered_df["Sales"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
col3.metric("🛒 Orders", f"{total_orders:,}")
col4.metric("💳 Avg Order", f"₹{avg_order:,.0f}")

st.divider()

# ---------------------------
# Monthly Sales Trend
# ---------------------------
st.subheader("📈 Monthly Sales Trend")

monthly_sales = filtered_df.groupby(
    filtered_df["Order Date"].dt.to_period("M")
)["Sales"].sum().reset_index()

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Revenue"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# Top Products
# ---------------------------
st.subheader("🏆 Top Products")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    top_products,
    x="Product Name",
    y="Sales",
    color="Sales"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# Category + Region
# ---------------------------
col5, col6 = st.columns(2)

with col5:

    st.subheader("📦 Category Sales")

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=0.4
    )

    st.plotly_chart(fig3, use_container_width=True)

with col6:

    st.subheader("🌍 Region Sales")

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig4 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Sales"
    )

    st.plotly_chart(fig4, use_container_width=True)

# ---------------------------
# Payment Mode
# ---------------------------
st.subheader("💳 Payment Mode Distribution")

payment_sales = (
    filtered_df.groupby("Payment Mode")["Sales"]
    .sum()
    .reset_index()
)

fig5 = px.pie(
    payment_sales,
    names="Payment Mode",
    values="Sales",
    hole=0.4
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------------------
# Data Table for Users
# ---------------------------
st.subheader("📄 Data Preview")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=300
)