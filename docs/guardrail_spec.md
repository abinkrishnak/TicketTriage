# DemoRetail deterministic guardrail specification v1.0

Status: rules specified and frozen before the official ten-case behavior run. Exact code/specification/fixture/check-contract hashes and UTC freeze time are recorded in `results/behavior/guardrail_freeze_v1.0.json`. The version is `1.0`; the freeze-manifest SHA-256 identifies the complete rule bundle. This file is part of that bundle and must not be edited after scoring.

## Scope and interface

`src.guardrails.assess(query, policy=None, catalog=None, extraction=None, generation=None, schemas=None, as_of=...)` returns advisory control decisions only. The runtime accepts no benchmark case ID, expected label or retrieval rank. No network, rented model, hybrid retrieval, classifier filtering, tool execution or agent loop is involved. Callers must pass the actual evaluation/service date and a trusted frozen policy catalogue; the academic default date is 2026-10-02 and must not be used as a permanent production clock.

The five primary outcomes are `abstain`, `clarify`, `escalate`, `human_review`, and `multi_policy_review`. `requires_human_review` is always true and `allow_automatic_action` always false. `hold_draft` is an additional diagnostic hold, not permission to send when false. Human selection, review and sending remain outside this module.

## Input rules and precedence

Text is lowercased with limited apostrophe normalization for matching; original evidence is neither rewritten nor resolved. Bounded regular expressions identify reported states and risks. Precedence is:

1. Reported security concern → `escalate`, without delaying for ordinary clarification.
2. Sensitive content, unauthorized execution/bypass request or recognized instruction override → `abstain`; preserve the security outcome if already triggered.
3. Recognized out-of-scope/promotional request → `abstain`.
4. Material conflicting reports → `human_review`.
5. Distinct substantive issues needing coordination → `multi_policy_review`.
6. Explicit human preference → `human_review`.
7. Unknown carrier acceptance or cancellation with no recognized dispatch state → `clarify`.
8. Unknown pending/posted state → `clarify`.
9. No recognized support topic → ask object, symptom and desired outcome with `clarify`.
10. Otherwise → `human_review`; recognition is not a policy or eligibility decision.

Only finite clarification templates are generated. They ask for reported carrier acceptance, safe pending/posted descriptions, or the object/symptom/objective. Unknowns and conflicts are not converted into facts. This is limited input triage, not general fact extraction. Words such as pending, posted or approved remain customer reports; the module cannot verify a backend state.

Security, explicit human preference, unresolved conflict, coordinated issues and bypass/action requests set a business-review requirement. When a card is explicitly supplied, its mandatory security/cancellation/missing-parcel/duplicate-charge/remedy/handoff review requirements are checked. Recognized business-day counts support the 5-day payment/refund and 3-day delivery conditions. Date parsing is deliberately limited; it does not calculate calendars or prove the correct timing anchor in arbitrary language. Human reviewers must check the starting event and uncertainty. A supplied DR-HUM-002 card needs a recognized procedural reason and never becomes a default nearest-neighbor answer.

## Saved-output and structured-fixture checks

| Check | Diagnostic / response |
|---|---|
| Invalid extraction or generation schema | Flag; invalid generation blocks draft |
| Customer quote not literally in query | Hold for evidence review |
| Recognized security/human/multiple signal omitted in extraction | Flag missed control signal |
| Missing selected policy | Abstain from drafting |
| Card differs from trusted catalogue or unknown ID | Abstain |
| Unapproved, not-yet-effective, stale or invalid-dated card | Abstain |
| Generated policy ID/version differs from supplied card | Hold for human evidence review |
| Missing quote or quote absent from named policy field | Hold for evidence review |
| Mandatory human review disabled | Abstain |
| Policy/state requires escalation but output flag is false | Set advisory `escalate`; preserve original output |
| `answerable_from_policy=false` on a nonempty draft | Hold for human inspection; do not assume the card actually mismatches |
| Recognized request for password/OTP/bank credentials/full card/API key in draft | Abstain |
| Recognized claim that assistant executed/verified a business action | Abstain |

Critical invalid evidence, schema, secret or executed-action checks override a draft's ordinary outcome with abstention. The independent business-review flag can remain true. Remaining evidence defects require human review unless a stronger abstain/escalate/multi-policy outcome already applies. Detection is conservative and may have false positives. Negation handling is clause-based and incomplete; it is not a semantic security guarantee. Unsupported prerequisites such as asking a customer for staff availability are not comprehensively detected.

## Evaluation protocol locked before behavior scoring

The behavior corpus is the unchanged `data/evaluation/ambiguous_unsupported_v1.0.csv`. Primary gold labels remain its authority. Secondary criteria are declared in `results/behavior/behavior_check_contract_v1.0.json` before scoring: required business-review flags, decisive clarification terms, action refusal and mandatory human review. The evaluator alone reads labels; it passes only original query text to the runtime.

No new model outputs exist for those ten cases. The official behavior run therefore measures **direct-input deterministic rule coverage**, not retrieval, extraction quality, policy-selected drafting or end-to-end safety. Uncertainty checks establish that the guardrail does not rewrite facts; safe-clarification checks cover its fixed questions. Draft-level credential, execution and evidence checks are explicitly NOT EXERCISED on the ten text-only cases. They are exercised separately through saved Stage 8 outputs and local structured fixtures.

Record expected/actual primary behavior, PASS/FAIL, preserved uncertainty, safe clarification, escalation correctness, prohibited-action handling, mandatory review and evidence/reason codes per case. Keep the ten-case metrics, 18-fixture results and 15-case Stage 8 replay separate. Stage 8 human labels do not change. Exact raw outputs are never repaired or overwritten. Freeze includes evaluator code and secondary scoring criteria. Refuse re-scoring into an existing official results file. No changes to rules after inspecting behavior scores; a future correction needs a new version, documented reason and clearly separate results.

## Pre-freeze development evidence and known limitation

The 18 predeclared local fixtures passed 17 checks and failed one: an unsupported airline-reservation request outside the explicit lexicon received clarification instead of abstention. Preserve this failure. No rule was added to make this probe pass. Stage 8 regression replay detected the five missed escalation flags identified in human review; this is expected on development evidence, not generalization. Input vocabulary and evaluation labels were known during design, so even a perfect ten-case score cannot support a production/generalization claim.

Human review remains necessary for semantic omissions, wrong starting events, subtle negation, unsupported promises or prerequisites outside the patterns, novel domains, adversarial phrasing, redaction and policy selection. An integration must enforce the returned hold/review controls; this module alone cannot prevent another application from ignoring them.
