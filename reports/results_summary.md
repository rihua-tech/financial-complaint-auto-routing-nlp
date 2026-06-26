# Results Summary

Status: Week 6 Scikit-learn baseline comparison completed. Future 2025 out-of-time validation, routing-confidence rules, and production readiness remain pending.

## Executive Summary

Week 6 compared three Scikit-learn TF-IDF baseline classifiers for complaint product classification: Logistic Regression, Multinomial Naive Bayes, and Linear SVM. Based only on the internal 2024 test split, TF-IDF + Linear SVM is the selected Version 1 baseline among these three models. This is not production readiness and does not include 2025 out-of-time validation.

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

## Week 6 Model Comparison: Scikit-learn Baselines

Dataset used: `data/processed/cfpb_complaints_2024_cleaned.csv`

Modeling scope: cleaned 2024 data only, filtered to product classes with at least 500 complaints. The 2025 holdout dataset was not loaded or used.

Models compared:

- TF-IDF + Logistic Regression.
- TF-IDF + Multinomial Naive Bayes.
- TF-IDF + Linear SVM.

Train/test split summary:

- Rows used after filtering: 49,196
- Selected product classes: 8
- Training rows: 39,356
- Test rows: 9,840
- Split: 80/20 train/test split with `stratify=y`, `test_size=0.20`, and `random_state=42`
- TF-IDF settings: `max_features=50000`, `ngram_range=(1, 2)`, `min_df=2`

Week 6 comparison metrics:

| Model | Accuracy | Macro precision | Macro recall | Macro F1 | Weighted precision | Weighted recall | Weighted F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TF-IDF + Logistic Regression | 0.8622 | 0.6803 | 0.8080 | 0.7332 | 0.8885 | 0.8622 | 0.8703 |
| TF-IDF + Multinomial Naive Bayes | 0.8516 | 0.8485 | 0.4035 | 0.4025 | 0.8641 | 0.8516 | 0.8307 |
| TF-IDF + Linear SVM | 0.9088 | 0.7910 | 0.7868 | 0.7877 | 0.9116 | 0.9088 | 0.9098 |

Best Version 1 baseline among these three models: TF-IDF + Linear SVM.

Rationale: Linear SVM produced the strongest balance of macro F1 and weighted F1 on the internal 2024 test split. Macro F1 matters because smaller product classes should not be ignored in complaint routing, while weighted F1 matters because overall routing volume is dominated by larger product classes. This selection is limited to the three Scikit-learn baselines tested here and should not be treated as production readiness, 2025 out-of-time validation, or final project model selection.

## Models Evaluated

Completed so far:

- TF-IDF + Logistic Regression: completed.
- TF-IDF + Naive Bayes: completed.
- TF-IDF + Linear SVM: completed.

## Evaluation Results

Week 6 internal 2024 test-set results are available below. These results support a Version 1 baseline choice among three Scikit-learn models only; they are not production readiness or 2025 out-of-time validation.

| Model | Accuracy | Macro precision | Macro recall | Macro F1 | Weighted precision | Weighted recall | Weighted F1 | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| TF-IDF + Logistic Regression | 0.8622 | 0.6803 | 0.8080 | 0.7332 | 0.8885 | 0.8622 | 0.8703 | Week 5 first baseline |
| TF-IDF + Naive Bayes | 0.8516 | 0.8485 | 0.4035 | 0.4025 | 0.8641 | 0.8516 | 0.8307 | Fast probabilistic baseline, but weak macro recall |
| TF-IDF + Linear SVM | 0.9088 | 0.7910 | 0.7868 | 0.7877 | 0.9116 | 0.9088 | 0.9098 | Selected Version 1 baseline among these three |

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
- Week 6 compared three Scikit-learn TF-IDF baselines on the same internal 2024 train/test split.
- TF-IDF + Linear SVM achieved the strongest overall comparison results: 0.9088 accuracy, 0.7877 macro F1, and 0.9098 weighted F1.
- TF-IDF + Multinomial Naive Bayes had high macro precision but much weaker macro recall, making it less suitable as the Version 1 routing baseline.
- The selected best Version 1 baseline is based only on the internal 2024 test split.
- These results are not production readiness and do not include 2025 out-of-time validation.

## Recommended Next Steps

- Use Week 7 for evaluation visuals and saving the selected baseline model, if Issue #7 requires those deliverables.
- Review per-class performance and class imbalance behavior in the correct evaluation issue.
- Add confusion matrix and evaluation visuals only if the correct later issue requires them.
- Keep the 2025 dataset separate for future out-of-time validation.
- Do not create routing-confidence rules until the routing issue.
