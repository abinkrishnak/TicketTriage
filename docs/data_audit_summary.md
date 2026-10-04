# Historical data and leakage audit

This summary packages existing audit evidence; it is not a new experiment or a change to the classifier evaluation.

| Stage | Recorded finding |
|---|---|
| Original Bitext data | 26,872 rows; no complete duplicate rows |
| Naive diagnostic split | 703 of 5,375 test requests had a normalized-text match in training: 13.08% |
| After scope selection and deduplication | 11,373 unique usable requests |
| Final evaluation split | 9,098 training requests and 2,275 test requests |
| Final split overlap | Zero exact/normalized train-test overlap |

The naive split was a diagnostic split used to identify leakage risk. It was not the final evaluation split. Absence of complete duplicate rows did not imply absence of repeated request wording. Scope selection and deduplication preceded the final split; the reduction in rows was not solely duplicate removal.

Zero normalized overlap does not prove semantic independence. Related templates and paraphrases can remain across the split. These checks do not establish production generalization.

## Provenance

The values above are transcribed from retained development records, not recomputed evaluations. These source records remain outside the public replay package:

- `results/eda/tables/eda_metrics.json` — SHA-256 `722bc105e497f0eda325e957035218560f4769b4d2a9918938ddd9b301ab1906`; original row/duplicate counts and diagnostic overlap.
- `results/preprocessing/tables/preprocessing_summary.csv` — SHA-256 `7c519310a182ad8306b2f151abdd1fa457df43e468aa428f27f48d8e01070d7d`; retained unique requests, final split sizes and normalized overlap. Exact textual equality necessarily implies normalized equality, so zero normalized overlap also excludes exact overlap.

Source hashes identify the retained records; they do not make the omitted files publicly reproducible. This is a public summary, not a bundled retraining dataset. See [dataset provenance](project_overview.md) and [layered evaluation](evaluation.md).
