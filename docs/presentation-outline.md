# Presentation scaffold: one system, two audiences

Recommended format: keep this repository as the source of truth and present a short Notion or Google Doc that links here. The repo preserves versioned formulas, lineage, and implementation details; the presentation should explain the system in one pass.

## The one-sentence proposal

> Measure the causal percentage change in quality-adjusted pod contribution supported per SPL FTE from randomized access to automation, then use workflow-level human attention to explain the mechanism.

## Suggested one-page flow

### 1. Start with the decision, not the dashboard

**Decision:** Should we invest in and scale SPL automation?

**Evidence needed:** Does access to the product increase economic leverage, through less human attention, without damaging quality?

### 2. Show the causal chain

```text
randomized access → realized automation → less SPL attention per unit
                                      ↘ more contribution per SPL
                         quality / delivery must not worsen
```

This separates five ideas that are easy to conflate:

- **access** is the experimental treatment;
- **usage** is adoption, not productivity;
- **attention saved** is the operational mechanism;
- **contribution per SPL** is the business outcome;
- **quality** is a constraint, not something hidden inside the productivity ratio.

### 3. State what can be measured now

| Layer | MVP measure | Status |
|---|---|---|
| Assignment | rollout cohort/date | Must be frozen at rollout |
| Usage | cleaned Hex automation/event share | Exists, definition under revision |
| Mechanism | SPL hours or sampled time per workflow | Partial/new |
| Economics | contribution output per SPL FTE | Requires pod mapping + finance + staffing join |
| Guardrails | QC, rework, delivery, SLA, expert outcomes | Existing systems; exact choices TBD |

The current Hex dashboard answers **how much observable activity used the tools**. It does not by itself answer **whether SPLs became more productive**.

### 4. Put the headline metric in the center

```math
P_{pt}=\frac{R_{pt}-C_{pt}}{\mathrm{SPL\ FTE}_{pt}}
```

`P` is pod contribution supported per full-time-equivalent SPL. The numerator and denominator use the same pod and period. SPL labor is not subtracted in `C`, because it is already the scarce input in the denominator.

Headline causal interpretation:

```math
\ln(P_{pt})=\alpha_p+\lambda_t+\beta\widehat A_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

```math
\text{10pp automation lift}=100\left(e^{0.10\beta}-1\right)\%
```

In words: a 10-percentage-point increase in automation induced by rollout causes an estimated X% change in contribution supported per SPL.

### 5. Explain what every operator is doing

| Element | Why it is there |
|---|---|
| `R - C` | Measures value after non-SPL variable delivery cost, not just top-line volume |
| `/ SPL FTE` | Converts pod output into leverage of the scarce SPL input |
| `ln(P)` | Makes differently sized pods comparable in proportional-change terms |
| `alpha_p` | Removes persistent differences between pods |
| `lambda_t` | Removes common week shocks and seasonality |
| `X` | Holds fixed prespecified time-varying confounders, not post-treatment mechanisms |
| `A-hat` | Uses only variation in automation caused by rollout, reducing selection bias |

### 6. Show the richer mechanism separately

```math
A_{pt}=\frac{\sum_w V_{pwt}M_wS_{pwt}}{\sum_w V_{pwt}M_w}
```

- `V`: number of workflow units;
- `M`: pre-treatment manual minutes per unit;
- `S`: share of those baseline minutes displaced.

The denominator is all baseline manual minutes for eligible work. The numerator is the subset displaced. It therefore measures the share of eligible human effort automated rather than a raw count of clicks or calls.

This is the ideal second-phase measure. It should not block the rollout study.

### 7. End with the proposed decision rule

Scale when randomized access produces:

1. a credible positive effect on contribution per SPL FTE or a clear reduction in human attention;
2. no material deterioration in prespecified quality and delivery outcomes;
3. sufficient adoption and first-stage strength to show the tool changed behavior;
4. a value estimate that exceeds implementation and operating cost.

## Talk track by audience

### For economists

- The primary causal estimate should be intention-to-treat from the rollout.
- IV/LATE can translate assignment into automation exposure if the first stage is strong.
- Workflow attention is a mechanism; realized staffing and volume can be post-treatment and should not automatically be controls.
- Prespecify outcome hierarchy, transformations, quality non-inferiority thresholds, and multiple-testing policy.

### For engineers

- Freeze immutable assignment and effective-dated person/pod mappings.
- Publish raw numerator/denominator components, exclusions, grains, and definition versions.
- Treat event counts as a proxy until workflows and manual-time weights exist.
- Make every panel row traceable back to telemetry, staffing, finance, and quality sources.

## The ask for the next sync

Ask the group to agree on four items:

1. the randomized unit and rollout waves;
2. the canonical SPL-to-pod/project mapping;
3. the finance numerator and SPL labor denominator;
4. one primary quality guardrail and its acceptable threshold.

Everything else can be staged after the experiment begins, provided raw source data and assignment history are retained.
