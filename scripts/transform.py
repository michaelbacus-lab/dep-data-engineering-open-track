from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "dpwh_flood_control_projects.csv"
SILVER_PATH = ROOT / "data" / "silver" / "dpwh_flood_control_projects_silver.csv"
REPORT_PATH = ROOT / "data" / "analytics" / "silver_data_report.txt"
LOG_PATH = ROOT / "data" / "analytics" / "dpwh_cleaning_log.csv"


def clean_currency(value: object) -> float | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if text == "":
        return None
    text = text.replace(",", "").replace("₱", "").replace("PHP", "").strip()
    try:
        return float(text)
    except ValueError:
        return None


def clean_date(value: object) -> pd.Timestamp | pd.NaT:
    if pd.isna(value):
        return pd.NaT
    text = str(value).strip()
    if text == "":
        return pd.NaT
    parsed = pd.to_datetime(text, errors="coerce")
    return parsed


def extract_reference(value: object, pattern: str) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if text == "":
        return None
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip()


def build_report(df: pd.DataFrame) -> str:
    rows = len(df)
    funding_years = df["FundingYear"].dropna()
    project_count = df["ProjectId"].nunique() if "ProjectId" in df.columns else 0
    approved_total = df["ApprovedBudgetForContract"].sum() if "ApprovedBudgetForContract" in df.columns else 0.0
    contract_total = df["ContractCost"].sum() if "ContractCost" in df.columns else 0.0

    exact_duplicate_rows = int(df.duplicated(keep="first").sum())
    repeated_project_groups = int(df["ProjectId"].value_counts().loc[lambda s: s > 1].shape[0]) if "ProjectId" in df.columns else 0

    if {"ApprovedBudgetForContract", "ContractCost"}.issubset(df.columns):
        contract_cost_gt_approved = int(
            ((df["ContractCost"].notna()) & (df["ApprovedBudgetForContract"].notna()) & (df["ContractCost"] > df["ApprovedBudgetForContract"])) .sum()
        )
    else:
        contract_cost_gt_approved = 0

    if {"StartDate", "ActualCompletionDate"}.issubset(df.columns):
        start_after_completion = int(
            ((pd.to_datetime(df["StartDate"], errors="coerce").notna())
             & (pd.to_datetime(df["ActualCompletionDate"], errors="coerce").notna())
             & (pd.to_datetime(df["StartDate"], errors="coerce") > pd.to_datetime(df["ActualCompletionDate"], errors="coerce"))).sum()
        )
    else:
        start_after_completion = 0

    missing_values = {
        column: int(df[column].isna().sum())
        for column in df.columns
        if df[column].isna().sum() > 0
    }

    lines = [
        "DPWH FLOOD CONTROL PROJECTS - SILVER DATA REPORT",
        f"Source: {SILVER_PATH}",
        "",
        "OVERVIEW",
        f"Rows: {rows}",
        f"Funding years: {int(funding_years.min())} to {int(funding_years.max())}",
        f"Regions: {df['Region'].nunique()}",
        f"Provinces: {df['Province'].nunique()}",
        f"Unique project IDs: {project_count}",
        f"Approved budget total: PHP {approved_total:,.2f}",
        f"Contract cost total: PHP {contract_total:,.2f}",
        "",
        "DATA QUALITY",
        f"Exact duplicate rows: {exact_duplicate_rows}",
        f"Repeated project ID groups: {repeated_project_groups}",
        f"Contract costs above approved budget: {contract_cost_gt_approved} of {len(df)} rows with both values",
        f"Start date after completion date: {start_after_completion}",
        "Missing values by column:",
        "Column",
    ]

    if missing_values:
        for column, count in sorted(missing_values.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"{column} {count}")
    else:
        lines.append("No missing values detected")

    return "\n".join(lines) + "\n"


