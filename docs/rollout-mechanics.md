# Rollout mechanics

The batched rollout is the simplest part of this study, and it stays simple as long as three
decisions are made deliberately: what gets randomized, how access is gated, and how
inference is done given how few units there are. This document settles each one.

## 1. Unit of randomization

The working proposal is to take the pool of SPLs and randomize with respect to project and
account. That is right, with one distinction that decides the whole design: whether project
and account are **strata** (randomize individuals, balanced across projects) or the
**randomized unit** itself (randomize whole projects).

The difference only matters when a project has more than one SPL. If two SPLs on the same
project land in opposite arms, the treated one shares prompts, agents, and templates with
the control one, and the control is no longer a control.

So the choice is an empirical question, answerable today:

| Finding | Unit | Reason |
|---|---|---|
| Most projects have one SPL | Individual SPL, stratified by project type/account/maturity | Individual assignment already is cluster assignment; maximum power |
| Many projects have several SPLs | Project or account cluster | Within-project contamination would otherwise destroy the contrast |
| Mixed | Cluster on project, stratify on account and maturity | Safe under both; costs some power |

**Action:** count SPLs per project and per account over the last complete quarter. That
distribution picks the unit. Nothing else about the design depends on this choice.

Regardless of unit, stratify on the variables that predict the outcome — project maturity,
project type, scale, and baseline adoption — and randomize rollout timing within strata.

## 2. Access gating

Password protection is a reasonable instinct and the wrong mechanism, for a reason that has
nothing to do with security.

A shared password cannot tell you who used the tool. It cannot distinguish an SPL who was
assigned access and chose not to use it from an SPL who borrowed a colleague's password, and
those two cases pull the estimate in opposite directions. Passwords also get shared, which
is not a hypothetical failure in a population that collaborates by design.

Gate on identity instead — a per-SPL feature flag or entitlement, with access logged:

- every access attempt is attributed to a person, so contamination becomes an observed
  variable rather than an assumption to argue about;
- exact first-access timestamps per person are recorded, which is the input the event study
  needs anyway;
- revoking or extending access to one person does not require re-gating everyone.

This is not more work than a password. It is the same gate keyed to the identity that
already exists.

One rule holds whichever gate is chosen: **the assignment record must be frozen
independently of the gate.** Access gates get adjusted ad hoc by whoever administers them,
and if assignment is inferred from the gate's current state, the study loses its
intention-to-treat basis. Record assignment once, in `experiment_assignment`, and never
overwrite it with realized access.

Track separately, per the schema in [`engineering-plan.md`](engineering-plan.md):
eligibility, assigned wave, assigned date, actual access date, observed usage, and any
detected sharing.

## 3. Waves

Use a stepped-wedge or batched rollout in which every eligible unit is eventually treated.
This is worth preferring on two grounds beyond the statistical ones: nobody is asked to be
permanently excluded from a tool their peers have, and each unit contributes both treated
and untreated periods, which absorbs persistent unit-level differences.

Practical rules:

- randomize timing within strata, not across the whole pool;
- keep the assigned date even if a unit is slow to adopt;
- avoid announcing individual dates far in advance, so units do not change behavior before
  treatment starts;
- inspect pre-treatment event-study coefficients for anticipation regardless.

## 4. Inference with few units

This is the part most likely to be underestimated. The SPL pool is small, and cluster-robust
standard errors are badly behaved with few clusters — they over-reject, so results look
more significant than they are. Roughly forty clusters is where the usual asymptotics start
to be trusted, and this study may have fewer.

Use randomization inference as the primary basis for p-values:

1. hold the realized outcomes fixed;
2. re-draw assignment thousands of times using the exact randomization procedure, strata
   included;
3. compare the realized estimate to the resulting distribution.

This is exact under the sharp null and does not rely on cluster counts. Report cluster-robust
standard errors alongside it for readability, not as the primary test.

Two supporting choices matter at this scale. Stratification buys more through balance than
through power, so stratify on anything that plausibly predicts the outcome. And prespecify
the primary outcome and guardrails before assignment, since with few units the temptation
to search across outcomes is strongest and the cost of doing so is highest.

## 5. Power, and what is needed to compute it

Power can be computed now, from existing data, because the only inputs that matter are the
pre-period variance of the chosen primary outcome and the number of units. Neither requires
the intervention to exist.

For a clustered design with `J` units, `m` periods each, and intra-cluster correlation
`rho`:

```math
\mathrm{MDE}
=
\left(z_{1-\alpha/2}+z_{\mathrm{power}}\right)
\sqrt{\frac{\sigma^2}{J\,\bar\pi(1-\bar\pi)}}
\sqrt{\frac{1+(m-1)\rho}{m}}
```

where `sigma^2` is the residual variance of the outcome after unit and period fixed effects,
and `pi-bar` is the share of unit-periods treated under the wave schedule.

Inputs to assemble:

| Input | Where it comes from |
|---|---|
| `J` | Unit count from the SPL-per-project distribution in §1 |
| `m` | Study length in weeks |
| `sigma^2` | Residual variance of the primary outcome in the pre-period |
| `rho` | Within-unit correlation in the pre-period |
| `pi-bar` | Wave schedule |

Run this for each candidate primary outcome before choosing one. An outcome whose MDE
exceeds any effect size worth acting on should not be the primary outcome, however much it
is the one people want to see. This is the same test applied to expert NPS in
[`measurement-decisions.md`](measurement-decisions.md), and it should be applied to the
economic outcome too.

## 6. Pre-launch checklist

1. SPL-per-project distribution computed; randomization unit chosen.
2. Strata defined from pre-treatment variables only.
3. Identity-based access gating in place, with access logging.
4. `experiment_assignment` frozen, independent of the gate.
5. Effective-dated person → pod → project capture running (see
   [`reconstructability.md`](reconstructability.md)).
6. Bucket C measures in field: baseline manual minutes, added survey items, workflow
   eligibility.
7. Power computed per candidate outcome; primary outcome and guardrails prespecified.
8. Randomization script saved, so the same procedure can be replayed for inference.
