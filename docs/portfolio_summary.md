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

### Model Evaluation

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
- **Protected sensitive artifacts:** Kept CSV files, complaint narratives, row-level predictions, and fitted model artifacts out of Git.

## Limitations

- Results use a sampled 2024 public CFPB dataset and may not transfer to private complaint channels.
- Historical product labels may be ambiguous and are not perfect operational ground truth.
- Class imbalance and small categories produce uneven estimate stability.
- Decision scores are not probabilities, and calibration was not evaluated.
- Thresholds are project assumptions, not stakeholder-approved production limits.
- The 2025 holdout was not used; out-of-time performance remains unknown.
- No fairness analysis, production workload study, monitoring result, deployment, or governance approval is claimed.

## Portfolio-Ready Description

Built a leakage-safe NLP complaint-routing prototype using Scikit-learn TF-IDF pipelines and Linear SVM, correcting duplicate-text contamination in the original evaluation and adding a tested human-review policy based on uncalibrated decision-score and margin signals. On a protected 2024 internal test fold, the model achieved 0.8712 accuracy and 0.7671 Macro F1; the selective routing policy covered 77.05% of cases with 95.03% accuracy among auto-routed recommendations while exposing materially higher risk in several smaller categories.

## Resume-Ready Bullets

- Built and evaluated an eight-class CFPB complaint-routing system with Python, Scikit-learn, TF-IDF, and Linear SVM, achieving **0.8712 accuracy** and **0.7671 Macro F1** on a leakage-safe 6,609-row internal test fold.
- Detected duplicate-text leakage affecting **39.39% of the superseded test split** and redesigned preprocessing and validation with SHA-256 text grouping and `StratifiedGroupKFold`, reducing development/test normalized-text overlap to **zero**.
- Implemented and tested a human-review routing policy using top decision score and score-margin thresholds, producing **77.05% coverage** and **95.03% auto-routed accuracy** while documenting category-level risk and non-probabilistic score limitations.