def main() -> None:
    raw_df = pd.read_csv(RAW_PATH, dtype=str, keep_default_na=False)
    log_rows: list[dict[str, object]] = []

    cleaned = raw_df.copy()

    municipality_mask = cleaned["Municipality"].fillna("").astype(str).str.strip().eq("")
    cleaned["Municipality"] = cleaned["Municipality"].replace(r"^\s*$", pd.NA, regex=True)
    cleaned["is_municipality_missing"] = municipality_mask.astype(bool)

    for idx, row in cleaned.loc[municipality_mask, ["ProjectId", "ContractId", "Municipality"]].iterrows():
        log_rows.append(
            {
                "row_index": idx,
                "project_id": row["ProjectId"],
                "contract_id": row["ContractId"],
                "field": "Municipality",
                "original_value": "",
                "cleaned_value": "NULL",
                "reason": "Blank municipality for district-wide record; retained as NULL to avoid dropping row.",
            }
        )

    approved_series = cleaned["ApprovedBudgetForContract"].astype(str)
    approved_cluster_mask = approved_series.str.contains("Clustered with Contract ID", case=False, na=False)
    cleaned["clustered_under_contract_id"] = approved_series.apply(
        lambda value: extract_reference(value, r"Clustered with Contract ID\s*([A-Za-z0-9]+)")
    )
    cleaned.loc[approved_cluster_mask, "ApprovedBudgetForContract"] = pd.NA
    cleaned["ApprovedBudgetForContract"] = pd.to_numeric(
        cleaned["ApprovedBudgetForContract"].astype(str).str.replace(",", "", regex=False),
        errors="coerce",
    )

    for idx, row in cleaned.loc[approved_cluster_mask, ["ProjectId", "ContractId", "ApprovedBudgetForContract", "clustered_under_contract_id"]].iterrows():
        log_rows.append(
            {
                "row_index": idx,
                "project_id": row["ProjectId"],
                "contract_id": row["ContractId"],
                "field": "ApprovedBudgetForContract",
                "original_value": raw_df.at[idx, "ApprovedBudgetForContract"],
                "cleaned_value": "NULL",
                "reason": f"Budget text was a cluster note; extracted reference contract ID {row['clustered_under_contract_id']}.",
            }
        )

    cost_series = cleaned["ContractCost"].astype(str)
    myca_cluster_mask = cost_series.str.contains("MYCA with Project ID", case=False, na=False)
    cleaned["myca_linked_project_id"] = cost_series.apply(
        lambda value: extract_reference(value, r"MYCA with Project ID\s*([A-Za-z0-9]+)")
    )
    cleaned.loc[myca_cluster_mask, "ContractCost"] = pd.NA
    cleaned["ContractCost"] = pd.to_numeric(
        cleaned["ContractCost"].astype(str).str.replace(",", "", regex=False),
        errors="coerce",
    )

    for idx, row in cleaned.loc[myca_cluster_mask, ["ProjectId", "ContractId", "ContractCost", "myca_linked_project_id"]].iterrows():
        log_rows.append(
            {
                "row_index": idx,
                "project_id": row["ProjectId"],
                "contract_id": row["ContractId"],
                "field": "ContractCost",
                "original_value": raw_df.at[idx, "ContractCost"],
                "cleaned_value": "NULL",
                "reason": f"Cost text was a MYCA linkage note; extracted linked project ID {row['myca_linked_project_id']}.",
            }
        )

    cleaned["FundingYear"] = pd.to_numeric(cleaned["FundingYear"], errors="coerce").astype("Int64")
    cleaned["ContractorCount"] = pd.to_numeric(cleaned["ContractorCount"], errors="coerce").astype("Int64")
    cleaned["ProjectLatitude"] = pd.to_numeric(cleaned["ProjectLatitude"], errors="coerce")
    cleaned["ProjectLongitude"] = pd.to_numeric(cleaned["ProjectLongitude"], errors="coerce")
    cleaned["ProvincialCapitalLatitude"] = pd.to_numeric(cleaned["ProvincialCapitalLatitude"], errors="coerce")
    cleaned["ProvincialCapitalLongitude"] = pd.to_numeric(cleaned["ProvincialCapitalLongitude"], errors="coerce")
    cleaned["ActualCompletionDate"] = pd.to_datetime(cleaned["ActualCompletionDate"], errors="coerce")
    cleaned["StartDate"] = pd.to_datetime(cleaned["StartDate"], errors="coerce")

    SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(SILVER_PATH, index=False)

    log_df = pd.DataFrame(log_rows)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not log_df.empty:
        log_df.to_csv(LOG_PATH, index=False)
    else:
        pd.DataFrame(columns=["row_index", "project_id", "contract_id", "field", "original_value", "cleaned_value", "reason"]).to_csv(LOG_PATH, index=False)

    report_text = build_report(cleaned)
    REPORT_PATH.write_text(report_text, encoding="utf-8")

    print(report_text)
    print(f"\nCleaning log written to: {LOG_PATH}")


if __name__ == "__main__":
    main()
