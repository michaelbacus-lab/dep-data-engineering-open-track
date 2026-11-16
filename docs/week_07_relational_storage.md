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

```text
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
