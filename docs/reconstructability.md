# Reconstructability: what can be built after the fact

This document answers the second half of the metrics question: if new measures are needed,
can they be constructed retroactively so the rollout is not delayed?

The short answer is that most of them can, and the exceptions are few enough to list. But
the reasoning that gets there needs one correction, because the usual version of it is
slightly too optimistic.

## The premise needs tightening

The standard argument is that any metric housed in a data store that is not deleted over
time can be reconstructed later. That is correct as stated. The difficulty is that
"not deleted over time" is an assumption about each source, not a property of data stores
in general, and it fails in two distinct ways.

**Deletion.** Event sources with finite retention windows drop raw records on a rolling
basis. Once the window passes, no amount of later effort recovers the period.

**Overwrite.** A table that is never deleted can still destroy history by being updated in
place. A current-state roster, org chart, or pod mapping holds only today's truth; last
quarter's assignment is simply gone, replaced rather than removed. This failure mode is
easy to miss because the table still exists and still looks complete.

Both failures are already visible in the current measurement stack rather than
hypothetical:

- The September 2026 Hex snapshot loaded only 28 of 90 days of Google Docs history. That is
  a retention or load-coverage gap in a source the study depends on.
- The same snapshot applies 2026-09-10 organizational labels to historical activity, because
  effective-dated mapping does not exist yet. That is an overwrite problem, and it means
  past pod membership currently cannot be reconstructed at all.

So the conclusion holds with a condition attached: metrics are reconstructable later if
their sources are durable and their keys are effective-dated, and at least one of those two
conditions does not hold today.

## Three buckets

Every variable the study needs falls into exactly one of these.

### Bucket A — reconstructable later, no action required

Raw events already land in a durable warehouse with stable identifiers, so the definitions
on top of them can change as often as needed.

| Variable | Source | Why it is safe |
|---|---|---|
| Surface numerators and denominators | Snowflake / warehouse event tables | Raw events retained; definitions are a view |
| Workflow labeling (`workflow_id`, eligibility) | Classifier over retained events | Labeling is post-hoc by construction |
| Tool-call telemetry, failure rates | Warehouse telemetry | Event grain preserved |
| Finance revenue and cost | Finance system of record | Closed periods are versioned, not overwritten |
| Delivery, QC, rework outcomes | Operational systems | Transactional records |

Workflow labeling belongs here, and that is the most useful single conclusion for the
sequencing question. The taxonomy can be designed and applied months after the rollout
starts without costing the study anything.

### Bucket B — reconstructable only if something is captured now

These sources are durable enough to query today and will not answer the same question in six
months. They need a capture job before the first wave, not a redesign.

| Variable | Risk | Action needed now |
|---|---|---|
| Person → pod → project assignment | Overwrite: current-state mapping only | Begin slowly-changing-dimension capture with effective dates |
| SPL allocation shares | Overwrite | Snapshot weekly and version |
| Studio auth activity | Deletion: log-source retention window | Archive to warehouse on a schedule |
| Slack activity history | Deletion: analytics history limits | Archive to warehouse on a schedule |
| Google Docs / Sheets edit history | Deletion: already showing a 28/90-day gap | Extend load window; archive |
| Project maturity, type, pricing model | Overwrite | Capture as effective-dated attributes |
| Roster and full-time labels | Overwrite | Version the roster weekly |

Two things make this bucket the priority. It is the only bucket where the cost of waiting is
silent — nothing fails, the data simply stops existing for the period nobody captured. And
the work is small: scheduled archival and effective-dated capture, not new instrumentation.

Before relying on any row above, get the actual retention window from the source owner and
record it. These are questions with factual answers, and the answers determine how urgent
the capture job is.

### Bucket C — not reconstructable, must precede treatment

These require a human to report or a measurement to be taken while the pod is still
untreated. After the first wave, the untreated state no longer exists to be measured.

| Variable | Why it cannot wait |
|---|---|
| Baseline manual minutes per workflow (`M_w`) | Defined as pre-treatment duration; a later measurement is endogenous to treatment |
| New time-use survey questions | Pre/post comparison requires a pre-period in field |
| App-derived time-use baseline | Same; needs a pre-treatment window |
| Workflow automation eligibility (`eligible_w`) | Must be declared before outcomes are seen, or selection enters the denominator |
| Randomization assignment and strata | Assignment is only exogenous if frozen before outcomes |
| Pre-period standardization moments for the adoption index | Must come from untreated periods |

This is the complete launch-blocking list, and it is short. Nothing in it requires new
engineering: it is one survey change, one time study, one eligibility review, and an
assignment table.

## Sequencing consequence

The three buckets imply a rollout that does not wait for the measurement build.

1. **Before wave 1:** everything in bucket C, plus the capture jobs in bucket B. The
   expensive-sounding work — workflow taxonomy, telemetry pipelines, attention measurement —
   is not here.
2. **During rollout:** bucket A definitions get built and refined against retained events.
   Definitions may change; the underlying data does not.
3. **After signal is established:** the workflow-time automation share and attention
   measures get constructed retroactively over the full study period, including its earliest
   weeks.

The only irreversible decision is what gets measured before the first pod is treated. Most
of what looks like prerequisite work is not.

## Standing requirement

Every analytical row must remain joinable through effective-dated keys:

```text
person_id → SPL assignment → pod_id → project_id → client/account_id
assignment_start <= event_time < assignment_end
```

A current-state org chart cannot satisfy this. Effective-dated capture is what moves the
mapping variables out of bucket B and makes retroactive reconstruction possible at all.
