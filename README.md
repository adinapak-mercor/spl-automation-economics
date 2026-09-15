# SPL Automation Economics

Internal scaffold for measuring whether automation makes Strategic Project Leads (SPLs) more productive and whether any operational gains translate into economic value.

This is a research design, not a finalized KPI. It is intended to give economists and engineers a shared map of:

- the causal question;
- every required variable and its source;
- the formulas and why they are constructed that way;
- what exists today versus what requires new instrumentation;
- the minimum viable study and the fuller long-run model.

## Research question

> Does randomized access to SPL automation reduce the human attention required to operate a pod and increase economic value supported per SPL without worsening quality or delivery?

## Formula stack at a glance

| Construct | Formula | Source variables | Interpretation |
|---|---|---|---|
| Surface usage | `A^s_{pt}=N^s_{pt}/D^s_{pt}` | Hex surface numerator and denominator | Within-surface Coil involvement; six separate metrics |
| SPL capacity | `F_{pt}=sum_i a_{ipt}` or `sum_i L_{ipt}/StandardHours_t` | Staffing allocation or time | Full-time-equivalent SPL input |
| Contribution output | `Y_{pt}=R_{pt}-C_{pt}` | Finance/project data | Revenue less non-SPL variable delivery cost |
| SPL leverage | `P_{pt}=Y_{pt}/F_{pt}` | Contribution output and SPL capacity | Contribution supported per SPL FTE |
| Human attention | `H_{pwt}=SPLMinutes_{pwt}/CompletedUnits_{pwt}` | Workflow/time records | Rework-inclusive SPL minutes per completed workflow |
| Primary causal effect | `ln(P_{pt})=alpha_p+lambda_t+tau Z_{pt}+delta'X_{pt}+epsilon_{pt}` | Randomized rollout plus outcome panel | Effect of being offered access |

The full input-to-formula dependency table is in [`docs/formula-map.md`](docs/formula-map.md).

## What the Hex snapshot changes

The [September 2026 saved snapshot](https://app.hex.tech/500e8e3f-f94b-4ca6-9ba1-d07bdc8e4dfb/hex/Coil-surface-activity-saved-snapshot-September-2026-034Ni63vTasQW1Fe7W7I7w/draft/logic?threadLayout=collapsed&projectView=app&view=app) reports six different activity measures:

| Surface | Unit | Latest saved share |
|---|---|---:|
| Snowflake | eligible native query record | 85.6% |
| Google Sheets | user/account × five-minute UTC window | 27.8% |
| Google Docs | user/account × five-minute UTC window | 5.1% |
| Slack | messages posted | 28.1% |
| Team Platform | actor × five-minute UTC window | 57.9% |
| Studio v1 | native account × five-minute UTC window | 10.0% |

These rates must not be pooled by adding their counts: queries, messages, and surface-specific windows do not share a unit or opportunity set. The exact source logic, filters, numerators, denominators, loaded periods, and snapshot checks are recorded in [`docs/hex-metric-specification.md`](docs/hex-metric-specification.md).

## Recommended primary estimate

The minimum viable economic outcome is pod contribution output per SPL FTE:

```math
Y_{pt}=R_{pt}-C_{pt},
\qquad
P_{pt}=\frac{Y_{pt}}{\mathrm{SPL\ FTE}_{pt}}
```

The primary estimand should be the effect of randomized rollout access, because it does not rely on constructing a false cross-surface automation percentage:

```math
\ln(P_{pt})
=
\alpha_p+\lambda_t+\tau Z_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

The headline result is:

```math
\mathrm{RolloutLift}=100\left(e^{\tau}-1\right)\%
```

Plain English:

> Being assigned access to the automation intervention causes an estimated **X% change in contribution supported per SPL**, subject to quality and delivery guardrails.

Estimate rollout effects on each Hex surface rate separately to show where behavior changed. A secondary IV estimate may translate rollout into an automation effect only after choosing a substantively valid scalar exposure. The “10pp automation effect” is valid for a 0-to-1 share such as workflow-time coverage, not for a standardized multi-surface usage index.

## Why this is only the MVP

The current Hex metrics are surface-specific activity proxies. They do not yet establish:

- which SPL workflow an event belongs to;
- whether that workflow should be automated;
- how much manual time the event represents;
- whether AI involvement actually displaced human labor.

The ideal cross-surface automation measure weights mutually exclusive eligible workflows by their pre-treatment manual time:

```math
A_{pt}
=
\frac{\sum_w V_{pwt}M_wS_{pwt}}
{\sum_w V_{pwt}M_w}
```

where `V` is workflow volume, `M` is baseline manual minutes, and `S` is the fraction of labor displaced by automation.

## Minimum viable study

Use a randomized or staggered rollout by pod/project and join:

- six versioned Hex surface metrics with raw numerator, denominator, unit, and coverage fields;
- stable SPL-to-pod mapping;
- SPL allocation or hours;
- pod revenue and variable delivery costs;
- existing quality and delivery outcomes.

This avoids blocking the first study on workflow-level time telemetry. Add workflow labeling and attention measurement only after establishing feasibility and signal.

## Repository map

- [`docs/formula-map.md`](docs/formula-map.md) — central metric dependency table, formula derivations, units, and estimands.
- [`docs/hex-metric-specification.md`](docs/hex-metric-specification.md) — exact Hex surface units, sources, numerator/denominator rules, and saved-snapshot checks.
- [`docs/variable-catalog.md`](docs/variable-catalog.md) — complete variable inventory, lineage, status, and proxy relationships.
- [`docs/methodology.md`](docs/methodology.md) — formulas, transformations, denominators, assumptions, and interpretations.
- [`docs/experiment-design.md`](docs/experiment-design.md) — batched rollout, estimands, spillovers, and robustness checks.
- [`docs/engineering-plan.md`](docs/engineering-plan.md) — grains, joins, validation tests, and staged implementation.
- [`docs/presentation-outline.md`](docs/presentation-outline.md) — economist/engineering-facing one-page presentation structure.
- [`docs/notion-equations.md`](docs/notion-equations.md) — optional copy-ready LaTeX blocks.
- [`data/variable_catalog.csv`](data/variable_catalog.csv) — machine-readable variable inventory for implementation planning.
- [`data/hex_snapshot_checks.csv`](data/hex_snapshot_checks.csv) — exact saved-snapshot reconciliation targets by surface.
- [`diagrams/causal-model.mmd`](diagrams/causal-model.mmd) — editable Mermaid source for the causal diagram.

## Source material

- [Economics SSOT](https://docs.google.com/document/d/16jbeq72m4u3CS1JMkH2qZyb7a8ApT9O0ByHrtbZEnUc/edit)
- [SPL JTBD workbook](https://docs.google.com/spreadsheets/d/1uIXvx8xJy8CgHKKigtqQ2rNHvxBYeXmNlYw7zTmKNO0/edit)
- [Coil surface activity saved snapshot · September 2026](https://app.hex.tech/500e8e3f-f94b-4ca6-9ba1-d07bdc8e4dfb/hex/Coil-surface-activity-saved-snapshot-September-2026-034Ni63vTasQW1Fe7W7I7w/draft/logic?threadLayout=collapsed&projectView=app&view=app)
- [Rex / Adina FDE sync](https://notes.granola.ai/t/ad9534c2-a48e-430d-9af0-f25d1a856894-008umkv4)

## Current recommendation

Start with the randomized rollout effect on SPL leverage, plus separate first stages for Snowflake, Sheets, Docs, Slack, Team Platform, and Studio. Do not report one combined Hex automation percentage. Treat workflow-time automation and human attention as the richer second phase, not a prerequisite for launch.
