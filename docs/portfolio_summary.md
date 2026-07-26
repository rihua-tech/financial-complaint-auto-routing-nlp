# Portfolio Summary

## Project Overview

Financial Complaint Auto-Routing with NLP is an end-to-end machine-learning project that classifies public CFPB consumer complaint narratives into eight financial product categories. It combines leakage-safe model evaluation with a human-in-the-loop routing policy that sends weaker or ambiguous model outputs to review.

The completed Version 1 system is an internal prototype and portfolio project, not a deployed production service.

## Business Problem

Complaint operations teams must route unstructured narratives to the correct product area. Fully manual triage can be slow and inconsistent, but uncontrolled automation can misroute complex or higher-risk cases. The project explores how an NLP model can provide consistent initial recommendations while reserving uncertain cases for human judgment.

## Technical Approach

1. Acquired and validated a monthly-balanced, daily-stratified 50,000-row 2024 CFPB sample.
2. Applied light text cleaning and aggregate data-quality checks.
3. Detected duplicate-text leakage in the original row-level split.
4. Removed conflicting-label text groups and repeated same-label rows, leaving 33,042 leakage-safe modeling rows.
5. Created a group-aware 26,433-row development set and 6,609-row final internal test set with zero normalized-text overlap.
6. Compared TF-IDF pipelines using Logistic Regression, Multinomial Naive Bayes, and Linear SVM.
7. Selected Linear SVM with five-fold group-aware development cross-validation and Macro F1.
8. Evaluated the model with overall, weighted, macro, and per-category metrics plus a confusion matrix.
9. Selected two routing thresholds from development out-of-fold decision scores and evaluated the locked policy once on the final test set.
10. Added tested routing-rule logic for threshold boundaries, invalid inputs, ties, and class-order safety.
11. Precommitted a two-phase 2025 holdout protocol and reproduced the complete 2024 reference before opening the out-of-time sample.
12. Evaluated the unchanged model and routing policy on leakage-resistant and operational 2025 cohorts, including classification, routing, category-risk, and descriptive drift analysis.

## Tech Stack

- Python
- Pandas and NumPy
- Jupyter Notebook
- Scikit-learn pipelines
- TF-IDF, Logistic Regression, Multinomial Naive Bayes, and Linear SVM
- Matplotlib and Seaborn
- Python `unittest`
- Git, GitHub, and GitHub Actions
- CFPB Consumer Complaint Database API

## Verified Results

### Locked 2024 Reference

| Internal 2024 metric | Result |
| --- | ---: |
| Accuracy | 0.8712 |
| Macro F1 | 0.7671 |
| Weighted F1 | 0.8715 |

### Human-Review Routing

| Policy item | Result |
| --- | ---: |
| Minimum top decision score | 0.08 |
| Minimum top-two score margin | 0.73 |
| Auto-routing coverage | 77.05% |
| Human-review rate | 22.95% |
| Auto-routed accuracy | 95.03% |
| Auto-routed misroute rate | 4.97% |

Both thresholds must pass for an automatic-routing recommendation. Linear SVM decision scores and margins are not calibrated probabilities.

The 4.97% misroute rate is aggregate and does not mean every category remained below 5%. Money transfer/virtual currency/money service, Vehicle loan or lease, Debt collection, and Credit card showed higher observed category-level risk. Smaller category samples also produce less stable estimates.

### One-Time 2025 Out-of-Time Validation

The fitted model, text preparation, eight-category scope, class order, evaluation cohorts, and routing thresholds remained locked. No 2025 result was used to fit, tune, calibrate, or select the model or policy.

The 30,156-row primary leakage-resistant cohort is the headline result. It excludes normalized-text overlap with the locked 2024 partitions, conflicting-label groups, and extra repeated same-label rows. The 49,225-row secondary operational cohort retains repeated texts and cross-year overlap and is reported only as a sensitivity view.

| 2025 headline metric | Primary result |
| --- | ---: |
| Accuracy | 0.8315 |
| Macro F1 | 0.7527 |
| Weighted F1 | 0.8306 |
| Auto-routing coverage | 72.51% |
| Human-review rate | 27.49% |
| Auto-routed accuracy | 92.03% |
| Auto-routed misroute rate | 7.97% |

