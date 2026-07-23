# Financial Complaint Auto-Routing with NLP

**Leakage-safe text classification and human-in-the-loop routing for public CFPB complaints**

[![CI](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/actions/workflows/ci.yml)

## Project Overview

Financial institutions, fintech firms, and complaint operations teams receive written complaints that must be routed to the appropriate product team. Manual triage can be slow and inconsistent, while an incorrect automated route can delay review or create operational risk.

This repository implements an internal Version 1 NLP prototype that predicts one of eight CFPB product categories from a public consumer complaint narrative. The model supplies a routing recommendation; a decision-score policy sends lower-signal or ambiguous cases to human review. It does not make legal or factual determinations and is not a deployed production service.

## Version 1 at a Glance

| Item | Verified result |
| --- | --- |
| Data source | Public CFPB consumer complaint narratives |
| Development period | 2024 only |
| Protected future holdout | Separate 2025 CFPB sample, 50,000 rows; reserved for future out-of-time validation and not loaded or used for Version 1 |
| Validated input sample | 50,000 rows |
| Rows after duplicate-leakage remediation | 33,042 |
| Development / final internal test | 26,433 / 6,609 |
| Product categories | 8 |
| Development/test normalized-text overlap | 0 groups |
| Selected model | TF-IDF + Linear SVM |
| Final internal-test accuracy | 0.8712 |
| Final internal-test Macro F1 | 0.7671 |
| Final internal-test Weighted F1 | 0.8715 |

These are internal 2024 results. They do not establish production readiness or performance on future data.

## Business Users and Workflow

The prototype is relevant to complaint intake, product operations, compliance operations, and risk analytics teams. It demonstrates this decision-support flow:

`Complaint narrative -> validation -> text preparation -> model recommendation -> routing rules -> automatic-route recommendation or human review -> aggregate reporting`

Human review remains central. The implemented routing rules assign complaints to review when either score threshold fails or model signals are tied, invalid, non-finite, or otherwise unusable. Higher-risk categories are not automatically assigned to review by the current code; a future business policy may add category-specific review controls.

## Completed Technical Approach

1. Downloaded and validated a monthly-balanced, daily-stratified 2024 CFPB sample.
2. Applied light text cleaning while preserving most complaint language.
3. Audited missing values, text-length outliers, duplicates, class balance, and label conflicts.
4. Removed normalized-text groups with conflicting labels and kept one representative from repeated same-label groups.
5. Used group-aware splitting so normalized duplicate text could not cross development and final-test partitions.
6. Compared Scikit-learn pipelines using TF-IDF with Logistic Regression, Multinomial Naive Bayes, and Linear SVM.
7. Selected Linear SVM using five-fold group-aware cross-validation on development data only.
8. Evaluated the selected pipeline once on the 6,609-row final internal test fold.
9. Selected routing thresholds from development out-of-fold decision scores, then applied the locked policy once to the final test set.
10. Added tested routing-rule utilities and aggregate documentation without committing narratives, row-level predictions, CSV files, or model artifacts.

### Model Comparison

| Model | Development CV Macro F1 |
| --- | ---: |
| TF-IDF + Logistic Regression | 0.7430 |
| TF-IDF + Multinomial Naive Bayes | 0.3519 |
| **TF-IDF + Linear SVM** | **0.7687** |

Values are five-fold group-aware development cross-validation means. Macro F1 was the primary selection metric because the eight categories are imbalanced.

## Leakage-Safe Evaluation

The original row-level split allowed 3,876 of 9,840 test rows (39.39%) to share normalized text with training. Those earlier results are superseded. The corrected workflow:

- excludes normalized-text groups that have conflicting product labels;
- retains one row from repeated same-label normalized-text groups;
- keeps normalized-text groups intact during splitting and cross-validation; and
- confirms zero normalized-text overlap between development and final internal test data.

The corrected confusion matrix and detailed reports are available here:

- [Row-normalized confusion matrix](reports/figures/confusion_matrix.png)
- [Technical results summary](reports/results_summary.md)
- [Aggregate error analysis](reports/error_analysis.md)
- [Completed Version 1 model card](reports/model_card.md)

![Corrected Version 1 confusion matrix](reports/figures/confusion_matrix.png)

### Additional Data and EDA Evidence

- [Data preparation proof](reports/figures/data_preparation_proof.png)
- [Product distribution chart](reports/figures/product_distribution.png)
- [Text-length distribution chart](reports/figures/text_length_distribution.png)

## Human-in-the-Loop Routing

Linear SVM produces decision scores, not calibrated probabilities. The routing analysis uses two signals:

| Locked rule | Threshold |
| --- | ---: |
| Minimum top decision score | 0.08 |
| Minimum top-two score margin | 0.73 |

Both thresholds must pass for an automatic-routing recommendation. Otherwise, the complaint is assigned to human review.

| Final-test routing metric | Result |
| --- | ---: |
| Auto-routing coverage | 0.7705 (77.05%) |
| Human-review rate | 0.2295 (22.95%) |
| Auto-routed accuracy | 0.9503 (95.03%) |
| Auto-routed misroute rate | 0.0497 (4.97%) |

The aggregate 4.97% misroute rate does not mean every category remained below 5%. Money transfer/virtual currency/money service, Vehicle loan or lease, Debt collection, and Credit card showed higher observed category-level routing risk. Several of these categories also have small auto-routed counts, so their estimates are less stable.

- [Routing decision-score summary](reports/figures/routing_decision_score_summary.png)

![Decision-score routing summary](reports/figures/routing_decision_score_summary.png)

The 5% development misroute rule is a project assumption, not a stakeholder-approved or production-validated risk limit. The results demonstrate selective routing behavior; they do not guarantee workload reduction in an operating environment.

## Tech Stack

- Python, Pandas, NumPy, and Requests
- Jupyter Notebook
- Scikit-learn pipelines and TF-IDF
- Logistic Regression, Multinomial Naive Bayes, and Linear SVM
- Matplotlib and Seaborn
- `unittest` routing-rule tests
- Git, GitHub, and GitHub Actions
- CFPB Consumer Complaint Database API

## Current Status

Completed:

- 2024 data ingestion, validation, cleaning, and exploratory analysis
- duplicate-leakage remediation and group-aware evaluation
- three-model comparison and Linear SVM selection
- final internal 2024 evaluation and aggregate error analysis
- decision-score threshold analysis and human-review recommendations
- tested routing-rule logic
- Version 1 results, model card, system documentation, and portfolio summary

Not implemented or approved:

- deployed prediction API or batch-scoring service
- operational dashboard or review queue
- production monitoring, secure storage, and audit logging
- scheduled retraining
- privacy, security, compliance, governance, or stakeholder approval

The fitted pipeline exists only as a local, Git-ignored artifact at `models/best_tfidf_classifier.joblib`. It is not committed to the repository. The repository does not provide a deployed inference service.

## Limitations

- The evaluation uses a sampled 2024 CFPB dataset, not institution-specific intake data.
- Within each daily sampling window, CFPB API pagination may still reflect API sort order rather than fully random selection.
- Public narratives and historical CFPB labels may contain ambiguity, label noise, and selection bias.
- The dominant credit-reporting category strongly influences weighted metrics.
- Smaller categories have lower support and less stable estimates.
- Exact normalized-text hashing does not detect paraphrased near-duplicates.
- Linear SVM decision scores and margins are not calibrated probabilities.
- Routing thresholds are project assumptions and have not received production or stakeholder approval.
- No fairness evaluation, probability calibration, operational workload study, or production monitoring result is claimed.
- The protected 2025 data was not loaded or used for Version 1 model selection, evaluation, or routing analysis.

## Roadmap

1. Run a separately governed 2025 out-of-time validation after the evaluation plan is locked.
2. Review category-specific error costs and routing thresholds with operational stakeholders.
3. Evaluate probability calibration and refine category-specific human-review policies.
4. Add privacy, security, fairness, explainability, monitoring, and drift controls before any production consideration.
5. Compare DistilBERT with the locked Version 1 baseline as future work, using the same leakage-safe data policy.
6. Design production APIs, dashboards, storage, retraining, and governance only after validation and approval.

## Repository Guide

| Path | Purpose |
| --- | --- |
| `notebooks/01_data_download.ipynb` | Local-first CFPB data acquisition and validation |
| `notebooks/02_eda_cleaning.ipynb` | Text cleaning and target preparation |
| `notebooks/03_data_quality_product_distribution.ipynb` | Data-quality and distribution analysis |
| `notebooks/04_sklearn_baseline_model.ipynb` | Leakage-safe comparison, selection, and final Version 1 evaluation |
| `notebooks/05_decision_score_routing.ipynb` | Development OOF threshold selection and final-test routing analysis |
| `notebooks/06_final_project_submission.ipynb` | Standalone course submission notebook |
| `reports/results_summary.md` | Verified Version 1 and routing results |
| `reports/model_card.md` | Intended use, limitations, oversight, and monitoring guidance |
| `docs/system_design.md` | Completed prototype components and future architecture |
| `docs/portfolio_summary.md` | Portfolio description and resume-ready bullets |
| `src/routing_rules.py` | Tested routing decision logic |
| `tests/test_routing_rules.py` | Routing boundary, validation, and class-order tests |

Raw and processed CSV files, complaint narratives, row-level predictions, and fitted model artifacts remain local and Git-ignored.

## Documentation

- [Business case](docs/business_case.md)
- [Data decisions and quality notes](docs/data_decisions.md)
- [Data-ingestion design](docs/data_ingestion.md)
- [Modeling plan and completed Version 1 workflow](docs/modeling_plan.md)
- [System design](docs/system_design.md)
- [Portfolio summary](docs/portfolio_summary.md)
