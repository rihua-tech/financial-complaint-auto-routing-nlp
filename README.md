# Financial Complaint Auto-Routing with NLP

**AI/NLP Business Solution for Complaint Routing and Human Review**

[![CI](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml)

This project is a business-oriented AI/NLP solution that uses public CFPB consumer complaint narratives to classify financial complaints into product categories and support faster, more consistent routing decisions.

`Business problem -> data ingestion -> NLP model -> evaluation -> routing recommendation -> human review`

## Project Highlights

- AI/NLP business solution for financial complaint auto-routing.
- Uses CFPB consumer complaint narratives as text input and product category as the target label.
- Builds separate 2024 and 2025 datasets for realistic model development and future holdout testing.
- Uses monthly-balanced + daily-stratified data ingestion to reduce recency bias.
- Demonstrates data ingestion, validation, sampling design, ML workflow planning, and business routing design.
- Compares TF-IDF classifiers using Logistic Regression, Multinomial Naive Bayes, and Linear SVM.
- Linear SVM is the selected Version 1 baseline among the three Scikit-learn models tested on the internal 2024 split.
- Completes a row-normalized confusion matrix and aggregate category-level error analysis for the selected baseline.
- Keeps confidence-based routing and human-review rules as future Week 8 work.
- Keeps raw complaint CSV files local-only and ignored by Git.

## Business Problem

Financial institutions, fintech companies, customer support teams, and compliance groups receive large volumes of written complaints. Manual triage can be slow, inconsistent, and difficult to scale when complaints need to be routed across mortgage, credit card, bank account, debt collection, credit reporting, or loan servicing teams.

This project simulates an NLP-assisted routing workflow that predicts a complaint product category from the consumer narrative.

## Business Users and Value

Target users include complaint operations teams, compliance teams, product operations teams, and risk analytics teams that need faster and more consistent complaint triage.

The planned solution is designed to support:

- Faster initial routing for routine complaint cases.
- More consistent product-category recommendations.
- Reduced manual review effort for high-confidence predictions.
- Human review for low-confidence, ambiguous, or higher-risk complaints.
- Better reporting on complaint volume, model performance, and review workload.

## Solution Approach

The project is organized as an AI/NLP business solution workflow:

`Complaint text -> data validation -> NLP model -> evaluation -> confidence-based routing -> human review -> reporting deliverables`

The solution framework has three layers:

1. **Data workflow**: Download and validate public CFPB complaint records, then prepare complaint narratives and product labels for analysis.
2. **Model workflow**: Build and evaluate baseline NLP classifiers using TF-IDF features and Scikit-learn models.
3. **Business workflow**: Convert model predictions into routing recommendations using confidence thresholds, human review rules, and reporting templates.

Week 6 baseline selection is complete, and Week 7 aggregate evaluation is complete with a selected-baseline per-category classification report, row-normalized confusion matrix, and aggregate error analysis. The Week 7 notebook saves the selected fitted pipeline locally to `models/best_tfidf_classifier.joblib`. The artifact is intentionally excluded from Git and is not included in the repository. Routing-confidence rules and 2025 out-of-time validation remain pending, and these internal development results do not establish production readiness.

## Tech Stack

- Python
- Pandas
- Requests
- Jupyter Notebook
- Scikit-learn
- TF-IDF
- GitHub Actions
- CFPB API

The notebook-driven workflow is complete through Week 7: data preparation and EDA, the first Logistic Regression baseline, a three-model Scikit-learn comparison, Version 1 baseline selection, and aggregate evaluation. The `src/` directory still contains placeholders or empty scaffolding for training, prediction, and routing, so it does not yet provide a complete reusable training or inference application.

## Current Status

- Week 1 setup: completed.
- Week 2 CFPB raw data download and validation: completed.
- Dataset sampling upgrade: separate 2024 and 2025 monthly-balanced + daily-stratified samples completed locally.
- Business solution framework documentation: added as a project structure update.
- Week 3 text cleaning and target label preparation: completed.
- Week 4 EDA and product category exploration: completed.
- Week 5 initial TF-IDF + Logistic Regression baseline: completed.
- Week 6 Scikit-learn model comparison and Version 1 baseline selection: completed.
- Week 7 final category-level evaluation, confusion matrix, aggregate error analysis, and local fitted pipeline: completed.
- Week 8 decision-score/confidence-based routing and human-review rules: next step.
- Week 9 final README and portfolio summary: planned.
- 2025 out-of-time validation: future work in a separate dedicated task.
- Version 2 DistilBERT experimentation: optional future work.

## Version 1 Baseline Results

Week 6 compared TF-IDF + Logistic Regression, TF-IDF + Multinomial Naive Bayes, and TF-IDF + Linear SVM using the same modeling scope, feature settings, and stratified internal 2024 train/test split. Linear SVM was the selected Version 1 baseline among the three Scikit-learn models tested on the internal 2024 split.

| Metric | Value |
| --- | ---: |
| Accuracy | 0.9085 |
| Macro F1 | 0.7880 |
| Weighted F1 | 0.9095 |

The evaluation used 9,840 internal 2024 test rows across eight product categories. These are internal development results, not evidence of production readiness or 2025 performance. Detailed category-level results remain in the evaluation reports rather than this README.

## Current Project Proof

The project has completed setup, CFPB data preparation, EDA, baseline comparison and selection, and aggregate evaluation through Week 7.

The current proof image shows an aggregate-only summary of the prepared 2024 CFPB modeling dataset, including row count, product labels, data-quality checks, and product-category distribution.

![Data preparation proof](reports/figures/data_preparation_proof.png)

Week 4 EDA proof artifacts:

- [Product distribution chart](reports/figures/product_distribution.png)
- [Text length distribution chart](reports/figures/text_length_distribution.png)

### Week 7 Evaluation

![Row-normalized confusion matrix](reports/figures/confusion_matrix.png)

- [Results summary](reports/results_summary.md)
- [Aggregate error analysis](reports/error_analysis.md)

## Dataset Design Summary

Dataset source: Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database.

The project uses complaint records with public consumer complaint narratives from the CFPB API.

- Input text column: `complaint_what_happened`
- Target label column: `product`

| Dataset | Purpose | Rows | Date range | Notes |
| --- | ---: | ---: | --- | --- |
| 2024 CFPB sample | Model development | 50,000 | 2024-01-01 to 2024-12-31 | Model development and internal testing |
| 2025 CFPB sample | Future holdout | 50,000 | 2025-01-01 to 2025-12-31 | Out-of-time validation |

Detailed monthly and daily validation results are documented in `docs/data_ingestion.md`.

## Data Decisions and Quality Notes

This project documents data decisions and quality risks in addition to reporting accuracy and F1 scores. The detailed notes cover the CFPB source, 2024 model-development data, separation of the 2025 out-of-time holdout, text cleaning, missing narratives, product labels, class imbalance, possible label noise, limitations of historical complaint categories, and future data drift.

[Data Decisions and Data Quality Notes](docs/data_decisions.md)

## Repository Structure

```text
.
|-- assets/                         # Placeholder for future diagrams or presentation assets
|-- data/
|   |-- raw/                        # Local-only raw CFPB data, ignored except .gitkeep
|   `-- processed/                  # Local-only processed data, ignored except .gitkeep
|-- docs/
|   |-- business_case.md            # Business problem, users, workflow, and limitations
|   |-- data_decisions.md           # Data decisions, quality risks, label limitations, and drift notes
|   |-- data_ingestion.md           # CFPB data-ingestion design and validation details
|   |-- modeling_plan.md            # Planned modeling and evaluation approach
|   `-- system_design.md            # Architecture and data flow
|-- models/                         # Local-only model artifacts, ignored except .gitkeep
|-- notebooks/
|   |-- 01_data_download.ipynb      # 2024/2025 CFPB raw data download and validation workflow
|   |-- 02_eda_cleaning.ipynb       # Week 3 text cleaning and target-label preparation
|   |-- 03_data_quality_product_distribution.ipynb # Week 4 data quality, product distribution, and text length EDA
|   `-- 04_sklearn_baseline_model.ipynb # Week 5-7 modeling, comparison, selection, and evaluation
|-- reports/
|   |-- figures/
|   |   |-- confusion_matrix.png      # Week 7 row-normalized confusion matrix
|   |   |-- data_preparation_proof.png # Aggregate-only Week 3 data-preparation proof
|   |   |-- product_distribution.png # Week 4 product distribution chart
|   |   `-- text_length_distribution.png # Week 4 text length distribution chart
|   |-- error_analysis.md           # Completed Week 7 aggregate error analysis
|   |-- model_card.md               # Model-documentation template; final synchronization pending
|   `-- results_summary.md          # Week 4-7 EDA, model comparison, and evaluation results
|-- src/
|   |-- clean_text.py               # Empty scaffold for future text-cleaning utilities
|   |-- download_data.py            # Reusable CFPB sampling, validation, and raw CSV helper functions
|   |-- predict.py                  # Prediction interface placeholder pending dedicated work
|   |-- routing_rules.py            # Routing policy placeholder pending Week 8 validation
|   `-- train_baseline.py           # Empty scaffold for future reusable training utilities
|-- requirements.txt
`-- README.md
```

## Data Safety Notes

- Raw CFPB CSV files are local-only and ignored by Git.
- Processed data and model artifacts are local-only.
- Do not upload raw complaint files or complaint narrative examples to GitHub.
- 2025 remains separate for future out-of-time validation.

Longer ingestion and raw-data handling notes are documented in `docs/data_ingestion.md`.

## Roadmap / Next Steps

- Complete Week 8 decision-score/confidence-based routing and human-review rules.
- Measure auto-routing coverage and the human-review rate after routing thresholds are defined and validated.
- Complete the Week 9 final README and portfolio summary.
- Run dedicated future 2025 out-of-time validation without using the holdout for training or model selection.
- Synchronize the final model card after the remaining evaluation and routing work.
- Optionally experiment with DistilBERT as a Version 2 model.


## Limitations

- The 2024 and 2025 datasets are sampled from the CFPB database, not the full CFPB database.
- Within each daily window, CFPB API pagination may still reflect the API sort order rather than fully random selection.
- The 2025 dataset is reserved for future out-of-time validation and should not be used for model training or model selection.
- Linear SVM decision scores are not calibrated probabilities, and routing thresholds have not yet been validated.
- Smaller product categories have lower support and therefore less stable performance estimates.
- Complaint narratives can be sensitive, even when sourced from public data, so any production workflow would require stronger privacy, access control, monitoring, and governance.
- Automated routing should support human review, not replace it, especially for low-confidence, ambiguous, regulated, or high-risk complaints.
