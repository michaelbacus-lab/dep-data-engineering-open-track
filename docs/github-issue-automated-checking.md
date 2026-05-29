# Proposal: Automate milestone submission checks for cohort builders

## Summary

Manual milestone review will not scale to 700 builders.

## Proposal

Add:

- a standard `dep-submission.yml` repo manifest
- builder-side GitHub Action prechecks
- a central validator pipeline in a DEP ops repo
- a Google Sheets or Airtable moderator tracker for official submissions

## Goal

Automate repeatable milestone checks and reserve moderators for judgment-based review.

## Scope

Milestone submission flow for `M0` through `M6`, not full weekly grading.

## Expected Outcome

Faster triage, more consistent review criteria, and lower moderator workload.
