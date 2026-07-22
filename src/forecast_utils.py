"""
forecast_utils.py
-----------------
Forecasting engine for Ethiopia Financial Inclusion (2025-2027).
Implements trend regression, event-augmented shocks, scenario bounds,
and forecast visualizations.
"""

from pathlib import Path
import matplotlib

matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")


def generate_forecasts(df: pd.DataFrame) -> pd.DataFrame:
    """Generates 2025-2027 projections under Baseline, Base (Event-Augmented),

    Optimistic, and Pessimistic scenarios.
    """
    # Historical anchor points (Findex + NBE observations)
    years_hist = np.array([2011, 2014, 2017, 2021, 2024])

    # Findex target series
    acc_hist = np.array([14.0, 22.0, 35.0, 46.0, 49.0])  # Access
    usg_hist = np.array([3.5, 7.0, 12.0, 20.0, 28.5])  # Usage

    forecast_years = np.array([2025, 2026, 2027])
    all_years = np.concatenate([years_hist, forecast_years])

    # Fit log-linear trends for baseline
    fit_acc = np.polyfit(years_hist, np.log(acc_hist), 1)
    fit_usg = np.polyfit(years_hist, np.log(usg_hist), 1)

    # Baseline extrapolation
    acc_base_trend = np.exp(np.polyval(fit_acc, forecast_years))
    usg_base_trend = np.exp(np.polyval(fit_usg, forecast_years))

    # Event Shocks (Cumulative impact from Safaricom M-Pesa, NBE Directives, Merchant Interoperability)
    # Lags spread over 2025-2027 horizon
    acc_event_shock = np.array([1.2, 2.5, 3.8])  # pp gain
    usg_event_shock = np.array([2.0, 4.2, 6.5])  # pp gain

    # Combine Scenarios
    acc_base_case = acc_base_trend + acc_event_shock
    acc_optimistic = acc_base_case + np.array([1.5, 3.0, 4.5])
    acc_pessimistic = acc_base_case - np.array([1.0, 2.0, 3.0])

    usg_base_case = usg_base_trend + usg_event_shock
    usg_optimistic = usg_base_case + np.array([2.0, 4.5, 7.0])
    usg_pessimistic = usg_base_case - np.array([1.5, 2.8, 4.0])

    # Assemble output dataframe
    results = []
    for i, yr in enumerate(forecast_years):
        results.append(
            {
                "Year": yr,
                "Access_Baseline": round(acc_base_trend[i], 2),
                "Access_BaseCase": round(acc_base_case[i], 2),
                "Access_Optimistic": round(acc_optimistic[i], 2),
                "Access_Pessimistic": round(acc_pessimistic[i], 2),
                "Usage_Baseline": round(usg_base_trend[i], 2),
                "Usage_BaseCase": round(usg_base_case[i], 2),
                "Usage_Optimistic": round(usg_optimistic[i], 2),
                "Usage_Pessimistic": round(usg_pessimistic[i], 2),
            }
        )

    return pd.DataFrame(results)


def plot_forecast_scenarios(
    forecast_df: pd.DataFrame, save_path: str = None
) -> plt.Figure:
    """Plots 2011-2027 Historical Trajectory with 2025-2027 Scenario Ranges."""
    years_hist = np.array([2011, 2014, 2017, 2021, 2024])
    acc_hist = np.array([14.0, 22.0, 35.0, 46.0, 49.0])
    usg_hist = np.array([3.5, 7.0, 12.0, 20.0, 28.5])

    years_fc = forecast_df["Year"].values

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)

    # --- Plot 1: Account Ownership (Access) ---
    ax1.plot(
        years_hist,
        acc_hist,
        "o-",
        color="#1f77b4",
        linewidth=2.5,
        label="Historical Data (Findex)",
    )

    # Base Case line connects from last historical point (2024)
    fc_years_plot = np.concatenate([[2024], years_fc])
    acc_base_plot = np.concatenate([[acc_hist[-1]], forecast_df["Access_BaseCase"].values])
    acc_opt_plot = np.concatenate([[acc_hist[-1]], forecast_df["Access_Optimistic"].values])
    acc_pess_plot = np.concatenate([[acc_hist[-1]], forecast_df["Access_Pessimistic"].values])

    ax1.plot(
        fc_years_plot,
        acc_base_plot,
        "s--",
        color="#2ca02c",
        linewidth=2,
        label="Base Case (Event-Augmented)",
    )
    ax1.fill_between(
        fc_years_plot,
        acc_pess_plot,
        acc_opt_plot,
        color="#2ca02c",
        alpha=0.2,
        label="Scenario Uncertainty (60% Target Band)",
    )

    # National target line
    ax1.axhline(
        y=60.0,
        color="crimson",
        linestyle=":",
        linewidth=1.8,
        label="NFIS National Target (60%)",
    )

    for y, val in zip(years_fc, forecast_df["Access_BaseCase"]):
        ax1.annotate(
            f"{val}%",
            (y, val),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontweight="bold",
            color="#2ca02c",
        )

    ax1.set_title(
        "Account Ownership Forecast (2025–2027)",
        fontsize=12,
        fontweight="bold",
    )
    ax1.set_xlabel("Year", fontsize=10)
    ax1.set_ylabel("% Adult Population", fontsize=10)
    ax1.legend(loc="upper left", fontsize=8.5)

    # --- Plot 2: Digital Payment Usage ---
    ax2.plot(
        years_hist,
        usg_hist,
        "o-",
        color="#ff7f0e",
        linewidth=2.5,
        label="Historical Data (Findex)",
    )

    usg_base_plot = np.concatenate([[usg_hist[-1]], forecast_df["Usage_BaseCase"].values])
    usg_opt_plot = np.concatenate([[usg_hist[-1]], forecast_df["Usage_Optimistic"].values])
    usg_pess_plot = np.concatenate([[usg_hist[-1]], forecast_df["Usage_Pessimistic"].values])

    ax2.plot(
        fc_years_plot,
        usg_base_plot,
        "s--",
        color="#d62728",
        linewidth=2,
        label="Base Case (Event-Augmented)",
    )
    ax2.fill_between(
        fc_years_plot,
        usg_pess_plot,
        usg_opt_plot,
        color="#d62728",
        alpha=0.18,
        label="Scenario Uncertainty Range",
    )

    for y, val in zip(years_fc, forecast_df["Usage_BaseCase"]):
        ax2.annotate(
            f"{val}%",
            (y, val),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontweight="bold",
            color="#d62728",
        )

    ax2.set_title(
        "Digital Payment Usage Forecast (2025–2027)",
        fontsize=12,
        fontweight="bold",
    )
    ax2.set_xlabel("Year", fontsize=10)
    ax2.set_ylabel("% Adult Population", fontsize=10)
    ax2.legend(loc="upper left", fontsize=8.5)

    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)

    return fig