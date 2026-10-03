# Report and demo language bank

Use the safe claim with its denominator, test condition and limitation. The contrasting wording below is explicitly an overstatement to avoid, not an additional result.

| Topic | Safe claim | Unsafe/overstated version to avoid |
|---|---|---|
| Classifier | “99.65% measures broad six-category classification on 2,275 cleaned Bitext holdout requests; macro F1 was 0.995978.” | “The system is 99.65% accurate.” |
| Classifier role | “The classifier is a fast hint and never filters retrieval; no ablation proves end-to-end necessity.” | “The classifier is essential to achieve these retrieval results.” |
| Retrieval | “Semantic retrieval was nominally higher at top-1 on this 60-query benchmark: 38/60 versus 35/60.” | “Semantic retrieval significantly outperformed TF-IDF.” |
| Target | “The +10-point objective was chosen after observing the TF-IDF aggregate and before semantic scoring. Actual improvement was +5 points, so the goal was missed.” | “The original 85% goal was achieved” or “the target was preregistered before any analysis.” |
| Candidate UI | “Semantic top-three included the gold card on 58/60 cases, supporting candidate discovery as a design hypothesis.” | “Candidate selection saves agents time” or “96.67% of final answers are correct.” |
| Query provenance | “The corpus and 45 controlled queries share assistant authorship; 15 personal queries are policy-aware, user-supplied and experience-inspired, with disclosed assistant-assisted adaptation.” | “Sixty independent real-customer tickets validated the system.” |
| LLM | “With gold policy supplied on 15 cases, final human generation ratings were 2 PASS, 6 PARTIAL and 7 FAIL.” | “RAG solved the cases reliably” or “the model has a production failure rate of 7/15.” |
| Structured output | “All 30 component outputs were schema-valid; factual and procedural quality still required review.” | “Valid JSON proves correctness.” |
| Human review | “One project-author reviewer adjudicated after seeing provisional assistant ratings; anchoring and independence are limitations.” | “An independent blinded reviewer validated the results.” |
| Rubric | “The preflight rubric is published alongside final case notes and disclosed adjudication differences.” | “Every human PASS means every control field passed a reproducible scoring rule.” |
| Guardrails | “10/10 declared behavior cases, 17/18 development fixtures, and five known missed escalations detected establish finite coverage/regression evidence.” | “The system is fully safe” or “guardrails catch all bad outputs.” |
| Known failure | “The airline-request fixture still clarifies instead of abstaining, showing an out-of-domain gap.” | “Unsupported requests are always rejected.” |
| Cost | “Measured FM cost was $0.00064629 per component ticket; review/runtime/escalation assumptions produce illustrative cost-to-serve scenarios.” | “The complete service costs only $0.00064629 per ticket.” |
| Economics | “Without a measured manual-handling baseline, this analysis estimates cost-to-serve scenarios, not savings, ROI, or break-even.” | “The prototype has proven ROI or a measured break-even volume.” |
| Latency | “Sequential component HTTP latency was 4.613s median and 6.093s p95 in this small experiment.” | “An employee resolves a ticket in 4.613 seconds.” |
| Governance | “Fictional policy metadata, data boundaries, hashes and mandatory human review support auditability; production compliance was not established.” | “The system is compliant and production-ready.” |
| Privacy | “The experiment used synthetic/generalized inputs; limited checks are not comprehensive PII redaction.” | “All sensitive information is automatically removed.” |
| Monitoring | “Saved experiment diagnostics exist; persistent production telemetry is future work.” | “The system is continuously monitored in production.” |
| Integrity | “Hashes identify exact recorded artifacts; they do not independently prove chronology or blinded preregistration.” | “The hashes prove the experiment was preregistered.” |
| Productivity | “No user study or manual-versus-assisted handling-time baseline was measured; selection may add friction.” | “Raj handles tickets faster and customers are more satisfied.” |
| Replay | “Offline mode replays saved outputs. Optional local preview ranks new tickets; fresh GPT drafting is not implemented.” | “The demo produces a new GPT response for any ticket.” |
| Agentic future | “This is a fixed workflow with no autonomous tool-action loop. Future agency would require permissions, caps, external ground truth, approvals, negative-case tests and rollback/auditability.” | “An autonomous agent already resolves support tickets.” |

Evidence: [evaluation](evaluation.md), [review rubric](fm_human_review_rubric.md), [plan versus delivered](plan_vs_delivered.md), [economics clarification](economics_interpretation.md), [workflow boundary](architecture.md#why-this-is-a-workflow-not-an-agent). All numbers refer to unchanged saved results; no new experiment accompanies these wording changes.
