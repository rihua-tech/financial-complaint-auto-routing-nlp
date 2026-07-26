# Results Summary

Status: Corrected Version 1 internal evaluation, decision-score routing analysis, and locked 2025 out-of-time validation are completed and documented.

## Executive Summary

The original Week 5–7 row-level split allowed identical normalized complaint texts to appear in both training and test data. An aggregate audit found that 3,876 of 9,840 original test rows (39.39%) shared normalized text with training. Those original internal metrics are superseded because they were affected by duplicate-text leakage.

The corrected workflow removes repeated same-label text rows, excludes normalized-text groups with conflicting product labels, and uses group-aware splitting throughout. Logistic Regression, Multinomial Naive Bayes, and Linear SVM were compared using five-fold group-aware cross-validation on development data only. Linear SVM remained the selected Version 1 baseline. It was then fitted on all development rows and evaluated once on the untouched final internal test fold.

Corrected final internal test results are 0.8712 accuracy, 0.7671 macro F1, and 0.8715 weighted F1. Development out-of-fold decision scores were then used to select an internal human-review policy before applying it once to the final internal test. These 2024 results remain the locked temporal reference rather than being replaced by the later holdout evaluation.

The committed two-phase protocol then evaluated the unchanged Version 1 workflow on 2025 data. The 30,156-row primary leakage-resistant cohort is the official headline result: accuracy was 0.8315, Macro F1 was 0.7527, and Weighted F1 was 0.8306. Routing coverage was 0.7251 with 0.9203 auto-routed accuracy and a 0.0797 misroute rate. These results show weaker primary out-of-time generalization than the locked 2024 reference. The 49,225-row secondary operational cohort is reported only as a sensitivity view because it retains repeated texts and cross-year overlap.

## Dataset and Locked Scope

- Local dataset: `data/processed/cfpb_complaints_2024_cleaned.csv`.
- Total prepared 2024 rows: 50,000.
- Required columns: `clean_complaint_text` and `product`.
- Locked Version 1 scope: the same eight product categories used in the original comparison.
- 2025 out-of-time source: 50,000 raw rows evaluated once under the committed locked protocol.

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

## Completed 2025 Out-of-Time Validation

The 2025 evaluation followed [`reports/2025_validation_protocol.md`](2025_validation_protocol.md). Before the CSV was opened, the saved model and both reference files matched their committed paths, sizes, and SHA-256 fingerprints, the compatible software environment loaded the model without warnings, and the locked 2024 reconstruction reproduced every row count, classification metric, and routing metric. No 2025 result was used to fit, tune, calibrate, select, or modify the model, preprocessing, category scope, `classes_` order, cohort rules, metrics, or routing thresholds.

### Holdout integrity and locked scope

| Validation item | Result |
| --- | ---: |
| Raw rows | 50,000 |
| Raw columns | 17 |
| Date range | 2025-01-01 through 2025-12-31 |
| Rows outside 2025 | 0 |
| Duplicate complaint IDs | 0 |
| Missing or blank required fields | 0 |
| Locked eight-category rows | 49,225 |
| Familiar out-of-scope rows | 775 |
| Familiar out-of-scope labels | 3 |
| Unfamiliar or changed labels | 0 |

The 775 familiar out-of-scope rows consisted of 403 payday/personal-loan rows, 238 prepaid-card rows, and 134 debt-or-credit-management rows. Locked cleaning produced no empty narratives.

### Duplicate, overlap, and cohort audit

| Audit | Unique groups | Affected rows |
| --- | ---: | ---: |
| Overlap with locked 2024 development | 161 | 3,772 |
| Overlap with locked 2024 final internal test | 42 | 1,807 |
| Overlap with either 2024 partition | 203 | 5,579 |
| Repeated same-label groups within 2025 | 5,033 | 23,843 |
| Conflicting-label groups within 2025 | 37 | 1,660 |

The 49,225-row secondary operational cohort retains all otherwise eligible locked-scope rows, including repeated texts and cross-year overlap. It is a sensitivity view. The primary cohort applies the precommitted exclusions in order:

| Primary-cohort stage | Excluded at stage | Remaining |
| --- | ---: | ---: |
| Start with locked-scope rows | 0 | 49,225 |
| Exclude overlap with either 2024 partition | 5,579 | 43,646 |
| Exclude remaining conflicting-label groups | 1,301 | 42,345 |
| Retain the first remaining same-label text | 12,189 | 30,156 |

The resulting 30,156-row primary leakage-resistant cohort has one row per normalized-text group, no conflicting-label group, and no overlap with either 2024 partition. It is the official headline 2025 result.

### Overall classification results

