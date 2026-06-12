# Modeling Plan

## Objective

The modeling objective is to classify CFPB consumer complaint narratives into financial product categories. The business objective is to support complaint routing recommendations while keeping low-confidence or ambiguous cases in a human review process.

No modeling results are reported in this document. This is a plan for future baseline work.

## Planned Input and Target

- Input text: `complaint_what_happened`
- Target label: `product`
- Model-development data source: local 2024 CFPB complaint CSV downloaded during the completed data-ingestion workflow.
- Future holdout data source: local 2025 CFPB complaint CSV downloaded separately for out-of-time validation.
- Sampling strategy: monthly-balanced + daily-stratified CFPB API sampling for each year. This reduces recency bias compared with the original late-2024 newest-first sample and improves within-month coverage compared with simple monthly newest-first sampling.

Week 3 EDA and cleaning must define the final 2024 modeling dataset before baseline training starts. The 2024 data may later be split into train, validation, and internal test sets. The 2025 data should remain separate as an out-of-time holdout dataset and should not be used during baseline model training or model selection.

## Planned Baseline Models

The initial baseline will use TF-IDF text features with traditional supervised classifiers:

- TF-IDF + Logistic Regression.
- TF-IDF + Naive Bayes.
- TF-IDF + Linear SVM.

These baselines are planned because they are practical, fast to train, and useful for establishing an interpretable performance benchmark before considering larger NLP models.

## Planned Evaluation Metrics

The planned model evaluation metrics are:

- Accuracy.
- Macro F1.
- Weighted F1.
- Per-class precision.
- Per-class recall.
- Per-class F1.
- Confusion matrix.

Evaluation results should be reported only after the baseline models are trained and evaluated.

## Planned Business Metrics

The planned business-oriented metrics are:

- Auto-routing coverage: share of complaints that meet auto-routing criteria.
- Human review rate: share of complaints sent to manual review.
- Low-confidence case rate: share of complaints below the confidence threshold.
- Top-3 prediction usefulness: whether the correct label appears in the model's top three predicted categories.
- Misroute risk indicators: categories with frequent confusion or low recall.

These metrics should be calculated after model outputs and routing thresholds are available.

## Planned Modeling Workflow

1. Complete Week 3 EDA and cleaning on the 2024 model-development dataset.
2. Define 2024 train, validation, and internal test split rules.
3. Build a TF-IDF preprocessing and modeling pipeline.
4. Train Logistic Regression, Naive Bayes, and Linear SVM baselines.
5. Compare metrics using a consistent evaluation set.
6. Select a baseline candidate for deeper error analysis.
7. Generate the results summary, error analysis, and model card.
8. Test routing thresholds against model confidence outputs.
9. Reserve the 2025 dataset for future out-of-time holdout testing after model selection.

## DistilBERT Future Work

A DistilBERT model is a future upgrade, not part of the current baseline framework. It should be considered only after:

- Baseline Scikit-learn models are trained and evaluated.
- Data cleaning and label handling decisions are documented.
- Baseline routing metrics are available.
- The additional complexity, runtime, and governance needs of a transformer model are justified.

Future DistilBERT work should be clearly compared against the baseline rather than presented as a replacement by default.
