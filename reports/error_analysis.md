# Error Analysis

Status: Corrected aggregate error analysis completed for the leakage-safe Version 1 baseline evaluation.

> **Scope clarification:** This report covers only the locked 2024 internal
> evaluation. The 2025 dataset had not been opened when this analysis was
> originally completed. The later one-time 2025 out-of-time evaluation is
> documented separately in [2025 Holdout Results](2025_holdout_results.md).

## Purpose

This report summarizes category-level results and confusion patterns for the selected TF-IDF + Linear SVM baseline after duplicate-text leakage remediation. It contains aggregate metrics only and does not include complaint narratives or row-level predictions.

## Evaluation Context

- Dataset: local processed 2024 complaints only.
- Duplicate policy: exclude conflicting-label normalized-text groups and retain one representative from repeated same-label groups.
- Rows after remediation: 33,042.
- Model selection: five-fold group-aware cross-validation on 26,433 development rows only.
- Final evaluation: one evaluation on an untouched 6,609-row internal test fold.
- Development/test normalized-text group overlap: 0.
- Selected model: TF-IDF + Linear SVM.
- Product categories: 8.
- 2025 scope: not used in this 2024 analysis; the later one-time evaluation is
  reported separately.

Corrected aggregate results are 0.8712 accuracy, 0.7671 macro F1, and 0.8715 weighted F1. These are internal development results, not production-readiness evidence, routing-policy validation, or 2025 performance.

## Per-Category Results

The category order comes from the fitted pipeline's `classes_` attribute.

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

## Categories Predicted More Reliably

The three highest category F1 scores are:

- Credit reporting or other personal consumer reports: 0.9360 F1 with 4,328 test rows.
- Mortgage: 0.8446 F1 with 177 test rows.
- Student loan: 0.8353 F1 with 126 test rows.

Mortgage and Student loan have much lower support than the dominant credit-reporting category, so their results have greater sampling uncertainty.

## Confusion Patterns

The corrected row-normalized confusion matrix is available at [`reports/figures/confusion_matrix.png`](figures/confusion_matrix.png). Important directed errors include:

- Credit reporting or other personal consumer reports was predicted as Debt collection 161 times, representing 3.72% of its actual test cases. This is the largest error by count.
- Debt collection was predicted as Credit reporting or other personal consumer reports 149 times, representing 19.03% of its actual test cases.
- Credit card was predicted as Credit reporting or other personal consumer reports 51 times, representing 10.06% of its actual test cases.
- Money transfer, virtual currency, or money service was predicted as Checking or savings account 48 times, representing 33.33% of its actual test cases.
- Checking or savings account was predicted as Credit card 31 times and as Money transfer, virtual currency, or money service 29 times, representing 7.24% and 6.78% of its actual test cases.
- Vehicle loan or lease was predicted as Credit reporting or other personal consumer reports in 14.66% of its actual test cases and as Debt collection in 9.48%.

## Interpretation

- Macro F1 remains below weighted F1 because performance is less consistent across smaller categories.
- Money transfer, virtual currency, or money service has the weakest F1 (0.5778) and recall (0.5417), with one-third of its test cases predicted as Checking or savings account.
- Vehicle loan or lease remains a lower-performing category, although its corrected F1 is 0.6783.
- Debt collection has substantial confusion with the dominant credit-reporting category.
- Weighted metrics remain strongly influenced by the credit-reporting category.
- The corrected metrics are lower than the superseded row-level-split metrics, consistent with removing duplicate-text leakage and changing the evaluation cohort.
- Linear SVM decision scores were not converted into calibrated probabilities, and no Week 8 routing threshold or human-review policy was created in this remediation.

## Recommendations

- Use the fitted pipeline's `classes_` attribute when mapping future decision-score columns to product labels.
- Treat Money transfer and Vehicle loan or lease as higher-risk categories during future routing-policy analysis.
- Keep the final internal test fold separate from future routing-threshold selection.
- Treat the completed 2025 evaluation as retrospective evidence and do not
  reuse it for tuning, calibration, threshold changes, or model selection;
  future unbiased promotion evidence requires a new untouched time period.
- Continue excluding complaint narratives and row-level predictions from committed evaluation reports.
