# Formula and variable dependency map

This is the central specification. It shows every measured input, every derived metric, and where each metric enters the causal analysis.

## 1. The three distinct questions

| Question | Metric family | What the answer means |
|---|---|---|
| Did access change behavior? | rollout `Z`, surface rates `A_s`, usage index `U` | Product adoption/compliance |
| Did automation reduce scarce input? | attention per completed unit `H` | Operational productivity mechanism |
| Did the business support more value per SPL? | contribution `Y`, SPL capacity `F`, leverage `P` | Economic productivity |

These are linked hypotheses, not interchangeable definitions of productivity.

## 2. Formula stack

| Level | Output | Function | Inputs | Unit | Used for |
|---:|---|---|---|---|---|
| 0 | surface numerator `N_s` | source-specific classification and deduplication | raw event records | query, message, or five-minute window | input to `A_s` |
| 0 | surface denominator `D_s` | source-specific eligible opportunity rule | native + Coil records | same unit as `N_s` within surface | input to `A_s` |
| 1 | surface share `A_s` | `N_s / D_s` | `N_s`, `D_s` | within-surface proportion | first-stage outcome |
| 1 | active-user breadth `B_s` | `AU_s / People` | qualifying active users, roster | employee proportion | adoption breadth |
| 1 | data coverage `K_s` | loaded days / selected days | load-status calendar | proportion | validity check |
| 2 | adoption index `U` | mean pre-period-standardized `A_s` | vector of surface shares | baseline standard deviations | optional compliance summary |
| 2 | SPL capacity `F` | sum allocation shares or hours / standard hours | effective-dated staffing | FTE | economic denominator |
| 2 | contribution output `Y` | recognized revenue minus non-SPL variable delivery cost | finance records | dollars | economic numerator |
| 3 | SPL leverage `P` | `Y / F` | contribution output, SPL FTE | dollars per SPL FTE | descriptive economic KPI |
| 3 | human attention `H` | SPL minutes / completed workflow units | time + workflow completion | minutes per unit | mechanism outcome |
| 4 | rollout effect `tau` | coefficient on randomized access in `ln(P)` | `P`, `Z`, fixed effects | log points | primary causal estimate |
| 4 | first-stage `pi_s` | coefficient on `Z` in each `A_s` | `A_s`, `Z` | surface-share points | confirms changed behavior |
| 4 | automation effect `beta` | coefficient on rollout-predicted credible automation | `P`, `A-hat` | semi-elasticity | secondary IV estimate |

## 3. Measured source variables

### Assignment and identity

```math
Z_{pt}\in\{0,1\}
```

- `Z_pt`: pod/project `p` is assigned access by period `t`.
- `pod_id`, `project_id`: canonical stable identities.
- `person_id`: stable employee identity.
- `a_ipt`: allocation share of SPL `i` to pod `p` in period `t`.

Assignment comes from the rollout table. Identities and allocation intervals come from org/project/staffing mappings. Events are attributed only when:

```math
start_{ip}\leq eventTime_i<end_{ip}
```

### Surface events

For each surface `s`, preserve:

```math
(unitId_s,\ personId,\ accountId,\ eventTime,\ sourceMarker,\ success,
\ eligibility,\ botFlag,\ definitionVersion)
```

The exact `unitId`, eligibility, numerator, and denominator differ by surface; see [Hex surface metrics](hex-metric-specification.md).

### Labor and finance

- `L_ipt`: SPL hours attributed to pod `p`.
- `R_pt`: recognized revenue.
- `C_pt`: non-SPL variable delivery costs.
- `c^SPL_t`: fully loaded SPL cost per FTE-period, if a dollar net-value measure is required.

### Workflow and quality

- `V_pwt`: completed occurrences of workflow `w`.
- `M_w`: pre-treatment manual minutes per occurrence.
- `S_pwt`: fraction of baseline minutes displaced by automation.
- `Q^j_pt`: quality guardrail `j`, retaining numerator and denominator when it is a rate.

## 4. Derived adoption metrics

### Surface shares

```math
A^s_{pt}=\frac{N^s_{pt}}{D^s_{pt}}
```

Why the denominator is valid: within one surface, `D_s` is the complete defined opportunity set and `N_s` is a subset of that same set. Therefore `0 <= N_s <= D_s` and `0 <= A_s <= 1`.

Why surface denominators do not add: the dimensions differ.

```math
[D^{SF}]=queries,\quad[D^{Slack}]=messages,\quad
[D^{Docs}]=[D^{Sheets}]=[D^{TP}]=[D^{Studio}]=five\text{-}minute\ windows
```

Even the window measures describe different populations and source systems. A raw sum would give more influence to surfaces that emit more units, not surfaces that consume more SPL labor.

### Standardized adoption index

```math
\widetilde A^s_{pt}=\frac{A^s_{pt}-\mu^s_0}{\sigma^s_0}
```

```math
U_{pt}=\frac{1}{|\mathcal S^0_p|}
\sum_{s\in\mathcal S^0_p}\widetilde A^s_{pt}
```

- `mu^s_0`, `sigma^s_0`: surface mean and standard deviation from the pre-treatment reference period.
- `S^0_p`: surfaces designated as relevant for pod `p` before rollout.

Why standardize: a one-point change in Snowflake's query share is not commensurate with a one-point change in Docs windows. Standardization expresses each movement in its own baseline standard-deviation units before averaging.

What `U` is not: it is not percent of tasks, time, or labor automated. It should be used only to summarize compliance or improve power across several adoption outcomes.

## 5. Derived labor and economic metrics

### SPL FTE

Allocation form:

```math
F_{pt}=\sum_i a_{ipt},\qquad 0\leq a_{ipt}\leq1
```

