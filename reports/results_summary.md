# Results Summary

Status: Week 7 evaluation outputs completed for the selected Version 1 baseline. Future 2025 out-of-time validation, routing-confidence rules, and production readiness remain pending.

## Executive Summary

Week 6 compared three Scikit-learn TF-IDF baseline classifiers for complaint product classification: Logistic Regression, Multinomial Naive Bayes, and Linear SVM. Based only on the internal 2024 test split, TF-IDF + Linear SVM is the selected Version 1 baseline among these three models. Week 7 generated its final classification report, row-normalized confusion matrix, aggregate error analysis, and a local ignored model artifact. This is not production readiness, final project model selection, or 2025 out-of-time validation.

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
| Macro precision | 0.6809 |
| Macro recall | 0.8101 |
| Macro F1 | 0.7344 |
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
| TF-IDF + Logistic Regression | 0.8622 | 0.6809 | 0.8101 | 0.7344 | 0.8885 | 0.8622 | 0.8703 |
| TF-IDF + Multinomial Naive Bayes | 0.8513 | 0.8486 | 0.4025 | 0.4008 | 0.8637 | 0.8513 | 0.8302 |
| TF-IDF + Linear SVM | 0.9085 | 0.7915 | 0.7869 | 0.7880 | 0.9114 | 0.9085 | 0.9095 |

Best Version 1 baseline among these three models: TF-IDF + Linear SVM.

Rationale: Linear SVM produced the strongest balance of macro F1 and weighted F1 on the internal 2024 test split. Macro F1 matters because smaller product classes should not be ignored in complaint routing, while weighted F1 matters because overall routing volume is dominated by larger product classes. This selection is limited to the three Scikit-learn baselines tested here and should not be treated as production readiness, 2025 out-of-time validation, or final project model selection.

## Week 7 Final Evaluation: TF-IDF + Linear SVM

Week 7 evaluated the selected Version 1 baseline on the same unchanged internal 2024 test split used in Weeks 5 and 6.

- Dataset: `data/processed/cfpb_complaints_2024_cleaned.csv`.
- Modeling scope: product classes with at least 500 complaints.
- Training rows: 39,356.
- Test rows: 9,840.
- Product categories: 8.
- Split: `test_size=0.20`, `random_state=42`, and `stratify=y`.
- 2025 holdout data: not loaded or used.

Final aggregate metrics:

| Metric | Value |
| --- | ---: |
| Accuracy | 0.9085 |
| Macro precision | 0.7915 |
| Macro recall | 0.7869 |
| Macro F1 | 0.7880 |
| Weighted precision | 0.9114 |
| Weighted recall | 0.9085 |
| Weighted F1 | 0.9095 |

Final classification report by product category:

| Product category | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Credit reporting or other personal consumer reports | 0.9663 | 0.9484 | 0.9573 | 7,226 |
| Debt collection | 0.7544 | 0.8312 | 0.7909 | 1,072 |
| Credit card | 0.7452 | 0.7806 | 0.7625 | 547 |
| Checking or savings account | 0.7554 | 0.8205 | 0.7866 | 429 |
| Mortgage | 0.8802 | 0.8305 | 0.8547 | 177 |
| Money transfer, virtual currency, or money service | 0.7323 | 0.6414 | 0.6838 | 145 |
| Student loan | 0.8217 | 0.8413 | 0.8314 | 126 |
| Vehicle loan or lease | 0.6762 | 0.6017 | 0.6368 | 118 |

The strongest per-category F1 scores are for Credit reporting or other personal consumer reports (0.9573), Mortgage (0.8547), and Student loan (0.8314). The weakest are Vehicle loan or lease (0.6368) and Money transfer, virtual currency, or money service (0.6838).

The row-normalized confusion matrix is saved at [`reports/figures/confusion_matrix.png`](figures/confusion_matrix.png). Important error patterns include Debt collection being predicted as Credit reporting or other personal consumer reports in 12.69% of its test cases, Money transfer being predicted as Checking or savings account in 26.90%, and Vehicle loan or lease being predicted as Credit reporting or other personal consumer reports in 22.88%. Full aggregate notes are in [`reports/error_analysis.md`](error_analysis.md).

The selected fitted pipeline was saved locally to `models/best_tfidf_classifier.joblib`. The artifact is approximately 3.21 MB and is excluded from Git by both `models/*` and `*.joblib` ignore rules.

These results use only the internal 2024 test split. They do not establish production readiness, final project model selection, or 2025 out-of-time performance.

## Models Evaluated

Completed so far:

- TF-IDF + Logistic Regression: completed.
- TF-IDF + Naive Bayes: completed.
- TF-IDF + Linear SVM: completed and selected as the Version 1 baseline among these three models.

## Evaluation Results

Week 6 internal 2024 test-set results are available below. These results support a Version 1 baseline choice among three Scikit-learn models only; they are not production readiness or 2025 out-of-time validation.

| Model | Accuracy | Macro precision | Macro recall | Macro F1 | Weighted precision | Weighted recall | Weighted F1 | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| TF-IDF + Logistic Regression | 0.8622 | 0.6809 | 0.8101 | 0.7344 | 0.8885 | 0.8622 | 0.8703 | Week 5 first baseline |
| TF-IDF + Naive Bayes | 0.8513 | 0.8486 | 0.4025 | 0.4008 | 0.8637 | 0.8513 | 0.8302 | Fast probabilistic baseline, but weak macro recall |
| TF-IDF + Linear SVM | 0.9085 | 0.7915 | 0.7869 | 0.7880 | 0.9114 | 0.9085 | 0.9095 | Selected Version 1 baseline among these three |

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
- TF-IDF + Linear SVM achieved the strongest overall comparison results: 0.9085 accuracy, 0.7880 macro F1, and 0.9095 weighted F1.
- TF-IDF + Multinomial Naive Bayes had high macro precision but much weaker macro recall, making it less suitable as the Version 1 routing baseline.
- The selected best Version 1 baseline is based only on the internal 2024 test split.
- Week 7 generated the final per-category classification report and a row-normalized confusion matrix for TF-IDF + Linear SVM.
- Credit reporting or other personal consumer reports, Mortgage, and Student loan produced the highest per-category F1 scores.
- Vehicle loan or lease and Money transfer, virtual currency, or money service produced the lowest per-category F1 scores.
- The saved fitted pipeline remains a local ignored artifact under `models/`.
- These results are not production readiness and do not include 2025 out-of-time validation.

## Recommended Next Steps

- Use the aggregate confusion patterns to prioritize future review of lower-support categories.
- Keep the 2025 dataset separate for future out-of-time validation.
- Evaluate model behavior on the 2025 holdout only in the dedicated out-of-time validation task.
- Do not create routing-confidence rules until the dedicated routing issue.
- Treat calibration, monitoring, and human-review thresholds as future work before any production-readiness assessment.
