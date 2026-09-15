# Measurement decisions: do the existing SPL metrics suffice?

This document answers the first open question directly: can the study run on metrics that
already exist, or does it require new ones? It gives a verdict per metric rather than a
general discussion, so the answer can be argued with or overridden item by item.

## Verdict vocabulary

Every metric is assigned exactly one role. Most measurement disputes on this project are
really disputes about role, not about data quality.

| Role | Meaning | Can it carry the headline? |
|---|---|---|
| Primary outcome | The result the study is designed to estimate | Yes |
| First stage / compliance | Evidence that the rollout changed behavior | No |
| Guardrail (non-inferiority) | Must not get worse; a null is the pass condition | No |
| Diagnostic | Used to debug the pipeline or interpret an estimate | No |
| Not usable | Should not be built on in its current form | No |

A metric can be excellent and still be unusable as an outcome. Surface activity rates are
the clearest case: they are well-defined and worth measuring, and they are still not
productivity.

## Existing metrics

### Weekly expert NPS

**Role: guardrail (non-inferiority). Not an outcome.**

The expectation that NPS will show no significant effect is probably right, and it is not a
problem, because NPS is not being asked to show an effect. It is being asked to rule out
harm to the expert experience.

That reframing has a consequence that needs handling before launch. A null result only
certifies safety if the study could have detected a harm worth caring about. So the
minimum detectable effect must be computed first, from actual pod-week response counts:

```math
\mathrm{MDE}\approx
\left(z_{1-\alpha/2}+z_{\mathrm{power}}\right)
\sigma_{\mathrm{NPS}}
\sqrt{\frac{1}{n_1}+\frac{1}{n_0}}
```

If the MDE turns out larger than the smallest NPS movement anyone would act on — which is
likely at weekly pod grain with partial response — then NPS cannot certify safety on its
own and a second experience guardrail is required. The two candidates are both census
measures rather than samples, so they carry far more information per pod-week:

- client and expert escalation counts;
- expert attrition or drop-off from the pod.

Report NPS with response rate and respondent composition every period. A shift in who
answers can move the score without any change in experience.

### Weekly time-use survey

**Role: primary source for baseline manual minutes. Requires a validation pass first.**

The doubt about this data is well placed, and it matters more than it looks, because the
survey sits on the critical path. Baseline manual minutes per workflow (`M_w`) is the
weight that makes the workflow-time automation share dimensionally valid, and `M_w` has to
be frozen before treatment. The survey is currently the only instrument that can produce
it. So survey trust is not a side question to resolve later; it gates the measure the study
eventually wants to report.

Validation design, runnable in two to three weeks on a volunteer subsample:

1. Pair the self-report against an independent measure for the same person-week —
   calendar time, app-derived time, or both.
2. Report the within-person correlation and the direction of bias, not just the average
   gap. Recall error that is stable per person is far less damaging than error that varies
   with workload.
3. Apply the decision rule below.

| Validation result | What the survey may be used for |
|---|---|
| Strong within-person correlation, stable bias | Levels: `M_w` in minutes |
| Weak correlation, or bias that moves with workload | Rankings only: order workflows by time, do not use minute levels |
| No usable relationship | Replace with a task-audit time study on a sample of workflows |

The middle row is the realistic outcome and it is worth planning for. Rankings tolerate a
lot more measurement error than levels do, and a ranking is still enough to choose which
workflows to instrument first. It is not enough to compute a weighted automation share.

### App usage and surface automation shares

**Role: first stage and compliance. Never an outcome.**

The concern that these do not correspond to productivity is correct, and the design already
depends on that being true: the six Hex surface rates appear only as first-stage outcomes
that test whether assigned access changed behavior. See
[`hex-metric-specification.md`](hex-metric-specification.md) for definitions and
[`formula-map.md`](formula-map.md) for the role assignment.

