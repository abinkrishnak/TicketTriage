# Project overview

TicketTriage is a PE6201 academic prototype for an employee at fictional retailer DemoRetail. It is a fixed workflow, not an agent. It interprets support wording and finds policy evidence while preserving human authority.

## Data provenance

Recorded dataset: `bitext/Bitext-customer-support-llm-chatbot-training-dataset`, revision `430d1a89bd93bd1fa23c16f29dd53e73f0087443`, v11 response CSV. The saved card declares CDLA-Sharing-1.0. Its synthetic language is public; it is not this project's real customer data. Raw Bitext records are not redistributed in this package.

From 26,872 original rows, 13 intents map to six broad categories and 11,373 usable unique requests. Normalized duplicate groups remain together; training/test sizes are 9,098/2,275. Vocabulary/IDF are learned on training data only. Responses and audit IDs are not features. Zero normalized overlap is not proof of semantic independence: a sampled audit found 19 cross-boundary near-duplicate candidates.

The policy layer is separate: 15 authored fictional cards in frozen DemoRetail Playbook v1.1, with conditions, exceptions, required facts, prohibitions, escalation and governance metadata. No real-company approval is claimed. Seven content fields form retrieval text: title, supported issue, short description, policy text, eligibility, exceptions and exclusions. IDs, categories and governance metadata are excluded from matching text.

Sixty frozen retrieval queries comprise 45 controlled and 15 personal/experience-inspired generalized questions, not live employer records. Ten ambiguous/unsupported cases test behavior separately. A deterministic 15-case coverage slice supplies GOLD policy for FM component evaluation and final human adjudication by Abin.

## Product and publication boundary

Saved replay displays evaluated evidence; local preview uses local classification, semantic candidates and direct-input checks only. New extraction/drafting is unavailable. Classifier categories never filter retrieval. A human explicitly selects policy; the prototype cannot send messages or execute transactions.

The public bundle contains final evidence and unedited parsed outputs, not credentials, private work documents, course materials or raw API logs. Local originals remain untouched. Publication exports and runtime bundles are derived views with source hashes, not replacements for frozen evidence. Historical notebooks are retained locally and summarized here because they depend on omitted data and contain provisional narrative.
