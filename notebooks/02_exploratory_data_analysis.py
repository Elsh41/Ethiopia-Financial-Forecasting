import os
from pathlib import Path
import sys

# Dynamic root path
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from eda_utils import plot_account_ownership_trajectory, plot_temporal_coverage

# 1. Load Enriched Dataset
data_path = project_root / "data" / "processed" / "ethiopia_fi_enriched_data.csv"
df = pd.read_csv(data_path)

print(f"Loaded {len(df)} total records for EDA.")

# Create figures directory
fig_dir = project_root / "reports" / "figures"
fig_dir.mkdir(parents=True, exist_ok=True)

# 2. Data Overview & Quality Assessment
print("\n--- RECORD DISTRIBUTION ---")
print(df["record_type"].value_counts())

print("\n--- CONFIDENCE DISTRIBUTION ---")
print(df["confidence"].value_counts(dropna=False))

# 3. Temporal Coverage Plot
fig1 = plot_temporal_coverage(df, save_path=str(fig_dir / "temporal_coverage.png"))
plt.close(fig1)

# 4. Access Trajectory & Event Overlay
events_df = df[df["record_type"] == "event"]
fig2 = plot_account_ownership_trajectory(
    df, events_df=events_df, save_path=str(fig_dir / "account_trajectory.png")
)
plt.close(fig2)

print("\nEDA Visualizations successfully generated in reports/figures/!")