Hours form:

```math
F_{pt}=\frac{\sum_iL_{ipt}}{StandardHours_t}
```

The denominator prevents a person supporting multiple pods from being counted as one full SPL in every pod. Allocation shares for a fully allocated person should satisfy `sum_p a_ipt = 1` over overlapping intervals.

### Contribution output

```math
Y_{pt}=R_{pt}-C_{pt}
```

`C_pt` excludes SPL labor in this definition because SPL labor appears explicitly as the productivity input. If the Finance extract already subtracts SPL labor, add it back or rename/redefine `Y` to avoid subtracting the same input in both numerator and denominator.

### Descriptive SPL leverage

```math
P_{pt}=\frac{Y_{pt}}{F_{pt}}
```

This is “contribution dollars supported per SPL FTE.” The ratio is intuitive, but it embeds a substantive restriction:

```math
\ln(P_{pt})=\ln(Y_{pt})-\ln(F_{pt})
```

Thus a log-ratio regression implicitly fixes the elasticity of output with respect to SPL labor at one. Always show a robustness model that estimates that elasticity rather than assuming it:

```math
\ln(Y_{pt})
=
\alpha_p+\lambda_t+\tau Z_{pt}+\gamma\ln(F_{pt})+\delta'X_{pt}+\varepsilon_{pt}
```

If staffing changes because of treatment, realized `F_pt` is a mechanism. The ratio is a policy-relevant total-leverage outcome, while the production model is a conditional-output specification. Report both and label the distinction.

### Dollar net-value alternative

```math
NV_{pt}=Y_{pt}-c^{SPL}_tF_{pt}-Cost^{tool}_{pt}-Cost^{implementation}_{pt}
```

Use `NV` for ROI or investment decisions. Use `P` for operational leverage. They answer different questions.

## 6. Workflow-time automation and attention

### Automation share in a common labor unit

```math
EligibleMinutes_{pt}=\sum_wV_{pwt}M_w
```

```math
DisplacedMinutes_{pt}=\sum_wV_{pwt}M_wS_{pwt}
```

```math
A^{time}_{pt}=\frac{DisplacedMinutes_{pt}}{EligibleMinutes_{pt}}
```

Why this denominator adds coherently: every summand has the same unit, minutes of baseline eligible manual labor.

```math
[V_{pwt}M_w]=workflowUnits\times\frac{minutes}{workflowUnit}=minutes
```

The numerator uses the same minutes multiplied by a displacement share `S` between zero and one. This is the first metric that can defensibly be called “percent of eligible SPL work automated.”

### Human attention per completed unit

```math
H_{pwt}=\frac{SPLMinutes_{pwt}}{CompletedUnits_{pwt}}
```

Include exception handling and rework in `SPLMinutes`. Otherwise the metric rewards automations that shift effort downstream.

## 7. Primary and secondary estimands

### Primary: effect of being offered automation

```math
\ln(P_{pt})
=
\alpha_p+\lambda_t+\tau Z_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

```math
RolloutLift=100\left(e^{\tau}-1\right)\%
```

This is the preferred primary estimate because `Z` is randomized and does not require pretending the six Hex surface rates share a unit.

### Surface first stages

```math
A^s_{pt}
=
\alpha^s_p+\lambda^s_t+\pi_s Z_{pt}+\theta_s'X_{pt}+\nu^s_{pt}
```

`pi_s` is the percentage-point change in surface `s` caused by rollout. Report the full prespecified set or declare one primary surface.

### Summary first stage

```math
U_{pt}=\alpha_p+\lambda_t+\pi_UZ_{pt}+\theta'X_{pt}+\nu_{pt}
```

`pi_U` is the change in the adoption index measured in baseline standard deviations.

### Secondary IV effect

Use IV only with a prespecified, substantively credible scalar exposure such as `A^time`, one primary surface, or clearly labeled `U`:

```math
A^*_{pt}=\alpha_p+\lambda_t+\pi Z_{pt}+\theta'X_{pt}+\nu_{pt}
```

```math
\ln(P_{pt})
=
\alpha_p+\lambda_t+\beta\widehat A^*_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

The familiar 10-percentage-point expression is valid only when `A*` is a 0-to-1 share:

```math
Lift_{10pp}=100\left(e^{0.10\beta}-1\right)\%
```

It is not valid for the standardized index `U`.

## 8. Why log, and when not to log

For a positive outcome `P`:

```math
\ln(P_1)-\ln(P_0)=\ln\left(\frac{P_1}{P_0}\right)
```

This makes the estimand proportional rather than dollar-level and often reduces right skew. With a binary randomized treatment, exact percent lift is `100(e^tau-1)`.

Do not log `P <= 0`. Pre-specify one of:

- a levels model for contribution per SPL;
- inverse hyperbolic sine as a sensitivity analysis, with careful interpretation;
- a positive operational outcome such as revenue or completed quality-adjusted units;
- a two-part analysis separating the probability of positive contribution from its magnitude.

Never drop non-positive observations silently.

## 9. Guardrails

For guardrail `j`:

```math
g_j\!\left(E[Q^j_{pt}]\right)
=
\alpha^j_p+\lambda^j_t+\tau^j_QZ_{pt}+\delta_j'X_{pt}
```

- identity link for continuous scores;
- binomial/logit or linear probability for success rates;
- Poisson/negative binomial for counts when variance supports it.

Preserve each quality numerator and denominator. Do not hide unrelated outcomes inside an unvalidated “quality-adjusted” composite.

## 10. The headline sentence

> Randomized access to the automation intervention changed pod contribution supported per SPL FTE by X%, while the six Hex surface metrics show where behavior changed and workflow attention and quality outcomes show how.
