[![CI](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml)

# Financial Complaint Auto-Routing with NLP

## Project Overview

This repository is a business-oriented AI/NLP solution framework for routing consumer financial complaints to the appropriate product or operations team. It uses public CFPB consumer complaint data and focuses on classifying complaint narratives into financial product categories.

The project is structured around an end-to-end business workflow:

`business problem -> data workflow -> model workflow -> evaluation results -> routing policy -> human review rules -> deliverables`

This repository is organized as a business solution framework rather than only a basic class-project layout. At the current project stage, Week 3 EDA, model training, and model performance reporting are not completed yet.

## Business Problem

Financial institutions, fintech companies, customer support teams, and compliance groups receive large volumes of written complaints. Manual triage can be slow, inconsistent, and difficult to scale. A complaint may need to be routed to a mortgage, credit card, bank account, debt collection, credit reporting, or loan servicing team.

This project simulates an NLP-assisted routing workflow that predicts a complaint product category from the consumer narrative. The prediction can help prioritize routing, reduce manual review effort, and create a structured audit trail for complaint operations.

## Business Users

Intended users include:

- Customer support operations teams that triage inbound complaints.
- Compliance teams that monitor complaint handling and escalation.
- Fintech and banking product operations teams that receive routed cases.
- Risk and analytics teams that track complaint trends and model performance.
- Business stakeholders who need transparent reporting on automation coverage and review volume.

## Business Value

The planned solution is designed to support:

- Faster initial complaint triage.
- More consistent routing recommendations across complaint channels.
- Better visibility into complaint category volume.
- Reduced manual effort for high-confidence, routine routing decisions.
- Human review for low-confidence or ambiguous cases.
- A repeatable evaluation process for model quality and operational readiness.

## Solution Overview

The solution framework has three layers:

1. **Data workflow**: Download and validate public CFPB complaint records, then prepare complaint narratives and product labels for analysis.
2. **Model workflow**: Train baseline NLP classifiers using TF-IDF features and Scikit-learn models, then evaluate model performance.
3. **Business workflow**: Convert model predictions into routing recommendations with confidence thresholds, human review rules, and reporting templates.

No trained model artifacts are currently included in the repository.

## End-to-End Workflow

1. **Business intake**: Define the routing problem, users, operational assumptions, and model decision boundaries.
2. **Data ingestion**: Download public CFPB complaint records locally through the Week 1 and Week 2 workflow.
3. **Data validation**: Check required fields, record counts, duplicate complaint IDs, missing narratives, and missing labels.
4. **EDA and cleaning**: Planned for Week 3 and not completed yet.
5. **Baseline modeling**: Planned TF-IDF models include Logistic Regression, Naive Bayes, and Linear SVM.
6. **Evaluation**: Planned evaluation includes accuracy, macro F1, weighted F1, per-class metrics, and a confusion matrix.
7. **Routing decision**: Planned routing rules will use predicted label, confidence, and prediction margin to decide whether to auto-route or send to human review.
8. **Human review**: Low-confidence, ambiguous, missing, or unsupported predictions should remain in a manual review queue.
9. **Reporting**: Results, error analysis, and model-card reports will be completed only after model training and evaluation.

## Current Status

- Week 1 setup: completed.
- Week 2 CFPB raw data download and validation: completed.
- Business solution framework documentation: added as a project structure update.
- Week 3 EDA and cleaning: planned and not completed yet.
- Version 1 Scikit-learn baseline: planned.
- Version 2 DistilBERT transformer upgrade: future work.

No EDA results, cleaned dataset, feature engineering results, trained model scores, charts, confusion matrices, or completed model evaluation results are reported yet.

## Dataset

Dataset source: Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database.

The project uses complaint records with public consumer complaint narratives from the CFPB API.

- Input text column: `complaint_what_happened`
- Target label column: `product`
- Raw local file: `data/raw/cfpb_complaints_2024_raw.csv`

The raw CSV is downloaded locally by `notebooks/01_data_download.ipynb`. It is not included in this repository and should not be uploaded to GitHub.

## Current Dataset Snapshot

The Week 2 raw download produced the following local dataset snapshot:

- Rows: 50,000
- Raw API columns: 17
- Product classes: 11
- Date range: 2024-12-11 to 2024-12-31
- Rows outside calendar year 2024: 0
- Missing or empty complaint narratives: 0
- Missing or empty product labels: 0
- Duplicate `complaint_id` values: 0

Important sampling note: the CFPB API returns records sorted newest first. This 50,000-row dataset is a late-2024 newest-first API sample, not a full-year random sample.

## Planned Deliverables

Planned deliverables include:

- Business case documentation.
- System design documentation.
- Modeling plan for baseline NLP classifiers.
- Week 3 EDA and cleaning notebook updates.
- Baseline model training notebook and supporting code.
- Results summary report after model training.
- Error analysis report after model evaluation.
- Model card after baseline model selection.
- Lightweight prediction and routing framework code.
- Final presentation or summary report for business stakeholders.

Reports in `reports/` are templates until model training and evaluation are completed.

## Repository Structure

```text
.
|-- assets/                         # Placeholder for future diagrams or presentation assets
|-- data/
|   |-- raw/                        # Local-only raw CFPB data, ignored except .gitkeep
|   `-- processed/                  # Local-only processed data, ignored except .gitkeep
|-- docs/
|   |-- business_case.md            # Business problem, users, workflow, and limitations
|   |-- modeling_plan.md            # Planned modeling and evaluation approach
|   `-- system_design.md            # Architecture and data flow
|-- models/                         # Local-only model artifacts, ignored except .gitkeep
|-- notebooks/
|   |-- 01_data_download.ipynb      # Completed Week 2 download workflow
|   |-- 02_eda_cleaning.ipynb       # Planned Week 3 EDA and cleaning
|   `-- 03_sklearn_baseline_model.ipynb
|-- reports/
|   |-- error_analysis.md           # Template, pending model evaluation
|   |-- model_card.md               # Template, pending model evaluation
|   `-- results_summary.md          # Template, pending model evaluation
|-- src/
|   |-- clean_text.py               # Placeholder for text cleaning utilities
|   |-- download_data.py            # Placeholder for download utilities
|   |-- predict.py                  # Lightweight prediction interface placeholder
|   |-- routing_rules.py            # Lightweight routing policy placeholder
|   `-- train_baseline.py           # Placeholder for baseline training utilities
|-- requirements.txt
`-- README.md
```

## Data Safety Notes

This repository preserves the existing data safety policy:

- Raw CFPB CSV files are local only and must not be committed.
- Processed data files are local only and must not be committed.
- CSV files are ignored globally through `.gitignore`.
- Saved model artifacts are ignored through `.gitignore`.
- Do not add complaint narrative samples to documentation or reports.
- Do not upload raw CFPB complaint files to GitHub.

The repository tracks only code, notebooks, documentation, templates, and placeholder files needed to reproduce the workflow.

## Limitations

- The current local raw dataset is a late-2024 newest-first API sample, not a full-year random sample.
- Week 3 EDA and cleaning are not complete yet.
- No baseline model has been trained yet.
- No model scores, charts, confusion matrices, or production readiness claims are available yet.
- Complaint narratives can be sensitive, even when sourced from public data. Any production workflow would require stronger privacy, access control, retention, monitoring, and governance controls.
- Automated routing should support, not replace, human review for ambiguous, low-confidence, regulated, or high-risk complaints.
