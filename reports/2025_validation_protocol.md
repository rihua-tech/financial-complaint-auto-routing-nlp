# 2025 Pre-Holdout Validation Protocol

Status: **Phase 1 protocol reviewed and ready to be locked in this commit. Phase 2 has not started.**

Related issue: [GitHub Issue #15](https://github.com/rihua-tech/financial-complaint-auto-routing-nlp/issues/15)

> **Post-execution notice:** This file preserves the validation protocol
> committed before the 2025 holdout was opened. Phase 2 was later completed
> without changing the locked model, preprocessing, cohort definitions,
> evaluation metrics, or routing thresholds. See
> [2025 Holdout Results](2025_holdout_results.md) for the completed evaluation.
> The 2025 dataset is now exhausted as an unbiased holdout and must not be
> reused for future tuning or model-selection decisions.

This protocol freezes the Version 1 evaluation plan before the 2025 CFPB
out-of-time holdout is opened, parsed, previewed, summarized, or evaluated. The
2025 CSV was read only as an uninterpreted byte stream to calculate its
file-level SHA-256 fingerprint. Its records, columns, labels, narratives, and
distributions were not inspected.

Phase 2 must not begin until this file has been reviewed, committed, and pushed
and every Phase 2 entry check below passes.

## Locked Baseline

| Item | Locked value |
| --- | --- |
| Baseline Git commit | `fddca32f466737901bbf95534d08030b32e9599e` |
| Development period | 2024 only |
| Model | Scikit-learn `Pipeline`: TF-IDF + Linear SVM |
| Model artifact | `models/best_tfidf_classifier.joblib` |
| 2025 evaluation source | `data/raw/cfpb_complaints_2025_raw.csv` |
| 2024 overlap-reference source | `data/processed/cfpb_complaints_2024_cleaned.csv` |
| Raw narrative field | `complaint_what_happened` |
| Model input after cleaning | `clean_complaint_text` |
| Target field | `product` |
| Corrected 2024 modeling rows | 33,042 |
| 2024 development rows | 26,433 |
| 2024 final internal-test rows | 6,609 |
| Development/test normalized-text overlap | 0 groups |
| Random state | 42 |

The baseline commit is the `origin/main` commit from which
`issue-15-2025-validation-protocol` was created. Neither the model nor either
data file is committed to Git.

## File Integrity Fingerprints

File sizes are exact byte counts. SHA-256 values are lowercase hexadecimal.

| File | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| `models/best_tfidf_classifier.joblib` | 3,392,109 | `4514e7e49e305e408e2eaaf296d8607b33e9320547685339eff263e4dda0c94a` |
| `data/raw/cfpb_complaints_2025_raw.csv` | 73,806,040 | `b59d7842e786f00d6be26b7980a42f67474acb9040db293ddd3641204d25eb3a` |
| `data/processed/cfpb_complaints_2024_cleaned.csv` | 54,908,639 | `b115eb0c4a20a881a6a45bfb74cb7d715a726537372baa7d68f09d657cdfd919` |

The previously documented ingestion checks establish these expected properties
for the fingerprinted 2025 raw file:

| Ingestion property | Expected value |
| --- | --- |
| Rows | 50,000 |
| Raw columns | 17 |
| Minimum `date_received` | `2025-01-01` |
| Maximum `date_received` | `2025-12-31` |

During Phase 2, stop before evaluation if any path, byte count, or fingerprint
does not match this table. Do not replace, regenerate, refit, or modify the
locked artifact in response to a mismatch.

## Software Environment

### Locked artifact creation environment

The Version 1 results summary records the environment used to create and
validate the saved artifact:

| Component | Version |
| --- | --- |
| Python | 3.11.15 |
| Scikit-learn | 1.9.0 |
| Pandas | 3.0.3 |
| NumPy | 2.4.6 |

### Current Phase 1 inspection environment

| Component | Version |
| --- | --- |
| Operating system | Windows 11 (`10.0.26200`) |
| Python | 3.13.9 |
| Scikit-learn | 1.7.2 |
| Pandas | 2.3.3 |
| NumPy | 2.3.5 |
| SciPy | 1.16.3 |
| Joblib | 1.5.2 |
| Matplotlib | 3.10.6 |
| Seaborn | 0.13.2 |
| Requests | 2.32.5 |
| Jupyter | 1.1.1 |
| Notebook | 7.4.5 |
| IPython kernel | 6.31.0 |

Loading the artifact only to inspect its metadata in the current environment
raised Scikit-learn `InconsistentVersionWarning` messages because the artifact
was saved with Scikit-learn 1.9.0 and the current runtime uses 1.7.2. Phase 2
must therefore use an isolated environment compatible with the documented
artifact-creation environment, ideally matching the recorded Python,
Scikit-learn, Pandas, and NumPy versions exactly. The artifact fingerprint must
remain unchanged, and loading it must not produce a version-compatibility
warning before any 2025 evaluation occurs.

The repository's `requirements.txt` does not pin versions, so it is not by
itself sufficient to reproduce the locked environment.

## Locked Category Scope and Class Order

The scope is the following eight CFPB product categories. Decision-score
columns must be interpreted in the fitted pipeline's exact `classes_` order:

1. `Checking or savings account`
2. `Credit card`
3. `Credit reporting or other personal consumer reports`
4. `Debt collection`
5. `Money transfer, virtual currency, or money service`
6. `Mortgage`
7. `Student loan`
8. `Vehicle loan or lease`

No label may be renamed, merged, split, reordered, or mapped into this scope
after the holdout is opened. Unfamiliar, changed, missing, blank, and
out-of-scope labels must be counted and reported rather than silently mapped.

## Exact Version 1 Text Preparation

The 2025 evaluation must reproduce the cleaning logic from
`notebooks/02_eda_cleaning.ipynb` exactly:

1. Treat a narrative or product value as missing when converting it to Pandas
   string type, stripping surrounding whitespace, replacing missing values with
   an empty string, and comparing it with `""` identifies it as blank.
2. Exclude rows missing either `complaint_what_happened` or `product`.
3. Convert a nonmissing narrative to `str`.
4. Replace URL-like substrings matching
   `https?://\S+|www\.\S+` with one space, using case-insensitive matching.
5. Replace each run matching `\s+` with one ordinary space.
6. Strip leading and trailing whitespace.
7. Convert `product` to Pandas string type and strip surrounding whitespace.
8. Retain only `clean_complaint_text` and `product`.
9. Exclude rows whose cleaned narrative or stripped product is empty.
10. Reset the remaining row index while preserving original CSV row order.

This cleaning does **not** lowercase text, remove punctuation or stop words, or
apply stemming or lemmatization. Lowercasing occurs later inside the locked
`TfidfVectorizer`.

For duplicate and overlap grouping, normalize a cleaned narrative with:

```python
" ".join(str(value).strip().split())
```

Then calculate SHA-256 over the normalized string encoded as UTF-8. Grouping is
case-sensitive because this normalization does not lowercase text. Normalized
text hashes are temporary internal identifiers and must not be exported or
committed.

## Locked Pipeline Configuration

Pipeline steps:

1. `tfidf`: `sklearn.feature_extraction.text.TfidfVectorizer`
2. `classifier`: `sklearn.svm.LinearSVC`

### TF-IDF

| Parameter | Locked value |
| --- | --- |
| `input` | `"content"` |
| `encoding` | `"utf-8"` |
| `decode_error` | `"strict"` |
| `strip_accents` | `None` |
| `lowercase` | `True` |
| `preprocessor` | `None` |
| `tokenizer` | `None` |
| `analyzer` | `"word"` |
| `token_pattern` | `r"(?u)\b\w\w+\b"` |
| `ngram_range` | `(1, 2)` |
| `stop_words` | `None` |
| `max_df` | `1.0` |
| `min_df` | `2` |
| `max_features` | `50_000` |
| `vocabulary` constructor argument | `None` |
| `binary` | `False` |
| `dtype` | `numpy.float64` |
| `norm` | `"l2"` |
| `use_idf` | `True` |
| `smooth_idf` | `True` |
| `sublinear_tf` | `False` |
| Fitted vocabulary/IDF length | 50,000 |

The fitted vocabulary and IDF values stored in the fingerprinted artifact are
locked. Do not reconstruct or replace them from 2024 or 2025 data.

### Linear SVM

| Parameter | Locked value |
| --- | --- |
| Classifier | `LinearSVC` |
| `penalty` | `"l2"` |
| `loss` | `"squared_hinge"` |
| `dual` | `"auto"` |
| `tol` | `0.0001` |
| `C` | `1.0` |
| `multi_class` | `"ovr"` |
| `fit_intercept` | `True` |
| `intercept_scaling` | `1` |
| `class_weight` | `"balanced"` |
| `verbose` | `0` |
| `random_state` | `42` |
| `max_iter` | `10_000` |
| Fitted input-feature count | 50,000 |

Do not call `fit` or `fit_transform` on any 2024 or 2025 data. Phase 2 may use
only the locked pipeline's `predict`, `decision_function`, and transform path.

## Locked 2024 Reference Reconstruction

The 2024 cleaned file may be used only to reproduce the original reference
groups and the already reported 2024 comparison values:

1. Require nonmissing `clean_complaint_text` and `product`.
2. Compute normalized-text hashes with the locked grouping rule.
3. Identify conflicting-label hashes across the full cleaned 2024 data.
4. Restrict rows to the locked eight-category scope.
5. Exclude every row belonging to a conflicting-label hash.
6. For repeated normalized text with the same product, retain the first row in
   original file order.
7. Confirm 33,042 rows and unique hashes remain.
8. Recreate
   `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)`.
9. Use fold `0` as the final internal test fold and all other folds as
   development.
10. Confirm 26,433 development rows, 6,609 final-test rows, all eight
    categories in both partitions, and zero hash overlap between partitions.

The reconstructed development and final-test hash sets may be held only in
memory for aggregate overlap calculations. They must not be saved or committed.

## Eligibility, Exclusions, and Cohorts

All rules in this section are fixed before the 2025 holdout is inspected.

### Eligibility and required counts

After Phase 2 begins, report these counts before calculating performance:

- presence of every required raw column:
  `complaint_what_happened`, `product`, `date_received`, and `complaint_id`;
- actual raw row and column counts;
- minimum and maximum parsed `date_received`;
- rows outside calendar year 2025;
- duplicate `complaint_id` values;
- rows with missing or blank narratives;
- rows with missing or blank product labels;
- rows becoming empty after cleaning;
- rows with unfamiliar, changed, or out-of-scope labels, by label;
- otherwise eligible rows in the locked eight-category scope;
- normalized-text overlaps with 2024 development and final-test groups,
  reported separately and as a union;
- repeated same-label normalized-text groups and affected rows within 2025;
- conflicting-label normalized-text groups and affected rows within 2025; and
- final primary- and secondary-cohort row counts.

Do not silently remove a row. Every exclusion category must be reported in
aggregate, with overlap between exclusion reasons handled by a documented,
sequential count flow.

An unexpected mismatch with the ingestion checks previously documented in
`docs/data_ingestion.md` is a blocker. Stop and report the mismatch; do not
create a new post-holdout exclusion, repair, replacement, or cohort rule in
response to information observed after the 2025 file is opened.

### Secondary operational cohort

The secondary operational cohort contains every otherwise eligible 2025 row:

- the cleaned narrative is nonempty;
- the stripped product label is nonempty; and
- the product label is in the locked eight-category scope.

This row-level cohort retains cross-year text overlaps, repeated same-label
texts, and conflicting-label text groups. Those conditions must still be
flagged and counted. This cohort estimates performance on the eligible 2025
sample as received and is a sensitivity analysis, not the primary
2024-versus-2025 comparison.

### Primary leakage-resistant cohort

Create the primary cohort from otherwise eligible rows in this fixed order:

1. Compute conflicting-label normalized-text hashes using all 2025 rows with
   usable cleaned text and a nonblank product label, before applying the
   eight-category filter.
2. Restrict to the locked eight-category scope.
3. Exclude rows whose normalized-text hash appears in either the reconstructed
   2024 development set or the reconstructed 2024 final-test set.
4. Exclude every row belonging to a 2025 conflicting-label hash.
5. For remaining repeated same-label hashes, retain the first row in original
   2025 CSV order.

The resulting cohort must contain one row per normalized-text hash, no
conflicting-label group, and no normalized-text overlap with either locked 2024
partition. It is the primary cohort for the main 2024-versus-2025
generalization comparison.

Excluding overlap with the 2024 final internal test is a conservative
prior-text-free evaluation rule. It does not mean those final internal-test
rows were used to fit the classifier; the classifier was fitted on the locked
2024 development partition only.

These definitions must not change after the 2025 data is opened. If an
unanticipated condition makes a definition impossible to apply, stop and
report it; do not improvise a new rule after viewing outcomes.

## Locked Routing Policy

Use `pipeline.classes_`, `pipeline.decision_function`, and
`src.routing_rules.route_from_scores`.

| Rule | Locked value |
| --- | ---: |
| Minimum top decision score | 0.08 |
| Minimum top-two score margin | 0.73 |

Both comparisons are inclusive. A row is an automatic-route candidate only
when `top_score >= 0.08` and `top_score - second_score >= 0.73`. Tied top
scores, low scores, low margins, invalid class labels, malformed arrays,
class/score count mismatches, and non-finite scores require human review using
the existing review reasons from `src/routing_rules.py`.

Decision scores and margins are model signals, **not calibrated
probabilities**. Do not describe or interpret them as probabilities.

## Planned Evaluation

Calculate every classification and routing result separately for the primary
and secondary cohorts. The primary cohort is the headline 2025 result.

### Classification metrics

- row count;
- accuracy;
- macro precision, recall, and F1;
- weighted precision, recall, and F1;
- per-category precision, recall, F1, and support in fitted `classes_` order; and
- confusion matrix counts plus a row-normalized confusion matrix
  (`normalize="true"`) for the primary cohort.

Use all eight locked labels explicitly and `zero_division=0`. Do not suppress a
category with zero support or zero predictions.

### Routing metrics

- automatic-routing row count and coverage;
- human-review row count and rate;
- auto-routed correct and incorrect row counts;
- auto-routed accuracy and misroute rate;
- review-reason counts and shares; and
- actual-category support, auto-routed count, coverage, review rate,
  auto-routed accuracy, and misroute rate in fitted `classes_` order.

Definitions:

- coverage = auto-routed rows / all cohort rows;
- review rate = human-review rows / all cohort rows;
- auto-routed accuracy = correct auto-routed rows / auto-routed rows; and
- misroute rate = incorrect auto-routed rows / auto-routed rows.

If a cohort or category has zero auto-routed rows, report auto-routed accuracy
and misroute rate as `NA`, not zero.

### Drift metrics

Report drift for the primary cohort against the locked 2024 final internal-test
reference; show the secondary cohort as a sensitivity view:

- **Class and label drift:** actual and predicted category counts and
  proportions, percentage-point changes, Jensen-Shannon distance with
  `base=2`, and counts of unfamiliar or changed labels.
- **Text drift:** cleaned character length and whitespace-token count using
  mean, standard deviation, median, 5th, 25th, 75th, and 95th percentiles;
  compare distributions using the two-sample Kolmogorov-Smirnov statistic.
- **Locked-vocabulary behavior:** TF-IDF nonzero-feature count per row using
  mean, median, 5th, and 95th percentiles, plus zero-feature row count and
  rate. Use only the locked vectorizer's transform path.
- **Decision-score drift:** top decision score and top-two margin using mean,
  standard deviation, median, 5th, 25th, 75th, and 95th percentiles; report
  two-sample Kolmogorov-Smirnov statistics and the shares failing each locked
  threshold.
- **Routing drift:** changes in coverage, review rate, auto-routed accuracy,
  misroute rate, review reasons, and actual-category routing results.

Statistical drift measures are descriptive diagnostics. They do not authorize
retuning, refitting, threshold changes, or production use.

### Locked 2024 comparison values

Compare the primary 2025 cohort with the locked 2024 final internal-test
reference using absolute differences calculated as `2025 - 2024`.

| Classification metric | Locked 2024 final internal-test reference |
| --- | ---: |
| Rows | 6,609 |
| Accuracy | 0.8712 |
| Macro precision | 0.7734 |
| Macro recall | 0.7621 |
| Macro F1 | 0.7671 |
| Weighted precision | 0.8721 |
| Weighted recall | 0.8712 |
| Weighted F1 | 0.8715 |

| Routing metric | Locked 2024 final internal-test reference |
| --- | ---: |
| Auto-routed rows | 5,092 |
| Human-review rows | 1,517 |
| Auto-routing coverage | 0.7705 |
| Human-review rate | 0.2295 |
| Auto-routed accuracy | 0.9503 |
| Auto-routed misroute rate | 0.0497 |

Also report per-category classification and routing differences and the
secondary-minus-primary 2025 cohort differences. A difference is evidence of
observed temporal or cohort change, not proof of its cause.

## Reporting and Data-Handling Rules

- Report only aggregate counts, metrics, and figures.
- Do not display or commit complaint narratives.
- Do not commit raw or processed data, row-level predictions, decision scores,
  normalized-text hashes, or model artifacts.
- Do not report calibrated probabilities; none exist for this model.
- Do not claim production readiness, deployment readiness, regulatory
  approval, workload reduction, or cost savings from holdout performance.
- Do not tune, retrain, refit, reselect, or replace the model based on 2025
  results.
- Do not change preprocessing, labels, class order, cohorts, exclusions,
  metrics, comparison rules, or routing thresholds after opening the holdout.
- After results are reviewed, the 2025 sample is no longer an unbiased
  holdout. Any later model or policy change requires a new untouched period.

## Phase 2 Entry Checks

Before opening or loading the 2025 CSV:

- [ ] This protocol has been reviewed, committed, and pushed.
- [ ] The execution environment is compatible with the artifact-creation
      environment and loads the artifact without version warnings.
- [ ] The model, 2025 CSV, and 2024 reference file paths, sizes, and SHA-256
      values match this protocol.
- [ ] The locked 2024 workflow has been reproduced before opening the 2025
      CSV, confirming:
  - 33,042 corrected modeling rows;
  - 26,433 development rows;
  - 6,609 final internal-test rows;
  - all eight classes in both partitions;
  - zero normalized-text overlap between development and final test;
  - the documented 2024 classification metrics reproduced to four decimal
    places;
  - 5,092 auto-routed rows and 1,517 human-review rows; and
  - the documented 2024 routing metrics reproduced to four decimal places.
- [ ] The loaded object is a fitted TF-IDF + Linear SVM pipeline.
- [ ] Pipeline step names, parameters, feature count, and `classes_` order
      match this protocol.
- [ ] Routing code uses the locked thresholds and existing
      `route_from_scores` implementation.
- [ ] No code path calls `fit` or `fit_transform`.

If any entry or 2024 reproduction check fails, Phase 2 must stop before the
2025 CSV is opened or loaded. Document the blocker and do not modify the locked
model or protocol to accommodate observed holdout outcomes.

## Sources of Truth

- GitHub Issue #15
- `notebooks/02_eda_cleaning.ipynb`
- `notebooks/04_sklearn_baseline_model.ipynb`
- `notebooks/05_decision_score_routing.ipynb`
- `src/routing_rules.py`
- `reports/results_summary.md`
- `reports/model_card.md`
- `docs/data_decisions.md`
- `docs/data_ingestion.md`
- `docs/modeling_plan.md`
