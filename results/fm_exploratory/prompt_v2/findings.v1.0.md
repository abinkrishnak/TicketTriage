# Exploratory prompt-v2 findings

Exploratory prompt-improvement follow-up on already-exposed cases.

Exactly 15 generation calls completed. No extraction/retrieval/classifier rerun, no retry, no fallback. Only the SYSTEM message changed in each submitted request. Original Stage 8 generation remains officially 2 PASS / 6 PARTIAL / 7 FAIL.

## Assessment status

User-approved exploratory baseline: 0 PASS / 3 PARTIAL / 11 FAIL / 1 REVIEW_BLOCKED. The v2 results below are assistant assessments under the same frozen checklist, awaiting user/human confirmation; they are not a new human-reviewed official benchmark. C14 remains REVIEW_BLOCKED as explicitly authorized.

V2 proposed generation: 0 PASS / 0 PARTIAL / 14 FAIL / 1 REVIEW_BLOCKED. Escalation: 10 PASS / 4 FAIL / 1 AMBIGUOUS.

| Case | Approved exploratory baseline | V2 proposal | Escalation baseline → v2 | Evidence summary |
|---|---|---|---|---|
| P01 | PARTIAL | FAIL | PASS → FAIL | Redundant prose questions removed; new false answerability and premature escalation cause regression. |
| C05 | FAIL | FAIL | PASS → PASS | Security guidance remains useful; false answerability persists even though policy_mismatch flag disappeared. |
| C09 | FAIL | FAIL | FAIL → PASS | Mandatory escalation fixed; false answerability newly introduced; repeated state questions remain. |
| P04 | FAIL | FAIL | PASS → FAIL | Return deadline restored and repeated acceptance question removed from prose; false answerability remains and escalation now incorrectly asserted. |
| C14 | REVIEW_BLOCKED | REVIEW_BLOCKED | AMBIGUOUS → AMBIGUOUS | Same escalation ambiguity retained as REVIEW_BLOCKED. False answerability is an additional observed defect, not permission to invent a final label. |
| C18 | FAIL | FAIL | PASS → PASS | Immediate review retained; false answerability and repeated receipt/tracking questions persist. |
| P07 | FAIL | FAIL | PASS → FAIL | Tracking threshold and not-yet-late guidance added; unnecessary questions remain and escalation now asserted without an established business-day threshold. |
| C23 | FAIL | FAIL | PASS → FAIL | Still fails to provide basic billing/single-later-attempt guidance; now invents reported payment uncertainty and escalates unnecessarily. |
| C27 | PARTIAL | FAIL | PASS → PASS | Provider dependency restored and prose no longer reasks known facts; stale structured missing list and new false answerability remain. |
| P10 | FAIL | FAIL | FAIL → PASS | Required duplicate-payment review flag corrected; irrelevant missing-information entries improved, but repeated status questions and new false answerability remain. |
| C32 | FAIL | FAIL | PASS → PASS | Inspection added; item-price-only refund scope still omitted. New false answerability and repeated date/condition questions remain. |
| C36 | FAIL | FAIL | FAIL → PASS | Overdue state and mandatory trace flag corrected; redundant date request and nonexact quote remain; false answerability is new. |
| P13 | PARTIAL | FAIL | PASS → PASS | Different damaged-item process stated more clearly; redundant date request persists, explicit unsafe-handling guidance lost, and false answerability newly introduced. |
| C41 | FAIL | FAIL | FAIL → PASS | Human referral/target now explained; staff availability no longer demanded in prose, but remains in missing_information. Escalation corrected; false answerability new. |
| C45 | FAIL | FAIL | FAIL → PASS | Summary structure now partly supplied and escalation corrected; policy-boundary element omitted, policy-answer question remains in structured missing_information, and answerability false. |

## Gains and regressions

- Of 11 baseline FAIL cases, zero improve in overall label and all 11 remain FAIL; C14 remains blocked. Three PARTIAL cases regress to FAIL: P01, C27, P13. Twelve cases retain the same overall status, including the blocked case.
- All five known missed escalation decisions are fixed: C09, P10, C36, C41, C45. Four previously accepted decisions regress to unnecessary escalation: P01, P04, P07, C23. Net escalation PASS count moves from 9 to 10; this does not establish net system benefit.
- All 15 outputs set answerable_from_policy=false while providing supported guidance. This affects Q10 in every case; 12 are new false-answerability defects, while C05/P04/C18 had this defect already. No output includes policy_mismatch; C05 retains security_concern. Absence of policy_mismatch does not repair false answerability.
- Known-fact questions in prose fully fixed in 3/12 originally affected cases: P01, P04, C27. Structured missing-information defects persist; this is not a claim that missing_information is fixed.
- Relevant-guidance defects fully fixed under Q06 in 4/9 affected cases: P04, P07, C27, C41. C32 and C45 improve partly; C09, C23 and P13 retain omissions.
- C41 no longer asks the customer for staff availability in the draft, but still lists it as missing information. Zero fully clean unsupported-prerequisite repairs; one customer-facing improvement with structured residue.
- Thirteen cases have at least one worsened assessable checklist criterion; that is different from the three overall-label regressions.

## Cost and latency

OpenRouter usage-reported total: US$0.00676335. Conservative uncached token calculation: US$0.00783855. The difference is consistent with 14,336 cached input tokens at half input price. Budget ceiling US$0.04. Input 35,865 tokens; output 4,098. These are API response accounting, not an independently inspected invoice.

Generation-only roundtrip latency: mean 3.227839 s; median 2.981611 s; linear p95 3.965789 s; min 2.506533 s; max 4.179772 s; summed call latency 48.417585 s. Per-call exact float measurements and usage are in saved parsed records. Excludes manual pauses, offline preflight and human review; not comparable to original combined extraction+generation latency without adjustment.

## Academic interpretation

The revised instructions coincided with better escalation recall on known failures and better guidance in some drafts, but also over-escalation and systematic answerability inconsistency. This run does not support adopting prompt v2 as a demonstrated overall improvement. Do not tune again on these outputs without a separately labelled exploratory plan.

The original returned system fingerprint was fp_d1cac234d1 for all 15 original generation calls; this run returned fp_ce3836fcfd throughout. Model alias/provider/settings remained fixed and no fallback occurred, but the provider fingerprint changed. A fingerprint difference does not identify the precise backend change; it prevents assuming an unchanged backend and attributing all differences solely to SYSTEM prompt revision. No backend version was silently substituted by the client.

Cases were already exposed and the evaluator is an assistant, not independent human adjudication. Frozen checklist aggregation intentionally penalizes control-field failures even when prose improves. Original official labels use earlier human adjudication and must remain distinct. No claim of accuracy, statistical superiority, production safety or unseen generalization follows.

## Integrity and stop point

Post-run checks confirm all 356 protected-source hashes and six preparation hashes unchanged; all 15 requests differ only in SYSTEM content; raw and parsed outputs agree and all schemas validate. Public repo/app/docs were not edited. No commit/push. The initial read-only catalogue lookup was blocked by the sandbox; the approved network-enabled lookup passed before the first inference. This was not an inference retry.

Execution is closed after 15 attempts. Await user approval; do not update README, report, Streamlit or public release.
