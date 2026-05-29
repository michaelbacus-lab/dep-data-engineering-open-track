# Automated Milestone Checking Plan

## Problem Statement

Manual milestone review will not scale well for a cohort of 700 builders. The program needs a way to automate repeatable checks, collect submissions consistently, and preserve moderator time for judgment-based review.

## Proposed Architecture

The system should use two layers:

1. Participant-side prechecks in each builder repo
2. Program-side authoritative validation for official milestone submissions

### Participant Repo Contract

Each builder repo should include a small machine-readable file named `dep-submission.yml`.

Suggested fields:

- `schema_version`
- `cohort`
- `github_username`
- `project_title`
- `track`
- `paths.readme`
- `paths.raw_dir`
- `paths.processed_dir`
- `paths.notebooks_dir`
- `paths.output_dir`
- `paths.ingest_script`
- `paths.transform_script`
- `paths.requirements`
- `milestones.m6.dashboard_url`

Notes:

- Do not store private email addresses in public repos.
- Use the form and moderator tracker for contact information.
- Keep paths configurable so the validators can support small repo differences.

### Participant-Side GitHub Action

The DEP starter template should ship with a reusable GitHub Actions workflow that:

- runs on `workflow_dispatch`
- optionally runs on push to the default branch
- reads `dep-submission.yml`
- validates milestone requirements selected by the builder
- publishes a markdown summary in the Actions run
- uploads a JSON artifact for machine-readable results

This workflow is a self-check only. It helps builders catch missing files, missing folders, broken links, and malformed repo structure before formal submission.

### Program-Side Validation

A separate DEP ops repo should handle official milestone validation.

Core pieces:

- validation workflows
- milestone validator scripts for `M0` through `M6`
- status tracking
- Google Sheets or Airtable sync
- reviewer report output

Suggested status values:

- `submitted`
- `auto_failed`
- `auto_pass_candidate`
- `needs_human_review`
- `passed`
- `improve`
- `resubmit_required`

### Submission Flow

1. Builder submits a form with:
   - email
   - GitHub username
   - repo URL
   - milestone
   - optional branch or ref
   - optional deployed URL for `M6`
2. The form writes to Google Sheets or Airtable.
3. An automation triggers a workflow in the DEP ops repo.
4. The workflow clones the builder repo, reads `dep-submission.yml`, and runs milestone validation.
5. The workflow writes back the result, failure notes, and a short moderator report.
6. Moderators review only the cases that require human judgment.

## Milestone Validation Model

Automation should pre-screen milestone requirements, not replace reviewer judgment.

### M0

Auto-check:

- public repo exists
- `README.md` exists
- repo has at least one commit
- at least one source URL is present

Human review:

- question is specific and answerable
- audience is clear
- README is written in the learner's own words

### M1

Auto-check:

- starter folder structure exists
- README includes source metadata
- repo is public
- first pull path marker exists

Human review:

- source is specific and usable

### M2

Auto-check:

- `/data/raw` exists and is non-empty
- `ingest.py` exists or manual process is documented
- source URL and date metadata are present

Human review:

- repeatability is credible, especially for manual-download paths

### M3

Auto-check:

- `/data/processed` exists and is non-empty
- transform script exists
- SQL file or notebook section exists
- validation markers exist

Human review:

- schema and grain quality
- cleaning logic
- data type correctness

### M4

Auto-check:

- notebook or figure outputs exist
- chart count threshold is met
- markdown commentary exists

Human review:

- charts are relevant
- interpretations are meaningful
- inference remains cautious

### M5

Path A auto-check:

- modeling notebook or script exists
- evaluation metric markers exist
- `requirements.txt` exists

Path B auto-check:

- segmentation output exists
- KPI section exists
- stakeholder brief exists
- `requirements.txt` exists

Human review:

- chosen path fits the project
- outputs are meaningful
- repo is professionally organized

### M6

Auto-check:

- dashboard or report artifact exists
- deployed URL responds
- README contains live link
- key links resolve

Human review:

- final output quality
- presentation readiness
- clarity for outside readers

## Moderator Workflow

Google Sheets or Airtable should be the moderator-facing review queue.

Recommended fields:

- participant email
- GitHub username
- cohort
- assigned moderator
- repo URL
- milestone
- track
- submission timestamp
- auto-check status
- auto-check score
- blocker summary
- reviewer verdict
- reviewer comment
- resubmission count
- final decision timestamp

Recommended views:

- new submissions
- auto-failed
- ready for human review
- assigned to me
- improve and resubmissions
- passed by milestone
- at-risk builders

Assignment rules:

- assign builders to moderators early and keep that ownership stable
- keep milestone review with the same moderator when possible
- escalate only unusual or disputed cases

## Rollout Phases

### Phase 1

- define the `dep-submission.yml` contract
- update the DEP starter template
- create the builder-side precheck workflow

### Phase 2

- create the DEP ops repo
- build milestone validators for `M0`, `M1`, and `M2`
- connect the submission form to Sheets or Airtable

### Phase 3

- expand validators through `M6`
- add moderator reports and resubmission handling
- pilot with a smaller group before full cohort rollout

### Phase 4

- add optional weekly activity signals for moderator triage
- use weekly signals for nudges only, not pass or fail decisions

## Acceptance Criteria

- obvious milestone failures are caught before moderator review
- moderators can open one tracker row and access all relevant evidence quickly
- private data stays out of public repos
- the system supports milestone review at 700-builder scale
