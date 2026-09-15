# Presentation scaffold: formula-first specification

Use the GitHub README as the entry point and [`formula-map.md`](formula-map.md) as the presentation. The most useful shared artifact for economists and engineers is a compact formula sheet with source lineage—not a high-level process diagram.

## Panel 1 — What is actually observed today?

```math
A^s_{pt}=\frac{N^s_{pt}}{D^s_{pt}}
```

| Surface `s` | Numerator `N_s` | Denominator `D_s` | Unit |
|---|---|---|---|
| Snowflake | MCP-tagged eligible queries | eligible native queries | query |
| Sheets | qualifying Coil windows | union of Coil/native spreadsheet windows | user/account × 5 min |
| Docs | qualifying Coil windows | union of Coil/native document windows | user/account × 5 min |
| Slack | qualifying Coil sends | Coil + native/non-Coil messages | message |
| Team Platform | automated-origin JobEvent windows | all nondeleted JobEvent actor-windows | actor × 5 min |
| Studio | Coil-OAuth native-auth windows | all native-auth account-windows | account × 5 min |

**Key statement:** Hex measures six within-surface activity shares. It does not measure one company-wide percent of work automated.

## Panel 2 — Why can these not be added?

```math
[D^{SF}]=queries,\quad [D^{Slack}]=messages,\quad
[D^{Sheets}]=[D^{Docs}]=[D^{TP}]=[D^{Studio}]=surface\text{-}specific\ windows
```

Adding counts across these denominators would weight surfaces by arbitrary emission frequency. Even the window metrics cover different applications and opportunity sets.

If one compliance summary is needed:

```math
U_{pt}=\frac{1}{|\mathcal S^0_p|}\sum_{s\in\mathcal S^0_p}
\frac{A^s_{pt}-\mu^s_0}{\sigma^s_0}
```

- `mu^s_0`, `sigma^s_0`: pre-treatment mean and standard deviation for surface `s`.
- `S^0_p`: surfaces declared relevant for the pod before treatment.
- `U`: average movement in baseline standard deviations.

Call `U` a **multi-surface adoption index**, never “automation percentage.”

## Panel 3 — What is the economic KPI?

```math
Y_{pt}=R_{pt}-C_{pt}
```

```math
F_{pt}=\sum_i a_{ipt}
\qquad\text{or}\qquad
F_{pt}=\frac{\sum_iL_{ipt}}{StandardHours_t}
```

```math
\boxed{P_{pt}=\frac{Y_{pt}}{F_{pt}}}
```

| Variable | Meaning | Source |
|---|---|---|
| `R_pt` | recognized revenue for pod `p`, period `t` | Finance/project data |
| `C_pt` | non-SPL variable delivery cost on the same boundary | Finance/project data |
| `a_ipt` | SPL `i`'s effective allocation share to pod `p` | staffing/pod mapping |
| `L_ipt` | SPL hours attributed to pod `p` | credible time records |
| `F_pt` | SPL full-time-equivalent capacity | derived |
| `P_pt` | contribution dollars supported per SPL FTE | derived |

Why the denominator works: an SPL split across pods contributes fractional allocation to each, so one person is not counted as multiple full people.

Why SPL cost is excluded from `C`: SPL labor is already the productivity input `F`. If the finance numerator subtracts SPL labor, the same input appears in both numerator and denominator.

## Panel 4 — What is the primary causal formula?

```math
\boxed{
\ln(P_{pt})
=
\alpha_p+\lambda_t+\tau Z_{pt}+\delta'X_{pt}+\varepsilon_{pt}}
```

```math
\boxed{RolloutLift=100\left(e^\tau-1\right)\%}
```

| Term | Meaning | Why included |
|---|---|---|
| `Z_pt` | randomized rollout assignment | creates exogenous treatment variation |
| `alpha_p` | pod fixed effect | removes persistent pod differences |
| `lambda_t` | period fixed effect | removes shared time shocks and seasonality |
| `X_pt` | prespecified pre-treatment/time-varying confounders | improves precision and adjusts valid external changes |
| `tau` | log-point effect of offered access | primary intent-to-treat estimate |

