# Version 2 DistilBERT Model Manifest

## Status and Scope

This manifest records the frozen local Version 2 DistilBERT challenger created
in Issue #40. The artifact was trained once on all 26,433 locked 2024
development rows after the five-fold development experiment selected the final
epoch count. It has not been evaluated on the 6,609-row final internal test or
on 2025/2026 data. Matched benchmark evaluation and Version 2 routing-policy
selection are deferred to Issue #41.

The model and all row-level development outputs remain local and Git-ignored.
This artifact is a challenger for an internal notebook-centered prototype, not
a production-approved model.

## Model and Tokenizer

| Item | Locked value |
|---|---|
| Model ID | `distilbert/distilbert-base-uncased` |
| Model revision | `12040accade4e8a0f71eabdb258fecc2e7e948be` |
| Model class | `DistilBertForSequenceClassification` |
| Tokenizer ID | `distilbert/distilbert-base-uncased` |
| Tokenizer revision | `12040accade4e8a0f71eabdb258fecc2e7e948be` |
| Tokenizer class | `DistilBertTokenizerFast` |
| Output labels | 8 |
| Maximum token length | 256 |
| Baseline Git commit | `0ec4759cebc3f823b67e05121cd26a5c4cfc537a` |

## Environment and Hardware

| Item | Recorded value |
|---|---|
| Conda environment | `complaint-v2` |
| Operating system | Windows 10 build 26200, 64-bit |
| Python | 3.11.15 |
| PyTorch | 2.9.1+cu126 |
| Transformers | 4.57.6 |
| Tokenizers | 0.22.2 |
| Datasets | 4.4.2 |
| Accelerate | 1.12.0 |
| Evaluate | 0.4.6 |
| Safetensors | 0.7.0 |
| Pandas | 3.0.3 |
| NumPy | 2.4.6 |
| SciPy | 1.16.3 |
| Scikit-learn | 1.9.0 |
| CPU | Intel64 Family 6 Model 158 Stepping 10, 6 physical/logical cores |
| RAM | 31.83 GiB |
| GPU | NVIDIA GeForce GTX 1650, 4,096 MiB |
| CUDA runtime | 12.6 |
| NVIDIA driver | 591.86 |

## Data and Label Boundaries

| Item | Value |
|---|---:|
| Cleaned source | `data/processed/cfpb_complaints_2024_cleaned.csv` |
| Source size | 54,908,639 bytes |
| Source SHA-256 | `b115eb0c4a20a881a6a45bfb74cb7d715a726537372baa7d68f09d657cdfd919` |
| Corrected modeling rows | 33,042 |
| Development rows used for final training | 26,433 |
| Final internal-test rows used for training/scoring | 0 |
| 2025/2026 rows accessed | 0 |

Canonical mapping:

| ID | Product category |
|---:|---|
| 0 | Checking or savings account |
| 1 | Credit card |
| 2 | Credit reporting or other personal consumer reports |
| 3 | Debt collection |
| 4 | Money transfer, virtual currency, or money service |
| 5 | Mortgage |
| 6 | Student loan |
| 7 | Vehicle loan or lease |

## Training Configuration

| Setting | Value |
|---|---:|
| Random seed | 42 |
| Learning rate | `2e-5` |
| Weight decay | `0.01` |
| Training batch size | 8 |
| Gradient accumulation | 2 |
| Effective batch size | 16 |
| Evaluation batch size during folds | 16 |
| Precision | FP16 |
| Optimizer | PyTorch AdamW |
| Adam betas / epsilon | `0.9`, `0.999` / `1e-8` |
| Warmup / scheduler | 10% / linear |
| Gradient clipping | `1.0` |
| Fold checkpoint metric | Validation Macro F1 |
| Fold early stopping | Patience 1, threshold 0 |
| Configuration used | Primary; fallback not required |

The five fold-best integer epochs were `[4, 2, 4, 4, 4]`. Their precommitted
integer median selected 4 final epochs. A fresh model from the locked revision
was trained once for exactly 4 epochs on all 26,433 development rows, with no
new validation split and no early stopping.

| Training stage | Runtime | Peak allocated | Peak reserved |
|---|---:|---:|---:|
| Five development folds | 1,430.99 min (23.85 hr) | 1,587.9 MiB maximum | 1,758.0 MiB maximum |
| Final full-development model | 349.84 min (5.83 hr) | 1,585.5 MiB | 1,738.0 MiB |
| Combined recorded training runtime | 1,780.83 min (29.68 hr) | — | — |

