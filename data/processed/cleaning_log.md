## Cleaning Log (Bronze -> Silver)

**Input:** `data/raw/dpwh_flood_control_projects.csv` (9,855 rows, 22 columns)
**Output:** `data/processed/dpwh_flood_control_projects_silver.csv` (9,855 rows, 25 columns)
**Principle:** nothing is dropped or zero-filled. Problem values are set to NULL and the original information is preserved in a flag or reference column.

### Decisions

| # | Issue | Rows | Decision | Reason |
|---|---|---|---|---|
| 1 | `Municipality` blank | 666 | Keep as NULL; add `is_municipality_missing` (boolean) | Rows are real projects; a flag lets analysis filter deliberately instead of silently losing them |
| 2 | `ApprovedBudgetForContract` holds text "Clustered with Contract ID X" | 130 | Set budget to NULL; store X in `clustered_under_contract_id` | Budget is bundled under another contract, not unknown. NULL, not 0, so totals and averages are not understated |
| 3 | `ApprovedBudgetForContract` holds text "MYCA with Project ID X" | 27 | Set budget to NULL; reference kept in `myca_linked_project_id` | Same MYCA multi-year pattern as decision 4. Together with decision 2, accounts for all 157 non-numeric budget values (130 + 27) |
| 4 | `ContractCost` holds text "MYCA with Project ID X" | 28 | Set cost to NULL; store X in `myca_linked_project_id` | Multi-year contract; cost is carried on the project's other funding-year row |
| 5 | Repeated `ProjectId` | 27 | No change | Expected MYCA pattern, not an error. True grain is `(ProjectId, ContractId, FundingYear)` |

### Checked, no action needed
- Exact duplicate rows: 0
- Leading/trailing whitespace and case variants in Region, Province, Municipality, Contractor, TypeOfWork: none
- Start date after completion date: 0
- Project coordinates outside the Philippines (lat 4-21, lon 116-127): 0
- `ContractorCount` vs number of "/"-separated contractors: matches on all rows

### Retained, not cleaned (to investigate in M4)
- **769 rows** where `ContractCost` > `ApprovedBudgetForContract`. Cause unknown (possibly variation orders); kept as-is.
- **Project duration range 14 to 2,012 days.** Extreme values are retained and will be flagged in Gold.

### Validation checks (run on every execution of `scripts/transform.py`)
1. Output row count equals input row count (9,855)
2. `(ProjectId, ContractId, FundingYear)` is unique
3. NULLs exist only in Municipality, ApprovedBudgetForContract, ContractCost and the two reference columns
4. Non-numeric budget values = rows with a reference ID (130 + 27); non-numeric cost values = 28
5. No start date after its completion date
6. Two consecutive runs produce identical output
