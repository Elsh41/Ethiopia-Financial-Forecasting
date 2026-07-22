"""
app.py
------
Streamlit Interactive Dashboard for Ethiopia Financial Inclusion Analysis & Forecasts.
Integrates Tasks 1-4: Historical Trends, Impact Matrices, and 2025-2027 Projections.
"""

import sys
from pathlib import Path

# Add src to system path for modular imports
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from forecast_utils import generate_forecasts, plot_forecast_scenarios
from impact_utils import build_association_matrix, plot_association_matrix

# Set page layout
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="📈",
    layout="wide",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 16px;
        color: #4B5563;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Title & Description
st.markdown(
    "<div class='main-header'>🇪🇹 Ethiopia Financial Inclusion & Event Impact Dashboard</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='sub-header'>Interactive analytical suite tracking Account Ownership, Digital Payment Usage, and Event Shocks (2011–2027).</div>",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    csv_path = project_root / "data" / "processed" / "ethiopia_fi_enriched_data.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    # Fallback dummy dataframe if file isn't present
    return pd.DataFrame(
        {
            "record_type": ["indicator", "impact_link"],
            "indicator": ["ACC_OWN_TOTAL", "Telebirr Launch"],
            "value_numeric": [49.0, 3.2],
        }
    )


df = load_data()

# Sidebar Navigation
st.sidebar.header("🕹️ Dashboard Controls")
page = st.sidebar.radio(
    "Navigate Views",
    [
        "1. Executive Overview & KPIs",
        "2. Event Impact Analysis",
        "3. Interactive Forecast (2025–2027)",
    ],
)

# -----------------------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------
if page == "1. Executive Overview & KPIs":
    st.header("📌 Executive Summary & Key Financial Inclusion KPIs")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Account Ownership (2024)",
            value="49.0%",
            delta="+3.0% vs 2021",
        )
    with col2:
        st.metric(
            label="Digital Payments Usage",
            value="28.5%",
            delta="+8.5% vs 2021",
        )
    with col3:
        st.metric(
            label="NFIS Target (2026/27)",
            value="60.0%",
            delta="11.0% Gap",
            delta_color="inverse",
        )
    with col4:
        st.metric(
            label="Mobile Money Active Users",
            value="~45M+",
            delta="Telebirr + M-Pesa",
        )

    st.markdown("---")

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.subheader("📈 Historical Trajectory (2011–2024)")
        hist_years = [2011, 2014, 2017, 2021, 2024]
        acc_vals = [14.0, 22.0, 35.0, 46.0, 49.0]
        usg_vals = [3.5, 7.0, 12.0, 20.0, 28.5]

        fig_hist, ax = plt.subplots(figsize=(7, 4), dpi=120)
        ax.plot(
            hist_years,
            acc_vals,
            "o-",
            label="Account Ownership (%)",
            color="#1f77b4",
            linewidth=2,
        )
        ax.plot(
            hist_years,
            usg_vals,
            "s-",
            label="Digital Payments Usage (%)",
            color="#ff7f0e",
            linewidth=2,
        )
        ax.set_title("Findex Trajectory for Ethiopia")
        ax.set_ylabel("% Adult Population")
        ax.legend()
        st.pyplot(fig_hist)

    with col_right:
        st.subheader("💡 Core Insights")
        st.info(
            "**Key Driver:** The rollout of Telebirr (2021) and Safaricom M-Pesa (2023) fundamentally decoupled digital payment usage from traditional bank account growth."
        )
        st.warning(
            "**Inclusion Gap:** Gender and rural disparities remain prominent. Male account ownership exceeds female ownership by ~12 percentage points."
        )

# -----------------------------------------------------------------------------
# PAGE 2: EVENT IMPACT ANALYSIS
# -----------------------------------------------------------------------------
elif page == "2. Event Impact Analysis":
    st.header("⚡ Macroeconomic & Policy Event Impact Matrix")

    st.write(
        "Quantifying the historical association between major fintech/regulatory events and core financial inclusion indicators."
    )

    matrix = build_association_matrix(df)

    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("Association Heatmap")
        fig_mat = plot_association_matrix(matrix)
        st.pyplot(fig_mat)

    with col2:
        st.subheader("Event Linkage Breakdown")
        st.dataframe(matrix.style.highlight_max(axis=0, color="lightgreen"), use_container_width=True)
        st.caption(
            "Values indicate estimated structural impact weight (pp boost) on indicators."
        )

# -----------------------------------------------------------------------------
# PAGE 3: INTERACTIVE FORECAST (2025–2027)
# -----------------------------------------------------------------------------
elif page == "3. Interactive Forecast (2025–2027)":
    st.header("🔮 Scenario-Based Forecasting (2025–2027)")

    # Sidebar Controls for Scenario Adjustment
    st.sidebar.subheader("⚙️ Scenario Tuning")
    event_shock_multiplier = st.sidebar.slider(
        "Event Shock Multiplier", 0.5, 2.0, 1.0, 0.1
    )

    forecast_df = generate_forecasts(df)

    # Apply interactive multiplier dynamically to Base Case
    forecast_df["Access_BaseCase"] = np.round(
        forecast_df["Access_Baseline"]
        + (
            forecast_df["Access_BaseCase"] - forecast_df["Access_Baseline"]
        )
        * event_shock_multiplier,
        2,
    )
    forecast_df["Usage_BaseCase"] = np.round(
        forecast_df["Usage_Baseline"]
        + (forecast_df["Usage_BaseCase"] - forecast_df["Usage_Baseline"])
        * event_shock_multiplier,
        2,
    )

    st.subheader("Forecast Trajectory Plot")
    fig_fc = plot_forecast_scenarios(forecast_df)
    st.pyplot(fig_fc)

    st.subheader("📊 Forecast Summary Data Table")
    st.dataframe(forecast_df, use_container_width=True)

    # Download Button for Report CSV
    csv_data = forecast_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Forecast CSV Data",
        data=csv_data,
        file_name="ethiopia_financial_inclusion_forecasts_2025_2027.csv",
        mime="text/csv",
    )