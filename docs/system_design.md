# System Design

## Scope

This repository implements a notebook-centered AI/NLP business solution prototype for CFPB complaint classification, leakage-safe evaluation, human-review routing, and one-time out-of-time validation. It does not implement a production prediction service.

## Architecture

```mermaid
flowchart LR
    subgraph Completed["Completed internal prototype"]
        A[Public CFPB API] --> B[Local Git-ignored CSV]
        B --> C[Validation and light text cleaning]
        C --> D[Duplicate and label-conflict remediation]
        D --> E[Group-aware development and final-test split]
        E --> F[TF-IDF plus Linear SVM]
        F --> G[Internal metrics and confusion matrix]
        F --> H[Decision scores and top-two margins]
        H --> I{Both routing thresholds pass?}
        I -->|Yes| J[Automatic-route recommendation]
        I -->|No| K[Human-review recommendation]
        V[Precommitted 2025 protocol] --> W[2024 reproduction and 2025 integrity gates]
        B2[Local Git-ignored 2025 CSV] --> W
        F --> W
        W --> X[Primary and secondary cohort evaluation]
        X --> Y[Classification routing and drift results]
        G --> L[Aggregate reports]
        J --> L
        K --> L
        Y --> L
    end

    subgraph Future["Future production components"]
        M[Prediction API or batch service]
        N[Human-review dashboard]
        O[Secure operational storage]
        P[Monitoring and drift detection]
        Q[Scheduled retraining]
        R[Deployment and governance approval]
    end
```

The completed and future subgraphs are intentionally separate. The repository produces model and routing evidence; it does not connect the prototype to live complaint intake or downstream business systems.

## Component Status

| Component | Status | Evidence or boundary |
| --- | --- | --- |
| Data ingestion | Completed for local research use | `notebooks/01_data_download.ipynb`, `docs/data_ingestion.md` |
| Data validation and text preparation | Completed | Notebooks 02-04 and aggregate documentation |
| Duplicate-leakage remediation | Completed | Conflicting groups removed; group overlap asserted as zero |
| Model comparison | Completed | Logistic Regression, Multinomial Naive Bayes, and Linear SVM |
| Selected classifier | Completed | TF-IDF + Linear SVM |
| Internal evaluation | Completed | 2024 final internal test metrics and confusion matrix |
| Routing analysis | Completed | Locked score and margin thresholds |
| Routing-rule implementation | Completed for prototype use | `src/routing_rules.py` |
| Routing-rule tests | Completed | `tests/test_routing_rules.py` |
| Pre-holdout protocol | Completed before 2025 access | `reports/2025_validation_protocol.md` |
| 2024 reproduction and 2025 integrity gates | Completed | `notebooks/07_2025_out_of_time_validation.ipynb` |
| 2025 cohort construction | Completed | Primary leakage-resistant and secondary operational cohorts |
| 2025 out-of-time evaluation | Completed | Classification, routing, drift, and 2024-versus-2025 comparisons |
| Aggregate reporting | Completed | Results summaries, model card, holdout report, and figures |
| Fitted model artifact | Local only | Git-ignored; not distributed in the repository |
| Prediction interface | Not implemented | No supported inference module, API, CLI, or batch service is provided |
| Production deployment | Not implemented or approved | Future work |

## Completed Data Flow

### 1. Ingestion and Validation

The data-ingestion notebook retrieves public CFPB complaints and validates required fields, date coverage, complaint identifiers, narrative availability, and product labels. Raw CSV files are stored locally under `data/raw/` and ignored by Git.

Version 1 development, model selection, internal evaluation, and routing-threshold selection used only the validated 2024 sample. The separate 2025 file was protected during development and later evaluated once as the locked out-of-time holdout.

### 2. Text Preparation

The prototype:

- removes URL-like text;
- collapses repeated whitespace;
- trims surrounding whitespace;
- checks missing narratives and labels;
- reports text-length outliers in aggregate; and
- preserves most language for TF-IDF.

Processed CSV files remain local and Git-ignored.

### 3. Leakage-Safe Modeling

Normalized cleaned text is represented by a stable SHA-256 grouping key. Conflicting-label groups are excluded, repeated same-label groups are reduced to one representative, and group-aware partitioning prevents normalized text from crossing development and final-test boundaries.