GPU values are PyTorch peak allocator measurements.

## Local OOF Artifact

| Item | Value |
|---|---|
| Relative path | `models/v2_distilbert_challenger/oof/development_oof_outputs.npz` |
| Rows | 26,433 |
| Size | 674,788 bytes |
| SHA-256 | `72d59db97819d6f06b968520eddac2d0c1d590f36dea4efa627e9c123c1e5b13` |
| Git status | Ignored by `models/*` |

The local file contains true labels, predicted labels, eight-class logits,
fold assignments, top softmax scores, and top-two softmax margins. Its
row-level contents are not displayed or committed.

Validated fold-output fingerprints:

| Fold | Size (bytes) | SHA-256 |
|---:|---:|---|
| 0 | 108,138 | `61582d95a025befd482d1b4b9dc95f92158de714ff5633536222a9ee9d23e95e` |
| 1 | 106,610 | `7c86b786ef38bb25a83470c2b066bc553c5fe1a16c02d910d912dd866c008b9a` |
| 2 | 107,727 | `ade2526fbd619d5aaf820f772de1362b3d85a3f4232d6d1c5e81bbb578c55038` |
| 3 | 107,255 | `5e3025a862757e4c9a8fd989db5f03748d8ce91e8db03627ee1588bbb5862faf` |
| 4 | 107,850 | `3e05f54ce1c24bfa2c4b6523aaa9b428cee1a7c59561d583235792b11c2fa978` |

## Frozen Final Artifact

Local directory:
`models/v2_distilbert_challenger/final/`

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| `config.json` | 1,229 | `745d87e88a54bd5bd349b14aae194a1f523189cb6d6f377463419487fa43e370` |
| `model.safetensors` | 267,851,024 | `e05900579f16e96d75df968cedb71b2b2fde3aae95f1bf73dbe7147306287c23` |
| `special_tokens_map.json` | 132 | `3c3507f36dff57bce437223db3b3081d1e2b52ec3e56ee55438193ecb2c94dd6` |
| `tokenizer.json` | 711,494 | `8b79639ec74b46604e730f505186eaafb1006d2fd00f2c4930d168bb7f894680` |
| `tokenizer_config.json` | 1,283 | `21c3bea73b6711617c657664adcd4d0b02ce20d2db4b2ebdd722a6da8da28bcd` |
| `training_args.bin` | 6,033 | `568405730a290d2928d67b32870a9a965253e46bc2e9ed516048100a9ba475d8` |
| `training_summary.json` | 3,329 | `b8a149005ac05614230937c3620fcda2162b9f39c126a1aefa95ef8721a0bfcf` |
| `vocab.txt` | 231,508 | `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3` |
| **Total** | **268,806,032** | — |

The saved artifact reloaded as
`DistilBertForSequenceClassification` with eight outputs and the exact locked
`label2id`/`id2label` mappings. The tokenizer reloaded as
`DistilBertTokenizerFast`. All saved model parameters passed a finite-value
check, and a synthetic input produced finite logits with shape `(1, 8)`. The
model and OOF paths are covered by the repository's `models/*` ignore rule,
and no model, checkpoint, or OOF file is staged.

## Warnings and Limitations

- The locked 256-token maximum truncates 38.0055% of development narratives,
  creating a material information-loss and compute trade-off.
- Windows could not use Hugging Face cache symlinks, so the ignored local cache
  may consume additional disk space; this did not change model behavior.
- The fresh sequence-classification head produced the expected initialization
  notice before training.
- FP16 training logged one transient infinite gradient norm during final epoch
  3. Training completed without an exception, the following epoch completed,
  and the saved model reloaded successfully. All saved parameters and the
  synthetic logits passed finite-value checks, confirming that the transient
  event did not leave non-finite values in the frozen artifact. This event
  should remain visible when interpreting reproducibility, but it did not
  invalidate the artifact checks.
- Exact bit-for-bit reproduction is not guaranteed across different hardware.
  The source, revisions, settings, seed, artifacts, and environment are
  recorded to support procedural reproduction.

## Next Step

Issue #41 will evaluate this frozen artifact on the shared locked 2024 final
internal-test benchmark and select a Version 2 selective-routing policy using
development OOF outputs only. Issue #40 makes no champion, temporal-validation,
production-readiness, cost-savings, or workload-reduction claim.