The honest headline is weaker temporal generalization: compared with the locked 2024 reference, primary accuracy fell by 0.0397, Weighted F1 by 0.0408, routing coverage by 0.0453, and routed accuracy by 0.0300, while review and misroute rates each increased by 0.0453 and 0.0300, respectively. Category-level analysis found both improvements and declines, and drift diagnostics documented changes in label mix, text, locked-vocabulary use, decision scores, and margins without assigning a cause.

## Human-in-the-Loop Design

The model does not replace reviewers. The implemented routing rules recommend human review when either threshold fails or score inputs are tied, invalid, non-finite, or otherwise unusable. Category-based review is not implemented; a future business policy may add category-specific controls for higher-risk categories, escalations, ambiguous narratives, or compliance-sensitive cases.

This design treats selective automation as a risk-management problem: coverage matters, but so do the error rate and the distribution of errors across categories.

## Key Data-Science and Engineering Decisions

- **Corrected evaluation leakage:** Replaced a row-level split after finding that 39.39% of the original test rows shared normalized text with training.
- **Used group-aware validation:** Kept normalized-text groups together during splitting and cross-validation.
- **Protected the final test fold:** Selected the model and routing thresholds using development data only.
- **Prioritized Macro F1:** Evaluated category balance rather than relying on majority-influenced accuracy alone.
- **Kept preprocessing in the pipeline:** Learned TF-IDF vocabulary and weights only from training folds.
- **Mapped scores safely:** Used the fitted classifier's `classes_` order instead of assuming a frequency-based category order.
- **Tested routing boundaries:** Covered inclusive thresholds, ties, malformed inputs, non-finite values, and label-score alignment.
- **Precommitted temporal validation:** Locked data rules, cohorts, metrics, fingerprints, and thresholds before inspecting the 2025 sample.
- **Reported degradation directly:** Kept the leakage-resistant cohort as the headline result even though the operational sensitivity cohort was more favorable.
- **Protected sensitive artifacts:** Kept CSV files, complaint narratives, row-level predictions, and fitted model artifacts out of Git.

## Limitations

- Results use sampled 2024 and 2025 public CFPB data and may not transfer to private complaint channels or the complete operational population.
- Historical product labels may be ambiguous and are not perfect operational ground truth.
- Class imbalance and small categories produce uneven estimate stability.
- Decision scores are not probabilities, and calibration was not evaluated.
- Thresholds are project assumptions, not stakeholder-approved production limits.
- The secondary 2025 cohort retains repeated texts and cross-year overlap and is a sensitivity view, not the headline result.
- The evaluated 2025 sample is no longer an untouched holdout; future model or policy changes require a new untouched validation period.
- No fairness analysis, production workload study, monitoring result, deployment, or governance approval is claimed.

## Portfolio-Ready Description

Built a leakage-safe NLP complaint-routing prototype using Scikit-learn TF-IDF pipelines and Linear SVM, corrected duplicate-text contamination, and added a tested human-review policy based on uncalibrated score and margin signals. A precommitted one-time 2025 validation kept the full workflow locked and found weaker headline performance on a 30,156-row leakage-resistant cohort: 0.8315 accuracy, 0.7527 Macro F1, 72.51% routing coverage, and 92.03% routed accuracy. Aggregate drift and category-risk analysis documented the limitations without claiming production readiness.

## Resume-Ready Bullets

- Built and evaluated an eight-class CFPB complaint-routing system with Python, Scikit-learn, TF-IDF, and Linear SVM, achieving **0.8712 accuracy** and **0.7671 Macro F1** on a leakage-safe 6,609-row 2024 internal test fold.
- Detected duplicate-text leakage affecting **39.39% of the superseded test split** and redesigned preprocessing and validation with SHA-256 text grouping and `StratifiedGroupKFold`, reducing development/test normalized-text overlap to **zero**.
- Precommitted and executed a one-time 2025 out-of-time validation with a locked model and routing policy; the **30,156-row leakage-resistant headline cohort** achieved **0.8315 accuracy**, **0.7527 Macro F1**, **72.51% coverage**, and **92.03% routed accuracy**, transparently documenting temporal degradation, drift, and category-level risk.
