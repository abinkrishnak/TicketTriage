# Why evaluation is layered

Broad classification asks which of six categories a request resembles. Exact policy retrieval distinguishes business conditions and states among 15 cards. Grounded drafting asks whether the model can give complete guidance and preserve control decisions. These are different questions, not one end-to-end accuracy.

## Broad category classification

On 2,275 cleaned held-out Bitext requests, majority accuracy was 22.64%; TF-IDF + Logistic Regression achieved 99.65% and macro F1 0.995978. This is synthetic holdout performance, not real-support accuracy. Normalized duplicate-aware splitting and training-only vectorization reduce leakage, but residual template similarity remains. The classifier has no OOD class; probabilities are uncalibrated.

## Exact policy retrieval

The frozen 60-query benchmark requires a primary policy. TF-IDF achieved 35/60 Recall@1 and 50/60 Recall@3; semantic retrieval achieved 38/60 and 58/60, MRR 0.7820707. Semantic gains/regressions were 9/6, with 29 both correct and 16 both wrong. The predeclared +10-point target required 41/60; 38/60 is +5 points, so the target was not met.

Personal queries are separate: both methods achieved 11/15 Recall@1 (73.33%); Recall@3 was 15/15 for TF-IDF and 14/15 for semantic retrieval. Semantic is not uniformly better. Candidate discovery improves overall, while temporal/state distinctions, negation and procedural objectives remain difficult. The UI exposes candidates instead of trusting top-1.

Model: `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. The default embedding limit is 256. Before scoring the user approved 512, supported by the underlying transformer; all policy/query texts passed the length gate without truncation. This is outside the default sentence-embedding configuration and longer-input quality is not guaranteed. No model search, chunking, hybrid retrieval, classifier filtering or reranking was used.

## FM evaluation deliberately uses GOLD policy

Fifteen fixed cases (five personal, ten controlled, one per card) received the correct policy intentionally. Retrieval failures therefore do not contaminate extraction/drafting evaluation. Extraction still feeds generation, so extraction errors can propagate; this is not independent generation-only or end-to-end evaluation.

Locked model: OpenRouter `openai/gpt-4o-mini`, OpenAI provider only, temperature 0, strict JSON Schema plus local validation, output caps 900/1,100, timeout 60 seconds, no automatic retries. All component outputs were schema-valid. Final human review by Abin on 2 October 2026 found:

| Check | PASS | PARTIAL | FAIL | AMBIGUOUS |
|---|---:|---:|---:|---:|
| Extraction | 4 | 11 | 0 | — |
| Generation | 2 | 6 | 7 | — |
| Escalation | 9 | — | 5 | 1 |

C41 contains the sole human-labeled unsupported prerequisite. Generation PASS cases are C05/P13; acceptance does not erase noted field defects. Incomplete guidance, repeated questions and missed escalation are major weaknesses. Final human labels supersede assistant proposals; original outputs remain unedited. This small coverage slice is not a population estimate.

## Independent deterministic controls

Guardrails v1.0 was frozen before scoring ten behavior cases. Primary outcomes matched 10/10: abstain 3/3, clarify 3/3, escalate 1/1, human_review 2/2, multi_policy_review 1/1. These are direct-input finite-rule checks; no new model drafts existed for these ten cases. Draft security/grounding was not tested in that benchmark.

Separate local fixtures passed 17/18. An unsupported airline request received clarification because its domain was outside the finite vocabulary; that failure remains. Saved Stage 8 replay detected all five known missed escalation controls. Replay is development regression evidence, not generalization. The benchmark meanings were known during design, so 10/10 does not prove end-to-end safety.

## Product implication

Strong category classification does not solve policy selection. Correct policy does not guarantee complete guidance. Guardrails add independent controls, but human review remains necessary. No production traffic or measured handling-time savings exists. Cost scenarios are assumptions, not measured savings.

A separate UI scope-display heuristic hides misleading recommendations for clearly non-support wording. It changes neither Guardrails v1.0 nor frozen labels. It uses finite topic signals, not a tuned confidence threshold, and is not a validated OOD detector. The novel-domain limitation remains.
