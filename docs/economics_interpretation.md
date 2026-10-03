# Economics: measured inputs versus illustrative scenarios

This clarification accompanies the unchanged [frozen cost-to-serve document](cost_to_serve.md) and [scenario values](../results/behavior/cost_to_serve_scenarios_v1.0.json). It adds no experiment, operational fact or new financial result.

## Measured

The fixed 15-case, gold-policy-conditioned FM component experiment measured:

- Mean FM variable cost: **US$0.00064629 per component ticket** for extraction plus generation.
- Sequential HTTP latency: median **4.613 seconds**, p95 **6.093 seconds**.

These are historical component measurements, not current price quotations, full service costs, end-to-end handling times or service-level guarantees. They exclude human policy selection and review. Source: [final human/measurement summary](../results/fm/final_human_summary.json).

## Illustrative assumptions

| Scenario | Local/runtime allocation | Review minutes | Hourly labor cost | Escalation probability | Extra cost per escalation |
|---|---:|---:|---:|---:|---:|
| Low review | $0.002 | 1 | $18 | 5% | $2 |
| Moderate review | $0.010 | 3 | $24 | 15% | $6 |
| High review | $0.030 | 6 | $30 | 30% | $12 |

Hourly wages, review minutes, escalation probabilities, escalation costs and runtime allocations are planning assumptions, not observed operations. Human generation FAIL frequency was not used as escalation probability.

`cost per ticket = FM variable cost + local/runtime allocation + review minutes × hourly labor cost / 60 + escalation probability × incremental escalation cost`

The unchanged scenario outputs are **$0.40264629**, **$2.11064629** and **$6.63064629** per ticket respectively. Review applies to every ticket; incremental escalation cost covers work beyond ordinary review. Human labor dominates the model charge in these chosen scenarios. No assertion about real staffing costs follows from that arithmetic.

**Without a measured manual-handling baseline, this analysis estimates cost-to-serve scenarios, not savings, ROI, or break-even.**

No productivity pilot, manual handling-time baseline or measured reduction in reviewer effort exists. Candidate selection could add friction. The proposed future pilot is described in [evaluation](evaluation.md#not-yet-evaluated-end-to-end); it has not been run.
