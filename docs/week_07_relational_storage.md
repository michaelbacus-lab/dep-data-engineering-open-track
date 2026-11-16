# Week 7 — Relational Storage & Star Schema Design

**Project Title:** Public Data Patterns in DPWH Flood Control Projects (2022–2025)  
**Target Audience:** Commission on Audit (COA) — Infrastructure Audit Division  
**Document Path:** `docs/week07_storage_schema_design.md`  

---

## Executive Summary

This document describes a **planned, not built** relational star schema for the DPWH Flood Control dataset. The current pipeline stores its cleaned and analysis-ready outputs as CSV files; it does not create or populate the fact and dimension tables described here. The design is a future relational model for organizing project, contractor, location, and implementing-office data.

---

## Star Schema Architecture

> **Status: Planned, not built.** The diagram below is a design proposal only. The implemented analysis-ready output is `data/processed/dpwh_flood_control_analysis_ready.csv`.

The proposed relational storage model centers on a core fact table surrounded by three primary dimension tables:

```
                  +--------------------------------+
                  |         dim_location           |
                  +--------------------------------+
                  | PK  location_id                |
                  |     province                   |
                  |     region                     |
                  +--------------------------------+
                                  │
                                  │ 1:N
                                  ▼
+-----------------------------------+     1:N     +-----------------------------------+
|      dim_implementing_office      |────────────►|    fact_flood_control_projects    |
+-----------------------------------+             +-----------------------------------+
| PK  office_id                     |             | PK  project_id                    |
|     district_engineering_office   |             | FK  contractor_id                 |
|     region                        |             | FK  location_id                   |
+-----------------------------------+             | FK  office_id                     |
                                                  |     contract_cost_php             |
                                  ▲               |     completion_date               |
                                  │ 1:N           |     cost_zscore_regional          |
                  +---------------+                |     latitude                      |
                  | dim_contractor|               |     longitude                     |
                  +---------------+               +-----------------------------------+
                  | PK  contractor_id             |
                  |     contractor_name           |
                  |     is_joint_venture          |
                  +-------------------------------+

```

## Implemented analysis-ready CSV: columns and types

The table below documents the implemented `data/processed/dpwh_flood_control_analysis_ready.csv`. It contains one row per project. The star schema described above is **planned, not built**; the pipeline currently produces this CSV, not relational fact and dimension tables.

Types below describe the data represented in the CSV. Dates are serialized as `YYYY-MM-DD`; blank cells represent missing values.

| Column | Type |
| :--- | :--- |
| `mainisland` | text |
| `region` | text |
| `province` | text |
| `legislativedistrict` | text |
| `municipality` | text |
| `district_engineering_office` | text |
| `project_id` | text |
| `projectname` | text |
| `typeofwork` | text |
| `fundingyear` | integer |
| `contractid` | text |
| `approvedbudgetforcontract` | decimal (PHP), nullable |
| `contract_cost_php` | decimal (PHP) |
| `actualcompletiondate` | date |
| `contractor` | text |
| `contractorcount` | integer |
| `startdate` | date |
| `projectlatitude` | decimal |
| `projectlongitude` | decimal |
| `provincialcapital` | text |
| `provincialcapitallatitude` | decimal |
| `provincialcapitallongitude` | decimal |
| `contract_cost_note` | text, nullable |
| `approved_budget_note` | text, nullable |
| `source_rows` | integer |
| `regional_avg_cost` | decimal (PHP) |
| `regional_std_cost` | decimal (PHP) |
| `cost_diff_from_regional_avg` | decimal (PHP) |
| `cost_zscore_regional` | decimal |
| `is_high_cost_outlier` | integer (0/1) |