| Cohort | Rows | Accuracy | Macro precision | Macro recall | Macro F1 | Weighted precision | Weighted recall | Weighted F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Locked 2024 final internal test | 6,609 | 0.8712 | 0.7734 | 0.7621 | 0.7671 | 0.8721 | 0.8712 | 0.8715 |
| **2025 primary leakage-resistant** | **30,156** | **0.8315** | **0.7577** | **0.7508** | **0.7527** | **0.8312** | **0.8315** | **0.8306** |
| 2025 secondary sensitivity | 49,225 | 0.8771 | 0.7573 | 0.7592 | 0.7569 | 0.8770 | 0.8771 | 0.8766 |

| Signed comparison (`2025 - 2024`) | Accuracy | Macro F1 | Weighted F1 |
| --- | ---: | ---: | ---: |
| Primary minus locked 2024 | -0.0397 | -0.0145 | -0.0408 |
| Secondary minus locked 2024 | +0.0059 | -0.0102 | +0.0052 |

Primary money-transfer F1 increased by 0.1455 from the locked 2024 reference, while student-loan F1 decreased by 0.1397. Primary credit-card F1 decreased by 0.0391 and debt-collection F1 decreased by 0.0331. These are observed temporal differences, not evidence of their cause. Smaller category supports make category-level estimates less stable.

### Overall routing results

Both unchanged thresholds remained in force: minimum top decision score `0.08` and minimum top-two margin `0.73`. Linear SVM decision scores and margins are not calibrated probabilities.

| Cohort | Auto-routed | Human review | Coverage | Review rate | Routed accuracy | Misroute rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Locked 2024 final internal test | 5,092 | 1,517 | 0.7705 | 0.2295 | 0.9503 | 0.0497 |
| **2025 primary leakage-resistant** | **21,867** | **8,289** | **0.7251** | **0.2749** | **0.9203** | **0.0797** |
| 2025 secondary sensitivity | 38,442 | 10,783 | 0.7809 | 0.2191 | 0.9424 | 0.0576 |

| Signed comparison (`2025 - 2024`) | Coverage | Review rate | Routed accuracy | Misroute rate |
| --- | ---: | ---: | ---: | ---: |
| Primary minus locked 2024 | -0.0453 | +0.0453 | -0.0300 | +0.0300 |
| Secondary minus locked 2024 | +0.0105 | -0.0105 | -0.0079 | +0.0079 |

The headline primary policy routed fewer rows, assigned more rows to human review, and made more errors among routed rows than in the 2024 reference. Its largest category-level misroute rates were debt collection (0.2356), vehicle loan or lease (0.2174), money transfer (0.2017), student loan (0.1667), and credit card (0.1557).

### Descriptive drift summary

- Actual-label Jensen-Shannon distance from 2024 was 0.0827 for primary and 0.0921 for secondary; predicted-label distance was 0.0673 and 0.0885, respectively.
- Credit reporting remained dominant but represented 0.6549 of the 2024 reference, 0.5917 of primary, and 0.7154 of secondary.
- Mean cleaned length changed from 1,268.67 characters in 2024 to 1,322.44 in primary and 1,143.73 in secondary; mean whitespace-token count was 220.13, 221.82, and 191.56.
- Mean nonzero TF-IDF features per row was 215.87 in 2024, 218.82 in primary, and 198.61 in secondary. Every cohort had zero all-zero TF-IDF rows.
- Mean top decision score changed from 0.6546 to 0.6321 in primary and 0.6838 in secondary; mean top-two margin changed from 1.4886 to 1.4221 and 1.5395.
- Primary failure rates increased for the top-score threshold (0.1672 to 0.1933), margin threshold (0.2180 to 0.2644), and both thresholds (0.1557 to 0.1828). These overlapping rates do not sum to 100%.

These diagnostics describe observed distribution changes; they do not establish statistical significance, causality, or a specific cause. Full category tables, review-reason results, distribution summaries, and figures are in the [2025 holdout report](2025_holdout_results.md), [primary confusion matrix](figures/2025_confusion_matrix.png), and [2024-versus-2025 comparison](figures/2024_vs_2025_comparison.png).

## Limitations and Next Steps

- The 2024 reference and 2025 validation use sampled public CFPB data, not institution-specific intake data or the complete operational population.
- The dominant credit-reporting category strongly influences weighted metrics.
- Smaller categories and routed subsets have less stable estimates.
- Linear SVM decision scores and score margins are not calibrated probabilities.
- The routing thresholds and 5% development rule are not production validated or business approved.
- Aggregate routing performance masks materially higher observed misroute rates in several categories.
- The secondary cohort retains repeated texts and prior-year overlap and is a sensitivity view, not the headline generalization result.
- The 2025 sample is no longer an untouched, unbiased holdout and cannot be reused for future tuning or selection.
- Any future model, preprocessing, category, cohort, or threshold change requires a new untouched validation period.
- Neither the 2024 nor 2025 results establish production readiness, deployment suitability, approved risk levels, cost savings, or workload reduction.
