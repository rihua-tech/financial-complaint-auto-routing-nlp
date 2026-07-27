# Business Case

## Business Problem

Financial services organizations receive written complaints across credit cards, mortgages, bank accounts, loans, debt collection, credit reporting, and money-transfer products. Each complaint must reach the appropriate team, but fully manual triage can be slow, inconsistent, and difficult to audit at high volume. An incorrect automated route can also delay handling or increase operational and compliance risk.

This project demonstrates a business-oriented NLP decision-support prototype that classifies a public CFPB complaint narrative into one of eight product categories and applies routing rules that recommend either an automatic route or human review.

## Intended Users

The prototype is relevant to:

- complaint intake and customer-support operations;
- product teams that receive routed complaints;
- compliance teams that oversee complaint handling and escalation;
- risk and analytics teams that evaluate model behavior; and
- managers who need aggregate visibility into routing and review volumes.

It is a decision-support prototype, not a production service or replacement for existing review obligations.

## Completed Internal Prototype

The completed Version 1 workflow:

1. validates a 50,000-row public CFPB sample from 2024;
2. applies light text cleaning and data-quality checks;
3. removes duplicate-text leakage and conflicting-label text groups;
4. uses group-aware development and final-test partitions with zero normalized-text overlap;
5. compares TF-IDF pipelines with Logistic Regression, Multinomial Naive Bayes, and Linear SVM;
6. selects Linear SVM using five-fold development cross-validation and Macro F1;
7. evaluates the selected pipeline on a 6,609-row final internal test fold;
8. applies locked decision-score and score-margin rules to recommend automatic routing or human review; and
9. evaluates the unchanged workflow once on a precommitted 2025 out-of-time holdout.

The fitted pipeline is stored only as a local, Git-ignored artifact. A deployed prediction service is not implemented.

## Verified Model Results

| Internal 2024 metric | Value |
| --- | ---: |
| Accuracy | 0.8712 |
| Macro F1 | 0.7671 |
| Weighted F1 | 0.8715 |

The difference between Macro F1 and Weighted F1 reflects class imbalance and less consistent performance across smaller categories. These metrics describe the internal 2024 sample only.

## Routing Policy and Business Interpretation

The routing policy requires both:

- top Linear SVM decision score of at least 0.08; and
- top-two score margin of at least 0.73.

Decision scores and margins are model signals, not calibrated probabilities.

| Final-test routing metric | Value |
| --- | ---: |
| Auto-routing coverage | 77.05% |
| Human-review rate | 22.95% |
| Auto-routed accuracy | 95.03% |
| Auto-routed misroute rate | 4.97% |

The results show that the policy can separate a larger lower-observed-risk subset from cases requiring review within this internal test. They do not guarantee a 77.05% reduction in manual workload: an operating organization may require additional review, exception handling, audits, or category-specific controls.

The aggregate 4.97% misroute rate also does not apply uniformly. Money transfer/virtual currency/money service, Vehicle loan or lease, Debt collection, and Credit card showed higher observed category-level risk. Several smaller categories have limited support, so their estimates are less stable.

## Completed 2025 Out-of-Time Validation

The 2025 evaluation followed a protocol committed before the holdout was opened. The fitted model, preprocessing, eight categories, class order, cohort definitions, metrics, and routing thresholds remained locked. The 2025 sample was not used for fitting, tuning, model selection, calibration, or threshold selection.

| Cohort | Rows | Accuracy | Macro F1 | Weighted F1 | Routing coverage | Review rate | Routed accuracy | Misroute rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Locked 2024 final internal test | 6,609 | 0.8712 | 0.7671 | 0.8715 | 0.7705 | 0.2295 | 0.9503 | 0.0497 |
| **2025 primary leakage-resistant** | **30,156** | **0.8315** | **0.7527** | **0.8306** | **0.7251** | **0.2749** | **0.9203** | **0.0797** |
| 2025 secondary operational sensitivity | 49,225 | 0.8771 | 0.7569 | 0.8766 | 0.7809 | 0.2191 | 0.9424 | 0.0576 |

The primary leakage-resistant cohort is the headline result. It excludes overlap with the locked 2024 partitions, conflicting-label groups, and extra repeated same-label rows. Its classification and routing performance weakened relative to the 2024 reference: the review rate increased from 0.2295 to 0.2749 and the routed misroute rate increased from 0.0497 to 0.0797.

The secondary operational cohort retains repeated text and cross-year overlap and is reported only as a sensitivity view. Category-level routing risk remained uneven, especially where supports and auto-routed counts were smaller. These findings reinforce the need for human review rather than establishing an approved automation level.

The 2025 sample is now exhausted as an unbiased holdout. Any future model, preprocessing, category, cohort, or threshold change requires a new untouched validation period.

## Human-in-the-Loop Role

A human reviewer remains responsible when:

- either routing threshold fails;
- model scores are invalid, tied, or malformed;
- the narrative is missing, ambiguous, or describes multiple products;
- a future business policy requires category-specific review for a category with higher observed routing risk;
- the complaint is escalated or compliance-sensitive; or
- business policy requires manual review.

Future operational design would need documented review procedures, override reasons, escalation rules, and quality feedback. Those processes are not implemented by this repository.

## Potential Value

Subject to controlled operational evaluation and governance, a similar workflow could support:

- more consistent initial product-category recommendations;
- future policy experimentation with category-specific review for ambiguous or higher-risk complaints;
- aggregate visibility into model errors and review volumes; and
- auditable experimentation with routing rules.

The project does not claim realized cost savings, guaranteed workload reduction, deployment, regulatory approval, or production readiness.

## Limitations and Production Considerations

- The data is a public CFPB sample, not institution-specific intake data.
- The 2025 sample was protected during development and evaluated once under the committed protocol; it is no longer an untouched holdout.
- Historical product labels may be ambiguous or differ from an organization's ownership structure.
- Class imbalance and small category samples make some estimates less stable.
- Linear SVM decision scores are not probabilities.
- The routing thresholds are project assumptions, not stakeholder-approved operating limits.
- No fairness study, calibration study, production workload study, or live monitoring has been completed.
- Complaint narratives may contain sensitive information.

Before production consideration, the workflow would require controlled operational evaluation, privacy and security review, compliance and governance approval, category-specific error-cost decisions, human-review procedures, monitoring, drift controls, secure storage, audit logging, and incident-response ownership.

## Next Business Decisions

1. Define category-specific error costs and stakeholder-approved human-review policies.
2. Decide which categories, if any, warrant controlled automatic-routing evaluation.
3. Establish human-review, escalation, override, privacy, governance, monitoring, and audit procedures.
4. Evaluate operational behavior in a controlled environment before making workload or value claims.
5. Protect a new independent validation period before evaluating any future model or policy change.
