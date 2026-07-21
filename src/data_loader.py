"""
data_loader.py
--------------
Modular utilities for loading, exploring, validating, and enriching
Ethiopia Financial Inclusion (FI) unified time-series data.
"""

from typing import Dict, Tuple
import pandas as pd
import numpy as np


class UnifiedDataLoader:
    """Handles loading and exploration of the Ethiopia FI unified dataset."""

    def __init__(self, unified_data_path: str, reference_codes_path: str):
        self.unified_data_path = unified_data_path
        self.reference_codes_path = reference_codes_path
        self.raw_data: Dict[str, pd.DataFrame] = {}
        self.ref_codes: pd.DataFrame = pd.DataFrame()

    def load_datasets() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Loads sheet 1 (data), sheet 2 (impact_links), and reference codes.

        Handles both Excel multi-sheet workbooks and CSV fallback formats.
        """
        try:
            # Try reading multi-sheet Excel file first
            self.raw_data["data"] = pd.read_excel(
                self.unified_data_path, sheet_name="data"
            )
            self.raw_data["impact_links"] = pd.read_excel(
                self.unified_data_path, sheet_name="impact_links"
            )
        except Exception:
            # Fallback for CSV loading
            self.raw_data["data"] = pd.read_csv(self.unified_data_path)
            self.raw_data["impact_links"] = pd.DataFrame()

        self.ref_codes = pd.read_csv(self.reference_codes_path)
        return (
            self.raw_data["data"],
            self.raw_data["impact_links"],
            self.ref_codes,
        )

    def validate_schema(self, df: pd.DataFrame) -> Dict[str, bool]:
        """Validates schema constraints:

        1. Observations & Targets MUST have a 'pillar' defined.
        2. Events MUST have 'pillar' set to Null/NaN (category is used instead).
        3. Impact_links MUST link to events via 'parent_id'.
        """
        checks = {}

        if "record_type" in df.columns:
            # Check 1: Events should have empty pillar
            events = df[df["record_type"] == "event"]
            checks["events_pillar_is_null"] = events["pillar"].isna().all()

            # Check 2: Observations and targets must have non-null pillar
            obs_targets = df[df["record_type"].isin(["observation", "target"])]
            checks["obs_target_pillar_is_populated"] = (
                obs_targets["pillar"].notna().all()
            )

        if "parent_id" in df.columns:
            # Check 3: Impact links parent_id presence
            impact_links = df[df["record_type"] == "impact_link"]
            checks["impact_links_have_parent_id"] = (
                impact_links["parent_id"].notna().all()
            )

        return checks

    def explore_summary(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Generates summary statistics by record_type, pillar, source_type, and confidence."""
        summaries = {}
        for col in ["record_type", "pillar", "source_type", "confidence"]:
            if col in df.columns:
                summaries[col] = df[col].value_counts(dropna=False).to_frame()

        if "observation_date" in df.columns:
            df["parsed_date"] = pd.to_datetime(
                df["observation_date"], errors="coerce"
            )
            summaries["temporal_range"] = pd.DataFrame(
                {
                    "min_date": [df["parsed_date"].min()],
                    "max_date": [df["parsed_date"].max()],
                    "total_records": [len(df)],
                }
            )

        if "indicator_code" in df.columns:
            summaries["indicator_coverage"] = (
                df.groupby("indicator_code")
                .agg(
                    record_count=("record_type", "count"),
                    earliest_date=("observation_date", "min"),
                    latest_date=("observation_date", "max"),
                )
                .reset_index()
            )

        return summaries


def enrich_dataset(
    original_df: pd.DataFrame, new_records: list
) -> pd.DataFrame:
    """Appends new enrichment records (observations, events, or impact_links)

    ensuring schema compliance.
    """
    new_df = pd.DataFrame(new_records)

    # Schema Compliance Enforcer
    if "record_type" in new_df.columns and "pillar" in new_df.columns:
        # Force events to have empty pillar
        new_df.loc[new_df["record_type"] == "event", "pillar"] = np.nan

    enriched_df = pd.concat([original_df, new_df], ignore_index=True)
    return enriched_df