Why log `P`: proportional effects are comparable across pod sizes and exact percent lift is `100(e^tau-1)`. Do not log non-positive values; prespecify a levels/two-part alternative.

Why assignment, not usage, is primary: high-performing pods can choose to use more. Random assignment is not selected by performance and does not require a false combined Hex rate.

## Panel 5 — How do we prove the treatment changed behavior?

Estimate one first stage per surface:

```math
\boxed{
A^s_{pt}
=
\alpha^s_p+\lambda^s_t+\pi_sZ_{pt}+\theta_s'X_{pt}+\nu^s_{pt}}
```

`pi_s` is the rollout-induced percentage-point change on surface `s`. Report all prespecified `pi_s` values or name one primary surface before seeing outcomes.

The summary-index first stage is:

```math
U_{pt}=\alpha_p+\lambda_t+\pi_UZ_{pt}+\theta'X_{pt}+\nu_{pt}
```

`pi_U` is measured in baseline standard deviations, not percentage points.

## Panel 6 — When is a “10pp automation effect” valid?

Only after creating a common 0-to-1 automation share, ideally using workflow time:

```math
EligibleMinutes_{pt}=\sum_wV_{pwt}M_w
```

```math
DisplacedMinutes_{pt}=\sum_wV_{pwt}M_wS_{pwt}
```

```math
\boxed{
A^{time}_{pt}
=
\frac{\sum_wV_{pwt}M_wS_{pwt}}
{\sum_wV_{pwt}M_w}}
```

- `V_pwt`: completed occurrences of workflow `w`.
- `M_w`: frozen pre-treatment manual minutes per occurrence.
- `S_pwt`: fraction of baseline minutes displaced, from zero to one.

Every summand is measured in minutes, so the denominator is coherent. This is the first cross-surface measure defensibly described as percent of eligible SPL work automated.

For rollout-predicted `A^time`:

```math
\ln(P_{pt})
=
\alpha_p+\lambda_t+\beta\widehat A^{time}_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

```math
\boxed{Lift_{10pp}=100\left(e^{0.10\beta}-1\right)\%}
```

Do not apply this expression to `U`, since `U` is not a 0-to-1 percentage.

## Panel 7 — What is the operational mechanism?

```math
\boxed{
H_{pwt}=\frac{SPLMinutes_{pwt}}{CompletedWorkflowUnits_{pwt}}}
```

```math
\ln(H_{pwt})
=
\alpha_{pw}+\lambda_t+\tau_HZ_{pt}+\delta'X_{pwt}+\varepsilon_{pwt}
```

Successful labor-saving automation implies `tau_H < 0`. Rework, exception handling, and quality-review minutes must remain in the numerator so effort is not merely shifted downstream.

## Panel 8 — What assumptions are embedded in the KPI?

Because:

```math
\ln(P_{pt})=\ln(Y_{pt})-\ln(F_{pt})
```

the leverage ratio implicitly fixes the output elasticity of SPL labor at one. Show this robustness model:

```math
\ln(Y_{pt})
=
\alpha_p+\lambda_t+\tau Z_{pt}
+\gamma\ln(F_{pt})+\delta'X_{pt}+\varepsilon_{pt}
```

If `F` changes because of treatment, the ratio is a total operational-leverage outcome, while the production model is output conditional on realized labor. These are different estimands.

## Panel 9 — What prevents false productivity?

For each quality outcome `j`:

```math
g_j\!\left(E[Q^j_{pt}]\right)
=
\alpha^j_p+\lambda^j_t+\tau^j_QZ_{pt}+\delta_j'X_{pt}
```

Report QC, rework, one-shot acceptance, delivery yield/SLA, and expert/client outcomes separately. Preserve rate numerators and denominators; do not hide them in an unexplained composite.

## The four decisions needed in the next sync

1. Randomization unit, rollout waves, and intervention components.
2. Effective-dated person → pod → project mapping and SPL allocation source.
3. Finance numerator: revenue recognition and exactly which variable costs enter `C`.
4. Primary economic outcome, primary Hex first stage, and quality non-inferiority guardrail.
