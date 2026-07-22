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





import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Ensure export directory exists
output_dir = "reports/figures"
os.makedirs(output_dir, exist_ok=True)

# 2. Historical Demographic Data (Findex 2017, 2021, 2024 Benchmark)
data = {
    "Year": [2017, 2021, 2024],
    "Male": [41.2, 53.1, 55.4],
    "Female": [29.1, 38.8, 42.6],
    "Urban": [52.0, 64.5, 68.2],
    "Rural": [29.5, 39.2, 42.1],
}

df_demo = pd.DataFrame(data)

# 3. Styling Configuration
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

x = np.arange(len(df_demo["Year"]))
width = 0.35

# Color Palette
color_male = "#1E3A8A"     # Deep Navy
color_female = "#EC4899"   # Pink/Magenta
color_urban = "#2563EB"    # Bright Blue
color_rural = "#D97706"    # Amber/Orange

# --- Subplot 1: Gender Inclusion Gap ---
rects1 = axes[0].bar(x - width/2, df_demo["Male"], width, label="Male", color=color_male, alpha=0.9)
rects2 = axes[0].bar(x + width/2, df_demo["Female"], width, label="Female", color=color_female, alpha=0.9)

axes[0].set_title("Gender Gap in Account Ownership (2017–2024)", fontsize=13, fontweight="bold", pad=12)
axes[0].set_ylabel("Account Ownership Rate (%)", fontsize=11)
axes[0].set_xticks(x)
axes[0].set_xticklabels(df_demo["Year"], fontsize=10)
axes[0].legend(frameon=True, facecolor="white", loc="upper left")
axes[0].set_ylim(0, 80)

# Add value labels on top of bars
for rect in rects1 + rects2:
    height = rect.get_height()
    axes[0].annotate(f"{height:.1f}%",
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 3),  
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=9, fontweight="bold")

# Annotate 2024 Gender Gap
axes[0].annotate("12.8% Gap",
                xy=(2 + width/2, 42.6), xytext=(2, 60),
                arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=6),
                fontsize=10, fontweight="bold", color="#991B1B")

# --- Subplot 2: Urban vs Rural Disparity ---
rects3 = axes[1].bar(x - width/2, df_demo["Urban"], width, label="Urban", color=color_urban, alpha=0.9)
rects4 = axes[1].bar(x + width/2, df_demo["Rural"], width, label="Rural", color=color_rural, alpha=0.9)

axes[1].set_title("Urban vs. Rural Account Ownership Gap (2017–2024)", fontsize=13, fontweight="bold", pad=12)
axes[1].set_xticks(x)
axes[1].set_xticklabels(df_demo["Year"], fontsize=10)
axes[1].legend(frameon=True, facecolor="white", loc="upper left")

# Add value labels on top of bars
for rect in rects3 + rects4:
    height = rect.get_height()
    axes[1].annotate(f"{height:.1f}%",
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 3),  
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=9, fontweight="bold")

# Annotate 2024 Urban-Rural Gap
axes[1].annotate("26.1% Gap",
                xy=(2 + width/2, 42.1), xytext=(2, 70),
                arrowprops=dict(facecolor="black", shrink=0.05, width=1, headwidth=6),
                fontsize=10, fontweight="bold", color="#991B1B")

plt.suptitle("Figure 3: Ethiopia Financial Inclusion Demographic Disparity Analysis", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout()

# 4. Save Figure 3 specifically to reports/figures/gender_rural_gap.png
fig_path = os.path.join(output_dir, "gender_rural_gap.png")
plt.savefig(fig_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"✅ Figure 3 successfully generated and saved to: {fig_path}")