"""Load the flood-control CSV into SQL Server's bronze schema."""

import argparse
import csv
import os
from pathlib import Path

import pyodbc


COLUMNS = (
    "MainIsland",
    "Region",
    "Province",
    "LegislativeDistrict",
    "Municipality",
    "DistrictEngineeringOffice",
    "ProjectId",
    "ProjectName",
    "TypeOfWork",
    "FundingYear",
    "ContractId",
    "ApprovedBudgetForContract",
    "ContractCost",
    "ActualCompletionDate",
    "Contractor",
    "ContractorCount",
    "StartDate",
    "ProjectLatitude",
    "ProjectLongitude",
    "ProvincialCapital",
    "ProvincialCapitalLatitude",
    "ProvincialCapitalLongitude",
)

TABLE = "bronze.dpwh_flood_control_projects"
DEFAULT_CSV = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "raw"
    / "dpwh_flood_control_projects.csv"
)
INSERT_SQL = (
    f"INSERT INTO {TABLE} ({', '.join(f'[{column}]' for column in COLUMNS)}) "
    f"VALUES ({', '.join('?' for _ in COLUMNS)})"
)


def load_csv(csv_path: Path, connection_string: str) -> int:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError("CSV headers do not match the expected 22-column schema.")

        with pyodbc.connect(connection_string, autocommit=False) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    "IF SCHEMA_ID(N'bronze') IS NULL "
                    "EXEC(N'CREATE SCHEMA bronze')"
                )
                definitions = ", ".join(
                    f"[{column}] NVARCHAR(MAX) NULL" for column in COLUMNS
                )
                cursor.execute(
                    "IF OBJECT_ID(N'bronze.dpwh_flood_control_projects', N'U') IS NULL "
                    f"CREATE TABLE {TABLE} ({definitions})"
                )
                cursor.execute(f"TRUNCATE TABLE {TABLE}")

                inserted = 0
                batch = []
                for row in reader:
                    if None in row or any(value is None for value in row.values()):
                        raise ValueError(
                            f"CSV row {reader.line_num} does not contain 22 fields."
                        )
                    batch.append(tuple(row[column] for column in COLUMNS))
                    if len(batch) == 500:
                        cursor.executemany(INSERT_SQL, batch)
                        inserted += len(batch)
                        batch.clear()

                if batch:
                    cursor.executemany(INSERT_SQL, batch)
                    inserted += len(batch)

                connection.commit()
                return inserted
            except Exception:
                connection.rollback()
                raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Input CSV path")
    args = parser.parse_args()

    connection_string = os.environ.get("SQLSERVER_CONNECTION_STRING")
    if not connection_string:
        raise SystemExit(
            "Set SQLSERVER_CONNECTION_STRING to your SQL Server ODBC connection string."
        )

    if not args.csv.is_file():
        raise SystemExit(f"CSV file not found: {args.csv}")

    inserted = load_csv(args.csv, connection_string)
    print(f"Loaded {inserted:,} rows into {TABLE}.")


if __name__ == "__main__":
    main()
