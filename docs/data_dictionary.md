# Data Dictionary — Raw DPWH Flood Control Projects File

**File:** `data/raw/dpwh_flood_control_projects.csv` (source and pull date in [`data/raw/SOURCE.md`](../data/raw/SOURCE.md))
**Shape:** 9,855 rows × 22 columns, comma-separated, UTF-8, header row, every value quoted
**Grain:** one row = one contract for one funding year. The key (`ProjectId`, `ContractId`, `FundingYear`) is unique. A multi-year (MYCA) project appears on 2–3 rows (one per funding year), so `ProjectId` alone is not unique: 9,827 distinct projects.

"Raw type" is what the values look like in the file. "Cleaned type" is the type after `scripts/transform.py`, which also lowercases the names and renames three of them (shown in the last column).

| # | Column | Raw type | Cleaned type | Description | Example | Notes | Cleaned name |
|---|---|---|---|---|---|---|---|
| 1 | `MainIsland` | text | text | Main island group of the project | `Luzon` | 3 values: Luzon, Visayas, Mindanao | `mainisland` |
| 2 | `Region` | text | text | Administrative region | `Cordillera Administrative Region` | 16 values | `region` |
| 3 | `Province` | text | text | Province (Metro Manila is treated as one province) | `Apayao` | 84 values | `province` |
| 4 | `LegislativeDistrict` | text | text | Congressional (legislative) district | `APAYAO (LEGISLATIVE DISTRICT)` | 252 values | `legislativedistrict` |
| 5 | `Municipality` | text | text | City or municipality where the project is located | `CITY OF PARAÑAQUE (METROPOLITAN MANILA)` | **666 blank**; left empty, not guessed | `municipality` |
| 6 | `DistrictEngineeringOffice` | text | text | DPWH office that implemented the project | `Apayao 2nd District Engineering Office` | 199 values | `district_engineering_office` |
| 7 | `ProjectId` | text | text | DPWH project identifier | `P00526268LZ` | 9,827 distinct; repeats on MYCA rows | `project_id` |
| 8 | `ProjectName` | text | text | Project title as recorded by DPWH | `Construction of Poblacion Flood Control Structure…` | Free text | `projectname` |
| 9 | `TypeOfWork` | text | text | Category of work | `Construction of Revetment` | 18 values | `typeofwork` |
| 10 | `FundingYear` | integer | integer | Budget year that funded this row | `2021` | 2018–2025 | `fundingyear` |
| 11 | `ContractId` | text | text | Contract identifier | `21PC0018` | 9,698 distinct; shared by MYCA rows and clustered contracts | `contractid` |
| 12 | `ApprovedBudgetForContract` | text (mostly numbers) | decimal, PHP | Approved Budget for the Contract (ABC), the ceiling price | `96500000` | **157 text values** ("Clustered with Contract ID …" 129, "MYCA with Project ID …" 28) become empty; text kept in `approved_budget_note` | `approvedbudgetforcontract` |
| 13 | `ContractCost` | text (mostly numbers) | decimal, PHP | Awarded contract amount | `92692943.8` | **28 text values** ("MYCA with Project ID …") become empty; text kept in `contract_cost_note`. Numeric range PHP 1.15M–289.5M | `contract_cost_php` |
| 14 | `ActualCompletionDate` | text `YYYY-MM-DD` | date | Date the project was completed | `2022-10-03` | 2022-07-01 to 2025-05-30; all valid | `actualcompletiondate` |
| 15 | `Contractor` | text | text | Winning contractor; joint ventures listed as `A / B` | `ASC CONSTRUCTION & CONCRETE PRODUCTS` | 2,409 names; 492 rows have names exactly 50 characters long, which suggests truncation | `contractor` |
| 16 | `ContractorCount` | integer | integer | Number of contractors in the award | `1` | 1–3; above 1 means a joint venture | `contractorcount` |
| 17 | `StartDate` | text `YYYY-MM-DD` | date | Date work started | `2021-03-18` | 2018-02-26 to 2025-03-14; all valid; never after the completion date | `startdate` |
| 18 | `ProjectLatitude` | decimal | decimal | Project site latitude (degrees) | `18.25091` | 5.77–20.46; all inside the Philippines | `projectlatitude` |
| 19 | `ProjectLongitude` | decimal | decimal | Project site longitude (degrees) | `121.04757` | 117.06–126.57 | `projectlongitude` |
| 20 | `ProvincialCapital` | text | text | Capital of the province | `Kabugao` | 84 values | `provincialcapital` |
| 21 | `ProvincialCapitalLatitude` | decimal | decimal | Latitude of the provincial capital | `18.0215` | Used for the dashboard bubble map | `provincialcapitallatitude` |
| 22 | `ProvincialCapitalLongitude` | decimal | decimal | Longitude of the provincial capital | `121.1716` | Used for the dashboard bubble map | `provincialcapitallongitude` |

## Columns added by the pipeline

| Column | File | Type | Description |
|---|---|---|---|
| `contract_cost_note` | cleaned, analysis-ready | text | Original text of a non-numeric `ContractCost` value |
| `approved_budget_note` | cleaned, analysis-ready | text | Original text of a non-numeric `ApprovedBudgetForContract` value |
| `source_rows` | analysis-ready | integer | Raw rows merged into the project (2–3 for MYCA projects, otherwise 1) |
| `regional_avg_cost` | analysis-ready | decimal, PHP | Mean contract cost in the project's region |
| `regional_std_cost` | analysis-ready | decimal, PHP | Standard deviation of contract cost in the region |
| `cost_diff_from_regional_avg` | analysis-ready | decimal, PHP | Project cost minus the regional mean |
| `cost_zscore_regional` | analysis-ready | decimal | (cost − regional mean) ÷ regional standard deviation |
| `is_high_cost_outlier` | analysis-ready | 0/1 | 1 when `cost_zscore_regional` ≥ 2.0 |

How the raw values are cleaned, with row counts and reasons, is in the cleaning log in [`scripts/README.md`](../scripts/README.md). The planned star schema (`location_id`, `office_id` and so on) in [`PROJECT_LOG.md`](PROJECT_LOG.md) and `sql/schema_ddl.sql` is a design for later, not the structure of these files.
