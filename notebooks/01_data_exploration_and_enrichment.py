import os
import sys
from pathlib import Path

# Dynamically add the 'src' directory to Python's search path
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

    
import pandas as pd
from data_loader import UnifiedDataLoader, enrich_dataset

# 1. Load Data
loader = UnifiedDataLoader(
    unified_data_path="../data/raw/ethiopia_fi_unified_data.xlsx",
    reference_codes_path="../data/raw/reference_codes.xlsx",
)

data_df, impact_links_df, ref_codes = loader.load_datasets()

# 2. Explore Schema & Summary
summary = loader.explore_summary(data_df)
print("=== RECORD TYPE DISTRIBUTION ===")
print(summary.get("record_type"))

print("\n=== PILLAR DISTRIBUTION ===")
print(summary.get("pillar"))

print("\n=== CONFIDENCE DISTRIBUTION ===")
print(summary.get("confidence"))

# 3. New Enrichment Records (Task 1 Requirement)
new_enrichment_data = [
    # New Observation: Global Findex Gender Disaggregation (2024)
    {
        "id": "OBS_2024_001",
        "record_type": "observation",
        "pillar": "Access",
        "indicator": "Account Ownership (% age 15+) - Female",
        "indicator_code": "ACC_OWN_FEMALE",
        "value_numeric": 41.5,
        "observation_date": "2024-10-01",
        "source_name": "World Bank Global Findex 2025",
        "source_url": "https://www.worldbank.org/en/publication/globalfindex",
        "source_type": "survey",
        "confidence": "high",
        "collected_by": "Task-1 Team",
        "collection_date": "2026-07-21",
        "notes": "Female account ownership data point to analyze gender gap dynamics.",
    },
    # New Observation: Telebirr Active User Base (2024)
    {
        "id": "OBS_2024_002",
        "record_type": "observation",
        "pillar": "Usage",
        "indicator": "Telebirr Registered Account Base",
        "indicator_code": "MOB_ACC_TELEBIRR",
        "value_numeric": 47500000,
        "observation_date": "2024-06-30",
        "source_name": "Ethio Telecom Annual Business Report 2023/24",
        "source_url": "https://www.ethiotelecom.et/",
        "source_type": "operator_report",
        "confidence": "high",
        "collected_by": "Task-1 Team",
        "collection_date": "2026-07-21",
        "notes": "Tracks mobile wallet growth vs active usage lag.",
    },
    # New Event: Safaricom M-Pesa Commercial Launch
    {
        "id": "EVT_2023_002",
        "record_type": "event",
        "pillar": None,  # MUST BE EMPTY FOR EVENTS PER SCHEMA
        "category": "product_launch",
        "indicator": "Safaricom M-Pesa Commercial Rollout",
        "observation_date": "2023-08-15",
        "source_name": "Safaricom Telecommunications Ethiopia",
        "source_url": "https://safaricom.et",
        "source_type": "press_release",
        "confidence": "high",
        "collected_by": "Task-1 Team",
        "collection_date": "2026-07-21",
        "notes": "Introduces foreign-backed mobile wallet competition to Telebirr.",
    },
    # New Impact Link: Connecting M-Pesa Event to Usage Indicator
    {
        "id": "IMP_2023_001",
        "record_type": "impact_link",
        "parent_id": "EVT_2023_002",  # Links to M-Pesa Event
        "pillar": "Usage",
        "related_indicator": "Digital Payment Adoption Rate",
        "impact_direction": "positive",
        "impact_magnitude": "medium",
        "lag_months": 6,
        "evidence_basis": "Competitive market entry drives adoption across urban centers with a 6-month agent network ramp-up lag.",
        "collected_by": "Task-1 Team",
        "collection_date": "2026-07-21",
        "notes": "Models lag between license issuance and active transaction volume.",
    },
]

# 4. Enrich & Export Dataset
enriched_df = enrich_dataset(data_df, new_enrichment_data)
os.makedirs("../data/processed", exist_ok=True)
enriched_df.to_csv(
    "../data/processed/ethiopia_fi_enriched_data.csv", index=False
)
print("\nEnriched dataset successfully exported to data/processed/!")