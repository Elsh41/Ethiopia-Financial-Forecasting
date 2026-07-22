# 🇪🇹 Ethiopia Financial Inclusion Forecasting & Impact Analysis (2011–2027)

An end-to-end analytical pipeline, event-impact modeling engine, and interactive dashboard designed to evaluate, quantify, and forecast financial inclusion trajectories in Ethiopia. 

This repository leverages historical World Bank Global Findex survey data, National Bank of Ethiopia (NBE) regulatory reports, and key industry milestones (e.g., Telebirr, Safaricom M-Pesa) to model financial inclusion dynamics and project 2025–2027 outcomes against national targets.

---

## 📌 Project Overview & Key Tasks

### Task 1: Data Exploration & Schema Enrichment
* **Objective:** Ingest, standardize, and enrich unified financial inclusion data across observations, macroeconomic events, and impact linkages.
* **Deliverables:**
  * Cleaned and normalized dataset: `data/processed/ethiopia_fi_enriched_data.csv`
  * Complete audit trail: `docs/data_enrichment_log.md`

### Task 2: Exploratory Data Analysis (EDA)
* **Objective:** Uncover structural growth patterns, gender adoption gaps, and post-2021 adoption momentum.
* **Deliverables:**
  * Visual metrics exported to `reports/figures/` (`temporal_coverage.png`, `account_trajectory.png`).
  * EDA analysis script: `notebooks/02_exploratory_data_analysis.py`.

### Task 3: Event Impact Modeling
* **Objective:** Quantify the structural shock of policy reforms, commercial fintech launches, and infrastructure investments on core financial indicators.
* **Deliverables:**
  * **Event-Indicator Association Matrix** capturing directional percentage-point impacts.
  * Historical validation against actual Telebirr launch metrics (2021–2024: 4.7% → 9.45% mobile money penetration).
  * Impact utilities: `src/impact_utils.py` & execution script `notebooks/03_event_impact_modeling.py`.
  * Methodology & assumptions documentation: `docs/event_impact_methodology.md`.

### Task 4: Forecasting Access and Usage (2025–2027)
* **Objective:** Project Account Ownership (Access) and Digital Payment Usage (Usage) under three distinct scenarios:
  * **Baseline:** Pure log-linear structural trend continuation.
  * **Base Case (Event-Augmented):** Structural trend + cumulative event shocks (M-Pesa rollout, interoperability mandates).
  * **Optimistic / Pessimistic Scenarios:** Upper and lower uncertainty bounds reflecting macroeconomic acceleration vs. liquidity/infrastructure bottlenecks.
* **Deliverables:**
  * Scenario dataset exported to `data/processed/forecasts_2025_2027.csv`.
  * Visualization of progress toward the 60% National Financial Inclusion Strategy (NFIS) target.
  * Forecasting engine: `src/forecast_utils.py` & execution script `notebooks/04_forecasting_access_and_usage.py`.
  * Documentation: `docs/forecasting_methodology.md`.

### Task 5: Interactive Financial Inclusion Dashboard
* **Objective:** Provide stakeholders with an interactive analytical interface to explore metrics, tune event shock multipliers, and inspect projections.
* **Deliverables:**
  * Production Streamlit Application: `dashboard/app.py`.

---

## 📁 Repository Structure

```text
Ethiopia-Financial-Forecast/
├── .vscode/                   # Workspace settings for environment & import paths
├── dashboard/
│   └── app.py                 # Streamlit interactive dashboard application
├── data/
│   ├── raw/                   # Original raw dataset inputs
│   └── processed/             # Cleaned datasets and generated forecast CSVs
├── docs/                      # Technical documentation & methodology reports
│   ├── data_enrichment_log.md
│   ├── event_impact_methodology.md
│   └── forecasting_methodology.md
├── notebooks/                 # Sequential analysis and execution scripts
│   ├── 01_data_exploration_and_enrichment.py
│   ├── 02_exploratory_data_analysis.py
│   ├── 03_event_impact_modeling.py
│   └── 04_forecasting_access_and_usage.py
├── reports/
│   └── figures/               # Generated heatmaps, trend charts, and scenario plots
├── src/                       # Reusable modular source code
│   ├── data_loader.py
│   ├── eda_utils.py
│   ├── impact_utils.py
│   └── forecast_utils.py
└── README.md                  # Project documentation overview