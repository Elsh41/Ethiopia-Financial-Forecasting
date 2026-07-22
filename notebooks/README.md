# Notebooks & Analysis Pipelines

This directory contains executable scripts and Jupyter notebooks for the Ethiopia Financial Inclusion forecasting pipeline.

## Execution Order

### 1. Data Exploration & Enrichment
* **File:** `01_data_exploration_and_enrichment.py` (or `.ipynb`)
* **Purpose:** Ingests raw data, normalizes schema formats, computes proxy indicators, assesses confidence levels, and exports `ethiopia_fi_enriched_data.csv`.

### 2. Exploratory Data Analysis (EDA)
* **File:** `02_exploratory_data_analysis.py` (or `.ipynb`)
* **Purpose:** Generates visual exploratory metrics including temporal data coverage heatmaps, account ownership growth trajectories, and event overlay impacts.
* **Outputs:** 
  * `reports/figures/temporal_coverage.png`
  * `reports/figures/account_trajectory.png`

## How to Run
From the root directory:
```bash
python notebooks/01_data_exploration_and_enrichment.py
python notebooks/02_exploratory_data_analysis.py