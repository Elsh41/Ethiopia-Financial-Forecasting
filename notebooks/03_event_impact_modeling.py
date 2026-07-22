import os
from pathlib import Path
import sys

# Dynamic root path setup
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import matplotlib.pyplot as plt
import pandas as pd
from impact_utils import (
    build_association_matrix,
    load_and_merge_impact_data,
    plot_association_matrix,
    validate_telebirr_historical_impact,
)

# 1. Load Data
data_path = project_root / "data" / "processed" / "ethiopia_fi_enriched_data.csv"
df = pd.read_csv(data_path)

fig_dir = project_root / "reports" / "figures"
fig_dir.mkdir(parents=True, exist_ok=True)

print("--- TASK 3: EVENT IMPACT MODELING ---")

# 2. Build Event-Indicator Association Matrix
matrix = build_association_matrix(df)
print("\nGenerated Event-Indicator Association Matrix:")
print(matrix)

# 3. Save Matrix Heatmap
fig_matrix = plot_association_matrix(
    matrix, save_path=str(fig_dir / "event_association_matrix.png")
)
plt.close(fig_matrix)

# 4. Perform Historical Validation (Telebirr 4.7% -> 9.45%)
fig_val = validate_telebirr_historical_impact(
    df, save_path=str(fig_dir / "telebirr_historical_validation.png")
)
plt.close(fig_val)

print(
    "\nTask 3 artifacts successfully generated in 'reports/figures/'!"
)