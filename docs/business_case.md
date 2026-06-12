# Business Case

## Business Problem

Financial services organizations receive written complaints across products such as credit cards, mortgages, bank accounts, loans, debt collection, and credit reporting. Routing each complaint to the correct product or operations team is a high-volume triage task that can become slow, inconsistent, and difficult to audit when handled fully by hand.

This project simulates a business workflow where NLP helps classify consumer complaint narratives into financial product categories for routing support.

## Intended Users

Intended users include:

- Customer support operations teams responsible for intake and triage.
- Product operations teams that receive routed complaints.
- Compliance teams that monitor complaint handling and escalation.
- Risk and analytics teams that evaluate complaint patterns and model behavior.
- Business managers who need visibility into routing volume, manual review workload, and automation coverage.

## Why Complaint Routing Matters

Complaint routing matters because delays or misroutes can create operational backlogs, poor customer experiences, inconsistent handling, and compliance risk. A structured routing process can help teams:

- Identify the likely product area quickly.
- Prioritize complaints that need specialized review.
- Track routing decisions and review outcomes.
- Report complaint volume by product category.
- Create feedback loops for improving operations.

## Operational Workflow

The planned operational workflow is:

1. A complaint narrative enters the intake queue.
2. The text is validated for minimum usable content.
3. A classification model predicts the most likely product category.
4. A routing policy evaluates prediction confidence and ambiguity.
5. High-confidence predictions may receive an auto-routing recommendation.
6. Low-confidence, missing, ambiguous, or unsupported predictions move to human review.
7. Review outcomes are logged for monitoring and future model improvement.
8. Summary reports track model performance and business impact.

This repository currently contains framework documentation and placeholders for this workflow. It does not yet contain a trained model.

## How NLP Supports Complaint Routing

NLP supports complaint routing by converting unstructured complaint narratives into model features and predicting a structured product category. The first planned baseline uses TF-IDF features with traditional Scikit-learn classifiers. These models are appropriate for a transparent baseline because they are comparatively fast to train, easy to evaluate, and easier to explain than larger transformer models.

The NLP component is intended to produce routing recommendations, not final business decisions.

## Human-in-the-Loop Review Concept

Human review remains part of the planned workflow. A complaint should be routed to manual review when:

- The model confidence is below the auto-routing threshold.
- The top predictions are too close together.
- Required input text is missing or too short.
- The predicted category is unsupported by downstream operations.
- Business rules require review because of risk, escalation, or compliance concerns.

Human review decisions can later be used as feedback for monitoring and model improvement.

## Success Metrics to Be Reported Later

Model quality metrics to report after baseline training:

- Accuracy.
- Macro F1.
- Weighted F1.
- Per-class precision, recall, and F1.
- Confusion matrix.

Business-oriented metrics to report after routing policy testing:

- Auto-routing coverage.
- Human review rate.
- Low-confidence case volume.
- Top-3 prediction usefulness.
- Misroute risk by product category.
- Review workload reduction estimate.

These metrics are planned only. No results are reported until model training and evaluation are complete.

## Limitations and Production Considerations

Current limitations:

- The current local dataset is a late-2024 newest-first CFPB API sample.
- EDA, cleaning, baseline training, and evaluation are not complete in this branch.
- No trained model artifact is available in the repository.
- Public CFPB narratives may differ from private institution-specific complaint channels.

Production considerations:

- Privacy review and access control for complaint text.
- Data retention and deletion policies.
- Bias, fairness, and performance monitoring across complaint categories.
- Human review procedures for ambiguous or high-risk cases.
- Audit logging for routing recommendations and review overrides.
- Monitoring for data drift and model performance degradation.
- Clear ownership for model updates, incident response, and compliance review.
