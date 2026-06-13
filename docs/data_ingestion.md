# CFPB Data Ingestion and Validation

This document captures the detailed data-ingestion design and validation snapshot for the CFPB complaint datasets used by this project. The README keeps a shorter portfolio summary; this file preserves the deeper dataset details for technical review.

## CFPB Source

Dataset source: Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database.

The project uses complaint records with public consumer complaint narratives from the CFPB API.

- Input text column: `complaint_what_happened`
- Target label column: `product`
- 2024 raw local file: `data/raw/cfpb_complaints_2024_raw.csv`
- 2025 raw local file: `data/raw/cfpb_complaints_2025_raw.csv`

The raw CSV files are downloaded locally by `notebooks/01_data_download.ipynb`. They are not included in this repository and should not be uploaded to GitHub.

## Notebook Behavior

The notebook defaults to `FORCE_DOWNLOAD = False`, so Run All validates existing local ignored CSVs when they are present and only calls the CFPB API when a raw CSV is missing or `FORCE_DOWNLOAD = True`.

This local-first behavior avoids unnecessary fresh API downloads during normal notebook reruns.

## Year-Based Dataset Design

The current data-ingestion strategy creates two separate year-based datasets:

- The 2024 dataset is for model development.
- The 2025 dataset is for future holdout / out-of-time validation.

The 2024 and 2025 datasets are downloaded separately, saved separately, and should not be combined and randomly split. This supports a more realistic business workflow where models are developed on historical complaints and later tested on future complaints.

## Sampling Strategy

Each year uses monthly-balanced + daily-stratified sampling instead of a single newest-first pull. The target is 50,000 records per year when available. January through November target 4,167 records each, and December is adjusted to 4,163 records so the total remains 50,000.

Within each month, the notebook allocates the monthly target across daily windows as evenly as possible. This reduces both late-year recency bias and within-month end-of-month bias.

The notebook keeps only rows with:

- Non-empty complaint narratives.
- Non-empty product labels.
- Unique `complaint_id` values.
- `date_received` values within the target year.

It preserves the original CFPB API columns in each raw local CSV for traceability.

## 2024 Model-Development Dataset

- Rows: 50,000
- Raw API columns: 17
- Product classes: 11
- Actual date range: 2024-01-01 to 2024-12-31
- Rows per month:
  - 2024-01: 4,167
  - 2024-02: 4,167
  - 2024-03: 4,167
  - 2024-04: 4,167
  - 2024-05: 4,167
  - 2024-06: 4,167
  - 2024-07: 4,167
  - 2024-08: 4,167
  - 2024-09: 4,167
  - 2024-10: 4,167
  - 2024-11: 4,167
  - 2024-12: 4,163
- Unique dates covered: 366 of 366
- Missing calendar dates: 0
- Rows per covered day range: 134 to 144
- Rows outside calendar year 2024: 0
- Missing or empty complaint narratives: 0
- Missing or empty product labels: 0
- Duplicate `complaint_id` values: 0
- All records within calendar year 2024: true
- Daily windows with shortfall before backfill: 0
- Total daily shortfall before backfill: 0
- Rows backfilled within month: 0
- Monthly shortfall after backfill: 0

## 2025 Future Holdout / Out-of-Time Dataset

- Rows: 50,000
- Raw API columns: 17
- Product classes: 11
- Actual date range: 2025-01-01 to 2025-12-31
- Rows per month:
  - 2025-01: 4,167
  - 2025-02: 4,167
  - 2025-03: 4,167
  - 2025-04: 4,167
  - 2025-05: 4,167
  - 2025-06: 4,167
  - 2025-07: 4,167
  - 2025-08: 4,167
  - 2025-09: 4,167
  - 2025-10: 4,167
  - 2025-11: 4,167
  - 2025-12: 4,163
- Unique dates covered: 365 of 365
- Missing calendar dates: 0
- Rows per covered day range: 20 to 749
- Rows outside calendar year 2025: 0
- Missing or empty complaint narratives: 0
- Missing or empty product labels: 0
- Duplicate `complaint_id` values: 0
- All records within calendar year 2025: true
- Daily windows with shortfall before backfill: 8
- Total daily shortfall before backfill: 801
- Rows backfilled within month: 801
- Monthly shortfall after backfill: 0

## Sampling Notes

The earlier Week 2 newest-first API sample covered only late 2024, and the first monthly-balanced sample still favored end-of-month records within each month. The current daily-stratified workflow reduces both issues by drawing records from every day of each target year, but each dataset is still a sample, not the full CFPB database.

Within each daily window, CFPB API pagination still reflects the API sort order rather than random selection.

## Data Safety Notes

This repository preserves the existing data safety policy:

- Raw CFPB CSV files are local only and must not be committed.
- Processed data files are local only and must not be committed.
- CSV files are ignored globally through `.gitignore`.
- Saved model artifacts are ignored through `.gitignore`.
- Do not add complaint narrative samples to documentation or reports.
- Do not upload raw CFPB complaint files to GitHub.

The repository tracks only code, notebooks, documentation, templates, and placeholder files needed to reproduce the workflow.
