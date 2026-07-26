# Model Card: Version 1 Financial Complaint Router

Status: Internal Version 1 prototype with completed 2024 internal evaluation and 2025 out-of-time validation. **Not approved for production use.**

## Model Details

| Item | Description |
| --- | --- |
| Model | TF-IDF + Linear SVM |
| Version | Version 1 |
| Task | Eight-class complaint product-category classification |
| Input | Public CFPB consumer complaint narrative |
| Output | Predicted CFPB product category and uncalibrated decision scores |
| Framework | Scikit-learn `Pipeline` |
| Selection objective | Development cross-validation Macro F1 |
| Artifact status | Fitted pipeline stored locally and excluded from Git |

The model converts complaint narratives into sparse TF-IDF features and applies a Linear SVM classifier. It supports an internal human-in-the-loop routing experiment; it is not a production decision engine.

## Intended Use

The model is intended to:

- provide an initial product-category routing recommendation for public CFPB complaint narratives;
- support analysis of complaint-routing performance and category-level errors;
- demonstrate selective automatic-routing recommendations with a human-review fallback; and
- serve as a locked Version 1 benchmark for temporal validation and future model comparison under a new validation design.

Human reviewers remain responsible for final routing, exception handling, escalations, and any legal, compliance, or customer-impacting decision.

## Out-of-Scope Use

The model must not be used to:

- make final legal, regulatory, factual, eligibility, credit, or customer-impacting decisions;
- replace required human, compliance, or subject-matter review;
- infer sensitive attributes or profile consumers;
- process private production complaint data without privacy, security, and governance approval;
- claim a calibrated probability from a Linear SVM decision score or score margin;
- generalize the measured 2025 sample results to other periods, populations, or operating conditions; or
- operate as a production routing service.

## Data

### Source and Period

- Source: public CFPB Consumer Complaint Database.
- Development period: calendar year 2024 only.
- Original validated sample: 50,000 rows.
- Input field: `complaint_what_happened`.
- Target field: `product`.
- 2025 out-of-time sample: 50,000 raw rows evaluated once under the committed locked protocol.

Raw and processed CSV files remain local and Git-ignored. Complaint narratives and row-level predictions are not committed.

### Eight-Category Scope

1. Checking or savings account
2. Credit card
3. Credit reporting or other personal consumer reports
4. Debt collection
5. Money transfer, virtual currency, or money service
6. Mortgage
7. Student loan
8. Vehicle loan or lease

### Text Preparation

The workflow uses light cleaning:

- remove URL-like text;
- collapse repeated whitespace;
- trim surrounding whitespace; and
- preserve most punctuation, wording, and phrase structure for TF-IDF.

The fitted pipeline learns TF-IDF vocabulary and weights only from its training partition. Cleaning and feature construction must remain consistent for any future inference implementation.

## Duplicate-Leakage Remediation

An audit found that 3,876 of 9,840 rows in the superseded row-level test split shared normalized text with training. Those earlier metrics are not current Version 1 results.

The corrected workflow:

1. creates a stable SHA-256 grouping key from normalized cleaned text;
2. excludes an entire normalized-text group when it has conflicting product labels;
3. retains one representative from repeated same-label groups;
4. keeps groups intact during development/test splitting and cross-validation; and
5. verifies zero normalized-text overlap between development and final test data.

After remediation, 33,042 rows and 33,042 unique normalized-text groups remained.

## Training, Selection, and Evaluation

- Development rows: 26,433.
- Final internal test rows: 6,609.
- Development/test normalized-text overlap: 0.
- Model candidates: TF-IDF + Logistic Regression, Multinomial Naive Bayes, and Linear SVM.
- Selection: five-fold group-aware cross-validation on development data only.
- Primary metric: Macro F1.
- Selected model: TF-IDF + Linear SVM.
- Final-test metrics were not used for model selection.

## Final Internal-Test Metrics

