import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from FRED_API import fetch_fred_data  # custom module

# 🎯 Streamlit app setup - Sets the page layout and header of your dashboard
st.set_page_config(page_title="Economic Dashboard", layout="wide")
st.title("📊 Economic Indicator Dashboard")
st.write("Compare economic indicators over time and analyze Year-over-Year (YoY) trends.")

# 📅 Year selection dropdowns ###################################################
years = list(range(2000, 2026))
col1, col2, _ = st.columns([2, 2, 8])
with col1:
    start_year = st.selectbox("Start Year", years, index=0)
with col2:
    end_year = st.selectbox("End Year", years, index=len(years) - 1)

# 🛑 Validate year range ########################################################
if start_year > end_year:
    st.error("⚠ Start year must be before end year.")
    st.stop()

# 📆 Format date range ormat dates to send to FRED API for filtering ###########
start_date = f"{start_year}-01-01"
end_date = f"{end_year}-12-31"

# 📦 Load FRED data ############################################################
import datetime

# 🗓️ Used as a cache key — changes monthly
import datetime

# 🗓️ Used as a cache key — changes once a month
current_month = datetime.date.today().strftime("%Y-%m")

@st.cache_data
def load_local_data():
    # Go up two levels from this file: /code → /api → /econ_dashboard
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    # Now go down into /data/fetch_fred_data.csv
    data_path = os.path.join(base_dir, "data", "fetch_fred_data.csv")
    
    return pd.read_csv(data_path, index_col=0, parse_dates=True)

df_full = load_local_data()


# 📦 Load the full dataset from FRED once per month
df_full = load_local_data()

df = df_full.loc[start_date:end_date]

# ❌ Stop if the slice is empty
if df.empty:
    st.error("⚠ No data found for this date range.")
    st.stop()

df = df.sort_index()

# ✅ Define available variables
available_variables = df.columns.tolist()

# 📌 Select economic indicators --------------------------------------
st.subheader("📌 Select Two Economic Indicators for Comparison")
col1, col2, _ = st.columns([2, 2, 8])  # Match the year dropdown layout
with col1:
    primary_variable = st.selectbox("Primary Indicator (Left Axis)", available_variables, index=0)
with col2:
    secondary_variable = st.selectbox("Secondary Indicator (Right Axis)", available_variables, index=1)

# 📊 Prepare YoY and charts -------------------------------------------
df_yoy = df.ffill().pct_change(periods=12) * 100

# --- Chart 1: Absolute Values ------------------------------------------
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df.index, y=df[primary_variable], name=primary_variable, mode="lines"))
fig1.add_trace(go.Scatter(x=df.index, y=df[secondary_variable], name=secondary_variable, mode="lines", yaxis="y2"))
fig1.update_layout(
    title="Absolute Values Over Time",
    xaxis_title="Date",
    yaxis=dict(title=primary_variable, side="left"),
    yaxis2=dict(title=secondary_variable, overlaying="y", side="right"),
    hovermode="x unified",
    template="plotly_white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5
    )
)


# --- Chart 2: YoY % Change ----------------------------------------------
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_yoy.index, y=df_yoy[primary_variable], name=f"{primary_variable} YoY %", mode="lines"))
fig2.add_trace(go.Scatter(x=df_yoy.index, y=df_yoy[secondary_variable], name=f"{secondary_variable} YoY %", mode="lines", yaxis="y2"))
fig2.update_layout(
    title="YOY Values Over Time",
    xaxis_title="Date",
    yaxis=dict(title=primary_variable, side="left"),
    yaxis2=dict(title=secondary_variable, overlaying="y", side="right"),
    hovermode="x unified",
    template="plotly_white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5
    )
)


# --- Chart 3: Scatter Plot with Correlation ---------------------------------
df_scatter = df_yoy[[primary_variable, secondary_variable]].dropna()
correlation = df_scatter[primary_variable].corr(df_scatter[secondary_variable])
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=df_scatter[primary_variable],
    y=df_scatter[secondary_variable],
    mode="markers",
    name="Scatter Points"
))
fig3.update_layout(
    title=f"Scatter Plot of YoY Changes<br>📌 Correlation: {correlation:.2f}",
    xaxis_title=f"{primary_variable} YoY %",
    yaxis_title=f"{secondary_variable} YoY %",
    template="plotly_white"
)

# 🎨 Display all charts side-by-side #################################################
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
with col3:
    st.plotly_chart(fig3, use_container_width=True)

# 📥 Download CSV ####################################################################
st.download_button(
    label="📥 Download Monthly Data as CSV",
    data=df.to_csv(index=True),
    file_name="economic_data_monthly.csv",
    mime="text/csv"
)

st.write("Data source: [FRED API](https://fred.stlouisfed.org/)")
