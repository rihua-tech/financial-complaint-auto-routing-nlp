# Error Analysis

Status: Week 7 aggregate error analysis completed for the selected Version 1 baseline.

## Purpose

This report summarizes where the selected TF-IDF + Linear SVM baseline performs well and where product-category errors occur. It uses only aggregate metrics and does not include raw complaint narratives.

## Evaluation Context

- Selected model: TF-IDF + Linear SVM.
- Evaluation data: unchanged internal test split from `data/processed/cfpb_complaints_2024_cleaned.csv`.
- Modeling scope: cleaned 2024 complaints in product classes with at least 500 records.
- Test rows: 9,840.
- Product categories: 8.
- Split: `test_size=0.20`, `random_state=42`, and `stratify=y`.
- 2025 holdout data: not loaded or used.

The test-set results are 0.9085 accuracy, 0.7880 macro F1, and 0.9095 weighted F1. These are internal development results, not production-readiness evidence or final project model selection.

## Per-Category Results

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

## Categories Predicted Well

The three highest per-category F1 scores are:

- Credit reporting or other personal consumer reports: 0.9573 F1 and 0.9484 recall.
- Mortgage: 0.8547 F1 and 0.8305 recall.
- Student loan: 0.8314 F1 and 0.8413 recall.

Mortgage and Student loan have much smaller test support than the dominant credit-reporting category, so their estimates should be interpreted with more uncertainty.

## Confusion Patterns

The row-normalized confusion matrix is available at [`reports/figures/confusion_matrix.png`](figures/confusion_matrix.png). The most important directed error patterns are:

- Credit reporting or other personal consumer reports was predicted as Debt collection 239 times, representing 3.31% of its actual test cases. This is the largest error by volume.
- Debt collection was predicted as Credit reporting or other personal consumer reports 136 times, representing 12.69% of its actual test cases.
- Money transfer, virtual currency, or money service was predicted as Checking or savings account 39 times, representing 26.90% of its actual test cases.
- Vehicle loan or lease was predicted as Credit reporting or other personal consumer reports 27 times, representing 22.88% of its actual test cases.
- Credit card was predicted as Credit reporting or other personal consumer reports 48 times and as Checking or savings account 41 times, representing 8.78% and 7.50% of its actual test cases.
- Checking or savings account was predicted as Credit card 36 times, representing 8.39% of its actual test cases.

Vehicle loan or lease and Money transfer, virtual currency, or money service are the weakest categories by F1 and recall. Their lower support and concentration of errors into broader financial-product categories make them priorities for future review.

## Interpretation

- Macro F1 remains below weighted F1 because performance is less consistent across the smaller categories.
- The high weighted metrics are strongly influenced by the dominant credit-reporting category.
- The confusion matrix describes aggregate error patterns only; no complaint narratives were reviewed or exposed.
- Linear SVM decision scores were not converted into calibrated probabilities, and no routing-confidence threshold or human-review policy was created in Week 7.

## Recommendations

- Keep the 2025 dataset separate for future out-of-time validation.
- Review the lower-support Vehicle loan or lease and Money transfer categories before defining any automated routing policy.
- Evaluate probability calibration or decision-score thresholds only in a dedicated routing-confidence task.
- Continue to exclude raw complaint narratives from committed evaluation reports.
