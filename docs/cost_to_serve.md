# Class 5 cost-to-serve scenarios

These are illustrative USD scenarios, not measured operations or evidence of savings. The measured FM variable cost is **US$0.00064629 per component ticket**, from the frozen Stage 8 gold-policy experiment. All other inputs below are assumptions. The experiment's average may not transfer to different ticket lengths, model prices, retries or workflows.

`cost per ticket = FM variable cost + allocated local/runtime cost + human review minutes × hourly labor cost / 60 + probability of escalation × incremental escalation cost`

## Inputs: measured versus assumed

| Scenario | Measured FM $/ticket | Assumed local/runtime $/ticket | Assumed review minutes | Assumed labor $/hour | Assumed escalation probability | Assumed extra cost per escalation |
|---|---:|---:|---:|---:|---:|---:|
| low_review | 0.00064629 | 0.002 | 1 | 18 | 0.05 | 2 |
| moderate_review | 0.00064629 | 0.010 | 3 | 24 | 0.15 | 6 |
| high_review | 0.00064629 | 0.030 | 6 | 30 | 0.30 | 12 |

## Derived scenario outputs

| Scenario | Review cost | Expected incremental escalation cost | Total $/ticket | Total $/1,000 tickets |
|---|---:|---:|---:|---:|
| low_review | 0.3 | 0.10 | 0.40264629 | 402.64629000 |
| moderate_review | 1.2 | 0.90 | 2.11064629 | 2110.64629000 |
| high_review | 3 | 3.60 | 6.63064629 | 6630.64629000 |

Review minutes apply to every ticket, including those escalated. Incremental escalation cost includes only work beyond that initial review, avoiding double counting. Local/runtime allocation represents a hypothetical per-ticket allocation of local compute/hosting overhead; it is not a measured laptop power or hosting bill. Scenario hourly costs are planning inputs, not wage estimates. Ticket volume of 1,000 is a scaling example, not a demand forecast.

Human review and escalation dominate these selected scenarios. For example, one additional review minute at $24/hour adds $0.40 per ticket—far more than the measured model charge. This is arithmetic sensitivity, not evidence of improved productivity or worse performance. Quality failures may increase review and escalation effort; the observed generation failure rate is not itself a measured escalation probability and is not used as one.

Stage 8 successful API evaluation spend was **$0.01158525**, with **$0.00234** still reserved conservatively for an earlier authentication failure (not confirmed billed), for a ledger total of **$0.01392525**. These are historical experiment amounts, separate from recurring per-ticket scenarios. **Stage 9 new API spend is $0; no paid calls occurred.** Development time, assessment effort, taxes, account top-up fees, long-term maintenance, integration, security and storage are excluded or unmeasured; this is a bounded scenario model, not a fully costed business case.

The unchanged Stage 8 HTTP latencies are extraction median 2.101 s, generation median 2.444 s, sequential median 4.613 s and p95 6.093 s. They exclude human review and do not establish labor savings. The optional lookup-time experiment was not run: there is no measured manual baseline, observed handling-time reduction or actual savings claim. Measured data and assumptions remain separate in `results/behavior/cost_to_serve_scenarios_v1.0.json` and `.csv`.
