# Results Summary

Status: Week 5 TF-IDF + Logistic Regression baseline completed. Future model comparison and final model selection remain pending.

## Executive Summary

Week 5 completed the first working baseline model for complaint product classification: TF-IDF text features with Logistic Regression. This is an initial baseline only, not final model selection.

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

Version 1 modeling scope recommendation: because the product distribution is highly imbalanced, Version 1 should start with the strongest product categories rather than all classes. A practical first option is to use categories with enough examples for stable baseline training, such as categories with at least 500 complaints. Week 5 used a practical first baseline scope of product classes with at least 500 complaints. Future modeling work can revisit the class scope after baseline comparisons. The full cleaned 2024 dataset should remain available locally for later experiments, and the 2025 dataset should remain separate for future out-of-time validation.

## Week 5 Baseline: TF-IDF + Logistic Regression

Dataset used: `data/processed/cfpb_complaints_2024_cleaned.csv`

Modeling scope: cleaned 2024 data only, filtered to product classes with at least 500 complaints. This keeps the first baseline focused on stronger product categories while the full cleaned 2024 dataset remains available locally for later experiments.

- Rows used after filtering: 49,196
- Selected product classes: 8
- Training rows: 39,356
- Test rows: 9,840
- Split: 80/20 train/test split with `stratify=y` and `random_state=42`

Pipeline summary:

- `TfidfVectorizer(max_features=50000, ngram_range=(1, 2), min_df=2)`
- `LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)`

Week 5 baseline metrics:

| Metric | Value |
| --- | ---: |
| Accuracy | 0.8622 |
| Macro precision | 0.6803 |
| Macro recall | 0.8080 |
| Macro F1 | 0.7332 |
| Weighted precision | 0.8885 |
| Weighted recall | 0.8622 |
| Weighted F1 | 0.8703 |

Class imbalance note: even after filtering to classes with at least 500 complaints, the dataset remains imbalanced. The largest selected category, `Credit reporting or other personal consumer reports`, still represents most records in the modeling subset.

This result is a baseline only and should not be treated as final model selection. The 2025 dataset remains separate for future out-of-time validation.

## Models Evaluated

Completed so far:

- TF-IDF + Logistic Regression.

Planned future comparisons:

- TF-IDF + Naive Bayes.
- TF-IDF + Linear SVM.

## Evaluation Results

Week 5 baseline test-set results are available below. Future baseline comparisons remain pending, and these results are not final model selection.

| Model | Accuracy | Macro F1 | Weighted F1 | Notes |
| --- | --- | --- | --- | --- |
| TF-IDF + Logistic Regression | 0.8622 | 0.7332 | 0.8703 | Week 5 first baseline; not final model selection |
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

- Week 5 established the first working TF-IDF + Logistic Regression baseline.
- The model achieved 0.8622 accuracy and 0.8703 weighted F1 on the internal 2024 test split.
- Macro F1 was lower at 0.7332, showing that smaller classes remain more challenging.
- These are baseline results only, not final model selection.

## Recommended Next Steps

- Compare additional Scikit-learn baseline classifiers in Week 6.
- Review per-class performance and class imbalance behavior.
- Add confusion matrix and evaluation visuals only in the correct later issue.
- Keep the 2025 dataset separate for future out-of-time validation.
- Do not create routing-confidence rules until the routing issue.
