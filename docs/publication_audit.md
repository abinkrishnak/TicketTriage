# Public release safety audit

Status: PASS. Audit date: 2 October 2026.

The allowlisted release was scanned for credential patterns, exact local credential values (in memory only), workstation paths, email addresses, private source references, excluded files and oversized assets. No matches were found. The environment template contains a placeholder only. Security-related words in fictional policies and schemas are intentional, not credentials. Binary assets are limited to the trusted small classifier, saved numeric embeddings and the app screenshot; their hashes are recorded in the publication manifest.

All 356 protected Stage 5â€“9 files remain unchanged. Copied evidence matches its development source. Public-copy offline smoke tests passed with outbound connections blocked, without a key or paid calls. No evaluations were rerun. See results/publication_validation.json.

This is a finite local audit, not a guarantee that every possible sensitive string can be recognized. Only fictional/generalized cases and the intentional reviewer attribution remain. Raw transport logs, private source documents, notebooks, credentials and model caches are excluded. Publish only this folder after owner approval. No GitHub push has occurred.

MIT is selected for original code/documentation; third-party notices and archived provenance identify upstream resources and preserve their rights. Optional new-ticket semantic preview requires separately installed dependencies and the pinned local model cache; saved replay does not.
