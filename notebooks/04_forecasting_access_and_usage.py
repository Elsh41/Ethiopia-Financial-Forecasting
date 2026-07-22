import os
from pathlib import Path
import sys

# Dynamic root path
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import matplotlib.pyplot as plt
from forecast_utils import generate_forecasts, plot_forecast_scenarios
import pandas as pd

# Load Enriched Data
data_path = project_root / "data" / "processed" / "ethiopia_fi_enriched_data.csv"
df = pd.read_csv(data_path)

fig_dir = project_root / "reports" / "figures"
fig_dir.mkdir(parents=True, exist_ok=True)

print("--- TASK 4: FORECASTING ACCESS AND USAGE (2025-2027) ---")

# 1. Generate Forecast Data Table
forecast_df = generate_forecasts(df)

print("\n=== FORECAST RESULTS TABLE (2025-2027) ===")
print(forecast_df.to_string(index=False))

# Export forecast table to CSV
forecast_csv = project_root / "data" / "processed" / "forecasts_2025_2027.csv"
forecast_df.to_csv(forecast_csv, index=False)
print(f"\nForecast data exported to: {forecast_csv}")

# 2. Generate and Save Scenario Visualizations
fig_forecast = plot_forecast_scenarios(
    forecast_df, save_path=str(fig_dir / "forecast_scenarios_2025_2027.png")
)
plt.close(fig_forecast)

print(
    "\nTask 4 visualizations successfully saved to 'reports/figures/forecast_scenarios_2025_2027.png'!"
)