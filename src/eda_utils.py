"""
eda_utils.py
------------
Visualization and analysis tools for Ethiopia Financial Inclusion EDA.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set style globally
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"


def plot_temporal_coverage(
    df: pd.DataFrame, save_path: str = None
) -> plt.Figure:
    """Generates a matrix/heatmap showing temporal coverage of indicators over time."""
    obs_df = df[df["record_type"] == "observation"].copy()

# Use format="mixed" to safely parse mixed date strings
    obs_df["year"] = pd.to_datetime(obs_df["observation_date"], format="mixed", errors="coerce").dt.year

# Drop records where year or indicator_code could not be resolved
    obs_df = obs_df.dropna(subset=["year", "indicator_code"])
    obs_df["year"] = obs_df["year"].astype(int)

    coverage_matrix = (
        obs_df.groupby(["indicator_code", "year"])["value_numeric"]
        .count()
        .unstack(fill_value=0)
    )

# Use a stable, modest figure size and sensible DPI to prevent memory allocation spikes
    num_rows = len(coverage_matrix)
    fig_height = max(4, min(10, num_rows * 0.4))

    fig, ax = plt.subplots(
        figsize=(10, fig_height), dpi=150)
    sns.heatmap(
        coverage_matrix,
        annot=True,
        fmt="d",
        cmap="YlGnBu",
        cbar=False,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title(
        "Temporal Data Coverage by Indicator (Observation Count per Year)",
        fontsize=12,
        pad=12,
        fontweight="bold",
    )
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Indicator Code", fontsize=10)
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
    return fig


def plot_account_ownership_trajectory(
    df: pd.DataFrame, events_df: pd.DataFrame = None, save_path: str = None
) -> plt.Figure:
    """Plots 2011-2024 Account Ownership trajectory with key event overlays."""
    acc_df = df[
        (df["record_type"] == "observation")
        & (
            df["indicator_code"].isin(
                ["ACC_OWN_TOTAL", "ACC_OWN_MALE", "ACC_OWN_FEMALE"]
            )
        )
    ].copy()
    acc_df["year"] = pd.to_datetime(acc_df["observation_date"], format="mixed", errors="coerce").dt.year
    acc_df = acc_df.sort_values("year")

    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)

    for code, group in acc_df.groupby("indicator_code"):
        label_map = {
            "ACC_OWN_TOTAL": "Total Account Ownership (%)",
            "ACC_OWN_MALE": "Male Ownership (%)",
            "ACC_OWN_FEMALE": "Female Ownership (%)",
        }
        style = (
            {"color": "#1f77b4", "linewidth": 2.5, "marker": "o"}
            if code == "ACC_OWN_TOTAL"
            else {"linestyle": "--", "marker": "s", "alpha": 0.8}
        )
        ax.plot(
            group["year"],
            group["value_numeric"],
            label=label_map.get(code, code),
            **style,
        )

        for _, row in group.iterrows():
            ax.annotate(
                f"{row['value_numeric']}%",
                (row["year"], row["value_numeric"]),
                textcoords="offset points",
                xytext=(0, 6),
                ha="center",
                fontweight="bold",
            )

    # Event overlays
    if events_df is not None and not events_df.empty:
        events = events_df.copy()
        events["year"] = pd.to_datetime(events["observation_date"], format="mixed", errors="coerce").dt.year
        for _, evt in events.iterrows():
            ax.axvline(
                x=evt["year"], color="crimson", linestyle=":", alpha=0.7
            )
            ax.text(
                evt["year"],
                ax.get_ylim()[0] + 2,
                f"  {evt.get('indicator', 'Event')}",
                rotation=90,
                color="crimson",
                fontsize=8,
            )

    ax.set_title(
        "Ethiopia Account Ownership Trajectory (2011-2024)",
        fontsize=12,
        fontweight="bold",
    )
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("% of Adults (15+)", fontsize=10)
    ax.legend(loc="upper left")
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
    return fig