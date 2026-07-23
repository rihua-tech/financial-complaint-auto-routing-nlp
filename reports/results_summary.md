# Results Summary

Status: Corrected Version 1 internal evaluation and Week 8 decision-score routing analysis are completed and documented. Dedicated 2025 out-of-time validation remains pending.

## Executive Summary

The original Week 5–7 row-level split allowed identical normalized complaint texts to appear in both training and test data. An aggregate audit found that 3,876 of 9,840 original test rows (39.39%) shared normalized text with training. Those original internal metrics are superseded because they were affected by duplicate-text leakage.

The corrected workflow removes repeated same-label text rows, excludes normalized-text groups with conflicting product labels, and uses group-aware splitting throughout. Logistic Regression, Multinomial Naive Bayes, and Linear SVM were compared using five-fold group-aware cross-validation on development data only. Linear SVM remained the selected Version 1 baseline. It was then fitted on all development rows and evaluated once on the untouched final internal test fold.

Corrected final internal test results are 0.8712 accuracy, 0.7671 macro F1, and 0.8715 weighted F1. Week 8 then used development out-of-fold decision scores to select an internal human-review policy before applying it once to the untouched final test set. These remain internal 2024 results, not production-readiness evidence or 2025 performance.

## Dataset and Locked Scope

- Local dataset: `data/processed/cfpb_complaints_2024_cleaned.csv`.
- Total prepared 2024 rows: 50,000.
- Required columns: `clean_complaint_text` and `product`.
- Locked Version 1 scope: the same eight product categories used in the original comparison.
- 2025 holdout: not loaded or used.

The eight locked categories remained viable after remediation. The smallest retained category contained 579 rows, above the original 500-row modeling-scope floor.

## Duplicate-Leakage Audit

A stable SHA-256 hash of normalized cleaned text was used only as an internal grouping identifier. Normalization converted text to string, trimmed surrounding whitespace, and collapsed repeated whitespace. Complaint narratives and row-level prediction exports were not displayed or committed.

| Audit measure | Count |
| --- | ---: |
| Total 2024 rows | 50,000 |
| Exact duplicate rows | 16,006 |
| Normalized text-and-label duplicate rows | 16,006 |
| Unique normalized texts | 33,918 |
| Normalized-text groups containing more than one row | 4,158 |
| Normalized-text groups containing conflicting labels | 74 |
| Rows in conflicting-label groups across all 11 categories | 1,781 |
| Original test rows whose normalized text appeared in training | 3,876 of 9,840 (39.39%) |

## Conservative Duplicate Policy

The corrected Version 1 workflow applies this policy before splitting:

1. Exclude every normalized-text group associated with more than one product label.
2. For repeated normalized text with the same product label, retain one representative modeling row.
3. Preserve the locked eight-category Version 1 scope.
4. Keep all complaint narratives and row-level identifiers local-only.

| Remediation measure | Rows |
| --- | ---: |
| Locked-scope rows before remediation | 49,196 |
| Locked-scope rows excluded with conflicting-label groups | 1,780 |
| Repeated same-label rows removed | 14,374 |
| Rows remaining after remediation | 33,042 |
| Unique normalized-text groups remaining | 33,042 |

No conflicting-label groups or repeated normalized-text groups remain in the corrected modeling data.

## Leakage-Safe Split Design

The final internal holdout uses `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)`. Deterministic fold 0 is the untouched final internal test set; the other folds form development data.

- Development rows and unique groups: 26,433.
- Final internal test rows and unique groups: 6,609.
- Development/test normalized-text group overlap: 0.
- Development model-selection folds: 5 group-aware folds.
- Final test metrics used for model selection: no.

All eight expected categories are present in development and final test data.

## Development Cross-Validation Comparison

All values are five-fold development-CV mean ± population standard deviation. Macro F1 is the primary selection metric; weighted F1 is the secondary tie-breaker.

