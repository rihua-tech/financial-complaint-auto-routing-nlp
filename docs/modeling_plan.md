# Modeling Plan and Version 1 Record

## Objective

The modeling objective is to classify public CFPB consumer complaint narratives into eight financial product categories. The business objective is to support initial routing recommendations while assigning weak or ambiguous model signals to human review; any category-specific review control remains a future business-policy decision.

This document preserves the original modeling rationale and records what was completed for Version 1. It does not authorize production use.

## Input, Target, and Data Boundaries

- Input text: `complaint_what_happened`.
- Target label: `product`.
- Development period: 2024 CFPB complaints only.
- Original validated sample: 50,000 rows.
- Future out-of-time holdout: a separate 2025 file that was not loaded or used.
- Data policy: raw and processed CSV files remain local and Git-ignored.

The original sampling strategy was monthly-balanced and daily-stratified to reduce newest-first recency bias. Version 1 uses the 2024 sample for data preparation, model selection, internal evaluation, and routing-rule analysis.

## Original Baseline Rationale

The baseline candidates were:

- TF-IDF + Logistic Regression;
- TF-IDF + Multinomial Naive Bayes; and
- TF-IDF + Linear SVM.

These models provide practical sparse-text baselines with different inductive biases. They train quickly, work directly with TF-IDF features, and establish an interpretable benchmark before any transformer experiment.

Macro F1 was the primary selection metric because it gives equal weight to each product category. Accuracy, Weighted F1, per-class precision/recall/F1, and a confusion matrix provide complementary evidence.

## Completed Version 1 Workflow

### 1. Light Text Cleaning

The workflow removes URL-like text, collapses repeated whitespace, and trims surrounding whitespace. It preserves most punctuation and wording. TF-IDF applies consistent lowercasing inside the pipeline.

Missing or empty narratives and labels are invalid for supervised text classification. Text-length outliers are reviewed at aggregate level rather than automatically removed solely because they are short or long.

### 2. Duplicate-Leakage Remediation

The superseded row-level split allowed 3,876 of 9,840 test rows to share normalized text with training. Version 1 corrects that leakage before splitting:

1. normalize cleaned text for grouping;
2. create a deterministic SHA-256 grouping key;
3. exclude every group associated with conflicting labels;
4. keep one representative from repeated same-label groups; and
5. assert that groups do not cross evaluation partitions.

After remediation, 33,042 rows and unique normalized-text groups remained in the locked eight-category scope.

### 3. Group-Aware Split

`StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)` defines the outer partition:

- development: 26,433 rows;
- final internal test: 6,609 rows; and
- development/test normalized-text overlap: 0.

The final internal test fold was excluded from model comparison and selection.

### 4. Three-Model Comparison

Each candidate used a Scikit-learn `Pipeline` with TF-IDF so vocabulary and inverse-document-frequency values were learned only from the applicable training fold.

| Model | Five-fold development CV Macro F1 |
| --- | ---: |
| TF-IDF + Logistic Regression | 0.7430 |
| TF-IDF + Multinomial Naive Bayes | 0.3519 |
| TF-IDF + Linear SVM | 0.7687 |

Linear SVM was selected using development Macro F1. Final-test metrics were not used in selection.

### 5. Final Internal Evaluation

The selected TF-IDF + Linear SVM pipeline was fitted on all 26,433 development rows and evaluated on the 6,609-row final internal test fold.

| Metric | Result |
| --- | ---: |
| Accuracy | 0.8712 |
| Macro F1 | 0.7671 |
| Weighted F1 | 0.8715 |

Per-category metrics and the row-normalized confusion matrix remain necessary because the dominant credit-reporting category strongly influences weighted metrics.

### 6. Decision-Score Routing

The routing analysis generated out-of-fold decision scores for all development rows, searched threshold pairs under the project assumptions, locked the selected rules, and then applied them once to the final test set.

| Routing rule | Locked threshold |
| --- | ---: |
| Minimum top decision score | 0.08 |
| Minimum top-two score margin | 0.73 |

Both thresholds must pass for an automatic-routing recommendation. Linear SVM decision scores and margins are not probabilities.

| Final-test routing metric | Result |
| --- | ---: |
| Auto-routing coverage | 0.7705 |
| Human-review rate | 0.2295 |
| Auto-routed accuracy | 0.9503 |
| Auto-routed misroute rate | 0.0497 |

The 4.97% aggregate misroute rate does not guarantee a rate below 5% for every category. Money transfer/virtual currency/money service, Vehicle loan or lease, Debt collection, and Credit card showed higher observed routing risk, and smaller category estimates are less stable.

### 7. Human-Review Policy

The prototype recommends human review for low top scores, low margins, tied scores, malformed or non-finite scores, and other unsupported inputs. Higher-risk categories and compliance-sensitive cases also require policy decisions beyond the model rules.

Routing behavior is tested in `tests/test_routing_rules.py`, including exact threshold boundaries, invalid inputs, ties, and class-order safety.

## Completed Artifacts

- `notebooks/04_sklearn_baseline_model.ipynb`: corrected Version 1 comparison and evaluation.
- `notebooks/05_decision_score_routing.ipynb`: routing threshold selection and final-test analysis.
- `reports/results_summary.md`: verified technical results.
- `reports/error_analysis.md`: aggregate category-level interpretation.
- `reports/model_card.md`: intended use, limitations, oversight, and monitoring recommendations.
- `src/routing_rules.py`: reusable routing-rule logic.
- `tests/test_routing_rules.py`: focused routing-rule tests.

The fitted pipeline is local and Git-ignored. A reusable production training or inference service is not complete.

## Future Work

### 2025 Out-of-Time Validation

The protected 2025 data remains future work. Before accessing outcomes, freeze the preprocessing, category scope, duplicate policy, fitted model, metrics, and routing rules. The holdout must not be used for additional selection or repeated tuning.

### DistilBERT

DistilBERT is a future Version 2 comparison, not part of Version 1. Any experiment should:

- use the same leakage-safe data boundaries;
- compare against the locked TF-IDF + Linear SVM baseline;
- report compute, latency, monitoring, and interpretability tradeoffs; and
- avoid accessing the 2025 holdout for model selection.

### Production Readiness

Future production consideration would require probability calibration or an explicitly non-probabilistic policy, category-specific error costs, privacy and security controls, fairness analysis, human-review operations, monitoring, drift detection, deployment design, and governance approval.
