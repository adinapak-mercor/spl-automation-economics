# Experiment design

## Objective

Estimate whether an intervention that increases SPL automation causes:

1. higher automation coverage;
2. lower human attention per workflow;
3. higher gross profit supported per SPL;
4. no deterioration in quality, delivery or expert experience.

## Unit of randomization

Prefer pod or project/account clusters over individual SPLs.

Individual randomization is vulnerable to interference because SPLs can share prompts, scheduled agents, templates and practices. Team leads can also spread treatment to nominal controls.

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

### First stage

```math
A_{pt}
=
\alpha_p+\lambda_t+\pi Z_{pt}+\theta'X_{pt}+\nu_{pt}
```

`pi` tests whether rollout assignment actually increases automation coverage.

### Rollout-instrumented effect

```math
\ln(P_{pt})
=
\alpha_p+\lambda_t+\beta\widehat{A}_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

`beta` is the local average treatment effect among pods whose automation responds to assignment, under the standard relevance, exclusion, independence and monotonicity assumptions.

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

- Gross profit before SPL labor cost per SPL FTE.

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

Workflow taxonomy, manual-minute weights and richer telemetry can be constructed later only if raw events and join keys are retained. New survey questions or screen/app-time measurement must be set up before treatment if they are needed for baseline comparison.

## Main threats

| Threat | Consequence | Mitigation |
|---|---|---|
| Spillovers | Controls receive treatment indirectly | Cluster randomization; track sharing |
| Adoption selection | Strong pods both adopt and perform better | Use assigned rollout, not usage alone |
| Changing pod membership | Misattributes events and outcomes | Effective-dated mappings |
| Event-count measurement error | Attenuates or distorts automation effect | Surface-specific validation; workflow/time subsample |
| Anticipation | Pods change before assigned date | Conceal timing where practical; inspect leads |
| Attrition/reorganizations | Composition changes after treatment | Preserve assignment; report balance/attrition |
| Outcome lag | Revenue does not react immediately | Mechanism outcomes plus event-study horizon |
| Multiple testing | Selective positive findings | Prespecify primary outcome and guardrails |
| Low power | Noisy pod metrics hide effects | Power analysis using pre-period variance |

## Decision rule

Do not commit to a full workflow telemetry build before confirming:

- the rollout moves the existing automation proxy;
- pod mapping and SPL denominators are sufficiently reliable;
- a plausible primary outcome has adequate variation and power;
- the result would change a product or deployment decision.