| Model | Accuracy | Macro precision | Macro recall | Macro F1 | Weighted precision | Weighted recall | Weighted F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| TF-IDF + Logistic Regression | 0.8358 ± 0.0030 | 0.7005 ± 0.0059 | 0.7991 ± 0.0102 | 0.7430 ± 0.0066 | 0.8574 ± 0.0016 | 0.8358 ± 0.0030 | 0.8425 ± 0.0028 |
| TF-IDF + Multinomial Naive Bayes | 0.7751 ± 0.0022 | 0.7243 ± 0.0069 | 0.3353 ± 0.0034 | 0.3519 ± 0.0035 | 0.7697 ± 0.0039 | 0.7751 ± 0.0022 | 0.7274 ± 0.0027 |
| TF-IDF + Linear SVM | 0.8735 ± 0.0038 | 0.7750 ± 0.0070 | 0.7655 ± 0.0066 | 0.7687 ± 0.0048 | 0.8745 ± 0.0033 | 0.8735 ± 0.0038 | 0.8736 ± 0.0037 |

Selected Version 1 baseline among these three models: **TF-IDF + Linear SVM**.

## Corrected Final Internal Test Evaluation

After development-only selection, the Linear SVM pipeline was fitted on all 26,433 development rows and evaluated once on the untouched 6,609-row final internal test fold.

| Metric | Value |
| --- | ---: |
| Accuracy | 0.8712 |
| Macro precision | 0.7734 |
| Macro recall | 0.7621 |
| Macro F1 | 0.7671 |
| Weighted precision | 0.8721 |
| Weighted recall | 0.8712 |
| Weighted F1 | 0.8715 |

### Per-Category Results

The category order below comes from the fitted pipeline's `classes_` attribute.

| Product category | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Checking or savings account | 0.7589 | 0.7944 | 0.7763 | 428 |
| Credit card | 0.7293 | 0.7653 | 0.7469 | 507 |
| Credit reporting or other personal consumer reports | 0.9391 | 0.9330 | 0.9360 | 4,328 |
| Debt collection | 0.7332 | 0.7510 | 0.7420 | 783 |
| Money transfer, virtual currency, or money service | 0.6190 | 0.5417 | 0.5778 | 144 |
| Mortgage | 0.8780 | 0.8136 | 0.8446 | 177 |
| Student loan | 0.8455 | 0.8254 | 0.8353 | 126 |
| Vehicle loan or lease | 0.6842 | 0.6724 | 0.6783 | 116 |

The corrected row-normalized confusion matrix is available at [`reports/figures/confusion_matrix.png`](figures/confusion_matrix.png), and aggregate interpretation is documented in [`reports/error_analysis.md`](error_analysis.md).

## Superseded Versus Corrected Results

The two evaluations use different row sets and split methods. The comparison documents the effect of replacing the leakage-affected row-level split; it is not a like-for-like model improvement experiment.

| Metric | Superseded row-level split | Corrected leakage-safe split | Change |
| --- | ---: | ---: | ---: |
| Test rows | 9,840 | 6,609 | -3,231 |
| Accuracy | 0.9085 | 0.8712 | -0.0373 |
| Macro F1 | 0.7880 | 0.7671 | -0.0209 |
| Weighted F1 | 0.9095 | 0.8715 | -0.0380 |

The superseded values should not be used as the current Version 1 results.

## Pipeline Class Order

1. Checking or savings account.
2. Credit card.
3. Credit reporting or other personal consumer reports.
4. Debt collection.
5. Money transfer, virtual currency, or money service.
6. Mortgage.
7. Student loan.
8. Vehicle loan or lease.

Week 8 decision-score columns were mapped using this fitted `classes_` order rather than a frequency-ordered label list.

## Local Model Reproducibility Metadata

The corrected fitted pipeline is saved locally at `models/best_tfidf_classifier.joblib`. It was validated after saving and remains excluded from Git.

| Item | Value |
| --- | --- |
| Python | 3.11.15 |
| Scikit-learn | 1.9.0 |
| Pandas | 3.0.3 |
| NumPy | 2.4.6 |
| Model size | 3,392,109 bytes (3.23 MB) |

## Business Routing Metrics

Week 8 evaluates whether the selected Linear SVM's top decision score and top-two score margin can identify lower-risk automatic-routing candidates. Decision scores and margins are model signals, not calibrated probabilities.

### Development OOF Threshold Selection

