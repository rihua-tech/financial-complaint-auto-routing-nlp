# Data Decisions and Data Quality Notes

## Project Context

This project predicts a financial product category from the text of a consumer complaint. It is intended to support complaint routing, with human review for ambiguous, lower-signal, or policy-sensitive cases.

Model metrics do not describe every source of risk. Data selection, cleaning, labels, class balance, and changes over time must also be documented.

## Quick Summary

| Area | Decision / Risk | Why it matters |
| --- | --- | --- |
| Data source | CFPB public complaint narratives and product labels | The source supports a realistic routing task but may not represent every institution's complaint channels. |
| Development data | 2024 data is used for training and model comparison. | A defined development period makes experiments easier to reproduce and audit. |
| Holdout data | 2025 was reserved during development, then evaluated once under a precommitted protocol. | The one-time evaluation provides temporal evidence, but the sample is now exhausted as an unbiased holdout. |
| Cleaning | Light text cleaning preserves most original meaning. | Aggressive cleaning could remove useful financial terms or context. |
| Duplicate text | Exclude conflicting-label text groups and retain one representative from repeated same-label groups before splitting. | Identical narratives crossing development and test data can inflate internal evaluation metrics. |
| Missing narratives | Records without usable narratives are removed from modeling data. | A text classifier cannot make a supported text-based prediction without input text. |
| Labels | CFPB product labels are useful but not perfect ground truth. | Categories can be ambiguous, inconsistent, or different from an institution's routing structure. |
| Imbalance | Use macro F1, weighted F1, and per-class metrics, not accuracy alone. | Overall accuracy can hide weak performance on smaller product classes. |
| Drift | Complaint language and category distributions may change. | Performance can decline as products, scams, behavior, reporting, and categories change. |

## Data Source

The data comes from the public Consumer Financial Protection Bureau (CFPB) Consumer Complaint Database:

- CFPB consumer complaint narratives as the input text.
- CFPB `product` categories as the target labels.

The complaint narrative field is `complaint_what_happened`. The model does not verify the facts in a narrative. CFPB data may also differ from complaints received through a specific institution's channels, so results may not transfer directly to another operating environment.

Raw and processed CSV files remain local and are not committed. Documentation and reports use aggregate information, not individual complaint narratives.

## Training Data Year

The project uses 2024 CFPB complaint data for preparation, exploratory analysis, training, internal validation, hyperparameter tuning, model comparison, and internal testing.

A defined development period makes evaluation easier to audit. However, 2024 complaints reflect the products, concerns, reporting practices, and CFPB category structure of that period. Performance on 2024 data does not guarantee later performance.

## 2025 Holdout Data

During development, the 2025 CFPB sample was reserved as a one-time out-of-time holdout. The evaluation plan and file fingerprints were committed before access, and the model, preprocessing, label scope, cohorts, metrics, and routing thresholds were frozen.

The dataset was then evaluated once after the complete 2024 workflow was reproduced. It was not used for:

- model fitting or refitting;
- feature, preprocessing, or category decisions based on observed outcomes;
- model or hyperparameter selection;
- probability calibration;
- routing-threshold selection; or
- repeated development validation.

The 2025 sample is now exhausted as an unbiased holdout. Any future model or policy change requires a new untouched validation period.

## Committed 2025 Cohort Decisions

### Primary leakage-resistant cohort

The 30,156-row primary cohort:

- excludes normalized-text overlap with the locked 2024 development and final-test partitions;
- excludes every conflicting-label normalized-text group;
- retains one representative from each remaining repeated same-label group; and
- serves as the headline generalization estimate.

### Secondary operational sensitivity cohort

The 49,225-row secondary cohort:

- retains all otherwise eligible rows in the locked eight-category scope;
- retains repeated text and cross-year overlap; and
- is reported only as a sensitivity view, not as the headline result.

The completed audit found 775 familiar out-of-scope rows and no unfamiliar or changed product labels. Descriptive diagnostics showed changes in category proportions, modest text and locked-vocabulary drift, and lower top decision scores and margins in the primary cohort. Primary classification and routing performance weakened relative to the locked 2024 reference. These findings describe observed differences; they do not establish statistical significance, causality, or a specific cause.

## Text Cleaning Decisions

Text cleaning is intentionally light. The current process:

- Removes obvious web addresses beginning with `http://`, `https://`, or `www.`.
- Replaces repeated whitespace with one space.
- Removes leading and trailing whitespace.

It does not lowercase text, remove punctuation or stop words, or apply stemming or lemmatization. This preserves most original language for TF-IDF and possible future transformer modeling.

This approach avoids removing useful terms or changing meaning, but it leaves spelling errors, redaction markers, boilerplate, and other noise. Cleaning rules must remain consistent between training and prediction.

## Duplicate and Conflicting-Label Policy

The Week 4 audit identified 16,006 exact duplicate rows in the prepared 2024 dataset. The original Week 5–7 row-level split did not keep identical texts together: 3,876 of 9,840 original test rows (39.39%) had normalized text that also appeared in training. Those original evaluation results are superseded.

