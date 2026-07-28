# Version 2 DistilBERT Challenger Experiment Plan

Status: **Pre-training experiment rules for GitHub Issue #38. No Version 2
training or evaluation has started.**

This plan is read together with the pinned
[Version 2 requirements](../requirements-v2.txt), the locked
[Version 1 results summary](../reports/results_summary.md), the precommitted
[2025 validation protocol](../reports/2025_validation_protocol.md), and the
completed [2025 holdout results](../reports/2025_holdout_results.md).

## Purpose and Business Question

Version 2 will compare:

- **Version 1 benchmark:** the locked TF-IDF + Linear SVM workflow; and
- **Version 2 challenger:** an uncased DistilBERT sequence classifier.

The business question is whether the transformer's added complexity produces
enough improvement in classification and selective routing to justify its
compute, latency, dependency, maintenance, monitoring, privacy, and governance
costs.

The repository remains a notebook-centered internal prototype. It is not a
production system, prediction service, or approved decision engine.

## Locked Version 1 Reference

Version 1 remains unchanged throughout Version 2 development.

| Boundary or metric | Locked value |
| --- | ---: |
| Corrected modeling rows | 33,042 |
| Development rows | 26,433 |
| Final internal-test rows | 6,609 |
| Development/final-test normalized-text overlap | 0 |
| Product categories | 8 |
| Final internal-test Accuracy | 0.8712 |
| Final internal-test Macro F1 | 0.7671 |
| Final internal-test Weighted F1 | 0.8715 |
| Minimum top decision score | 0.08 |
| Minimum top-two score margin | 0.73 |
| Final internal-test routing coverage | 0.7705 |
| Final internal-test routed accuracy | 0.9503 |
| Final internal-test misroute rate | 0.0497 |

Version 1 will not be retrained, retuned, reselected, or replaced during
Version 2 development. Its model artifact, preprocessing, category scope,
class order, routing thresholds, and verified results remain the comparison
reference.

## Version 2 Data Boundaries

Version 2 must:

- use only the same local cleaned 2024 source as Version 1:
  `data/processed/cfpb_complaints_2024_cleaned.csv`;
- verify that source against the existing 54,908,639-byte SHA-256 fingerprint
  `b115eb0c4a20a881a6a45bfb74cb7d715a726537372baa7d68f09d657cdfd919`;
- reproduce the same normalized-text grouping rule;
- exclude the same conflicting-label groups;
- retain the first representative from each repeated same-label group;
- reproduce exactly 33,042 corrected modeling rows;
- reproduce the same 26,433 development rows and 6,609-row final internal
  test;
- reproduce zero normalized-text overlap between those partitions;
- reproduce the outer
  `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)` split with
  fold 0 as the final internal test;
- reproduce the five fixed development folds using
  `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)` on the
  development partition; and
- use development folds only for all Version 2 decisions.

The 2024 final internal test must not influence token length, checkpoint,
epoch, routing threshold, training configuration, model setting, or fallback
decisions. The 2025 data must not be used for training, tuning, calibration,
threshold selection, or model redesign.

The 2024 final internal test is a shared matched benchmark. Because its Version
1 outcomes are already known, it is not a new untouched Version 2 holdout.

## Categories and Label Mapping

Class order is fixed independently of frequency and DataFrame row order.

| ID | Product category |
| ---: | --- |
| 0 | Checking or savings account |
| 1 | Credit card |
| 2 | Credit reporting or other personal consumer reports |
| 3 | Debt collection |
| 4 | Money transfer, virtual currency, or money service |
| 5 | Mortgage |
| 6 | Student loan |
| 7 | Vehicle loan or lease |

The deterministic mappings are:

```python
label2id = {
    "Checking or savings account": 0,
    "Credit card": 1,
    "Credit reporting or other personal consumer reports": 2,
    "Debt collection": 3,
    "Money transfer, virtual currency, or money service": 4,
    "Mortgage": 5,
    "Student loan": 6,
    "Vehicle loan or lease": 7,
}
id2label = {label_id: label for label, label_id in label2id.items()}
```

Both mappings must be written into the final model configuration and verified
after reload. No category may be renamed, merged, split, omitted, or reordered.

## Model and Tokenizer

The selected official Hugging Face base is:

