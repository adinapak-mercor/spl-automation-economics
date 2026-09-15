# Methodology and formula derivations

## Indexing and notation

- `p`: pod
- `t`: week or other consistent time period
- `w`: mutually exclusive workflow
- `i`: SPL
- `Z`: assigned rollout
- `A`: automation exposure
- `H`: human-attention mechanism
- `P`: SPL economic leverage
- `Q`: quality or delivery guardrail

## 1. Automation exposure

### Minimum viable Hex proxy

```math
A^{Hex}_{pt}
=
\frac{\mathrm{AutomatedEvents}_{pt}}
{\mathrm{AutomatedEvents}_{pt}+\mathrm{ManualEvents}_{pt}}
```

This is inexpensive because the underlying events already exist. It is a proxy, not the target construct: different surfaces emit different numbers of events for comparable user goals, and an automated event does not necessarily imply meaningful labor displacement.

Use this measure only after the current backfill and surface-weighting work is complete. Report surface-specific rates alongside any overall rate.

### Ideal workflow-weighted measure

```math
A_{pt}
=
\frac{\sum_{w\in\mathcal{E}}V_{pwt}M_wS_{pwt}}
{\sum_{w\in\mathcal{E}}V_{pwt}M_w}
```

Definitions:

- `E` is the set of workflows judged automation-eligible.
- `V_pwt` is the number of workflow occurrences.
- `M_w` is pre-treatment manual minutes per occurrence.
- `S_pwt` is the fraction of baseline manual labor displaced, from 0 to 1.

### Why the denominator adds up

The denominator is the estimated counterfactual manual labor required for all eligible workflow occurrences:

```math
\mathrm{EligibleManualMinutes}_{pt}
=
\sum_{w\in\mathcal{E}}V_{pwt}M_w
```

The numerator is the portion of those same baseline minutes displaced by automation:

```math
\mathrm{DisplacedManualMinutes}_{pt}
=
\sum_{w\in\mathcal{E}}V_{pwt}M_wS_{pwt}
```

Therefore `A_pt` is bounded between 0 and 1 when `0 <= S_pwt <= 1`.

The construction is valid only when:

1. Workflow occurrences are mutually exclusive and not double-counted.
2. Numerator and denominator contain the same eligible workflows and period.
3. Manual-time weights are fixed from a pre-treatment baseline.
4. Eligibility is defined before observing treatment outcomes.
5. `S` represents labor displaced, not simply AI involvement.

## 2. SPL labor input

### Allocation-share construction

```math
\mathrm{SPL\ FTE}_{pt}=\sum_i a_{ipt}
```

where `a_ipt` is SPL `i`'s allocation share to pod `p` during period `t`.

For a fully allocated SPL:

```math
\sum_p a_{ipt}=1
```

This prevents an SPL who supports three pods from being counted as three full people.

### Hours construction

```math
\mathrm{SPL\ FTE}_{pt}
=
\frac{\sum_i L_{ipt}}
{\mathrm{StandardHours}_t}
```

Use allocation shares if reliable time records do not exist. Use hours for workflow-level attention analysis when they are credible.

## 3. Economic output

```math
GP_{pt}=R_{pt}-C_{pt}
```

- `R_pt` is revenue recognized for the pod and period.
- `C_pt` is non-SPL variable delivery cost for the same pod and period.

Using output before SPL labor cost allows SPL labor to remain the explicit productivity denominator. If finance's official gross-profit definition already subtracts SPL labor, either add that labor cost back for this model or use a separately named contribution measure to avoid double-counting SPL labor.

All revenue and costs must use the same:

- pod/project assignment;
- accounting period;
- recognition convention;
- currency;
- cost boundary.

## 4. Primary outcome: SPL leverage

```math
P_{pt}
=
\frac{GP_{pt}}
{\mathrm{SPL\ FTE}_{pt}}
```

This measures economic value supported by one full-time-equivalent SPL. It captures both potential channels:

- more output with the same SPL resources;
- the same output with fewer SPL resources.

