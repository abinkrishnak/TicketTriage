# Running and exploring TicketTriage

From the repository folder, use the README's Python 3.14 environment commands, then run `python -m streamlit run app.py` with that environment active. The server binds to `http://127.0.0.1:8502`; no deployment or public exposure is required. Opening it makes no API calls, needs no key and defaults to saved evidence.

## Saved examples

| Example | Purpose | Original supplied policy |
|---|---|---|
| P13 | Useful damaged-item draft; final generation PASS | DR-REF-003 |
| P04 | Wrong semantic top-1; correct card at rank 3 | DR-CAN-002 |
| C05 | Security escalation despite recovery ranking first | DR-ACC-002 |
| C36 | Original model missed required escalation | DR-REF-002 |
| A03 | Unknown dispatch state needs clarification | No single selected policy |
| A01 | Unsupported expired discount | No applicable policy |

Inspect candidates and explicitly select/confirm the original card before viewing a saved draft. Selecting another card cannot attach or regenerate that draft. Editing the saved ticket invalidates replay. A03/A01 have only saved input-rule evidence, no GPT output or semantic ranking. Historical model defects remain visible alongside final human review and guardrail diagnostics.

## Local ticket preview

Use the three suggested tickets or type generalized support text. Install optional local semantic dependencies once with `python -m pip install -r requirements-local.txt`. Place the pinned `sentence-transformers/all-MiniLM-L6-v2` revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` files in `.local_runtime/models/all-MiniLM-L6-v2/<revision>/`, or set `TICKETTRIAGE_MODEL_DIR` to an existing reviewed local model folder in your shell. On the original project laptop this cache already exists. The application verifies the recorded file hashes; it never downloads weights. A new clone without these files still supports saved replay and local classification, and displays a useful message when semantic preview is unavailable.

No paid model mode is implemented. New tickets get no GPT extraction/draft. All 15 policies compete; classifier predictions never filter retrieval. Queries exceeding 512 tokenizer tokens are rejected without truncation. First local model loading can take tens of seconds; saved replay avoids that load.

For “What is your name?”, the UI warns that the input does not appear to match supported topics and hides candidate guidance. Any forced classifier probabilities appear only under technical diagnostics. This finite topic heuristic is not validated OOD detection; novel unsupported wording can still be misclassified or clarified. It does not change Guardrails v1.0 or benchmark labels.

## Troubleshooting and boundaries

Restore a named missing/corrupt artifact instead of rerunning experiments. An absent API key has no effect. The small trusted classifier is included, while large MiniLM weights, raw datasets and virtual environments are excluded. Dependencies need one-time installation; offline does not mean installation without local packages. Use a different local port if 8502 is busy. Effective/review dates use the actual laptop date; do not alter frozen policies to bypass stale-evidence checks.

No send/action buttons or persistent reviewer decisions exist. Final human authority and finite-check limitations remain visible. This guide describes operation, not a scripted final presentation or production deployment.