The same corrected 26,433-row development set and five `StratifiedGroupKFold` folds were reconstructed with `random_state=42`. For each fold, a cloned copy of the locked TF-IDF + Linear SVM pipeline was fitted on the fold-training rows and used to generate decision scores for the fold-validation rows. Each development row therefore received one out-of-fold prediction without using the final test set.

Score columns were mapped using each fitted pipeline's `classes_` order. For every development row, the analysis calculated the predicted label, top score, second-highest score, top-two margin, and correctness. Row-level scores and predictions remained local-only and were not exported.

Candidate top-score and margin thresholds were derived from two-decimal values at 2.5-percentage-point development OOF quantiles, producing 40 candidates for each threshold and 1,600 threshold pairs. A policy qualified when it met both internal project assumptions:

- Maximum development OOF misroute rate: 5%.
- Minimum development OOF coverage: 5%.

Among 1,379 qualifying candidates, the policy with highest coverage was selected. Ties favored lower misroute rate and then lower thresholds. The selected thresholds were locked before any final-test decision scores were generated.

| Locked routing threshold | Value |
| --- | ---: |
| Minimum top decision score | 0.08 |
| Minimum top-two score margin | 0.73 |

Both thresholds must pass for automatic routing. Invalid or non-finite scores, tied top scores, low top scores, and low margins require human review.

The 5% development rule is an analytical assumption for this college project, not a stakeholder-approved or production-validated risk standard.

### Aggregate Routing Results

| Metric | Development OOF | Untouched final test |
| --- | ---: | ---: |
| Rows | 26,433 | 6,609 |
| Auto-routed rows | 20,170 | 5,092 |
| Human-review rows | 6,263 | 1,517 |
| Auto-routing coverage | 0.7631 | 0.7705 |
| Human-review rate | 0.2369 | 0.2295 |
| Auto-routed accuracy | 0.9506 | 0.9503 |
| Auto-routed misroute rate | 0.0494 | 0.0497 |

The final-test policy was applied once after the thresholds were locked. Its 4.97% aggregate misroute rate is an internal holdout result, not evidence that the same rate will persist across future time periods or operating conditions.

### Final-Test Category-Level Routing Results

| Product category | Support | Auto-routed | Coverage | Review rate | Auto-routed accuracy | Misroute rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Checking or savings account | 428 | 263 | 0.6145 | 0.3855 | 0.9278 | 0.0722 |
| Credit card | 507 | 309 | 0.6095 | 0.3905 | 0.8738 | 0.1262 |
| Credit reporting or other personal consumer reports | 4,328 | 3,719 | 0.8593 | 0.1407 | 0.9796 | 0.0204 |
| Debt collection | 783 | 505 | 0.6450 | 0.3550 | 0.8455 | 0.1545 |
| Money transfer, virtual currency, or money service | 144 | 47 | 0.3264 | 0.6736 | 0.6383 | 0.3617 |
| Mortgage | 177 | 115 | 0.6497 | 0.3503 | 0.9043 | 0.0957 |
| Student loan | 126 | 83 | 0.6587 | 0.3413 | 0.9518 | 0.0482 |
| Vehicle loan or lease | 116 | 51 | 0.4397 | 0.5603 | 0.8235 | 0.1765 |

The highest observed category-level auto-routed misroute rates were for money transfer/virtual currency/money service, vehicle loan or lease, debt collection, and credit card. These results show that meeting a 5% aggregate development target does not guarantee a 5% rate within every category. Smaller auto-routed counts also make category estimates less stable.

The aggregate visualization is available at [`reports/figures/routing_decision_score_summary.png`](figures/routing_decision_score_summary.png).

The completed intended-use, oversight, and monitoring documentation is available in the [`reports/model_card.md`](model_card.md).

## Limitations and Next Steps

- The corrected results still use an internal 2024 sample and do not establish production readiness.
- The dominant credit-reporting category strongly influences weighted metrics.
- Smaller categories have lower final-test support and less stable estimates.
- Linear SVM decision scores and score margins are not calibrated probabilities.
- The routing thresholds and 5% development rule are not production validated or business approved.
- Aggregate routing performance masks materially higher observed misroute rates in several categories.
- The 2025 dataset remains reserved for dedicated future out-of-time validation and was not loaded or used here.