The selected Scikit-learn pipeline combines TF-IDF and Linear SVM. The pipeline is fitted locally and saved to an ignored model path; it is not a committed deployable artifact.

### 4. Internal Evaluation

The workflow reports:

- Accuracy, Macro F1, and Weighted F1;
- per-category precision, recall, F1, and support;
- a row-normalized confusion matrix;
- duplicate-leakage audit results; and
- aggregate error interpretation.

All reported evaluation data is aggregate. Complaint narratives and row-level predictions are not committed.

### 5. Routing Rules

The routing policy uses:

- minimum top decision score: 0.08; and
- minimum top-two score margin: 0.73.

Both conditions must pass for an automatic-routing recommendation. Otherwise, the result is a human-review recommendation. Decision scores are not calibrated probabilities.

`src/routing_rules.py` validates score arrays and class-label alignment, applies inclusive threshold boundaries, and routes tied, malformed, non-finite, or below-threshold scores to review.

### 6. Human Review

The repository identifies cases for review but does not implement a review queue or dashboard. A future operational workflow would need:

- reviewer identity and access controls;
- reason codes, overrides, and escalation rules;
- category-specific risk policies;
- audit logging;
- service-level expectations; and
- feedback and quality-review processes.

### 7. Locked 2025 Out-of-Time Validation

Before opening the 2025 CSV, the project committed the model configuration, cleaning rules, file fingerprints, classes, cohorts, metrics, comparison rules, and routing thresholds. Notebook 07 then:

- reproduced the complete locked 2024 reference gate;
- verified the 2025 file path, size, fingerprint, and ingestion structure;
- constructed the 30,156-row primary leakage-resistant headline cohort;
- constructed the 49,225-row secondary operational sensitivity cohort, which retains repeated text and cross-year overlap; and
- evaluated classification, routing, category behavior, and descriptive drift without fitting or changing the workflow.

Primary 2025 accuracy was 0.8315, Macro F1 was 0.7527, and routing coverage was 0.7251 with 0.9203 routed accuracy and a 0.0797 misroute rate. These weaker headline results are reported directly; the more favorable secondary cohort remains a sensitivity view.

The 2025 sample is now exhausted as an unbiased holdout. Any future model or routing-policy change requires a new untouched validation period.

### 8. Reporting

Completed reporting includes:

- `notebooks/07_2025_out_of_time_validation.ipynb`;
- `reports/2025_validation_protocol.md`;
- `reports/2025_holdout_results.md`;
- `reports/results_summary.md`;
- `reports/error_analysis.md`;
- `reports/model_card.md`;
- `reports/figures/confusion_matrix.png`; and
- `reports/figures/routing_decision_score_summary.png`;
- `reports/figures/2025_confusion_matrix.png`; and
- `reports/figures/2024_vs_2025_comparison.png`.

## Future Production Architecture

The following components are not implemented:

### Prediction API or Batch Service

A supported service would need versioned preprocessing, model loading, input validation, authentication, rate limits, error handling, and reproducible deployment.

### Dashboard and Human-Review Queue

A future interface would present the recommended category, review reason, relevant model signals, and approved context without exposing unnecessary sensitive text.

### Secure Production Storage

Production complaint text and outputs would require encryption, access controls, retention rules, deletion procedures, environment separation, and privacy review.

### Monitoring

A monitoring system would track data quality, category distributions, routing coverage, review rates, overrides, per-category performance, score and margin distributions, drift, latency, and service health. No live monitoring result exists.

### Scheduled Retraining

Retraining would require a versioned label taxonomy, reviewed training data, reproducible pipelines, regression tests, independent evaluation, rollback plans, and a new protected holdout.

### Deployment and Governance Approval

Any deployment would require privacy, security, compliance, model-risk, operational, and stakeholder approval. The current thresholds are project assumptions and are not approved production limits.

## Security and Privacy Boundaries

- Raw and processed CSV files are local and ignored by Git.
- Fitted model artifacts are local and ignored by Git.
- Complaint narratives and row-level predictions are excluded from reports.
- The repository contains aggregate metrics and public-data workflow code only.
- Public availability of a narrative does not remove the need for stronger controls in a production environment.
