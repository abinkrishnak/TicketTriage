# Streamlit Community Cloud deployment

Prepared 3 October 2026. This is deployment/UX work, not a new evaluation. No live GPT mode, key loading, automatic model download or business-action tool is added.

## Audit findings before edits

| Area | Finding | Decision |
|---|---|---|
| `.streamlit/config.toml` | Laptop loopback binding and port 8502 are inappropriate defaults for a hosted app | Remove explicit address/port; let Community Cloud supply them; keep usage telemetry disabled |
| `requirements.txt` | Exact base pins existed, but Linux availability had not been checked | Preserve training-compatible classifier versions; resolve base dependencies against Linux/Python 3.13 wheels |
| `requirements-local.txt` | Separate torch/transformers/Sentence-Transformers stack is not installed by root requirements | Keep it optional for desktop/local-cache use, out of the lightweight cloud install |
| `src/demo.py` semantic loader | Exact MiniLM revision is local-files-only; large weights are not in Git | No startup download; disclose unavailable new-ticket semantics and continue classification/input checks |
| Runtime paths | Core data paths derive from the repository path, not a Windows drive; optional model errors could expose absolute cache paths | Keep portable paths and give generic optional-model errors without showing cache locations |
| Replay assets | Six examples, small classifier, policies, saved embeddings and parsed outputs are bundled with runtime hashes | Use unchanged saved evidence; no full model cache required for replay |
| Privacy wording | “Stays local” is ambiguous on a remote server | Explain browser-to-demo-server processing and the absence of outbound inference APIs |
| Policy validity | Frozen cards have real effective/review dates | Preserve checks. After a card expires, confirmation/draft replay is blocked; a portfolio URL is not policy renewal |

## Supported profile

**Saved evidence:** P13 damaged item; P04 confusable cancellation; C05 security; C36 missed refund escalation; A03 unknown dispatch; A01 unsupported discount. Inspect saved classifier output and candidates where recorded, select/confirm the original valid policy, and inspect unedited extraction/draft plus final human review. A03/A01 have behavior evidence only, with no invented ranking or GPT draft.

**New-ticket limited preview:** server-local classifier, finite scope/state checks and mandatory human-review diagnostics. Semantic retrieval is unavailable without both optional dependencies and the exact verified model cache. Its absence produces a notice, not a download, different model, lexical substitute or crash. Manual policy inspection remains possible and does not produce new text.

