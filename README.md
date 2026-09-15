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

## The two open questions, answered

Both questions currently blocking the study have answers that fit in a paragraph each. The
supporting reasoning is in the linked documents.

### Are the existing metrics of SPL work good enough?

They are good enough to start and not good enough to finish, and the reason is role rather
than quality. Expert NPS is a non-inferiority guardrail, not an effect metric, and it needs
a minimum-detectable-effect calculation before a null can be read as evidence of no harm.
The surface activity shares are first-stage compliance measures that prove the rollout
changed behavior; they are never outcomes. The weekly time-use survey sits on the critical
path because it is the only current source for baseline manual minutes, so it needs a short
validation pass against an independent time measure, with a fallback to rankings rather
than levels if it does not hold up. The genuine gap in the existing set is not noise in any
one metric: it is that nothing measures SPL output volume, which is the quantity most likely
to move inside the study window. Full verdicts in
[`docs/measurement-decisions.md`](docs/measurement-decisions.md).

### If new metrics are needed, can they be built after the fact?

Mostly yes. Workflow labeling is a classifier over retained events and can be built months
after launch at no cost to the study. Baseline manual minutes cannot, because a weight
measured after treatment is endogenous to the treatment it is meant to weight — so the
workflow proposal should be split in two, since only half of it has a deadline. The
reconstruction argument does need one correction: "housed in a store that is not deleted"
also has to mean "not overwritten," and the current pod mapping fails that test, which is
why the September snapshot applies 2026-09-10 org labels to historical activity. Sources
with rolling retention and mappings that update in place need capture jobs now, and the
cost of skipping them is silent — nothing breaks, the period simply stops existing.
Bucket-by-bucket analysis in [`docs/reconstructability.md`](docs/reconstructability.md).

### How should the batched rollout work?

Simple, as expected, with three decisions worth making deliberately. The randomization unit
follows from the SPL-per-project distribution: individual SPLs where projects have one lead,
project clusters where they have several. Access should be gated on identity rather than a
shared password — not for security, but because a shared password cannot distinguish an SPL
who declined to adopt from one who borrowed a colleague's access. And with few units,
cluster-robust standard errors over-reject, so randomization inference should be the primary
test. Mechanics and pre-launch checklist in
[`docs/rollout-mechanics.md`](docs/rollout-mechanics.md).

### One caveat on the primary outcome

Contribution per SPL FTE can only respond to automation if pod revenue can respond to SPL
effort inside the study window. Where revenue is fixed by contract, milestone, or priced off
delivered expert hours, it cannot, and a null would describe pricing rather than
productivity. Classify eligible pods by pricing model early; if most cannot move, lead with
an effort-responsive operational outcome and treat the economic one as confirmatory.

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

## Collated version for Google Docs

The whole design is collated into one document at
[`docs/collated-document.md`](docs/collated-document.md), deduplicated and renumbered so it
reads as a single paper rather than a folder of notes. The presentation outline and the
copy-ready equation list are folded into it and are not maintained separately.

To get it into Google Docs with tables and equations intact:

```
python3 tools/build_docs_html.py docs/collated-document.md dist/spl-automation-economics.html
```

1. Open `dist/spl-automation-economics.html` in a browser.
2. Select all, copy, and paste into an empty Google Doc. Pasting HTML preserves headings,
   bold, monospace and real tables; pasting Markdown does not.
3. Run **Extensions → Auto-LaTeX Equations → Render Equations**. All 47 equations are
   emitted as literal double-dollar-delimited LaTeX for the add-on to pick up, and the
   build asserts that no unpaired delimiter appears anywhere in the prose.

The build joins each equation onto a single line, because the add-on matches delimiters
within one paragraph, and converts spelled-out Greek in inline symbol references to real
Greek characters so `tau_H` reads as a symbol rather than as a word.

## Repository map

- [`docs/formula-map.md`](docs/formula-map.md) — central metric dependency table, formula derivations, units, and estimands.
- [`docs/hex-metric-specification.md`](docs/hex-metric-specification.md) — exact Hex surface units, sources, numerator/denominator rules, and saved-snapshot checks.
- [`docs/variable-catalog.md`](docs/variable-catalog.md) — complete variable inventory, lineage, status, and proxy relationships.
- [`docs/methodology.md`](docs/methodology.md) — formulas, transformations, denominators, assumptions, and interpretations.
- [`docs/experiment-design.md`](docs/experiment-design.md) — batched rollout, estimands, spillovers, and robustness checks.
- [`docs/measurement-decisions.md`](docs/measurement-decisions.md) — per-metric verdicts on whether existing SPL measures suffice, and what role each may play.
- [`docs/reconstructability.md`](docs/reconstructability.md) — what can be built after the fact, what must be captured now, and what blocks launch.
- [`docs/rollout-mechanics.md`](docs/rollout-mechanics.md) — randomization unit, access gating, waves, few-cluster inference, and power.
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

Start with the randomized rollout effect, plus separate first stages for Snowflake, Sheets,
Docs, Slack, Team Platform, and Studio. Do not report one combined Hex automation
percentage. Treat workflow-time automation and human attention as the richer second phase,
not a prerequisite for launch.

Choose the primary outcome by computing its minimum detectable effect from pre-period
variance before the analysis plan is frozen, and check whether pod revenue can respond to
SPL effort within the window. Where it cannot, lead with an effort-responsive operational
outcome and report contribution per SPL FTE as confirmatory.