| Metric | Value |
| --- | ---: |
| Accuracy | 0.8712 |
| Macro precision | 0.7734 |
| Macro recall | 0.7621 |
| Macro F1 | 0.7671 |
| Weighted precision | 0.8721 |
| Weighted recall | 0.8712 |
| Weighted F1 | 0.8715 |

The weighted metrics are strongly influenced by the dominant credit-reporting category. Macro and per-category metrics are necessary to interpret performance across the eight classes.

## Routing Policy

Week 8 used development out-of-fold decision scores to select a two-threshold policy before applying it once to the final test set.

| Rule | Locked value |
| --- | ---: |
| Minimum top decision score | 0.08 |
| Minimum top-two score margin | 0.73 |

Both thresholds must pass for an automatic-routing recommendation. Tied, invalid, non-finite, low-top-score, or low-margin inputs require human review.

Linear SVM decision scores and top-two margins are **not calibrated probabilities**.

### Locked 2024 Final-Test Routing Results

| Metric | Value |
| --- | ---: |
| Auto-routing coverage | 0.7705 |
| Human-review rate | 0.2295 |
| Auto-routed accuracy | 0.9503 |
| Auto-routed misroute rate | 0.0497 |

The 4.97% misroute rate is aggregate. It does not mean every product category remained below 5%.

Higher observed category-level routing risk appeared in:

- Money transfer, virtual currency, or money service
- Vehicle loan or lease
- Debt collection
- Credit card

Smaller auto-routed samples make several category-level estimates less stable. The thresholds and 5% development rule are project assumptions, not production-validated or stakeholder-approved risk limits.

## Completed 2025 Out-of-Time Validation

The 2025 evaluation used a precommitted two-phase protocol. Before the CSV was opened, the saved pipeline and reference files passed integrity checks and the locked 2024 workflow reproduced its row counts, classification metrics, and routing metrics. During evaluation, the fitted model, text preparation, 50,000-feature TF-IDF representation, eight categories, `classes_` order, cohorts, comparison rules, and thresholds remained unchanged. No fitting, tuning, calibration, model selection, category change, or threshold change used 2025 results.

### Cohorts

- **Primary leakage-resistant cohort (headline): 30,156 rows.** It excludes normalized-text overlap with either locked 2024 partition, excludes all 2025 conflicting-label text groups, and retains the first row from each remaining repeated same-label group.
- **Secondary operational cohort (sensitivity view): 49,225 rows.** It retains all otherwise eligible locked-scope rows, including repeated texts and cross-year overlap, so it is not the headline generalization estimate.

### Classification and routing results

| Cohort | Accuracy | Macro F1 | Weighted F1 | Routing coverage | Review rate | Routed accuracy | Misroute rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Locked 2024 final internal test | 0.8712 | 0.7671 | 0.8715 | 0.7705 | 0.2295 | 0.9503 | 0.0497 |
| **2025 primary leakage-resistant** | **0.8315** | **0.7527** | **0.8306** | **0.7251** | **0.2749** | **0.9203** | **0.0797** |
| 2025 secondary sensitivity | 0.8771 | 0.7569 | 0.8766 | 0.7809 | 0.2191 | 0.9424 | 0.0576 |

Primary generalization weakened. Relative to the locked 2024 reference, primary accuracy decreased by 0.0397, Macro F1 by 0.0145, Weighted F1 by 0.0408, routing coverage by 0.0453, and routed accuracy by 0.0300. Human-review rate increased by 0.0453 and misroute rate increased by 0.0300. The more favorable secondary results do not replace the primary conclusion because the secondary cohort retains repeated texts and cross-year overlap.

Category behavior was uneven. Primary money-transfer F1 increased by 0.1455, while student-loan F1 decreased by 0.1397; credit-card and debt-collection F1 also declined. Primary category-level misroute rates ranged from 0.0343 for mortgage to 0.2356 for debt collection, with smaller supports producing less-stable estimates.

### Observed drift

