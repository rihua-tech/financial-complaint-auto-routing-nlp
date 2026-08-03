# Version 2 DistilBERT Challenger Model Card

## Model Details

| Item | Value |
|---|---|
| Status | Frozen transformer challenger |
| Base model and tokenizer | `distilbert/distilbert-base-uncased` |
| Exact revision | `12040accade4e8a0f71eabdb258fecc2e7e948be` |
| Architecture | `DistilBertForSequenceClassification` |
| Output categories | 8, in the canonical locked order |
| Maximum token length | 256 |
| Training data | 26,433 locked 2024 development rows |
| Final training epochs | 4, the median of fold-best epochs `[4, 2, 4, 4, 4]` |
| Routing signals | Top softmax score and top-two softmax margin |
| Locked routing thresholds | Top score `0.22`; margin `0.91` |
| Artifact storage | Local and Git-ignored |

The complete training configuration, environment, and file fingerprints are recorded in the [`Version 2 model manifest`](v2_model_manifest.md). All saved parameters and synthetic logits passed finite-value checks.

## Intended Use

The model is a frozen challenger for an internal, notebook-centered complaint-routing prototype. It predicts one of eight CFPB product categories and supports a selective-routing analysis in which both locked score conditions must pass before an automatic-routing recommendation is made.

The model is intended for research, portfolio demonstration, matched benchmarking, and future controlled validation. It is not a production service, does not replace human reviewers, and must not make legal, compliance, eligibility, or factual determinations.

## Data and Evaluation Boundaries

- Duplicate-conflict remediation produced 33,042 corrected 2024 modeling rows.
- The model was developed only on the 26,433-row 2024 development partition.
- The shared 6,609-row 2024 internal test was scored only after the model and routing policy were frozen. Because Version 1 outcomes were already known, it is a matched benchmark rather than a new untouched Version 2 holdout.
- The 2025 comparison is retrospective because Version 1 had already used the sample. The 30,156-row primary leakage-resistant cohort is the headline result; the 49,225-row secondary operational cohort is only a sensitivity view.
- No 2025 result changed model weights, tokenizer, maximum length, epochs, learning rate, loss, class weights, calibration, thresholds, or selection rules.

## Development Evidence

Five-fold development OOF evaluation covered all 26,433 development rows exactly once.

| Metric | Development OOF result |
|---|---:|
| Accuracy | 0.8797 |
| Macro F1 | 0.7820 |
| Weighted F1 | 0.8776 |
| Locked-policy coverage | 0.7550 |
| Locked-policy routed accuracy | 0.9514 |
| Locked-policy misroute rate | 0.0486 |

The routing thresholds were selected from development OOF outputs only under the precommitted coverage and misroute constraints. Softmax scores and margins are uncalibrated signals, not probabilities or confidence.

## Matched 2024 Benchmark Evidence

| Metric | Frozen Version 2 result |
|---|---:|
| Rows | 6,609 |
| Accuracy | 0.8882 |
| Macro F1 | 0.7949 |
| Weighted F1 | 0.8859 |
| Routing coverage | 0.8177 |
| Review rate | 0.1823 |
| Routed accuracy | 0.9476 |
| Misroute rate | 0.0524 |

Version 2 improved Accuracy, Macro F1, Weighted F1, and coverage over Version 1 on the shared benchmark, but routed accuracy was slightly lower and the misroute rate slightly higher. Debt collection, credit card, student loan, and vehicle loan or lease had higher Version 2 category-level routing risk. See the [`shared 2024 comparison`](v1_v2_2024_comparison.md).

## Retrospective 2025 Evidence

| Cohort | Rows | Accuracy | Macro F1 | Weighted F1 | Coverage | Review rate | Routed accuracy | Misroute rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Primary leakage-resistant headline** | **30,156** | **0.8404** | **0.7620** | **0.8364** | **0.7571** | **0.2429** | **0.9174** | **0.0826** |
| Secondary operational sensitivity | 49,225 | 0.8751 | 0.7586 | 0.8701 | 0.8007 | 0.1993 | 0.9431 | 0.0569 |

