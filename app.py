import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Last Mile Delivery Dashboard", layout="wide")

# --------------------------
# LOAD DATA
# --------------------------
df = pd.read_csv("Last mile Delivery Data.csv")

# --------------------------
# DATA CLEANING
# --------------------------
df = df.dropna()  # simple, safe for assignment

# Convert types
df["Delivery_Time"] = pd.to_numeric(df["Delivery_Time"], errors='coerce')
df["Agent_Age"] = pd.to_numeric(df["Agent_Age"], errors='coerce')
df["Agent_Rating"] = pd.to_numeric(df["Agent_Rating"], errors='coerce')

# Create Late Delivery Flag
mean_time = df["Delivery_Time"].mean()
std_time = df["Delivery_Time"].std()
df["Late"] = df["Delivery_Time"] > (mean_time + std_time)

# --------------------------
# SIDEBAR FILTERS
# --------------------------
st.sidebar.title("Filters")

weather_filter = st.sidebar.multiselect("Weather", df["Weather"].unique())
traffic_filter = st.sidebar.multiselect("Traffic", df["Traffic"].unique())
vehicle_filter = st.sidebar.multiselect("Vehicle", df["Vehicle"].unique())
area_filter = st.sidebar.multiselect("Area", df["Area"].unique())
category_filter = st.sidebar.multiselect("Category", df["Category"].unique())

filtered_df = df.copy()

if weather_filter:
    filtered_df = filtered_df[filtered_df["Weather"].isin(weather_filter)]
if traffic_filter:
    filtered_df = filtered_df[filtered_df["Traffic"].isin(traffic_filter)]
if vehicle_filter:
    filtered_df = filtered_df[filtered_df["Vehicle"].isin(vehicle_filter)]
if area_filter:
    filtered_df = filtered_df[filtered_df["Area"].isin(area_filter)]
if category_filter:
    filtered_df = filtered_df[filtered_df["Category"].isin(category_filter)]

st.title("📦 Last Mile Delivery Dashboard")

# --------------------------
# KPIs
# --------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Avg Delivery Time", round(filtered_df["Delivery_Time"].mean(),2))
col2.metric("% Late Deliveries", f"{round(filtered_df['Late'].mean()*100, 2)}%")
col3.metric("Total Deliveries", len(filtered_df))

st.markdown("---")

# --------------------------
# 1. DELAY ANALYZER
# --------------------------
st.subheader("🚦 Delay Analyzer (Weather & Traffic)")

delay_weather = filtered_df.groupby("Weather")["Delivery_Time"].mean().reset_index()
delay_traffic = filtered_df.groupby("Traffic")["Delivery_Time"].mean().reset_index()

col1, col2 = st.columns(2)

fig1 = px.bar(delay_weather, x="Weather", y="Delivery_Time", title="Avg Delivery Time by Weather")
col1.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(delay_traffic, x="Traffic", y="Delivery_Time", title="Avg Delivery Time by Traffic")
col2.plotly_chart(fig2, use_container_width=True)

# --------------------------
# 2. VEHICLE COMPARISON
# --------------------------
st.subheader("🚚 Vehicle Performance Comparison")

vehicle_avg = filtered_df.groupby("Vehicle")["Delivery_Time"].mean().reset_index()
fig3 = px.bar(vehicle_avg, x="Vehicle", y="Delivery_Time", title="Avg Delivery Time by Vehicle Type")
st.plotly_chart(fig3, use_container_width=True)

# --------------------------
# 3. AGENT PERFORMANCE SCATTER
# --------------------------
st.subheader("🧍 Agent Performance Scatter Plot")

fig4 = px.scatter(
    filtered_df,
    x="Agent_Rating",
    y="Delivery_Time",
    color="Agent_Age",
    title="Agent Rating vs Delivery Time (Colored by Age)"
)
st.plotly_chart(fig4, use_container_width=True)

# --------------------------
# 4. AREA HEATMAP
# --------------------------
st.subheader("📍 Area Heatmap")

area_avg = filtered_df.groupby("Area")["Delivery_Time"].mean().reset_index()

fig5 = px.density_heatmap(
    area_avg,
    x="Area",
    y="Delivery_Time",
    title="Heatmap of Delivery Time by Area",
    nbinsx=len(area_avg)
)
st.plotly_chart(fig5, use_container_width=True)

# --------------------------
# 5. CATEGORY BOXPLOT
# --------------------------
st.subheader("📦 Category Delivery Time Distribution")

fig6 = px.box(filtered_df, x="Category", y="Delivery_Time", title="Delivery Time by Category")
st.plotly_chart(fig6, use_container_width=True)
