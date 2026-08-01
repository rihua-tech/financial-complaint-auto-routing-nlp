# Version 2 Retrospective 2025 Comparison Protocol

Status: **Pre-execution protocol for GitHub Issue #42. Version 2 scoring on
2025 data must not begin until this protocol has been reviewed and committed.**

Related issue: [GitHub Issue #42](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/issues/42)

This protocol is governed by the committed
[Version 2 experiment plan](../docs/v2_experiment_plan.md), the original
[Version 1 2025 validation protocol](2025_validation_protocol.md), the
[completed Version 1 2025 results](2025_holdout_results.md), the
[Version 1 results summary](results_summary.md), the
[Version 2 data manifest](v2_data_manifest.md), the
[Version 2 model manifest](v2_model_manifest.md), and the
[shared 2024 champion-challenger comparison](v1_v2_2024_comparison.md).

## Purpose, Scope, and Required Language

Issue #42 will compare the frozen Version 1 TF-IDF + Linear SVM benchmark and
the frozen Version 2 DistilBERT challenger on the existing 2025 cohorts.

- This is a **retrospective 2025 comparison**.
- The 2025 sample was already evaluated for Version 1 and is exhausted as an
  unbiased holdout. It is not a new untouched Version 2 holdout.
- The 30,156-row primary leakage-resistant cohort is the headline result.
- The 49,225-row secondary operational cohort is an operational sensitivity
  view because it retains repeated texts and cross-year overlap.
- The comparison may identify a preferred internal challenger or candidate
  for future validation, but it will not declare a final independently
  temporally validated champion.
- A new untouched time period is required before any final project-champion
  decision. A project champion would still not be a production-approved
  model.

The repository remains a notebook-centered internal prototype. The protocol
creation phase does not run either model, generate 2025 predictions, or
calculate new metrics.

## Protocol Baseline and Environment

| Item | Locked value |
| --- | --- |
| Protocol branch | `v2/issue-5-2025-retrospective` |
| Baseline Git commit | `495aa48d48db0318e14de0601d64fe4e1ef3c24f` |
| Conda environment | `complaint-v2` |
| Python | 3.11.15 |
| Scikit-learn | 1.9.0 |
| PyTorch | 2.9.1+cu126 |
| Transformers | 4.57.6 |
| Tokenizers | 0.22.2 |
| CUDA device | NVIDIA GeForce GTX 1650 |

The execution notebook must record the observed Git commit, environment, and
hardware. A mismatch in an asset fingerprint, class mapping, source count,
cohort count, or locked setting is a blocker; it does not authorize replacing
an artifact or changing this protocol.

## Frozen Version 1 Assets and Policy

| Item | Locked value |
| --- | --- |
| Model | TF-IDF + Linear SVM |
| Local artifact | `models/best_tfidf_classifier.joblib` |
| Size | 3,392,109 bytes |
| SHA-256 | `4514e7e49e305e408e2eaaf296d8607b33e9320547685339eff263e4dda0c94a` |
| Minimum top decision score | 0.08 |
| Minimum top-two decision-score margin | 0.73 |
| Class order | Fitted `pipeline.classes_`, matching the canonical order below |

Version 1 must be loaded without fitting. Use its existing text preparation,
fitted TF-IDF vocabulary and IDF values, `predict`, `decision_function`, and
the committed routing implementation. Version 1 decision scores and margins
are uncalibrated model signals, not probabilities.

## Frozen Version 2 Assets and Policy

### Model and tokenizer

| Item | Locked value |
| --- | --- |
| Model ID | `distilbert/distilbert-base-uncased` |
| Model revision | `12040accade4e8a0f71eabdb258fecc2e7e948be` |
| Model class | `DistilBertForSequenceClassification` |
| Tokenizer ID | `distilbert/distilbert-base-uncased` |
| Tokenizer revision | `12040accade4e8a0f71eabdb258fecc2e7e948be` |
| Tokenizer class | `DistilBertTokenizerFast` |
| Output labels | 8 |
| Maximum token length | 256 |
| Final artifact directory | `models/v2_distilbert_challenger/final/` |

The frozen final-artifact inventory is:

| File | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| `config.json` | 1,229 | `745d87e88a54bd5bd349b14aae194a1f523189cb6d6f377463419487fa43e370` |
| `model.safetensors` | 267,851,024 | `e05900579f16e96d75df968cedb71b2b2fde3aae95f1bf73dbe7147306287c23` |
| `special_tokens_map.json` | 132 | `3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6` |
| `tokenizer.json` | 711,494 | `8b79639ec74b46604e730f505186eaafb1006d2fd00f2c4930d168bb7f894680` |
| `tokenizer_config.json` | 1,283 | `21c3bea73b6711617c657664adcd4d0b02ce20d2db4b2ebdd722a6da8da28bcd` |
| `training_args.bin` | 6,033 | `568405730a290d2928d67b32870a9a965253e46bc2e9ed516048100a9ba475d8` |
| `training_summary.json` | 3,329 | `b8a149005ac05614230937c3620fcda2162b9f39c126a1aefa95ef8721a0bfcf` |
| `vocab.txt` | 231,508 | `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3` |
| **Total** | **268,806,032** | — |

Every file must match before 2025 scoring. Reloaded model parameters and a
synthetic output must be finite, the model must expose eight outputs, and the
model and tokenizer mappings must match the canonical mapping.

### Routing policy

| Item | Locked value |
| --- | --- |
| Local policy path | `models/v1_v2_2024_comparison/v2_routing_policy.json` |
| Policy SHA-256 | `9ca16a8533f26f8e00fd9d57c654af66fa78e21880f7fa7783a9d1adf964d818` |
| Development OOF source | `models/v2_distilbert_challenger/oof/development_oof_outputs.npz` |
| Development OOF SHA-256 | `72d59db97819d6f06b968520eddac2d0c1d590f36dea4efa627e9c123c1e5b13` |
| Minimum top softmax score | 0.22 |
| Minimum top-two softmax-score margin | 0.91 |

The Version 2 policy was selected from development OOF outputs before final
benchmark scoring. It must be reloaded and fingerprinted, not reselected or
rewritten. Both comparisons are inclusive and both thresholds must pass for
automatic routing. Transformer softmax scores and score margins are
**uncalibrated model signals**; they must not be called calibrated
probabilities, likelihoods, or real-world confidence.

### Frozen Version 2 inference configuration

Version 2 2025 scoring must use the same frozen configuration used for the
shared 2024 benchmark:

- evaluation-only inference with the reloaded final model in evaluation mode;
- batch size 16;
- tokenizer and model revision recorded above;
- standard DistilBERT special tokens;
- maximum length 256 with truncation enabled;
- dynamic per-batch padding to the longest sequence in the batch;
- canonical `label2id` and `id2label` mappings;
- CUDA inference with FP16 autocast in the validated `complaint-v2`
  environment; and
- no gradients, optimizer, fitting, calibration, or parameter updates.

Argmax labels, top softmax scores, and top-two margins must use the canonical
eight-class order. An unavailable or incompatible frozen artifact or execution
environment is a blocker, not permission to alter the model or policy.

## Canonical Eight-Category Label Order

Class order is fixed independently of frequency, source order, or predictions.

| Label ID | Product category |
| ---: | --- |
| 0 | Checking or savings account |
| 1 | Credit card |
| 2 | Credit reporting or other personal consumer reports |
| 3 | Debt collection |
| 4 | Money transfer, virtual currency, or money service |
| 5 | Mortgage |
| 6 | Student loan |
| 7 | Vehicle loan or lease |

No category may be renamed, merged, split, omitted, reordered, or mapped from
frequency or DataFrame row order.

## Locked 2025 Source and Cohorts

### Source integrity and structure

| Item | Locked value |
| --- | ---: |
| Source | `data/raw/cfpb_complaints_2025_raw.csv` |
| Source rows | 50,000 |
| Raw columns | 17 |
| File size | 73,806,040 bytes |
| SHA-256 | `b59d7842e786f00d6be26b7980a42f67474acb9040db293ddd3641204d25eb3a` |
| Date range | 2025-01-01 through 2025-12-31 |
| Duplicate complaint IDs | 0 |
| Missing or blank required fields | 0 |
| Locked eight-category rows | 49,225 |
| Familiar out-of-scope rows | 775 |
| Unfamiliar or changed labels | 0 |

The source file must be verified before parsing and remain unchanged. Required
fields are `complaint_what_happened`, `product`, `date_received`, and
`complaint_id`. Structural checks must be reported only in aggregate.

### Reproduction rules

Reproduce the cleaning, normalized-text grouping, overlap audit, conflict
handling, source-order preservation, and eight-category filtering exactly as
committed in the original Version 1 2025 protocol. Do not create a new
exclusion or cohort rule in response to Version 2 outcomes.

The secondary operational sensitivity cohort contains every otherwise
eligible locked-scope row:

| Cohort | Locked rows | Interpretation |
| --- | ---: | --- |
| Primary leakage-resistant | 30,156 | Official headline temporal comparison |
| Secondary operational sensitivity | 49,225 | Sensitivity view retaining repeated texts and cross-year overlap |

The primary cohort must reproduce this sequential flow:

| Primary-cohort stage | Excluded at stage | Remaining rows |
| --- | ---: | ---: |
| Start with locked-scope rows | 0 | 49,225 |
| Exclude overlap with either locked 2024 partition | 5,579 | 43,646 |
| Exclude remaining 2025 conflicting-label rows | 1,301 | 42,345 |
| Retain the first remaining same-label text | 12,189 | 30,156 |

The primary cohort must contain one row per normalized-text group, no
conflicting-label group, no normalized-text overlap with either locked 2024
partition, and all eight categories. The secondary cohort must preserve all
49,225 locked-scope rows. Both frozen models must receive exactly the same
rows within each cohort.

## Existing Reference Results to Reproduce

The Version 1 2025 results are existing evidence, not new outcomes to select
or tune against. Notebook 11 must reproduce them before Version 2 scoring.
Displayed values must match to four decimal places; full-precision values must
be used for calculations.

| Cohort | Rows | Accuracy | Macro F1 | Weighted F1 | Coverage | Review rate | Routed accuracy | Misroute rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2025 primary headline | 30,156 | 0.8315 | 0.7527 | 0.8306 | 0.7251 | 0.2749 | 0.9203 | 0.0797 |
| 2025 secondary sensitivity | 49,225 | 0.8771 | 0.7569 | 0.8766 | 0.7809 | 0.2191 | 0.9424 | 0.0576 |

The following shared 2024 results are frozen comparison references:

| Metric | Version 1 | Version 2 |
| --- | ---: | ---: |
| Accuracy | 0.8712 | 0.8882 |
| Macro F1 | 0.7671 | 0.7949 |
| Weighted F1 | 0.8715 | 0.8859 |
| Routing coverage | 0.7705 | 0.8177 |
| Human-review rate | 0.2295 | 0.1823 |
| Routed accuracy | 0.9503 | 0.9476 |
| Misroute rate | 0.0497 | 0.0524 |

A failed Version 1 reproduction, source mismatch, or cohort mismatch must stop
execution before Version 2 2025 scoring. Do not change either model or policy
to force a match.

## Locked Evaluation Plan

### Classification

Evaluate both frozen models separately on the primary and secondary cohorts.
Use the eight labels explicitly in canonical order and `zero_division=0`.
Calculate:

- row count and correct/incorrect prediction counts;
- accuracy;
- macro precision, recall, and F1;
- weighted precision, recall, and F1;
- per-category precision, recall, F1, and support; and
- confusion-matrix counts and row-normalized confusion matrices.

No category may be suppressed because of zero support or zero predictions.

### Selective routing

Apply each model's already locked routing policy without alteration. For each
model and cohort, calculate:

- auto-routed and human-review row counts;
- routing coverage and human-review rate;
- correct and incorrect auto-routed counts;
- routed accuracy and misroute rate;
- mutually exclusive review-reason counts and shares; and
- category-level support, auto-routed count, coverage, review rate, routed
  accuracy, and misroute rate.

Use `NA`, not zero, when a cohort or category has no auto-routed rows. Do not
calculate a misroute-rate difference when either comparison value is `NA`.

### Locked comparisons

Use full-precision values for calculations and round only for display.
Precommit the following descriptive comparisons:

1. For each model, compare the locked 2024 shared benchmark with the 2025
   primary headline cohort and the 2025 secondary sensitivity cohort.
2. Within each 2025 cohort, compare Version 2 with Version 1.
3. For each model, compare the secondary cohort with the primary cohort as a
   sensitivity analysis.
4. Compare overall classification, per-category classification, overall
   routing, review reasons, and category-level routing risk.

Signed differences must be calculated as `later or challenger - reference`:

- temporal comparison: `2025 - 2024`;
- model comparison: `Version 2 - Version 1`; and
- cohort sensitivity: `secondary - primary`.

Differences are descriptive evidence of observed model, time-period, or cohort
behavior. They do not establish causality or statistical significance.

### Transformer top-score and margin drift

For Version 2, report aggregate distributions for the top softmax score and
top-two softmax-score margin on:

- development OOF outputs, as policy-selection context;
- the frozen-model 2024 shared benchmark;
- the 2025 primary cohort; and
- the 2025 secondary cohort.

Report mean, population standard deviation, median, 5th, 25th, 75th, and 95th
percentiles; the shares failing the top-score threshold, margin threshold, and
both thresholds; and the mutually exclusive routing reasons. Two-sample
Kolmogorov-Smirnov statistics may be reported as descriptive diagnostics.

Development OOF signals come from the five development fold models, whereas
2024 and 2025 signals come from the frozen final model. This distinction must
remain explicit. Softmax scores and margins are uncalibrated model signals and
must not be interpreted as probabilities or proof of a cause.

### Token-length and truncation behavior

Use only the frozen tokenizer revision. Audit aggregate complete token lengths
with special tokens, no padding, and no truncation for the primary and
secondary cohorts. Do not display token IDs or row-level lengths.

Compare 2025 with the locked 26,433-row development audit:

| Development statistic | Locked value |
| --- | ---: |
| Mean tokens | 289.0243 |
| Population standard deviation | 386.8186 |
| Median tokens | 187 |
| 75th percentile | 352 |
| 90th percentile | 601 |
| 95th percentile | 837.4 |
| 99th percentile | 1,784 |
| Maximum | 8,136 |
| At or below 256 tokens | 61.9945% |
| Above 256 tokens | 38.0055% |
| Above 512 tokens | 13.4150% |

For both 2025 cohorts, report minimum, mean, population standard deviation,
median, 75th, 90th, 95th, and 99th percentiles, maximum, and the shares at or
below and above 256 tokens and above 512 tokens. The 256-token maximum is
already locked. Observed 2025 token lengths or truncation rates must not change
the tokenizer, maximum length, model, or any policy.

## Prohibited Changes and Claims

No 2025 result may change:

- Version 1 or Version 2 model weights;
- the tokenizer, tokenizer revision, vocabulary, or special-token behavior;
- the 256-token maximum or dynamic-padding rule;
- training epochs, learning rate, optimizer, scheduler, loss function, label
  smoothing, or class weights;
- preprocessing, cleaning, category scope, class order, cohort definitions,
  or exclusions;
- calibration;
- Version 1 thresholds `0.08` and `0.73`;
- Version 2 thresholds `0.22` and `0.91`; or
- model-selection, challenger, promotion, or champion rules.

Do not retrain, fine-tune, fit, refit, tune, calibrate, or reselect either
model or policy. After the retrospective run, do not return to Version 2
development to improve results against 2025.

The Issue #42 report and documentation must not claim:

- a new untouched Version 2 holdout;
- a final independently temporally validated champion;
- calibrated probabilities or real-world confidence;
- causality or statistical significance;
- production or deployment readiness;
- regulatory, governance, or risk approval; or
- cost savings or workload reduction.

## Locked Execution Order

1. Review and commit this protocol before any Version 2 2025 scoring.
2. Verify all source, model, tokenizer, OOF, and policy fingerprints; reproduce
   the existing primary and secondary cohort membership and aggregate counts.
3. Reproduce the committed Version 1 classification and routing results on
   both cohorts.
4. Evaluate the frozen Version 2 model and locked policy on the 30,156-row
   primary headline cohort.
5. Evaluate the same frozen Version 2 model and policy on the 49,225-row
   secondary operational sensitivity cohort.
6. Calculate the precommitted aggregate comparisons and diagnostics, then
   create reports and aggregate figures.
7. Update documentation using verified aggregate results without changing a
   model, tokenizer, cohort, or policy.

The execution notebook must stop before Version 2 scoring if any prerequisite,
fingerprint, environment, source, cohort, or Version 1 reproduction check
fails.

## Planned Issue #42 Deliverables

- `reports/v2_2025_retrospective_protocol.md`
- `notebooks/11_v2_2025_retrospective_comparison.ipynb`
- `reports/v2_2025_retrospective_results.md`
- `reports/v2_model_card.md`
- verified aggregate figures under `reports/figures/`
- updates to `README.md` and `docs/portfolio_summary.md`
- verified resume-ready bullets based only on completed aggregate results

This protocol phase creates only the first file. The remaining deliverables
must not be represented as complete before Notebook 11 runs successfully and
their values are verified.

## Privacy and Artifact Rules

- Display and commit only aggregate counts, metrics, tables, interpretations,
  and figures.
- Do not display or commit complaint narratives, complaint IDs,
  normalized-text hashes, token IDs, row-level token lengths, row-level true
  or predicted labels, logits, decision scores, softmax scores, or margins.
- Do not create or commit a processed 2025 CSV.
- Store any required row-level predictions, scores, timing records, or cohort
  membership artifacts only under a Git-ignored path beneath `models/`.
- Keep model files, tokenizer files, caches, checkpoints, source CSVs, and
  local policy artifacts Git-ignored and unstaged.
- Do not expose machine-specific absolute paths in notebook outputs, reports,
  or figures.
- Do not include raw complaint examples in documentation.

## Execution Validation Checklist

Before closing Issue #42, confirm:

- [ ] This protocol was committed before Version 2 2025 scoring.
- [ ] Every frozen asset, source, OOF, and policy size or fingerprint matched.
- [ ] The environment, model class, tokenizer, parameters, and canonical label
      mapping matched.
- [ ] The primary cohort reproduced exactly 30,156 rows and remained the
      headline result.
- [ ] The secondary cohort reproduced exactly 49,225 rows and remained labeled
      as an operational sensitivity view.
- [ ] Both frozen models evaluated exactly the same rows within each cohort.
- [ ] The committed Version 1 results reproduced before Version 2 scoring.
- [ ] Version 2 thresholds remained `0.22` and `0.91`; Version 1 thresholds
      remained `0.08` and `0.73`.
- [ ] No fitting, fine-tuning, calibration, threshold selection, or model or
      policy modification occurred.
- [ ] Classification, routing, category-level, temporal, model-comparison,
      transformer-signal, and token-length diagnostics were completed.
- [ ] Primary results were reported as headline results and secondary results
      as a sensitivity view.
- [ ] All 2025 language was retrospective and made no final champion or
      production claim.
- [ ] Row-level and sensitive artifacts remained local, Git-ignored, and
      unstaged.
- [ ] Notebook 11 ran from beginning to end with sequential execution counts,
      zero error outputs, and all validation checks passing.
- [ ] Every report value and figure matched verified notebook aggregates.
- [ ] Markdown links and figure paths resolved.
- [ ] Only approved Issue #42 deliverables changed.

## Sources of Truth

- [GitHub Issue #42](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/issues/42)
- [`docs/v2_experiment_plan.md`](../docs/v2_experiment_plan.md)
- [`reports/2025_validation_protocol.md`](2025_validation_protocol.md)
- [`reports/2025_holdout_results.md`](2025_holdout_results.md)
- [`reports/results_summary.md`](results_summary.md)
- [`reports/v2_data_manifest.md`](v2_data_manifest.md)
- [`reports/v2_model_manifest.md`](v2_model_manifest.md)
- [`reports/v1_v2_2024_comparison.md`](v1_v2_2024_comparison.md)