Relative to Version 1 on the primary cohort, Version 2 improved Accuracy by 0.0089, Macro F1 by 0.0093, Weighted F1 by 0.0057, and coverage by 0.0320. Routed accuracy was 0.0029 lower and the misroute rate 0.0029 higher. Relative to Version 2's shared 2024 benchmark, primary Accuracy declined by 0.0478, Macro F1 by 0.0330, Weighted F1 by 0.0495, coverage by 0.0606, and routed accuracy by 0.0302; review and misroute rates each increased by 0.0606 and 0.0302.

The slight Macro F1 gains over Version 1 were precision-led: macro precision rose while macro recall fell on both 2025 cohorts, consistent with the observed debt-collection and student-loan recall declines.

The largest primary F1 gains versus Version 1 were money transfer (+0.0384) and checking or savings (+0.0338). Student loan (-0.0257) and debt collection (-0.0129) declined. Primary category-level misroute rates were especially high for student loan (0.3208), debt collection (0.2984), and money transfer (0.2420). These figures are descriptive project evidence, not approved risk levels.

The full retrospective evidence is in [`Version 2 Retrospective 2025 V1-versus-V2 Comparison`](v2_2025_retrospective_results.md).

## Signal and Token Behavior

The 2025 primary top-score mean was 0.9386 and the top-two-margin mean was 0.8915, both below the frozen-model 2024 benchmark values of 0.9504 and 0.9136. The primary margin-threshold failure share increased from 0.1823 to 0.2429. These shifts are descriptive; they do not establish why behavior changed.

The locked 256-token limit truncates 38.01% of 2024 development narratives, 41.15% of 2025 primary narratives, and 31.75% of 2025 secondary narratives. The primary 2025 mean token length was 299.26, with a median of 207. This material information-loss and compute trade-off must be considered when interpreting results.

## Performance and Operational Requirements

The frozen artifact is 256.35 MiB, approximately 79 times the Version 1 serialized artifact. On the recorded Windows workstation, steady-state Version 2 throughput was approximately 15 rows per second for the fixed 128-row, batch-size-16 benchmark, compared with more than 3,400 rows per second for Version 1. These local measurements include tokenization for Version 2 and are hardware- and implementation-specific, not production service-level benchmarks.

Version 2 requires the PyTorch, Transformers, tokenizer, and model-artifact stack. Operational use would require secure artifact management, privacy controls, access restrictions, audit logging, monitoring, drift controls, latency planning, and human-review governance.

## Limitations and Risks

- The 2024 and 2025 data are sampled public CFPB complaints, not the complete operational population or institution-specific intake data.
- Evaluation is limited to eight selected product categories with substantial class imbalance.
- Credit reporting dominates the sample and strongly influences weighted metrics.
- Small category supports make per-category estimates less stable.
- The 256-token ceiling removes part of many narratives.
- Softmax scores and margins are not calibrated probabilities.
- The routing thresholds are project assumptions, not stakeholder-approved production risk standards.
- The secondary 2025 cohort retains repeated texts and prior-year overlap and is only a sensitivity view.
- The 2025 sample is exhausted as unbiased evidence and cannot be reused for tuning, calibration, threshold changes, or model selection.
- No fairness, causality, statistical-significance, production-readiness, deployment-readiness, cost-savings, workload-reduction, regulatory-approval, or governance-approval claim is made.

## Human Oversight

Human review remains required when either locked routing threshold fails. Category-specific review is not implemented by the current policies. Future business governance may require additional category-specific controls, especially where observed category risk is high or support is small. Such a policy would require stakeholder approval and new validation; it must not be tuned against the exhausted 2025 sample.

## Status and Required Future Evidence

- **Version 1:** temporally validated benchmark.
- **Version 2:** frozen transformer challenger with matched 2024 evaluation and retrospective 2025 comparison.
- **Independent Version 2 temporal promotion evidence:** pending a new untouched period, currently planned as full-year 2026 data.

The 2025 retrospective evidence is mixed and does not justify declaring Version 2 the independently validated temporal champion. Version 1 remains the temporally validated benchmark; Version 2 remains the preferred internal challenger for a future untouched evaluation. A future project champion would still not be a production-approved model.