Fallbacks, in descending order of preference:

```math
P^{Revenue}_{pt}=\frac{R_{pt}}{\mathrm{SPL\ FTE}_{pt}}
```

```math
P^{Projects}_{pt}=\frac{\mathrm{ComparableActiveProjects}_{pt}}{\mathrm{SPL\ FTE}_{pt}}
```

Revenue per SPL is easier to construct but ignores delivery cost. Projects per SPL requires a defensible project-complexity adjustment.

## 5. Why use a logarithm

The main outcome model is:

```math
\ln(P_{pt})
=
\alpha_p+\lambda_t+\beta A_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

The logarithm is useful because:

1. `P` is typically right-skewed across pods.
2. Proportional changes are more comparable than dollar changes across differently sized pods.
3. Coefficients can be interpreted in percentage terms.

Because `A` is a 0-to-1 share and is not logged, `beta` is a **semi-elasticity**, not an elasticity.

For a 10-percentage-point increase in automation:

```math
\mathrm{Lift}_{10pp}
=
100\left(e^{0.10\beta}-1\right)\%
```

For small effects, the approximation is:

```math
\mathrm{Lift}_{10pp}\approx 10\beta\%
```

Do not use `ln(P)` when `P <= 0`. Prespecify a levels model or a suitable alternative transformation rather than silently dropping non-positive pods.

## 6. Human-attention mechanism

```math
H_{pwt}
=
\frac{\mathrm{SPLMinutes}_{pwt}}
{\mathrm{CompletedWorkflowUnits}_{pwt}}
```

This measures the scarce input automation is intended to reduce. Include rework minutes in the numerator.

```math
\ln(H_{pwt})
=
\alpha_{pw}+\lambda_t+\beta_HA_{pwt}+\delta'X_{pwt}+\varepsilon_{pwt}
```

Successful labor-saving automation implies `beta_H < 0`.

## 7. Structural production model

```math
\ln(Y_{pt})
=
\alpha_p+\lambda_t+\beta_YA_{pt}
+\gamma\ln(L_{pt})+\delta'X_{pt}+\varepsilon_{pt}
```

This estimates whether automation raises output while holding SPL labor fixed. It is a useful secondary specification but not identical to the SPL-leverage estimand.

Important distinction:

- `GP / SPL FTE` measures the combined business effect of more output and/or less labor.
- The production function estimates output augmentation conditional on a specified labor input.
- Controlling for realized post-treatment labor can block part of the labor-saving effect. Use it only when that conditional estimand is intentional.

## 8. Quality and delivery outcomes

For each guardrail:

```math
g\!\left(E[Q_{pt}]\right)
=
\alpha_p+\lambda_t+\beta_QA_{pt}+\delta'X_{pt}
```

Choose link function `g` by outcome:

| Outcome | Suggested form | Desired direction |
|---|---|---|
| One-shot acceptance | Binomial/logit or linear probability | Non-negative |
| Delivery yield | Binomial/logit or linear probability | Non-negative |
| Rework rate | Binomial/logit | Non-positive |
| Failures/escalations | Poisson/negative binomial where appropriate | Non-positive |
| QC score | Levels model | Non-negative |
| Expert NPS | Levels model with respondent/composition checks | Non-negative |

Do not average unlike guardrails into an unexplained composite score.

## 9. Controls and fixed effects

- `alpha_p`: pod fixed effects remove time-invariant differences such as persistent client mix or baseline operating style.
- `lambda_t`: week fixed effects absorb firm-wide changes, seasonality and shared product releases.
- `X_pt`: prespecified time-varying factors such as maturity, pricing or externally driven demand.

Avoid controlling for variables caused by treatment when estimating the total treatment effect. SPL hours, staffing changes, workflow volume and demand served may be mechanisms rather than confounders.

## 10. Main reported metric

> **Automation-driven SPL productivity lift:** the causal percentage change in gross profit supported per SPL FTE resulting from a 10-percentage-point increase in automation coverage, with quality and delivery reported as separate guardrails.
