from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "data" / "silver" / "dpwh_flood_control_projects_silver.csv"
OUTPUT_PATH = ROOT / "data" / "analytics" / "missing_municipality_rows.csv"


def main() -> None:
    df = pd.read_csv(CSV_PATH, keep_default_na=True)

    if "Municipality" not in df.columns:
        raise ValueError("The CSV file does not contain a 'Municipality' column.")

    missing_rows = df[
        df["Municipality"].isna() | df["Municipality"].astype(str).str.strip().eq("")
    ].copy()

    if "is_municipality_missing" in missing_rows.columns:
        missing_rows = missing_rows[missing_rows["is_municipality_missing"].fillna(False)]

    missing_rows = missing_rows.sort_values(["Region", "Province", "DistrictEngineeringOffice", "ProjectId"]).reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    missing_rows.to_csv(OUTPUT_PATH, index=False)

    print(f"Total rows with missing municipality: {len(missing_rows)}")
    print("")
    print(missing_rows.head(20).to_string(index=False))
    print("")
    print(f"Saved output to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