One addition worth making explicit. These metrics decide whether the study is interpretable
at all. If the rollout moves none of the surface rates, the correct conclusion is that the
experiment had no uptake, not that automation had no effect. Without a first stage, a null
on the primary outcome cannot be distinguished from a failed intervention. That makes the
surface rates load-bearing even though they can never be the result.

They also must not be summed. Queries, messages, and surface-specific five-minute windows
do not share a unit or an opportunity set, so a combined rate is dominated by whichever
surface happens to emit events most often.

### What the existing metric set does not contain

None of the three existing sources measures SPL output volume — delivered or accepted work
units attributable to a pod-week. That is the quantity most likely to respond to automation
inside the study window, and its absence is the real gap in the existing metrics, more than
the noise in any one of them.

## Proposed new metrics

Each proposal is scored on when it must exist, because that determines whether it can delay
the study. The full retention analysis is in
[`reconstructability.md`](reconstructability.md).

| Proposal | Must exist before treatment? | Notes |
|---|---|---|
| Discrete workflow taxonomy | Partly | Split it; see below |
| Telemetry / app-derived time use | Depends on source retention | Verify retention per source before assuming |
| Added time-use survey questions | Yes | Baseline cannot be recovered afterwards |

### Discrete workflows: split the concept

The workflow proposal is really two measures with two different deadlines, and treating them
as one is what creates the false choice between instrumenting properly and launching soon.

- **Workflow labeling** — assigning a retained event to a workflow — is a classifier applied
  to stored data. It is fully reconstructable after the fact, as long as the raw events and
  the join keys survive. This does not need to block anything.
- **Baseline manual minutes** — the `M_w` weight — is a pre-treatment measurement of how long
  the work took before automation touched it. Once a pod is treated, its baseline is gone.
  This is not reconstructable, and it is the only part of the workflow build with a hard
  pre-launch deadline.

So the answer to whether workflows can be constructed after the fact is: the taxonomy yes,
the weights no. Freezing a rough `M_w` on the current survey before the first wave is more
valuable than a precise one built afterwards, because a post-treatment weight is endogenous
to the treatment it is supposed to measure.

### Telemetry and app-derived time

App-derived time is attractive because it avoids recall error, and it carries two problems
worth stating in advance. Time with an application open is not time working in it, and
automation can reduce app time without reducing cognitive load, so a fall in app time is
not automatically a fall in human attention.

Its feasibility as a retroactive measure depends entirely on how long each source keeps
raw records. That is a question with a factual answer per source, and the answer should be
obtained rather than assumed; see [`reconstructability.md`](reconstructability.md).

### Added survey questions

The cheapest proposal to build and the one with the longest effective lead time, because a
new question yields a usable baseline only after a full pre-treatment period in field. Any
question needed for a pre/post comparison has to ship before the first wave.

## Consequence for the outcome hierarchy

There is a threat to the primary outcome that comes from contract structure rather than from
measurement, and it deserves to be resolved before the analysis plan is frozen.

Contribution per SPL FTE responds to automation only if pod revenue can respond to SPL
effort within the study window. Where revenue is fixed by contract, milestone, or priced off
delivered expert hours, reducing SPL time does not raise the numerator at all in the short
run. The estimate is then driven almost entirely by movement in the denominator, and a null
result would say more about pricing than about productivity.

This is not the same as the outcome-lag threat. Lag means the response is slow; this means
the response may be structurally absent for the duration of the study.

Recommended ordering, subject to a check of how pods are actually priced:

1. **Primary:** an SPL-effort-responsive operational outcome — SPL minutes per delivered
   unit, or comparable projects supported per SPL FTE.
2. **Confirmatory:** contribution per SPL FTE, over a longer horizon than the operational
   outcome.
3. **Guardrails:** quality, delivery, and experience, each reported separately.

The check is small and should happen early: classify the eligible pods by pricing model and
count how many have revenue that could move within the window. If most cannot, the economic
outcome becomes a long-run confirmatory measure and the study needs an operational primary.