Descriptive diagnostics found changes in actual and predicted label proportions, text length, whitespace-token count, locked-vocabulary utilization, top decision scores, and top-two score margins. The dominant credit-reporting category represented 65.49% of the 2024 reference, 59.17% of primary, and 71.54% of secondary. No cohort contained an all-zero TF-IDF row. Primary top-score, margin, and joint threshold-failure rates all increased from the 2024 reference, consistent with its higher human-review rate. These observations do not establish statistical significance, causality, or a specific cause.

The 2025 sample has now been inspected and evaluated. It is no longer an untouched, unbiased holdout and must not be reused to tune or select a future model, routing policy, or threshold. Any later model or policy change requires a new untouched validation period.

## Human Oversight

Human review remains required for:

- cases that fail either routing threshold;
- tied, missing, malformed, or non-finite model outputs;
- categories covered by a future business policy requiring category-specific review;
- ambiguous or multi-product narratives;
- missing or unusable complaint text;
- escalated or compliance-sensitive cases; and
- any use where policy requires a human decision.

An operational system would also need reviewers to record outcomes and override reasons. No such production review workflow is implemented here.

## Limitations and Risks

- Results come from sampled 2024 and 2025 CFPB data and may not transfer to institution-specific data or the complete operational population.
- Public narratives represent only complaints with usable published text.
- Historical CFPB product labels are imperfect machine-learning ground truth.
- Class imbalance creates more stable estimates for the dominant category than for smaller categories.
- The 2025 secondary cohort contains repeated texts and overlap with prior-year reference groups and is only a sensitivity view.
- Exact text hashing does not detect paraphrased or semantic near-duplicates.
- Decision scores are not probabilities, and probability calibration was not evaluated.
- No fairness evaluation or subgroup performance claim is available.
- No production workload, service-level, cost-savings, or monitoring result is available.
- Taxonomy, language, data-source, and class-distribution drift may reduce performance.
- The 2025 sample is no longer available as an unbiased holdout for future changes.
- Complaint text may contain sensitive information and would require stronger production controls.

## Monitoring Recommendations

Before and during any future controlled deployment, establish:

- input validation, missing-text rates, and text-length monitoring;
- label and predicted-category distribution monitoring;
- auto-routing coverage and human-review rate monitoring;
- overall and per-category accuracy, precision, recall, F1, and misroute rates when labels become available;
- reviewer override and escalation tracking;
- decision-score and margin distribution monitoring without treating scores as probabilities;
- vocabulary, category, and temporal drift checks;
- privacy, security, incident-response, and audit-log controls; and
- explicit thresholds for review, rollback, recalibration, or retraining.

These are recommendations only. A production monitoring system has not been implemented.

## 2025 Validation Status

Dedicated 2025 out-of-time validation is complete. The primary leakage-resistant cohort is the headline result and showed weaker classification and routing generalization than the locked 2024 reference. The secondary operational cohort is a sensitivity view only. See the [complete 2025 holdout report](2025_holdout_results.md), [primary confusion matrix](figures/2025_confusion_matrix.png), and [2024-versus-2025 comparison](figures/2024_vs_2025_comparison.png).

These results do not authorize changes to the locked thresholds and do not establish production readiness, deployment suitability, approved risk levels, cost savings, or workload reduction.

## Artifact, Deployment, and Approval Status

- The fitted pipeline is local at `models/best_tfidf_classifier.joblib`.
- The artifact is Git-ignored and is not committed.
- A production prediction API, dashboard, secure storage layer, and monitoring service are not implemented.
- Privacy, security, compliance, governance, and stakeholder approvals have not been completed.
- **This model is not approved for production use.**

See the [results summary](results_summary.md) for consolidated 2024 and 2025 tables, the [2025 holdout report](2025_holdout_results.md) for the temporal evaluation, and the [routing visualization](figures/routing_decision_score_summary.png) for the original 2024 routing analysis.