**Optional local semantics:** unchanged `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, maximum 512 tokens, saved policy vectors, all 15 policies compete. Install `requirements-local.txt` and obtain the exact cache separately for a controlled local environment. Hash verification precedes use. No performance claim is refreshed by this deployment.

**No live GPT:** no OpenRouter/OpenAI transport is imported by the app, no key is requested/read, and no fresh extraction/draft or backend action is offered.

## Why not automatic MiniLM downloads?

Public weights could technically be fetched by a deployment with network access, but the current model loader is intentionally offline and hash-pinned. Adding torch plus the language-model stack introduces substantial installed/runtime overhead, cold-start network dependence and model-loading latency. We did not measure their live cloud memory behavior and therefore cannot certify reliable operation under shared resources. Saved replay is the reliable baseline; the user-authorized limited-preview fallback is used rather than promising untested cloud semantics.

Streamlit's [resource guidance](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app) says limits are variable; its listed approximate figures are dated February 2024, not a guaranteed allocation for this app. No resource-capacity benchmark or model-download experiment was performed.

## Deploy after review and publication

1. Use repository `abinkrishnak/TicketTriage`, the intended published branch, and entrypoint **`app.py`** at repository root.
2. Select **Python 3.13** in Advanced settings. Do not add secrets. Root `requirements.txt` includes all dependencies required for the supported lightweight profile.
3. Allow Community Cloud to build the environment. No OS package file or GPU is needed for this profile.
4. Check all six saved examples and a fictional new-ticket preview in the deployed app. This local preparation is not a claim that Community Cloud has already been tested.
5. Add the actual Streamlit URL to README only after deployment succeeds. No URL has been invented.

Sources checked 3 October 2026: [Python selection and deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [dependency handling](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies). Top-level versions are pinned; transitive versions are resolved by pip, so this is not a fully hash-locked environment.

## Privacy and runtime boundary

User text goes from the browser to the running Streamlit server. Classification/input checks, and optional local retrieval if installed, execute there. The app sends no entered text to an external inference API and deliberately writes no ticket files. Model objects are cached, not ticket predictions; ticket text stays in the session's state. Hosting infrastructure can keep access/operational logs: do not promise zero retention. Use fictional/generalized tickets only, never credentials or confidential data. Outbound GitHub links are navigation links, not automated ticket submission.

The repository includes a placeholder `.env.example`, not `.env` or a key. No key is needed. Frozen models, policies, guardrails, labels, prompts and results are unchanged. Historical publication/runtime manifests retain their original scope; this deployment does not rewrite evaluation history.

## Validation boundaries

Linux/Python 3.13 base dependency resolution succeeded using compatible wheels. Runtime smoke validation uses a separate Windows/Python 3.14 environment installed from only root requirements, without torch/Sentence-Transformers or the MiniLM cache. This tests the selected missing-model fallback rather than pretending to be a live Linux service. A final Community Cloud runtime smoke check is still required after the owner publishes/deploys.

### Completed local smoke check — 3 October 2026

- App starts and all six saved examples load: P13, P04, C05, C36, A03, A01. The four saved GPT drafts display unchanged after their original policy is selected and confirmed.
- New-ticket classification works with root requirements only. Missing MiniLM dependencies/cache produce an explicit unavailable notice; no alternate model or download is attempted.
- Non-support text hides misleading category/candidate guidance. Missing replay evidence gives a friendly error rather than an unhandled exception.
- Portfolio header, replay disclosure, workflow, evaluation values and limitations render. Source navigation is visible.
- With a test-only clock set to 2 January 2027, stale policy blocks confirmation and draft display. No policy date/content was edited to pass this check.
- Keys were absent from the test process, external socket connections were blocked, and zero outbound attempts occurred. Installed dependencies pass `pip check`.
- All 356 protected development artifacts and public frozen evidence remain byte-identical. No benchmark was rerun and no model/policy/prompt/result was changed.
- The public-file scan found no `.env`, credentials, private documents or workstation paths. Placeholder `.env.example` and fictional policy/security terminology are intentional; the scan is not a comprehensive compliance certification.

An earlier 45-second UI-test timeout occurred during first-use SciPy/scikit-learn imports in the fresh environment. The resumed test passed with a longer harness timeout; classifier behavior and frozen artifacts were not changed. Cold-start delay remains possible on a shared cloud host. The local smoke summary is retained outside the public repository at development-relative `.local_runtime/cloud-demo-smoke.json`; it is deployment evidence, not a new scored experiment.

## Cross-platform integrity correction — 4 October 2026

The deployed error for `data/demo/saved_examples.json` was reproduced from the committed Git blob: the historical manifest hash covers Windows CRLF bytes, while Git stored LF bytes (`core.autocrlf=true`, no repository attribute override). The working tree contained 793 CRLF line endings; the committed blob contained LF endings. Parsed JSON was identical, and all byte differences were explained by newline representation.

- Historical expected hash, also the unchanged Windows working-tree hash: `dc609b09872923be04a9c00121eac51b1f7658739e41796a6f3f1e6ad10c1a63`.
- Committed Git/LF hash: `a858186c835bb3e5a955cfaa3959d9eaab193b1a142954a3a39935329d3d3ede`.
- The same representation mismatch affected `data/demo/semantic_model_assets.json`; other checked runtime artifacts matched their committed-byte hashes.

The verifier still tries the exact byte hash first. For only four explicitly allowlisted runtime text files (saved examples, semantic asset manifest, policy JSON and guardrail Python source), a mismatch additionally checks UTF-8 bytes represented with LF or CRLF against the **unchanged historical expected hash**. Conversion is in memory only: CRLF pairs become LF, then an alternate candidate expands LF to CRLF. No JSON parsing/reserialization, whitespace trimming, BOM removal, lone-CR conversion or Unicode normalization is used. Escaped JSON string characters are untouched. Model weights, classifier and embedding binaries retain exact-byte validation. Optional model-cache verification also retains exact-byte validation.

This preserves detection of substantive changes without depending on checkout newline settings. No evidence file, manifest hash, output, policy, model, prompt, label or result was replaced. No Git renormalization was performed. This is a deployment portability correction, not a new experiment or integrity-check bypass.

Validation passed for the Windows working tree and a disposable checkout of exact committed LF blobs: all six runtime manifest entries verified, all six examples loaded, all four stored drafts (including P13 and C36) and their control evidence displayed unchanged, and stale-policy confirmation/draft blocking remained enforced under a simulated expired date. Modified JSON content, added whitespace, a BOM, bare-CR text and binary newline alteration were rejected in disposable test fixtures. Keys were absent, external connections blocked and zero outbound attempts observed. All 356 protected development artifacts and public evidence bytes remained unchanged. The LF test simulates checkout bytes locally; deployment of the correction still requires an owner-approved commit/push and cloud restart.
