# Portfolio Summary

## Project Overview

Financial Complaint Auto-Routing with NLP is an end-to-end machine-learning project that classifies public CFPB consumer complaint narratives into eight financial product categories. It combines leakage-safe model evaluation with a human-in-the-loop routing policy that sends weaker or ambiguous model outputs to review.

The completed project compares a temporally validated TF-IDF + Linear SVM benchmark with a frozen DistilBERT challenger. It remains an internal notebook-centered prototype and portfolio project, not a deployed production service.

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
13. Fine-tuned DistilBERT across five fixed development folds, generated one OOF result for each of 26,433 development rows, and froze the final model and tokenizer.
14. Selected a separate transformer routing policy using development OOF outputs only, then compared the frozen V1 and V2 models on the shared 6,609-row 2024 benchmark.
15. Committed a retrospective protocol before scoring Version 2 on 2025, preserved the 30,156-row leakage-resistant cohort as the headline result, and kept all row-level outputs local and Git-ignored.

## Tech Stack

- Python
- Pandas and NumPy
- Jupyter Notebook
- Scikit-learn pipelines
- TF-IDF, Logistic Regression, Multinomial Naive Bayes, and Linear SVM
- PyTorch, Transformers, DistilBERT, and Hugging Face tokenization
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

### Version 2 Champion-Challenger Results

On the shared 2024 benchmark, frozen DistilBERT improved Accuracy from 0.8712 to 0.8882 and Macro F1 from 0.7671 to 0.7949, while raising routing coverage from 0.7705 to 0.8177. Its routed accuracy was slightly lower (0.9476 versus 0.9503), and its artifact and compute requirements were substantially larger.

The 2025 comparison is retrospective, not a new untouched Version 2 holdout. On the primary leakage-resistant cohort, Version 2 achieved 0.8404 Accuracy, 0.7620 Macro F1, 0.7571 coverage, and 0.9174 routed accuracy. Those results slightly improved classification and coverage over Version 1, but the Version 2 misroute rate was slightly higher (0.0826 versus 0.0797), and student-loan and debt-collection category risk worsened materially. Both models weakened relative to their shared 2024 benchmark.

Version 1 remains the temporally validated benchmark. Version 2 remains the frozen transformer challenger with matched 2024 evidence and a retrospective 2025 comparison. Independent Version 2 temporal promotion evidence requires a new untouched period.

## Human-in-the-Loop Design

The models do not replace reviewers. Their separately locked routing policies recommend human review when either model-specific signal threshold fails. Category-based review is not implemented; a future business policy may add category-specific controls for higher-risk categories, escalations, ambiguous narratives, or compliance-sensitive cases.

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
- **Froze the challenger before comparison:** Locked DistilBERT training, tokenizer, model artifact, and development-only routing policy before shared-benchmark and retrospective scoring.
- **Reported mixed evidence:** Preserved stronger Version 2 classification results alongside higher primary routing risk and category-level weaknesses.
- **Protected sensitive artifacts:** Kept CSV files, complaint narratives, row-level predictions, and fitted model artifacts out of Git.

## Limitations

- Results use sampled 2024 and 2025 public CFPB data and may not transfer to private complaint channels or the complete operational population.
- Historical product labels may be ambiguous and are not perfect operational ground truth.
- Class imbalance and small categories produce uneven estimate stability.
- Linear SVM decision scores and DistilBERT softmax scores and margins are not calibrated probabilities.
- The locked 256-token transformer limit truncates a material share of narratives.
- Thresholds are project assumptions, not stakeholder-approved production limits.
- The secondary 2025 cohort retains repeated texts and cross-year overlap and is a sensitivity view, not the headline result.
- The evaluated 2025 sample is no longer an untouched holdout; future model or policy changes require a new untouched validation period.
- No fairness analysis, production workload study, monitoring result, deployment, or governance approval is claimed.

## Portfolio-Ready Description

Built a leakage-safe, human-in-the-loop complaint-routing study comparing TF-IDF + Linear SVM with a frozen DistilBERT challenger. The project corrected duplicate-text leakage, generated complete development OOF evidence, locked separate routing policies before evaluation, and reported both gains and category-level risks on a shared 2024 benchmark and retrospective 2025 cohorts. Version 1 remains the temporally validated benchmark; Version 2 remains the frozen challenger pending a new untouched validation period.

## Resume-Ready Bullets

- Built a leakage-safe eight-class CFPB complaint-routing benchmark and DistilBERT challenger with complete five-fold OOF evaluation; frozen DistilBERT reached **0.8882 Accuracy** and **0.7949 Macro F1** on the shared 6,609-row 2024 benchmark versus **0.8712** and **0.7671** for TF-IDF + Linear SVM.
- Precommitted and executed a frozen V1-versus-V2 retrospective comparison on a **30,156-row leakage-resistant 2025 cohort**; DistilBERT reached **0.8404 Accuracy**, **0.7620 Macro F1**, and **75.71% routing coverage** while documenting category-level routing risk and temporal drift.
