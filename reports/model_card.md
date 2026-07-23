# Model Card: Version 1 Financial Complaint Router

Status: Completed documentation for an internal 2024 prototype. **Not approved for production use.**

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
- serve as a Version 1 benchmark for future out-of-time validation or model comparison.

Human reviewers remain responsible for final routing, exception handling, escalations, and any legal, compliance, or customer-impacting decision.

## Out-of-Scope Use

The model must not be used to:

- make final legal, regulatory, factual, eligibility, credit, or customer-impacting decisions;
- replace required human, compliance, or subject-matter review;
- infer sensitive attributes or profile consumers;
- process private production complaint data without privacy, security, and governance approval;
- claim a calibrated probability from a Linear SVM decision score or score margin;
- claim performance on 2025 or other future-period data; or
- operate as a production routing service.

## Data

### Source and Period

- Source: public CFPB Consumer Complaint Database.
- Development period: calendar year 2024 only.
- Original validated sample: 50,000 rows.
- Input field: `complaint_what_happened`.
- Target field: `product`.
- 2025 holdout: not loaded or used for this Version 1 evaluation or routing analysis.

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

### Final-Test Routing Results

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

- Results come from a sampled 2024 CFPB dataset and may not transfer to institution-specific data.
- Public narratives represent only complaints with usable published text.
- Historical CFPB product labels are imperfect machine-learning ground truth.
- Class imbalance creates more stable estimates for the dominant category than for smaller categories.
- Exact text hashing does not detect paraphrased or semantic near-duplicates.
- Decision scores are not probabilities, and probability calibration was not evaluated.
- No fairness evaluation or subgroup performance claim is available.
- No production workload, service-level, cost-savings, or monitoring result is available.
- Taxonomy, language, data-source, and class-distribution drift may reduce performance.
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

Dedicated 2025 out-of-time validation has **not** been completed. The 2025 data was not loaded or used by the Version 1 modeling, internal evaluation, or routing-analysis workflows. Future validation must keep model, preprocessing, category scope, and evaluation rules fixed before accessing holdout outcomes.

## Artifact, Deployment, and Approval Status

- The fitted pipeline is local at `models/best_tfidf_classifier.joblib`.
- The artifact is Git-ignored and is not committed.
- A production prediction API, dashboard, secure storage layer, and monitoring service are not implemented.
- Privacy, security, compliance, governance, and stakeholder approvals have not been completed.
- **This model is not approved for production use.**

See the [results summary](results_summary.md) for detailed tables and the [routing visualization](figures/routing_decision_score_summary.png) for aggregate routing results.
