# Business Case

## Business Problem

Financial services organizations receive written complaints across credit cards, mortgages, bank accounts, loans, debt collection, credit reporting, and money-transfer products. Each complaint must reach the appropriate team, but fully manual triage can be slow, inconsistent, and difficult to audit at high volume. An incorrect automated route can also delay handling or increase operational and compliance risk.

This project demonstrates an internal NLP prototype that classifies a public CFPB complaint narrative into one of eight product categories and applies routing rules that recommend either an automatic route or human review.

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
7. evaluates the selected pipeline on a 6,609-row final internal test fold; and
8. applies locked decision-score and score-margin rules to recommend automatic routing or human review.

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

Subject to future validation and governance, a similar workflow could support:

- more consistent initial product-category recommendations;
- future policy experimentation with category-specific review for ambiguous or higher-risk complaints;
- aggregate visibility into model errors and review volumes; and
- auditable experimentation with routing rules.

The project does not claim realized cost savings, guaranteed workload reduction, deployment, regulatory approval, or production readiness.

## Limitations and Production Considerations

- The data is a public CFPB sample, not institution-specific intake data.
- The corrected evaluation is internal to 2024; the protected 2025 holdout was not used.
- Historical product labels may be ambiguous or differ from an organization's ownership structure.
- Class imbalance and small category samples make some estimates less stable.
- Linear SVM decision scores are not probabilities.
- The routing thresholds are project assumptions, not stakeholder-approved operating limits.
- No fairness study, calibration study, production workload study, or live monitoring has been completed.
- Complaint narratives may contain sensitive information.

Before production consideration, the workflow would require out-of-time validation, privacy and security review, compliance and governance approval, category-specific error-cost decisions, human-review procedures, monitoring, drift controls, secure storage, audit logging, and incident-response ownership.

## Next Business Decisions

1. Complete a pre-specified 2025 out-of-time validation without changing the locked Version 1 design based on holdout outcomes.
2. Define category-specific error costs and acceptable routing policies with stakeholders.
3. Decide which categories, if any, can receive automatic-routing recommendations.
4. Establish human-review, escalation, override, and audit procedures.
5. Evaluate operational impact in a controlled environment before making workload or value claims.