The corrected Version 1 workflow creates an internal grouping key by converting `clean_complaint_text` to string, trimming surrounding whitespace, collapsing repeated whitespace, and applying a deterministic SHA-256 hash. The hash is used only as a grouping identifier; complaint text and row-level hashes are not exported or committed.

Before group-aware splitting, the corrected workflow applies this conservative policy:

1. If a normalized-text group is associated with more than one product label, exclude the entire group from supervised Version 1 training and evaluation.
2. If normalized text repeats with the same product label, retain one representative modeling row.
3. Preserve the locked eight-category Version 1 scope.
4. Verify that no normalized-text group crosses the development/final-test split or any development cross-validation fold.

Across the full 2024 dataset, 74 normalized-text groups contain conflicting labels and account for 1,781 rows. Within the locked eight-category scope, 1,780 rows from those groups were excluded and 14,374 repeated same-label rows were removed. The corrected modeling data contains 33,042 rows and 33,042 unique normalized-text groups. Every locked category remains above the original 500-row modeling-scope floor.

The corrected evaluation reserves one deterministic fold from `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)` as the final internal test set. Model comparison uses separate group-aware cross-validation within development data only. This prevents normalized duplicate-text leakage and keeps final test metrics out of model selection.

## Missing Narratives

Rows with missing or empty narratives are removed. Blank strings count as missing, as do rows that become empty after cleaning.

A text classifier cannot learn from or make a supported prediction without text. Keeping these records could create invalid features or misleading results. Rows with missing or empty product labels are also removed because supervised training requires a target.

This removal may create selection bias: complaints without public narratives may differ from those with narratives. The model therefore represents only records with usable text and labels. In a real routing system, a missing narrative should trigger a data-quality check or human review, not a model prediction.

## Product Labels

The target is the CFPB `product` category attached to each complaint. It is a practical routing label, but not perfect or universal ground truth.

A complaint can mention several products or problems, while this task uses one product label. Categories can overlap in language, and the CFPB taxonomy may differ from an institution's routing structure.

Label names, definitions, and mappings should be versioned. Any category merging, removal, or remapping should be documented before evaluation.

## Class Imbalance

CFPB product categories may be highly imbalanced. A model can achieve high accuracy on the largest categories while performing poorly on less common ones.

Accuracy alone is not enough. Evaluation should include:

- **Macro F1**, which gives each class equal importance and helps reveal weak performance on smaller classes.
- **Weighted F1**, which summarizes performance while accounting for the number of records in each class.
- **Per-class precision, recall, and F1**, which show which product categories are routed well and which need improvement or human review.

Confusion matrices and class support counts add context. Class filtering, weighting, resampling, or label merging can change the task's business meaning and must be documented.

## Possible Label Noise

Real-world complaint categories may contain label noise. A narrative can be ambiguous, describe several products, or fail to clearly identify the assigned category. Selection may also depend on the information available at intake and how the record was reviewed.

Similar narratives may therefore receive different labels, and some labels may be subjective or inconsistent. This limits what text-only modeling can learn. Error analysis should distinguish model errors from ambiguous or possibly inconsistent labels without copying raw narratives into repository reports.

## Limitations of Historical Complaint Categories

Historical CFPB categories support complaint intake and reporting; they were not designed as machine-learning ground truth. They reflect the taxonomy, policies, and operational decisions in use when each complaint was recorded.

These historical labels may:

- Combine complaints that require different routing actions.
- Separate complaints that use very similar language.
- Omit information that a human reviewer would use.
- Differ from an organization's current product ownership or escalation rules.
- Change in meaning when categories are added, renamed, merged, or retired.

The model may reproduce these boundaries and inconsistencies. Predictions are routing recommendations, not final legal, compliance, or factual determinations.

## Future Data Drift

Future complaint data may differ from the 2024 development data. Important drift risks include:

- New financial products, services, payment methods, or providers.
- New scams, fraud patterns, and terminology.
- Changes in consumer behavior, expectations, and writing style.
- Changes to CFPB reporting, collection, publication, or redaction practices.
- Economic changes that alter complaint volume and subject matter.
- Changes to product categories, category definitions, or class proportions.

Drift can affect narrative text and target labels. Monitoring should compare future data with development data using class distributions, missing-value rates, text lengths, locked-vocabulary behavior, decision-score and margin distributions, and per-class performance when labels become available.

Material drift should trigger review of the model and label mapping. New or changed categories may require updated training data, revised mappings, retraining, and a new independent holdout period.

## Summary

The project uses CFPB narratives and product categories, with 2024 used for development and 2025 protected during development before one-time out-of-time evaluation. The primary leakage-resistant cohort remains the headline result, while the secondary operational cohort is a sensitivity view. The 2025 sample is now exhausted as an unbiased holdout. Key risks include class imbalance, missing-narrative selection bias, label noise, historical category limitations, and temporal drift; metrics should be interpreted with these risks and data decisions kept versioned.
