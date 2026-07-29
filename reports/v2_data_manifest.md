# Version 2 Transformer Data Manifest

Status: **Issue #39 data reconstruction and tokenization design completed. The
maximum token length and label mapping are locked before Version 2 training.**

This manifest records the aggregate outputs reproduced by
[`notebooks/08_v2_transformer_data_preparation.ipynb`](../notebooks/08_v2_transformer_data_preparation.ipynb).
It follows the committed
[`docs/v2_experiment_plan.md`](../docs/v2_experiment_plan.md) and does not
change any Version 1 data boundary, split, category, metric, or artifact.

## Source Integrity

| Item | Verified value |
| --- | --- |
| Source | `data/processed/cfpb_complaints_2024_cleaned.csv` |
| File size | 54,908,639 bytes |
| SHA-256 | `b115eb0c4a20a881a6a45bfb74cb7d715a726537372baa7d68f09d657cdfd919` |
| Source rows | 50,000 |
| Required fields | `clean_complaint_text`, `product` |
| Missing or blank required values | 0 |
| Other data sources opened | None |

The file path, size, and fingerprint were checked before CSV parsing. Only the
two required columns were loaded. No 2025 or 2026 data was opened.

## Execution Environment

| Item | Version or path |
| --- | --- |
| Conda environment | `complaint-v2` |
| Python | 3.11.15 |
| Pandas | 3.0.3 |
| NumPy | 2.4.6 |
| Scikit-learn | 1.9.0 |
| Transformers | 4.57.6 |
| Tokenizers | 0.22.2 |
| PyTorch runtime | 2.9.1+cu126 |
| PyTorch expected base | 2.9.1 |
| Notebook kernel | `Python (complaint-v2)` |

## Duplicate-Conflict Remediation

Grouping text uses the locked normalization:

```python
" ".join(str(value).strip().split())
```

Conflicting-label groups were identified across the complete cleaned source
before applying the eight-category scope. After scope restriction, every row
in a conflicting-label group was excluded. The first original row was then
retained from each repeated same-label group.

| Measure | Count |
| --- | ---: |
| Source rows | 50,000 |
| Conflicting-label groups in the complete source | 74 |
| Locked-scope rows before remediation | 49,196 |
| Locked-scope conflicting rows excluded | 1,780 |
| Repeated same-label rows removed | 14,374 |
| Corrected modeling rows | 33,042 |

The retained rows preserve original source order. The corrected modeling data
contains one row per normalized-text group and no conflicting-label group.

## Locked Outer Split

The shared 2024 split was reconstructed with:

```python
StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
```

Fold 0 is the final internal test; the other outer folds form development.

| Measure | Count |
| --- | ---: |
| Corrected modeling rows | 33,042 |
| Development rows | 26,433 |
| Final internal-test rows | 6,609 |
| Development/final-test normalized-text overlap | 0 |
| Categories present in development | 8 |
| Categories present in final internal test | 8 |

The final internal-test rows were reconstructed only to verify the locked
boundary. They were not used for token-length selection, token-length
statistics, model initialization, training, scoring, or evaluation.

## Fixed Development Folds

The five development folds use a second
`StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)` on the
26,433-row development partition.

| Fold | Training rows | Validation rows | Group overlap | Training classes | Validation classes |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 21,146 | 5,287 | 0 | 8 | 8 |
| 1 | 21,146 | 5,287 | 0 | 8 | 8 |
| 2 | 21,146 | 5,287 | 0 | 8 | 8 |
| 3 | 21,147 | 5,286 | 0 | 8 | 8 |
| 4 | 21,147 | 5,286 | 0 | 8 | 8 |

Every development row is assigned to exactly one validation fold, and every
fold has zero normalized-text group overlap between training and validation.

## Canonical Label Mapping

Class order is fixed independently of frequency and row order.

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

`label2id` maps the categories above to IDs 0 through 7. `id2label` is its
deterministic inverse. Neither mapping may be derived from frequency or
DataFrame row order.

## Locked Tokenizer

| Item | Locked value |
| --- | --- |
| Tokenizer ID | `distilbert/distilbert-base-uncased` |
| Revision | `12040accade4e8a0f71eabdb258fecc2e7e948be` |
| Class | `DistilBertTokenizerFast` |
| Vocabulary size | 30,522 |
| Maximum supported length | 512 tokens |
| CLS token ID | 101 |
| SEP token ID | 102 |
| PAD token ID | 0 |
| UNK token ID | 100 |

Only the tokenizer was loaded. No DistilBERT classification model or model
weights were initialized or downloaded by Notebook 08. Tokenizer cache files
remain outside Git.

## Development Token-Length Audit

The audit covers only the 26,433 development rows. Tokenization included
special tokens with no padding and no truncation. The standard deviation below
is the population standard deviation for the complete development partition.

| Statistic | Tokens |
| --- | ---: |
| Minimum | 4 |
| Mean | 289.0243 |
| Population standard deviation | 386.8186 |
| Median | 187 |
| 75th percentile | 352 |
| 90th percentile | 601 |
| 95th percentile | 837.4 |
| 99th percentile | 1,784 |
| Maximum | 8,136 |

| Coverage or truncation measure | Development rows |
| --- | ---: |
| At or below 128 tokens | 36.9765% |
| Above 128 tokens | 63.0235% |
| At or below 256 tokens | 61.9945% |
| Above 256 tokens | 38.0055% |
| Above 512 tokens | 13.4150% |

## Locked Maximum Token Length

The precommitted rule selects 128 tokens only when at least 95% of development
rows fit. Otherwise it selects 256, which is the compute ceiling.

Only 36.9765% of development rows fit within 128 tokens, so the locked Version
2 maximum token length is:

**256 tokens**

At 256 tokens, development coverage is 61.9945% and residual truncation is
38.0055%. The residual truncation is reported as observed; the candidate set
was not expanded after inspection. Final-test and 2025 token lengths did not
influence this decision.

The 38.0055% residual truncation rate is a material information-loss and
compute trade-off that must be considered when interpreting Version 2 results.

## Truncation and Dynamic Padding

Future Version 2 tokenization must:

- add the tokenizer's standard special tokens;
- truncate each sequence to the locked 256-token maximum;
- avoid fixed dataset-wide padding; and
- use `DataCollatorWithPadding(padding="longest")` so each batch is padded only
  to its longest truncated sequence.

A four-row in-memory development smoke test produced matching input and
attention-mask shapes of `(4, 256)`. The batch was padded to its longest
truncated sequence, did not exceed the locked maximum, and was not saved.

## Privacy and Artifact Restrictions

- Complaint narratives, complaint IDs, normalized-text hashes, token IDs,
  row-level token lengths, and tokenized rows must not be displayed or
  committed.
- CSV files, tokenizer caches, model weights, checkpoints, and row-level
  prediction artifacts remain local and Git-ignored.
- Notebook 08 creates no processed transformer dataset or row-level export.
- The final internal test is reserved for the later matched benchmark and was
  not evaluated in Issue #39.
- No classification model was initialized or trained.
- No predictions, logits, softmax scores, calibration outputs, or routing
  signals were generated.
- No 2025 or 2026 data was accessed.

Static review of Notebook 08 found no model initialization, training,
prediction, final-test token audit, or row-level export code.

Issue #39 locks only the leakage-safe data reconstruction, development folds,
label mapping, tokenizer revision, 256-token maximum, and dynamic-padding
design.
