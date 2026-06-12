# Model Card

Status: Template only. To be completed after baseline model selection and evaluation.

## Model Details

- Model name: TBD.
- Model type: TBD.
- Version: TBD.
- Training date: TBD.
- Owner: TBD.
- Intended workflow: Complaint product-category routing support.

## Intended Use

The model is intended to support initial routing recommendations for consumer financial complaint narratives. It should be used as a decision-support tool with human review for low-confidence, ambiguous, missing, unsupported, or high-risk cases.

## Out-of-Scope Use

The model should not be used to:

- Make final regulatory, legal, or customer-impacting decisions without review.
- Replace required human review or compliance procedures.
- Score private complaint data without privacy and governance review.
- Infer sensitive attributes or profile consumers.

## Training Data

To be completed after Week 3 EDA and cleaning.

Planned details:

- Data source.
- Date range.
- Number of records.
- Included labels.
- Excluded records and reasons.
- Known sampling limitations.

## Evaluation Data

To be completed after train, validation, and test split decisions are finalized.

## Metrics

No metrics are available yet.

Planned metrics:

- Accuracy.
- Macro F1.
- Weighted F1.
- Per-class precision, recall, and F1.
- Confusion matrix.
- Auto-routing coverage.
- Human review rate.
- Top-3 prediction usefulness.

## Limitations

To be completed after evaluation.

Known current limitations:

- No trained model is available yet.
- The current local raw data sample is not a full-year random sample.
- Public CFPB complaint narratives may not match institution-specific complaint channels.
- Model predictions may be less reliable for underrepresented or ambiguous categories.

## Human Oversight

Human review should be required for low-confidence, ambiguous, missing, unsupported, escalated, or compliance-sensitive cases.

## Monitoring Plan

To be completed before any production use.

Planned monitoring areas:

- Prediction quality over time.
- Category-level precision and recall.
- Human override rate.
- Auto-routing coverage.
- Low-confidence volume.
- Data drift and label distribution changes.

## Approval Status

Not approved for production use. This model card is a template pending model training and evaluation.