| Item | Locked value |
| --- | --- |
| Model ID | `distilbert/distilbert-base-uncased` |
| Model revision | `12040accade4e8a0f71eabdb258fecc2e7e948be` |
| Tokenizer ID | `distilbert/distilbert-base-uncased` |
| Tokenizer revision | `12040accade4e8a0f71eabdb258fecc2e7e948be` |
| Sequence-classification architecture | `DistilBertForSequenceClassification` |
| Number of labels | 8 |
| Maximum supported sequence length | 512 tokens |

The revision was resolved from the official
[Hugging Face model metadata](https://huggingface.co/api/models/distilbert/distilbert-base-uncased).
The locked
[configuration](https://huggingface.co/distilbert/distilbert-base-uncased/blob/12040accade4e8a0f71eabdb258fecc2e7e948be/config.json)
identifies DistilBERT with 512 position embeddings. Version 2 will initialize
`DistilBertForSequenceClassification` from that base revision with
`num_labels=8` and the locked mappings above.

Model or tokenizer weights must not be downloaded during Issue #38 and must
never be committed to Git. Later issues must use the exact revision, not
`main`, a moving tag, or an unrecorded cache state.

## Token-Length Selection Rule

Issue #39 will make the token-length decision using development text only.
Using the locked tokenizer revision, it must tokenize all 26,433 development
rows with special tokens, no padding, and no truncation solely to calculate
aggregate lengths.

The precommitted candidate set is `{128, 256}` tokens:

1. Calculate the percentage of development rows whose complete tokenized
   length is at most each candidate.
2. Select 128 when it covers at least 95% of development rows.
3. Otherwise select 256.
4. Report the selected coverage and the percentage that would be truncated.
5. Lock the choice in `reports/v2_data_manifest.md` before training.

The compute ceiling is 256 tokens even if fewer than 95% of rows fit. Any
residual truncation must be reported rather than expanding the candidate set
after inspection. Dynamic padding will pad each batch only to its longest
sequence.

Final-test and 2025 token lengths must not be calculated before the value is
locked and cannot alter the decision afterward.

## Training Configuration and Budget

One primary configuration and one deterministic memory fallback are allowed.
There is one seed and no broad hyperparameter grid.

| Setting | Locked plan |
| --- | --- |
| Random seed and data seed | 42 |
| Learning rate | `2e-5` |
| Weight decay | `0.01` |
| Loss | Standard unweighted cross-entropy; no label smoothing |
| Maximum epochs per fold | 4 |
| Per-device training batch size | 8 |
| Gradient accumulation | 2 steps |
| Effective training batch size | 16 rows per optimizer step on one device |
| Per-device evaluation batch size | 16 |
| Optimizer | PyTorch AdamW (`betas=(0.9, 0.999)`, `eps=1e-8`) |
| Learning-rate schedule | Linear decay |
| Warmup | First 10% of optimizer steps, rounded up |
| Evaluation and checkpoint frequency | End of each epoch |
| Checkpoint-selection metric | Development-fold validation Macro F1 |
| Best-model behavior | `load_best_model_at_end=True`, maximize Macro F1 |
| Early stopping | Patience 1 epoch; threshold 0.0 |
| Mixed precision | CUDA FP16 enabled; BF16 disabled |
| Gradient clipping | Maximum norm `1.0` |
| Seed count | 1 |

The primary run requires a clean, compatible CUDA-enabled environment. The
only memory fallback is training batch size 4, gradient accumulation 4, and
evaluation batch size 8, preserving the effective training batch size of 16.
The fallback may be activated only after a documented CUDA out-of-memory error
before a completed fold result. If it also fails, stop and report the resource
blocker; do not reduce token length or change other settings.

Each fold starts independently from the same locked base revision. A
disappointing fold or aggregate result does not authorize new learning rates,
seeds, epochs, losses, token lengths, or other configuration changes.

For the final full-development model, take the median of the five integer
best-epoch numbers selected by fold validation Macro F1. Train once from the
locked base revision on all 26,433 development rows for exactly that many
epochs, using the same configuration and no final-test feedback. The epoch
rule and result must be recorded before final-test scoring.

## Development and Final-Model Procedure

The controlled sequence for Issues #39 and #40 is:

1. Reconstruct and verify the five fixed development folds.
2. Initialize and train one fresh DistilBERT model per fold.
3. Generate exactly one out-of-fold prediction and one local score vector for
   every development row.
4. Report each fold and aggregate development classification metrics.
5. Select the final epoch count with the precommitted median-best-epoch rule.
6. Train one final model on all 26,433 development rows.
7. Freeze, reload, and SHA-256 fingerprint the final model and tokenizer.
8. Evaluate that frozen artifact later on the shared 2024 final internal
   benchmark in Issue #41.

Out-of-fold row-level outputs remain local and Git-ignored. Only aggregate
metrics, fingerprints, and manifests may be committed.

## Version 2 Routing Signals

Version 2 routing uses:

- the largest eight-class softmax score; and
- the difference between the largest and second-largest softmax scores.

These values are **uncalibrated model signals**. They must not be called
calibrated probabilities, likelihoods, or real-world confidence.

Issue #41 will select Version 2 thresholds from development out-of-fold outputs
only. Version 1 thresholds `0.08` and `0.73` must not be reused automatically
because the models have different score scales.

The Version 2 candidate grid and selection rule are fixed:

1. For top scores and margins separately, calculate development OOF quantiles
   from `0.000` through `0.975` in increments of `0.025`.
2. Round candidate values to two decimals and remove duplicates.
3. Evaluate every candidate threshold pair, using inclusive comparisons and
   requiring a positive margin.
4. Keep policies with development OOF coverage at least `0.05` and development
   OOF misroute rate at most `0.05`.
5. Select highest coverage; ties select lower misroute rate, then lower
   top-score threshold, then lower margin threshold.

If no policy qualifies, report that outcome and do not weaken the assumptions
after seeing final-test or 2025 results. Thresholds are locked before any
Version 2 final-test scoring.

## Champion-Challenger Comparison

Issue #41 will compare the locked Version 1 benchmark and frozen Version 2
challenger using full-precision calculations and rounded display values.

**Classification**

- Accuracy;
- macro precision, recall, and F1;
- weighted precision, recall, and F1;
- per-category precision, recall, F1, and support; and
- confusion-matrix counts and row-normalized confusion matrices.

**Routing**

- coverage and review rate;
- routed accuracy and misroute rate;
- category-level coverage and risk;
- matched-risk comparisons; and
- matched-coverage comparisons.

All matched operating points must be selected using development OOF outputs
before final-test scoring. Matched-risk comparisons evaluate coverage at common
development risk limits; matched-coverage comparisons evaluate misroute rate at
common development coverage targets.

**Compute**

- artifact size;
- training time;
- CPU single-row latency;
- CPU batch throughput;
- GPU latency and throughput when available; and
- peak GPU memory during training.

Transformer inference timing must include tokenization. Timing methods must
record hardware, warmup runs, measured repetitions, batch size, and summary
statistics.

**Business trade-offs**

- explainability;
- dependency and artifact complexity;
- monitoring and drift requirements;
- privacy and governance requirements; and
- human-review implications.

No single metric automatically determines the preferred challenger. The
recommendation must present classification, routing, compute, and governance
trade-offs together and report weaker results as clearly as improvements.

## 2025 Retrospective Restriction

The 2025 sample was already evaluated once for Version 1 and is exhausted as
an unbiased holdout. Its existing 30,156-row primary leakage-resistant cohort
and 49,225-row secondary operational cohort may be scored for Version 2 only
after the model, tokenizer, checkpoint, training procedure, preprocessing,
label mapping, and routing thresholds are completely frozen.

Issue #42 must call this a **retrospective comparison**, not a new Version 2
holdout. No 2025 result may change the model, tokenizer, checkpoint, epoch
count, training setting, preprocessing, calibration, label mapping, cohort, or
routing threshold. After the retrospective run, the project must not return to
Version 2 development to improve results against 2025.

The primary leakage-resistant cohort remains the headline temporal comparison;
the secondary operational cohort remains a sensitivity view.

## Promotion Language

Before evaluation on a new untouched period:

- Version 1 is the **temporally validated benchmark**.
- Version 2 is the **DistilBERT challenger**.
- Version 2 may become the **preferred internal challenger** or
  **preferred candidate for future validation**.
- Version 2 must not be called the independently temporally validated
  champion.

A future complete untouched period, currently planned as full-year 2026 CFPB
data in Issue #43, is required for the final project champion decision.

A project champion is not a production-approved model. Production use would
still require separate privacy, security, fairness, operational, governance,
monitoring, and stakeholder approval.

## Reproducibility and Artifact Policy

### Target Version 2 environment

The target interpreter is Python `3.11.15`. Direct dependencies are pinned in
`requirements-v2.txt`:

| Package | Version |
| --- | ---: |
| pandas | 3.0.3 |
| numpy | 2.4.6 |
| scipy | 1.16.3 |
| scikit-learn | 1.9.0 |
| matplotlib | 3.10.6 |
| seaborn | 0.13.2 |
| requests | 2.32.5 |
| joblib | 1.5.2 |
| jupyter | 1.1.1 |
| notebook | 7.4.5 |
| torch | 2.9.1 |
| transformers | 4.57.6 |
| datasets | 4.4.2 |
| accelerate | 1.12.0 |
| evaluate | 0.4.6 |
| safetensors | 0.7.0 |

On 2026-07-27, official PyPI metadata confirmed that these releases exist,
that every declared `Requires-Python` range accepts Python 3.11, and that their
declared direct dependency constraints accept this set. Windows CPython 3.11
wheels were present for the compiled core packages. The environment was
intentionally not installed or import-tested in Issue #38; GPU/CUDA
compatibility therefore remains an entry check for Issue #40.

Do not add a machine-specific CUDA wheel URL to the requirements file. Create a
separate environment and follow the official PyTorch installation guidance for
the target machine while preserving `torch==2.9.1`.

### Read-only planning-host snapshot

| Item | Observed value |
| --- | --- |
| Operating system | Microsoft Windows 11 Pro, version `10.0.26200`, 64-bit |
| Current Python | 3.13.9, Anaconda |
| CPU | Intel Core i5-8400 at 2.80 GHz; 6 cores / 6 logical processors |
| RAM | 31.83 GiB |
| Discrete GPU | NVIDIA GeForce GTX 1650 |
| GPU memory | 4,096 MiB |
| NVIDIA driver | 591.86 |
| Driver-reported CUDA compatibility | 13.1 |
| Local CUDA toolkit | `nvcc` unavailable; `CUDA_PATH` not set |
| Current PyTorch metadata | 2.13.0 installed, but import fails with an OpenMP runtime conflict |
| Transformers, Datasets, Accelerate, Evaluate, Safetensors | Not installed |

The current environment is not the planned V2 environment and must not be
altered in Issue #38. Training cannot begin until a clean Python 3.11
environment imports all pinned packages and PyTorch verifies the intended CUDA
device without warnings or runtime conflicts.

### Records and local artifacts

Later issues must record:

- Git commit SHA;
- operating system, Python, and direct dependency versions;
- CPU, total RAM, GPU, GPU memory, CUDA runtime, and driver;
- random seed and deterministic settings;
- model and tokenizer IDs and exact revisions;
- input-data path, byte size, and SHA-256;
- final model/tokenizer file inventory, byte sizes, and SHA-256 values; and
- training time, peak GPU memory, and evaluation-timing method.

Use local Git-ignored paths beneath:

- `models/v2_distilbert_challenger/hf_cache/`;
- `models/v2_distilbert_challenger/folds/`; and
- `models/v2_distilbert_challenger/final/`.

Model weights, tokenizers, checkpoints, caches, CSV files, complaint
narratives, normalized-text hashes, tokenized rows, and row-level predictions
or scores remain local and must not be committed.

Exact bit-for-bit equality across different hardware, CUDA kernels, or driver
versions is not guaranteed. The project must record enough information to
reproduce the procedure and compare aggregate results within documented
numeric tolerances.

## Issue Mapping

- [Issue #39](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/issues/39):
  reconstruct the locked data, audit development token lengths, lock
  tokenization and label mappings, and create the data manifest.
- [Issue #40](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/issues/40):
  run the five development-fold fine-tuning jobs, create OOF outputs, select
  the epoch, train the full-development artifact, and fingerprint it.
- [Issue #41](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/issues/41):
  lock Version 2 routing thresholds from development OOF signals and perform
  the matched 2024 classification, routing, latency, size, and business
  comparison.
- [Issue #42](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/issues/42):
  score the fully frozen challenger on the existing 2025 cohorts as a
  retrospective comparison and update verified documentation.
- [Issue #43](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/issues/43):
  precommit a new protocol and evaluate both locked models once on complete,
  untouched full-year 2026 data before the final project champion decision.

## Out of Scope

Issue #38 does not include:

- DistilBERT training or checkpoint creation;
- transformer dataset preparation or tokenization;
- 2024 final-test scoring;
- 2025 scoring;
- 2026 data acquisition;
- a production API, batch service, dashboard, or review queue;
- probability calibration;
- deployment or production monitoring;
- fairness claims;
- workload-reduction or cost-savings claims;
- production or regulatory approval; or
- any change to Version 1 data, code, artifacts, metrics, or thresholds.
