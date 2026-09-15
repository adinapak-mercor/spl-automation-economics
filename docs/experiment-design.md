# Experiment design

## Objective

Estimate whether an intervention that increases SPL automation causes:

1. higher Coil involvement on the prespecified Hex surfaces;
2. lower human attention per workflow;
3. higher contribution output supported per SPL;
4. no deterioration in quality, delivery or expert experience.

## Unit of randomization

The unit is decided by one empirical fact: how many SPLs share a project. Individual
randomization is vulnerable to interference because SPLs can share prompts, scheduled
agents, templates and practices, and team leads can spread treatment to nominal controls —
but that interference only exists where a project holds more than one SPL. Where projects
have a single lead, individual randomization already is cluster randomization and is
strictly more powerful.

Compute the SPL-per-project distribution before choosing. The decision table and the
access-gating design are in [`rollout-mechanics.md`](rollout-mechanics.md).

Recommended approach:

- stratify eligible pods by project maturity, type, scale and baseline adoption;
- randomize rollout timing within strata;
- use a stepped-wedge or batched rollout so all eligible pods can eventually receive treatment;
- retain assignment even if a pod does not adopt immediately.

## Treatment definition

Record separately:

- eligibility;
- assigned rollout cohort and date;
- actual access/enabled date;
- intervention type and intensity;
- actual adoption/automation;
- cross-pod sharing or contamination.

Do not define treatment solely as observed usage. High-performing pods may self-select into adoption.

## Estimands

### Intent to treat

```math
\ln(P_{pt})
=
\alpha_p+\lambda_t+\tau Z_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

`tau` estimates the effect of being assigned the rollout, regardless of adoption.

### Surface-specific first stages

```math
A^s_{pt}
=
\alpha^s_p+\lambda^s_t+\pi_s Z_{pt}+\theta_s'X_{pt}+\nu^s_{pt}
```

`pi_s` tests whether rollout assignment changes Coil involvement on surface `s`. Snowflake queries, Slack messages, and five-minute windows on the other surfaces are not pooled.

If one summary first stage is prespecified, use a baseline-standardized adoption index:

```math
U_{pt}=\frac{1}{|\mathcal S^0_p|}
\sum_{s\in\mathcal S^0_p}
\frac{A^s_{pt}-\mu^s_0}{\sigma^s_0}
```

```math
U_{pt}
=
\alpha_p+\lambda_t+\pi_U Z_{pt}+\theta'X_{pt}+\nu_{pt}
```

`U` is a multi-surface adoption index in baseline standard deviations, not percent of work automated.

### Rollout-instrumented effect

```math
\ln(P_{pt})
=
\alpha_p+\lambda_t+\beta\widehat{A}_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

`beta` is the local average treatment effect among pods whose selected exposure responds to assignment, under the standard relevance, exclusion, independence and monotonicity assumptions. Run this only for a prespecified scalar exposure with a defensible meaning: a primary surface, the clearly labeled index `U`, or the later workflow-time automation share. A “10pp” interpretation is invalid for `U`.

### Mechanism

```math
\ln(H_{pwt})
=
\alpha_{pw}+\lambda_t+\beta_H\widehat{A}_{pwt}+\delta'X_{pwt}+\varepsilon_{pwt}
```

This tests whether automation reduces human attention per completed workflow.

## Dynamic effects

Expect learning and organizational adjustment. Estimate an event study around assigned rollout:

```math
\ln(P_{pt})
=
\alpha_p+\lambda_t
+\sum_{k\neq-1}\beta_k\,1[t-T_p=k]
+\delta'X_{pt}+\varepsilon_{pt}
```

Use pre-treatment coefficients to examine parallel trends. Post-treatment coefficients show whether effects appear immediately or only after workflows and staffing adapt.

## Outcome hierarchy

### Primary

- Contribution output before SPL labor cost per SPL FTE.

### Mechanism

- Human attention per completed workflow.
- Rework-inclusive SPL minutes.
- Manual interventions per workflow.

### Secondary

- Revenue per SPL FTE.
- Comparable projects supported per SPL.
- Setup/ramp/cycle time.
- Capacity released and redeployed.

### Guardrails

- One-shot acceptance.
- QC score and rework.
- Delivery yield and SLA performance.
- Expert NPS/satisfaction.
- Client escalations.
- Automation failure and human override rates.

## Minimum viable rollout

Before launch, require only:

1. versioned assignment and rollout dates;
2. stable effective-dated pod/project mapping;
3. preserved raw automation events;
4. SPL allocation or FTE;
5. one viable economic/operational outcome;
6. one quality guardrail.

Workflow taxonomy can be constructed later; manual-minute weights cannot, because a weight
measured after treatment is endogenous to it. New survey questions and app-time measurement
must be in field before treatment if they are needed for baseline comparison. The full
split between what is reconstructable, what needs capturing now, and what blocks launch is
in [`reconstructability.md`](reconstructability.md).

## Main threats

| Threat | Consequence | Mitigation |
|---|---|---|
| Spillovers | Controls receive treatment indirectly | Cluster randomization; track sharing |
| Adoption selection | Strong pods both adopt and perform better | Use assigned rollout, not usage alone |
| Changing pod membership | Misattributes events and outcomes | Effective-dated mappings |
| Incommensurate surface units | A combined rate is dominated by arbitrary query/message/window volume | Separate first stages; optional standardized index; no summed rate |
| Surface measurement error | Attenuates or distorts automation effect | Versioned definitions; surface validation; workflow/time subsample |
| Snapshot coverage gaps | Missing days are mistaken for zero usage | Coverage flags; common loaded-day windows; do not impute zero |
| Current roster applied historically | Reorganizations misclassify past departments | Effective-dated pod/person mapping for analysis |
| Anticipation | Pods change before assigned date | Conceal timing where practical; inspect leads |
| Attrition/reorganizations | Composition changes after treatment | Preserve assignment; report balance/attrition |
| Outcome lag | Revenue does not react immediately | Mechanism outcomes plus event-study horizon |
| Multiple testing | Selective positive findings | Prespecify primary outcome and guardrails |
| Low power | Noisy pod metrics hide effects | Power analysis using pre-period variance |
| Revenue insensitive to SPL effort | Primary economic outcome cannot respond within the study window, so a null reflects pricing rather than productivity | Classify eligible pods by pricing model; lead with an effort-responsive operational primary and treat contribution per FTE as confirmatory |
| Few randomized units | Cluster-robust standard errors over-reject and results look more significant than they are | Randomization inference as the primary test; stratify for balance |
| Shared access credential | Assignment and realized access diverge unobservably; borrowed access is indistinguishable from non-adoption | Identity-based gating with access logging; assignment frozen independently of the gate |

## Decision rule

Do not commit to a full workflow telemetry build before confirming:

- the rollout moves at least one prespecified surface metric or the adoption index;
- pod mapping and SPL denominators are sufficiently reliable;
- a plausible primary outcome has adequate variation and power;
- the result would change a product or deployment decision.
