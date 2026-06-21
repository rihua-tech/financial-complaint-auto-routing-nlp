# Results Summary

Status: Week 4 EDA completed. Baseline model training and evaluation sections remain templates.

## Executive Summary

To be completed after baseline model training.

## Dataset Used

The modeling dataset for Version 1 is `data/processed/cfpb_complaints_2024_cleaned.csv`. It was created from the 2024 CFPB complaint data during Week 3 cleaning.

The dataset contains only the modeling columns `clean_complaint_text` and `product`. Raw and processed CSV files remain local-only and are not committed. The 2025 dataset remains separate for future out-of-time validation.

## Week 4 EDA: Data Quality and Product Distribution

Dataset used: `data/processed/cfpb_complaints_2024_cleaned.csv`

The cleaned 2024 modeling dataset contains 50,000 rows and 11 product classes. The required modeling columns are present: `clean_complaint_text` and `product`.

Missing value summary:

- Missing `clean_complaint_text`: 0
- Missing `product`: 0
- Empty cleaned text values: 0

Duplicate row count: 16,006.

Top product categories:

| Product | Count | Percentage |
| --- | ---: | ---: |
| Credit reporting or other personal consumer reports | 36,128 | 72.26% |
| Debt collection | 5,357 | 10.71% |
| Credit card | 2,735 | 5.47% |
| Checking or savings account | 2,146 | 4.29% |
| Mortgage | 887 | 1.77% |

Text length summary:

- Mean word count: 182.13
- Median word count: 117
- Minimum word count: 1
- Maximum word count: 5,853
- Mean character length: 1,051.42
- Median character length: 679
- Minimum character length: 10
- Maximum character length: 32,550

Class imbalance note: the largest category, `Credit reporting or other personal consumer reports`, represents 72.26% of the prepared 2024 dataset. Several product categories each represent less than 2% of records.

Version 1 modeling scope recommendation: because the product distribution is highly imbalanced, Version 1 should start with the strongest product categories rather than all classes. A practical first option is to use categories with enough examples for stable baseline training, such as categories with at least 500 complaints. The final class selection should be confirmed in Week 5 before model training. The full cleaned 2024 dataset should remain available locally for later experiments, and the 2025 dataset should remain separate for future out-of-time validation.

## Models Evaluated

To be completed after baseline model training.

Planned models:

- TF-IDF + Logistic Regression.
- TF-IDF + Naive Bayes.
- TF-IDF + Linear SVM.

## Evaluation Results

No model results are available yet.

| Model | Accuracy | Macro F1 | Weighted F1 | Notes |
| --- | --- | --- | --- | --- |
| TF-IDF + Logistic Regression | TBD | TBD | TBD | To be completed after training |
| TF-IDF + Naive Bayes | TBD | TBD | TBD | To be completed after training |
| TF-IDF + Linear SVM | TBD | TBD | TBD | To be completed after training |

## Business Routing Metrics

To be completed after model predictions and routing thresholds are available.

Planned metrics:

- Auto-routing coverage.
- Human review rate.
- Low-confidence case rate.
- Top-3 prediction usefulness.
- Misroute risk indicators.

## Key Findings

To be completed after evaluation.

## Recommended Next Steps

To be completed after evaluation.
