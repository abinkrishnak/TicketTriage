# Final evidence inventory

| Evidence | Location |
|---|---|
| Classifier metrics and per-class/confusion tables | `results/metrics/` |
| TF-IDF/semantic predictions, comparison and per-subset summary | `results/retrieval/` |
| Final human FM metrics and 15 complete unedited parsed output pairs | `results/fm/` |
| Ten behavior results, 18 local fixtures and Stage 8 replay | `results/behavior/` |
| Scenario inputs and derived economics | `results/behavior/cost_to_serve_scenarios_v1.0.*` |
| Policy, 60-query benchmark, behavior and FM component cases | `data/` |
| Six-example portable replay and runtime hashes | `data/demo/` |
| Exact system prompts and schema/builders from Stage 8 | `prompts/`, `src/llm/`, `data/evaluation/` |
| Frozen guardrail implementation/specification | `src/guardrails/`, `docs/guardrail_spec.md` |

`results/publication_provenance.json` maps copies/exports to source hashes. `PUBLICATION_MANIFEST.json` is the exact proposed file allowlist. Derived summaries are labeled, not substituted for originals. The 15-case evidence is parsed response content, not raw API transport logs; field values and human labels are unchanged. Assistant proposals remain in original local evidence and are not final public metrics.

Six historical notebooks stay local. They contain development/provisional narrative and depend on omitted raw/processed data and private source audit context; consolidated documentation and final tables are more useful to a reader. Plans, handoff prompts, authentication/debug logs, raw work/course documents, previous policy versions and duplicate reports are excluded without deleting local originals. This release supports an offline demo and inspectable results, not complete retraining from a bundled raw dataset.
