[![CI](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml)

# Financial Complaint Auto-Routing with NLP

This project builds a supervised machine learning pipeline to classify consumer financial complaint narratives into financial product categories using the CFPB Consumer Complaint Database.

## Project Goal

The goal is to support automated complaint routing by predicting the correct product category from a consumer complaint narrative.

## Project Status

- Week 1 setup: completed
- Week 2 CFPB raw data download: completed
- Week 3 EDA and cleaning: planned
- Version 1 Scikit-learn baseline: planned
- Version 2 DistilBERT transformer upgrade: planned

No EDA, feature engineering, model training, or model evaluation results are reported yet.

## Dataset

Dataset source: Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database.

The project uses complaint records with public consumer complaint narratives from the CFPB API.

- Input text column: `complaint_what_happened`
- Target label column: `product`
- Raw local file: `data/raw/cfpb_complaints_2024_raw.csv`

The raw CSV is downloaded locally by `notebooks/01_data_download.ipynb`. It is not included in this repository and should not be uploaded to GitHub.

## Current Dataset Snapshot

The Week 2 raw download produced the following local dataset:

- Rows: 50,000
- Raw API columns: 17
- Product classes: 11
- Date range: 2024-12-11 to 2024-12-31
- Rows outside calendar year 2024: 0
- Missing or empty complaint narratives: 0
- Missing or empty product labels: 0
- Duplicate `complaint_id` values: 0

Important sampling note: the CFPB API returns records sorted newest first. This 50,000-row dataset is a late-2024 newest-first API sample, not a full-year random sample.

## Data Privacy and Storage

The raw CSV is local only and is not committed to GitHub.

The repository is configured to ignore raw data files:

- `data/raw/*`
- `*.csv`

This keeps the downloaded complaint data out of version control while preserving the notebook code needed to recreate the local file.

## Notebook Workflow

- `notebooks/01_data_download.ipynb`: completed CFPB API raw data download and validation
- `notebooks/02_eda_cleaning.ipynb`: planned EDA and cleaning
- `notebooks/03_sklearn_baseline_model.ipynb`: planned TF-IDF baseline modeling

## Modeling Plan

Version 1 will build a Scikit-learn baseline using TF-IDF features and traditional supervised classifiers:

- Logistic Regression
- Naive Bayes
- Linear SVM

Planned Version 1 pipeline:

`CFPB complaint narrative -> TF-IDF features -> Scikit-learn classifier -> product category`

Version 2 will compare the Scikit-learn baseline with a DistilBERT transformer model.

## Skills Demonstrated

At the current stage, the repository demonstrates data collection and validation work and documents the planned modeling workflow for later notebooks.

- Python
- Pandas
- API data collection
- Data validation
- Natural Language Processing
- NLP classification planning
- TF-IDF
- Scikit-learn
- Classification modeling
- Model evaluation metrics: accuracy, precision, recall, F1-score, and confusion matrix
