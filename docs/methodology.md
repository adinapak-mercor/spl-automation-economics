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

## 1. Automation and adoption exposure

### Hex provides a vector, not one automation rate

For each surface `s`:

```math
A^s_{pt}=\frac{N^s_{pt}}{D^s_{pt}}
```

The September 2026 Hex snapshot defines six different units:

| Surface | `N_s` | `D_s` | Unit |
|---|---|---|---|
| Snowflake | eligible query with `mcp` source tag | eligible native query | query record |
| Sheets | window with qualifying Coil Sheets write | union of Coil and native spreadsheet-edit windows | user/account × five-minute UTC window |
| Docs | window with qualifying Coil batch update | union of Coil and native document-edit windows | user/account × five-minute UTC window |
| Slack | qualifying deduplicated Coil sends | Coil sends plus compatible native/non-Coil messages | posted message |
| Team Platform | JobEvent window with automated/agent/external queue marker | nondeleted JobEvent actor-windows | actor × five-minute UTC window |
| Studio | native-auth window with Coil OAuth client ID | any native-auth account-window | account × five-minute UTC window |

The numerators are subsets of their own denominators, so every `A_s` is a valid within-surface share. The denominators cannot be summed across surfaces because their dimensions and source populations differ. Exact definitions are in [`hex-metric-specification.md`](hex-metric-specification.md).

Use `A_s` as separate adoption/compliance outcomes. If one summary is necessary, use a pre-treatment standardized index:

```math
\widetilde A^s_{pt}=\frac{A^s_{pt}-\mu^s_0}{\sigma^s_0}
```

```math
U_{pt}=\frac{1}{|\mathcal S^0_p|}
\sum_{s\in\mathcal S^0_p}\widetilde A^s_{pt}
```

`U` is measured in baseline standard deviations and should be labeled “multi-surface adoption index.” It is not a percentage of work automated. A 10-percentage-point effect is not defined for `U`.

### Ideal workflow-time measure

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

This workflow-time measure is the first cross-surface measure for which “share of eligible SPL work automated” is dimensionally defensible. Both numerator and denominator are minutes.

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
Y_{pt}=R_{pt}-C_{pt}
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
\frac{Y_{pt}}
{\mathrm{SPL\ FTE}_{pt}}
```

This measures economic value supported by one full-time-equivalent SPL. It captures both potential channels:

- more output with the same SPL resources;
- the same output with fewer SPL resources.

It is a descriptive KPI with an embedded production assumption:

```math
\ln(P_{pt})=\ln(Y_{pt})-\ln(\mathrm{SPL\ FTE}_{pt})
```

The log ratio implicitly fixes the elasticity of output with respect to SPL labor at one. Report a robustness model that estimates that elasticity:

```math
\ln(Y_{pt})
=
\alpha_p+\lambda_t+\tau Z_{pt}
+\gamma\ln(\mathrm{SPL\ FTE}_{pt})+\delta'X_{pt}+\varepsilon_{pt}
```

If rollout changes staffing, realized SPL FTE is a post-treatment mechanism. The ratio estimates total operational leverage; the production model estimates conditional output. They should be labeled separately rather than treated as interchangeable.

Fallbacks, in descending order of preference:

```math
P^{Revenue}_{pt}=\frac{R_{pt}}{\mathrm{SPL\ FTE}_{pt}}
```

```math
P^{Projects}_{pt}=\frac{\mathrm{ComparableActiveProjects}_{pt}}{\mathrm{SPL\ FTE}_{pt}}
```

Revenue per SPL is easier to construct but ignores delivery cost. Projects per SPL requires a defensible project-complexity adjustment.

## 5. Why use a logarithm

For a credible 0-to-1 automation share, the secondary automation model is:

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

The primary randomized estimate does not require an automation percentage:

```math
\ln(P_{pt})
=
\alpha_p+\lambda_t+\tau Z_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

```math
\mathrm{RolloutLift}=100\left(e^\tau-1\right)\%
```

This is preferable with the current Hex data because `Z` has a common definition while the six `A_s` measures do not have a common unit.

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
\alpha_{pw}+\lambda_t+\tau_HZ_{pt}+\delta'X_{pwt}+\varepsilon_{pwt}
```

Successful labor-saving rollout implies `tau_H < 0`. A rollout-instrumented workflow-time automation specification is a secondary mechanism estimate.

## 7. Structural production model

```math
\ln(Y_{pt})
=
\alpha_p+\lambda_t+\beta_YA_{pt}
+\gamma\ln(L_{pt})+\delta'X_{pt}+\varepsilon_{pt}
```

This estimates whether automation raises output while holding SPL labor fixed. It is a useful secondary specification but not identical to the SPL-leverage estimand.

Important distinction:

- `Y / SPL FTE` measures the combined business effect of more output and/or less labor.
- The production function estimates output augmentation conditional on a specified labor input.
- Controlling for realized post-treatment labor can block part of the labor-saving effect. Use it only when that conditional estimand is intentional.

## 8. Quality and delivery outcomes

For each guardrail:

```math
g\!\left(E[Q_{pt}]\right)
=
\alpha_p+\lambda_t+\tau_QZ_{pt}+\delta'X_{pt}
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

## 10. Main reported metrics

Primary:

> **Rollout-driven SPL productivity lift:** the causal percentage change in contribution supported per SPL FTE caused by assigned access, with quality and delivery reported separately.

Supporting:

- the rollout-induced change in each of the six Hex surface rates;
- the rollout-induced change in a clearly labeled standardized adoption index;
- the change in rework-inclusive SPL minutes per completed workflow;
- a 10-percentage-point automation effect only after a credible 0-to-1 workflow-time or prespecified surface share exists.
