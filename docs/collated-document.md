# SPL Automation Economics

**Measurement system and experimental design for estimating whether automation makes Strategic Project Leads more productive.**

Internal research design, September 2026. This is a design document, not a finalized KPI. It gives economists and engineers one shared map of the causal question, every required variable and its source, the formulas and why they are built that way, what exists today versus what needs new instrumentation, and the minimum viable study versus the fuller long-run model.

## How to read this document

Equations are written as LaTeX between double-dollar delimiters. Run **Extensions → Auto-LaTeX Equations → Render Equations** once after pasting, to convert them into rendered images. Re-running is safe; already-rendered equations are skipped.

Sections 1, 3, 4 and 7 are the decision content and can be read alone. Sections 2, 5, 8 and 9 are reference material for whoever implements the pipeline.

---

## 1. Summary

### 1.1 Research question

> Does randomized access to SPL automation reduce the human attention required to operate a pod, and increase economic value supported per SPL, without worsening quality or delivery?

### 1.2 Three questions that are often conflated

Most disagreement about this project comes from mixing these three. They need different metrics, and a metric that answers one cannot answer another.

| Question | Metric family | What an answer means |
|---|---|---|
| Did access change behavior? | rollout `Z`, surface rates `A_s`, adoption index `U` | Product adoption and compliance |
| Did automation reduce the scarce input? | attention per completed unit `H` | Operational productivity mechanism |
| Did the business support more value per SPL? | contribution `Y`, SPL capacity `F`, leverage `P` | Economic productivity |

### 1.3 Are the existing metrics of SPL work good enough?

They are good enough to start and not good enough to finish, and the reason is role rather than quality.

Expert NPS is a non-inferiority guardrail, not an effect metric. The expectation that it will show no significant effect is almost certainly right and is not a problem, because it is not being asked to show one. It needs a minimum-detectable-effect calculation before a null can be read as evidence of no harm.

The surface activity shares are first-stage compliance measures that establish whether the rollout changed behavior. They are never outcomes. The concern that nobody knows which of them corresponds to productivity is correct, and the design depends on that being true.

The weekly time-use survey sits on the critical path, which is easy to miss. It is the only current source for baseline manual minutes, and those must be frozen before treatment. So its trustworthiness gates the measure the study eventually wants to report, and it needs a short validation pass with a documented fallback.

The genuine gap in the existing set is not noise in any one metric. It is that **nothing measures SPL output volume** — delivered or accepted work units per pod-week — which is the quantity most likely to move inside the study window. Full verdicts in section 3.

### 1.4 If new metrics are needed, can they be built after the fact?

Mostly yes, and the exceptions are few enough to list.

Workflow labeling is a classifier applied to retained events, so it can be built months after launch at no cost to the study. Baseline manual minutes cannot, because a weight measured after treatment is endogenous to the treatment it is meant to weight. The workflow proposal is therefore two measures with two different deadlines, and treating them as one is what creates the false choice between instrumenting properly and launching soon.

The reconstruction argument needs one correction. "Housed in a store that is not deleted" also has to mean "not overwritten." A current-state pod mapping is never deleted and still destroys history by updating in place, which is why the September snapshot applies 2026-09-10 org labels to historical activity. Sources with rolling retention and mappings that update in place need capture jobs now, and the cost of skipping them is silent: nothing fails, the period simply stops existing. Bucket-by-bucket analysis in section 4.

### 1.5 How should the batched rollout work?

Simple, as expected, with three decisions worth making deliberately.

The randomization unit follows from one fact that can be computed today — the number of SPLs per project. Where projects have a single lead, individual randomization already is cluster randomization and is strictly more powerful. Where they have several, within-project sharing would destroy the contrast and the unit must be the project.

Access should be gated on identity rather than a shared password. Not for security: a shared password cannot distinguish an SPL who was assigned access and declined to adopt from one who borrowed a colleague's credentials, and those two cases bias the estimate in opposite directions.

With few randomized units, cluster-robust standard errors over-reject, so randomization inference should be the primary basis for p-values. Mechanics and pre-launch checklist in section 7.

### 1.6 One caveat on the primary outcome

Contribution per SPL FTE can only respond to automation if pod revenue can respond to SPL effort inside the study window. Where revenue is fixed by contract, milestone, or priced off delivered expert hours, it cannot, and the estimate would be driven almost entirely by movement in the denominator. A null would then describe pricing rather than productivity.

This is not the outcome-lag problem already on the threat list. Lag means the response is slow; this means it may be structurally absent for the study's duration.

The check is small and should happen early: classify eligible pods by pricing model and count how many have revenue that could move within the window. If most cannot, lead with an effort-responsive operational outcome and treat contribution per SPL FTE as a longer-horizon confirmatory measure.

### 1.7 Recommended primary estimate

The minimum viable economic outcome is pod contribution output per SPL FTE:

```math
Y_{pt}=R_{pt}-C_{pt}, \qquad P_{pt}=\frac{Y_{pt}}{\mathrm{SPL\ FTE}_{pt}}
```

The primary estimand should be the effect of randomized rollout access, because it does not rely on constructing a false cross-surface automation percentage:

```math
\ln(P_{pt}) = \alpha_p+\lambda_t+\tau Z_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

```math
\mathrm{RolloutLift}=100\left(e^{\tau}-1\right)\%
```

In plain English:

> Being assigned access to the automation intervention causes an estimated X% change in contribution supported per SPL, subject to quality and delivery guardrails.

Estimate rollout effects on each Hex surface rate separately, to show where behavior changed. A secondary instrumental-variables estimate may translate rollout into an automation effect only after a substantively valid scalar exposure has been chosen. The familiar "10 percentage point automation effect" is valid for a 0-to-1 share such as workflow-time coverage; it is not defined for a standardized multi-surface index.

### 1.8 Why this is only the minimum viable study

The current Hex metrics are surface-specific activity proxies. They do not establish which SPL workflow an event belongs to, whether that workflow should be automated, how much manual time the event represents, or whether AI involvement actually displaced human labor.

Add workflow labeling and attention measurement after establishing feasibility and signal, not before. The full sequencing argument is in section 4.

### 1.9 The headline sentence

> Randomized access to the automation intervention changed pod contribution supported per SPL FTE by X%, while the six Hex surface metrics show where behavior changed, and workflow attention and quality outcomes show how.

---

## 2. What is measured today: the six Hex surfaces

Source: [Coil surface activity, saved snapshot, September 2026](https://app.hex.tech/500e8e3f-f94b-4ca6-9ba1-d07bdc8e4dfb/hex/Coil-surface-activity-saved-snapshot-September-2026-034Ni63vTasQW1Fe7W7I7w/draft/logic?threadLayout=collapsed&projectView=app&view=app).

This is a saved snapshot, not a live source. Surface histories end on different dates, missing days remain gaps, and department and title labels as of 2026-09-10 are applied to historical activity.

### 2.1 The most important implication

There is no mathematically defensible combined Hex automation percentage in this snapshot. Each surface has a different observational unit:

```math
A_{spt}=\frac{N_{spt}}{D_{spt}},\qquad s\in \{\mathrm{Snowflake,Sheets,Docs,Slack,TeamPlatform,Studio}\}
```

`N_s` and `D_s` are valid only within surface `s`. Adding them across surfaces would treat one SQL query, one Slack message, and one five-minute account window as interchangeable units.

Therefore:

- use the six `A_s` measures separately as adoption and compliance outcomes;
- use randomized access `Z` as the primary causal treatment;
- do not describe a weighted or standardized Hex index as "percent of work automated";
- reserve that interpretation for a workflow-time measure whose numerator and denominator are both minutes of eligible work.

### 2.2 Why the surface denominators cannot be added

Within one surface, `D_s` is the complete defined opportunity set and `N_s` is a subset of that same set, so `0 <= N_s <= D_s` and `0 <= A_s <= 1`. Across surfaces the dimensions differ:

```math
[D^{SF}]=queries,\quad[D^{Slack}]=messages,\quad [D^{Docs}]=[D^{Sheets}]=[D^{TP}]=[D^{Studio}]=five\text{-}minute\ windows
```

Even the window measures describe different applications, populations and source systems. A raw sum would give the most influence to whichever surface emits the most units, not to the surface that consumes the most SPL labor.

### 2.3 Surface definitions

| Surface | Unit | Numerator `N_s` | Denominator `D_s` | Rate |
|---|---|---|---|---|
| Snowflake | eligible native query record | query carries the `mcp` source tag | native query in an eligible account, passing query-type pruning and excluding types such as `ALTER_SESSION` | `A^{SF}=N/D` |
| Google Sheets | user/account × 5-minute UTC window | union window contains a successful allowlisted Coil Sheets write from ClickHouse | distinct union of Coil Sheets windows and native Drive spreadsheet-edit windows from Panther | `A^{Sheets}=N/D` |
| Google Docs | user/account × 5-minute UTC window | union window contains a successful `docs.documents.batchUpdate` Coil call | distinct union of Coil Docs windows and native Drive document-edit windows | `A^{Docs}=N/D` |
| Slack | posted message | status-OK MCP send or executed queue send, deduplicated by request or queue ID, scheduled sends excluded | Coil-attributed sends plus native and non-Coil messages after compatible attribution and deduplication | `A^{Slack}=C/(C+N)` |
| Team Platform | non-null actor × 5-minute UTC window | JobEvent window has a linked queue marker with source type `automation`, `agent` or `external` | distinct actor-windows on nondeleted JobEvents | `A^{TP}=N/D` |
| Studio v1 | native Studio account × 5-minute UTC window | window contains any authentication bearing the Coil Okta OAuth client ID | distinct account-windows with any native authentication across API routes | `A^{Studio}=N/D` |

#### Snowflake

Let `q` index native query records:

```math
D^{SF}_{pt}=\sum_q \mathbf 1\{q\text{ belongs to }(p,t),\ q\text{ is eligible}\}
```

```math
N^{SF}_{pt}=\sum_q \mathbf 1\{q\text{ is eligible},\ \mathrm{source}(q)=\texttt{mcp}\}
```

The newer method expands what counts as automated, because the older implementation discarded some MCP Snowflake calls. Changes across methodology versions are therefore not behavioral changes unless recomputed on a common definition.

#### Google Sheets and Google Docs

Let `b=(i,a,k)` be a person, account and five-minute UTC window. For surface `s`:

```math
C^s_b=\mathbf 1\{\text{a qualifying Coil event occurs in }b\}, \qquad G^s_b=\mathbf 1\{\text{a qualifying native Drive edit occurs in }b\}
```

```math
N^s_{pt}=\sum_{b\in(p,t)}C^s_b, \qquad D^s_{pt}=\sum_{b\in(p,t)}\mathbf 1\{C^s_b=1\lor G^s_b=1\}
```

The union denominator prevents a window present in both systems from being counted twice. Five-minute sessionization reduces distortion from different sampling and emission rates between ClickHouse and the native Drive API. It does not establish that a Coil window replaced all manual labor in that window.

#### Slack

Let `C_pt` be qualifying Coil sends and `N_pt` compatible native and non-Coil posted messages after attribution and deduplication:

```math
A^{Slack}_{pt}=\frac{C_{pt}}{C_{pt}+N_{pt}}
```

The older method did not include Coil sends in the total message opportunity set. Scheduling is excluded, so this rate must not be used as a measure of scheduled-agent adoption.

#### Team Platform

Let `b=(actor, five\text{-}minute\ window)`:

```math
J_b=\mathbf 1\{\text{at least one nondeleted JobEvent occurs in }b\}, \qquad K_b=\mathbf 1\{\text{a linked queue marker has source in } \{automation,agent,external\}\}
```

```math
A^{TP}_{pt} = \frac{\sum_{b\in(p,t)}J_bK_b}{\sum_{b\in(p,t)}J_b}
```

Sessionization prevents one automated task that emits many JobEvents from mechanically receiving more weight.

#### Studio v1

Let `b=(native\ account, five\text{-}minute\ window)`:

```math
T_b=\mathbf 1\{\text{any native Studio authentication occurs in }b\}, \qquad O_b=\mathbf 1\{\text{any authentication in }b\text{ bears the Coil OAuth client ID}\}
```

```math
A^{Studio}_{pt} = \frac{\sum_{b\in(p,t)}T_bO_b}{\sum_{b\in(p,t)}T_b}
```

The denominator includes reads, polling, setup, and requests that later fail. This is the share of authenticated Studio activity with Coil OAuth involvement, not the share of successful Studio work automated.

### 2.4 Active users, breadth and coverage

For person `i`, surface `s` and saved week `t`, a qualifying active user has a positive surface numerator on at least four distinct loaded UTC days:

```math
Active_{ist} = \mathbf 1\left\{ \sum_{d\in t}\mathbf 1(N_{isd}>0)\geq4 \right\}
```

```math
AU_{gst}=\sum_i \mathbf 1\{group_i=g,\ matchedFTE_i=1\}\,Active_{ist}, \qquad Breadth_{gst}=\frac{AU_{gst}}{People_g}
```

`People_g` is the full-time salaried roster count, including employees with no recorded activity. Because missing days cannot qualify, compare breadth only across complete saved weeks. The 2026-09-10 roster is applied retrospectively, so historical department breakouts can be misclassified after reorganizations.

For a requested date set `T`:

```math
Coverage_s(T) = \frac{\sum_{d\in T}\mathbf 1\{\text{surface }s\text{ loaded on }d\}}{|T|}
```

Missing days must remain missing; they are not zero-activity days. Do not compare surfaces on a nominal calendar period unless the actual loaded-day intersection is used, or missingness is explicitly modeled.

### 2.5 Saved snapshot values

Descriptive reconciliation checks, not model constants.

| Surface | Latest saved 7-day period | `N / D` | Rate | History loaded |
|---|---:|---:|---:|---:|
| Snowflake | 2026-09-04 to 2026-09-10 | 1,087,475 / 1,270,690 | 85.6% | 89/90 days |
| Google Sheets | 2026-09-04 to 2026-09-10 | 18,212 / 65,437 | 27.8% | 28/90 days |
| Google Docs | 2026-09-04 to 2026-09-10 | 1,456 / 28,811 | 5.1% | 28/90 days |
| Slack | 2026-09-03 to 2026-09-09 | 142,768 / 507,419 | 28.1% | 90/90 days |
| Team Platform | 2026-09-04 to 2026-09-10 | 4,155 / 7,173 | 57.9% | 90/90 days |
| Studio v1 | 2026-09-07 to 2026-09-13 | 15,640 / 155,645 | 10.0% | 89/90 days |

Studio's displayed 90-day summary is 129,316 Coil OAuth windows over 1,504,297 total windows, or 8.6%, across 655 accounts with activity from 2026-06-16 through 2026-09-13.

### 2.6 What each metric can and cannot identify

| Metric | Defensible interpretation | Not defensible |
|---|---|---|
| `A_s` | Within-surface share of observed eligible activity carrying the specified Coil marker | Percent of SPL labor automated |
| `Breadth_s` | Share of rostered employees using the surface numerator on four or more loaded days | Share of employees made productive |
| `N_s` | Volume of Coil-attributed units under that surface definition | Hours saved |
| `D_s` | Surface-specific observed opportunity set | A common opportunity set across surfaces |
| `Coverage_s` | Completeness of the saved time series | Evidence that missing days had zero activity |

---

## 3. Are the existing metrics of SPL work good enough?

This section answers the question per metric rather than in general, so the answer can be argued with or overridden item by item.

### 3.1 Verdict vocabulary

Every metric is assigned exactly one role. Most measurement disputes on this project are really disputes about role, not about data quality.

| Role | Meaning | Can it carry the headline? |
|---|---|---|
| Primary outcome | The result the study is designed to estimate | Yes |
| First stage / compliance | Evidence that the rollout changed behavior | No |
| Guardrail (non-inferiority) | Must not get worse; a null is the pass condition | No |
| Diagnostic | Used to debug the pipeline or interpret an estimate | No |
| Not usable | Should not be built on in its current form | No |

A metric can be excellent and still be unusable as an outcome. Surface activity rates are the clearest case: they are well defined and worth measuring, and they are still not productivity.

### 3.2 Weekly expert NPS

**Role: guardrail (non-inferiority). Not an outcome.**

The expectation that NPS will show no significant effect is probably right, and it is not a problem, because NPS is not being asked to show an effect. It is being asked to rule out harm to the expert experience.

That reframing has a consequence that needs handling before launch. A null result only certifies safety if the study could have detected a harm worth caring about. So the minimum detectable effect must be computed first, from actual pod-week response counts:

```math
\mathrm{MDE}\approx \left(z_{1-\alpha/2}+z_{\mathrm{power}}\right) \sigma_{\mathrm{NPS}} \sqrt{\frac{1}{n_1}+\frac{1}{n_0}}
```

If the MDE turns out larger than the smallest NPS movement anyone would act on, which is likely at weekly pod grain with partial response, then NPS cannot certify safety on its own and a second experience guardrail is required. The two candidates are both census measures rather than samples, so they carry far more information per pod-week:

- client and expert escalation counts;
- expert attrition or drop-off from the pod.

Report NPS with response rate and respondent composition every period. A shift in who answers can move the score without any change in experience.

### 3.3 Weekly time-use survey

**Role: primary source for baseline manual minutes. Requires a validation pass first.**

The doubt about this data is well placed, and it matters more than it looks, because the survey sits on the critical path. Baseline manual minutes per workflow, `M_w`, is the weight that makes the workflow-time automation share dimensionally valid, and `M_w` has to be frozen before treatment. The survey is currently the only instrument that can produce it. So survey trust is not a side question to resolve later; it gates the measure the study eventually wants to report.

Validation design, runnable in two to three weeks on a volunteer subsample:

1. Pair the self-report against an independent measure for the same person-week: calendar time, app-derived time, or both.
2. Report the within-person correlation and the direction of bias, not just the average gap. Recall error that is stable per person is far less damaging than error that varies with workload.
3. Apply the decision rule below.

| Validation result | What the survey may be used for |
|---|---|
| Strong within-person correlation, stable bias | Levels: `M_w` in minutes |
| Weak correlation, or bias that moves with workload | Rankings only: order workflows by time, do not use minute levels |
| No usable relationship | Replace with a task-audit time study on a sample of workflows |

The middle row is the realistic outcome and it is worth planning for. Rankings tolerate far more measurement error than levels do, and a ranking is still enough to choose which workflows to instrument first. It is not enough to compute a weighted automation share.

### 3.4 App usage and surface automation shares

**Role: first stage and compliance. Never an outcome.**

The concern that these do not correspond to productivity is correct, and the design already depends on it being true: the six Hex surface rates appear only as first-stage outcomes that test whether assigned access changed behavior. Definitions are in section 2.

One addition worth making explicit. These metrics decide whether the study is interpretable at all. If the rollout moves none of the surface rates, the correct conclusion is that the experiment had no uptake, not that automation had no effect. Without a first stage, a null on the primary outcome cannot be distinguished from a failed intervention. That makes the surface rates load-bearing even though they can never be the result.

They also must not be summed, for the reasons in section 2.2.

### 3.5 What the existing metric set does not contain

None of the three existing sources measures SPL output volume: delivered or accepted work units attributable to a pod-week. That is the quantity most likely to respond to automation inside the study window, and its absence is the real gap in the existing metrics, more than the noise in any one of them.

### 3.6 Proposed new metrics

Each proposal is scored on when it must exist, because that determines whether it can delay the study. The retention analysis behind the middle column is in section 4.

| Proposal | Must exist before treatment? | Notes |
|---|---|---|
| Discrete workflow taxonomy | Partly | Split it; see 3.7 |
| Telemetry and app-derived time use | Depends on source retention | Verify retention per source before assuming |
| Added time-use survey questions | Yes | Baseline cannot be recovered afterwards |

### 3.7 Discrete workflows: split the concept

The workflow proposal is really two measures with two different deadlines, and treating them as one is what creates the false choice between instrumenting properly and launching soon.

**Workflow labeling** — assigning a retained event to a workflow — is a classifier applied to stored data. It is fully reconstructable after the fact, as long as the raw events and join keys survive. This does not need to block anything.

**Baseline manual minutes** — the `M_w` weight — is a pre-treatment measurement of how long the work took before automation touched it. Once a pod is treated, its baseline is gone. This is not reconstructable, and it is the only part of the workflow build with a hard pre-launch deadline.

So the answer to whether workflows can be constructed after the fact is: the taxonomy yes, the weights no. Freezing a rough `M_w` on the current survey before the first wave is more valuable than a precise one built afterwards, because a post-treatment weight is endogenous to the treatment it is supposed to measure.

### 3.8 Telemetry and app-derived time

App-derived time is attractive because it avoids recall error, and it carries two problems worth stating in advance. Time with an application open is not time working in it. And automation can reduce app time without reducing cognitive load, so a fall in app time is not automatically a fall in human attention.

Its feasibility as a retroactive measure depends entirely on how long each source keeps raw records. That is a question with a factual answer per source, and the answer should be obtained rather than assumed.

### 3.9 Added survey questions

The cheapest proposal to build, and the one with the longest effective lead time, because a new question yields a usable baseline only after a full pre-treatment period in field. Any question needed for a pre/post comparison has to ship before the first wave.

### 3.10 Consequence for the outcome hierarchy

There is a threat to the primary outcome that comes from contract structure rather than from measurement, and it should be resolved before the analysis plan is frozen.

Contribution per SPL FTE responds to automation only if pod revenue can respond to SPL effort within the study window. Where revenue is fixed by contract, milestone, or priced off delivered expert hours, reducing SPL time does not raise the numerator at all in the short run. The estimate is then driven almost entirely by movement in the denominator, and a null result would say more about pricing than about productivity.

This is not the same as the outcome-lag threat. Lag means the response is slow; this means the response may be structurally absent for the duration of the study.

Recommended ordering, subject to a check of how pods are actually priced:

1. **Primary:** an SPL-effort-responsive operational outcome, such as SPL minutes per delivered unit or comparable projects supported per SPL FTE.
2. **Confirmatory:** contribution per SPL FTE, over a longer horizon than the operational outcome.
3. **Guardrails:** quality, delivery and experience, each reported separately.

The check is small and should happen early: classify the eligible pods by pricing model and count how many have revenue that could move within the window. If most cannot, the economic outcome becomes a long-run confirmatory measure and the study needs an operational primary.

---

## 4. What can be built after the fact?

If new measures are needed, can they be constructed retroactively so the rollout is not delayed? Mostly yes, and the exceptions are few enough to list. But the reasoning that gets there needs one correction, because the usual version is slightly too optimistic.

### 4.1 The premise needs tightening

The standard argument is that any metric housed in a data store that is not deleted over time can be reconstructed later. That is correct as stated. The difficulty is that "not deleted over time" is an assumption about each source, not a property of data stores in general, and it fails in two distinct ways.

**Deletion.** Event sources with finite retention windows drop raw records on a rolling basis. Once the window passes, no amount of later effort recovers the period.

**Overwrite.** A table that is never deleted can still destroy history by being updated in place. A current-state roster, org chart or pod mapping holds only today's truth; last quarter's assignment is simply gone, replaced rather than removed. This failure mode is easy to miss because the table still exists and still looks complete.

Both failures are already visible in the current measurement stack rather than hypothetical:

- The September 2026 Hex snapshot loaded only 28 of 90 days of Google Docs history. That is a retention or load-coverage gap in a source the study depends on.
- The same snapshot applies 2026-09-10 organizational labels to historical activity, because effective-dated mapping does not exist yet. That is an overwrite problem, and it means past pod membership currently cannot be reconstructed at all.

So the conclusion holds with a condition attached: metrics are reconstructable later if their sources are durable **and** their keys are effective-dated, and at least one of those two conditions does not hold today.

### 4.2 Bucket A: reconstructable later, no action required

Raw events already land in a durable warehouse with stable identifiers, so the definitions on top of them can change as often as needed.

| Variable | Source | Why it is safe |
|---|---|---|
| Surface numerators and denominators | Snowflake and warehouse event tables | Raw events retained; definitions are a view |
| Workflow labeling (`workflow_id`, eligibility) | Classifier over retained events | Labeling is post-hoc by construction |
| Tool-call telemetry, failure rates | Warehouse telemetry | Event grain preserved |
| Finance revenue and cost | Finance system of record | Closed periods are versioned, not overwritten |
| Delivery, QC and rework outcomes | Operational systems | Transactional records |

Workflow labeling belongs here, and that is the most useful single conclusion for the sequencing question. The taxonomy can be designed and applied months after the rollout starts without costing the study anything.

### 4.3 Bucket B: reconstructable only if something is captured now

These sources are durable enough to query today and will not answer the same question in six months. They need a capture job before the first wave, not a redesign.

| Variable | Risk | Action needed now |
|---|---|---|
| Person to pod to project assignment | Overwrite: current-state mapping only | Begin slowly-changing-dimension capture with effective dates |
| SPL allocation shares | Overwrite | Snapshot weekly and version |
| Studio auth activity | Deletion: log-source retention window | Archive to warehouse on a schedule |
| Slack activity history | Deletion: analytics history limits | Archive to warehouse on a schedule |
| Google Docs and Sheets edit history | Deletion: already showing a 28/90-day gap | Extend load window; archive |
| Project maturity, type, pricing model | Overwrite | Capture as effective-dated attributes |
| Roster and full-time labels | Overwrite | Version the roster weekly |

Two things make this bucket the priority. It is the only bucket where the cost of waiting is silent: nothing fails, the data simply stops existing for the period nobody captured. And the work is small, being scheduled archival and effective-dated capture rather than new instrumentation.

Before relying on any row above, get the actual retention window from the source owner and record it. These are questions with factual answers, and the answers determine how urgent each capture job is.

### 4.4 Bucket C: not reconstructable, must precede treatment

These require a human to report, or a measurement to be taken, while the pod is still untreated. After the first wave the untreated state no longer exists to be measured.

| Variable | Why it cannot wait |
|---|---|
| Baseline manual minutes per workflow (`M_w`) | Defined as pre-treatment duration; a later measurement is endogenous to treatment |
| New time-use survey questions | Pre/post comparison requires a pre-period in field |
| App-derived time-use baseline | Same; needs a pre-treatment window |
| Workflow automation eligibility (`eligible_w`) | Must be declared before outcomes are seen, or selection enters the denominator |
| Randomization assignment and strata | Assignment is only exogenous if frozen before outcomes |
| Pre-period standardization moments for the adoption index | Must come from untreated periods |

This is the complete launch-blocking list, and it is short. Nothing in it requires new engineering: it is one survey change, one time study, one eligibility review, and an assignment table.

### 4.5 Sequencing consequence

The three buckets imply a rollout that does not wait for the measurement build.

1. **Before wave 1:** everything in bucket C, plus the capture jobs in bucket B. The expensive-sounding work — workflow taxonomy, telemetry pipelines, attention measurement — is not here.
2. **During rollout:** bucket A definitions get built and refined against retained events. Definitions may change; the underlying data does not.
3. **After signal is established:** the workflow-time automation share and attention measures get constructed retroactively over the full study period, including its earliest weeks.

The only irreversible decision is what gets measured before the first pod is treated. Most of what looks like prerequisite work is not.

### 4.6 Standing requirement

Every analytical row must remain joinable through effective-dated keys:

```text
person_id → SPL assignment → pod_id → project_id → client/account_id
assignment_start <= event_time < assignment_end
```

A current-state org chart cannot satisfy this. Effective-dated capture is what moves the mapping variables out of bucket B and makes retroactive reconstruction possible at all.

---

## 5. Formulas and methodology

### 5.1 Notation

| Symbol | Meaning |
|---|---|
| `p` | pod |
| `t` | week or other consistent period |
| `w` | mutually exclusive workflow |
| `i` | SPL |
| `s` | surface |
| `Z` | assigned rollout |
| `A` | automation or adoption exposure |
| `F` | SPL full-time-equivalent capacity |
| `Y` | contribution output |
| `P` | SPL economic leverage |
| `H` | human attention per completed unit |
| `Q` | quality or delivery guardrail |

### 5.2 The formula stack

| Level | Output | Function | Inputs | Unit | Used for |
|---:|---|---|---|---|---|
| 0 | surface numerator `N_s` | source-specific classification and deduplication | raw event records | query, message or 5-minute window | input to `A_s` |
| 0 | surface denominator `D_s` | source-specific eligible opportunity rule | native and Coil records | same unit as `N_s` | input to `A_s` |
| 1 | surface share `A_s` | `N_s / D_s` | `N_s`, `D_s` | within-surface proportion | first-stage outcome |
| 1 | active-user breadth `B_s` | `AU_s / People` | qualifying active users, roster | employee proportion | adoption breadth |
| 1 | data coverage `K_s` | loaded days / selected days | load-status calendar | proportion | validity check |
| 2 | adoption index `U` | mean pre-period-standardized `A_s` | vector of surface shares | baseline standard deviations | optional compliance summary |
| 2 | SPL capacity `F` | allocation shares, or hours over standard hours | effective-dated staffing | FTE | economic denominator |
| 2 | contribution output `Y` | revenue less non-SPL variable delivery cost | finance records | dollars | economic numerator |
| 3 | SPL leverage `P` | `Y / F` | contribution output, SPL FTE | dollars per SPL FTE | descriptive economic KPI |
| 3 | human attention `H` | SPL minutes over completed units | time and workflow completion | minutes per unit | mechanism outcome |
| 4 | rollout effect `tau` | coefficient on randomized access in `ln(P)` | `P`, `Z`, fixed effects | log points | primary causal estimate |
| 4 | first stage `pi_s` | coefficient on `Z` in each `A_s` | `A_s`, `Z` | surface-share points | confirms changed behavior |
| 4 | automation effect `beta` | coefficient on rollout-predicted credible exposure | `P`, predicted `A` | semi-elasticity | secondary IV estimate |

### 5.3 Measured source variables

**Assignment and identity.** `Z_pt` indicates that pod or project `p` is assigned access by period `t`. Identities `pod_id`, `project_id` and `person_id` must be canonical and stable, and `a_ipt` is the allocation share of SPL `i` to pod `p` in period `t`. Events are attributed only when

```math
start_{ip}\leq eventTime_i<end_{ip}
```

**Surface events.** For each surface, preserve

```math
(unitId_s,\ personId,\ accountId,\ eventTime,\ sourceMarker,\ success, \ eligibility,\ botFlag,\ definitionVersion)
```

**Labor and finance.** `L_ipt` is SPL hours attributed to pod `p`; `R_pt` is recognized revenue; `C_pt` is non-SPL variable delivery cost; `c^SPL_t` is fully loaded SPL cost per FTE-period, needed only for a dollar net-value measure.

**Workflow and quality.** `V_pwt` is completed occurrences of workflow `w`; `M_w` is pre-treatment manual minutes per occurrence; `S_pwt` is the fraction of baseline minutes displaced by automation; `Q^j_pt` is guardrail `j`, retaining numerator and denominator when it is a rate.

### 5.4 Adoption and automation exposure

#### Surface shares

```math
A^s_{pt}=\frac{N^s_{pt}}{D^s_{pt}}
```

Valid within surface, not across surfaces, for the dimensional reason given in section 2.2. Use the six shares as separate adoption and compliance outcomes.

#### Standardized adoption index

If one scalar summary is needed for power or reporting, standardize each surface using only pre-treatment moments:

```math
\widetilde A^s_{pt}=\frac{A^s_{pt}-\mu^s_0}{\sigma^s_0}, \qquad U_{pt}=\frac{1}{|\mathcal S^0_p|} \sum_{s\in\mathcal S^0_p}\widetilde A^s_{pt}
```

Here `mu^s_0` and `sigma^s_0` are the surface mean and standard deviation from the pre-treatment reference period, and `S^0_p` is the set of surfaces designated relevant for pod `p` before rollout.

Why standardize: a one-point change in Snowflake's query share is not commensurate with a one-point change in Docs windows. Standardization expresses each movement in its own baseline standard-deviation units before averaging.

What `U` is not: it is not the percent of tasks, time or labor automated. Label it a **multi-surface adoption index** and use it only to summarize compliance or improve power. The expression "a 10-percentage-point increase in `U`" is undefined.

#### The ideal workflow-time measure

```math
EligibleMinutes_{pt}=\sum_{w\in\mathcal E}V_{pwt}M_w, \qquad DisplacedMinutes_{pt}=\sum_{w\in\mathcal E}V_{pwt}M_wS_{pwt}
```

```math
A^{time}_{pt}=\frac{\sum_{w\in\mathcal E}V_{pwt}M_wS_{pwt}}{\sum_{w\in\mathcal E}V_{pwt}M_w}
```

Why this denominator adds coherently: every summand carries the same unit.

```math
[V_{pwt}M_w]=workflowUnits\times\frac{minutes}{workflowUnit}=minutes
```

The numerator is the same minutes multiplied by a displacement share between zero and one, so `A^time` is bounded between 0 and 1. This is the first cross-surface measure that can defensibly be called "percent of eligible SPL work automated."

The construction is valid only when all five of these hold:

1. Workflow occurrences are mutually exclusive and not double-counted.
2. Numerator and denominator contain the same eligible workflows and period.
3. Manual-time weights are fixed from a pre-treatment baseline.
4. Eligibility is defined before treatment outcomes are observed.
5. `S` represents labor displaced, not merely AI involvement.

### 5.5 SPL labor input

Allocation form:

```math
F_{pt}=\sum_i a_{ipt},\qquad 0\leq a_{ipt}\leq1
```

Hours form:

```math
F_{pt}=\frac{\sum_iL_{ipt}}{StandardHours_t}
```

The denominator prevents a person supporting multiple pods from being counted as a full SPL in every one of them. For a fully allocated SPL, allocation shares should satisfy `sum_p a_ipt = 1` over overlapping intervals. Use allocation shares when reliable time records do not exist, and hours for workflow-level attention analysis when they are credible.

### 5.6 Economic output and SPL leverage

```math
Y_{pt}=R_{pt}-C_{pt}
```

`C_pt` excludes SPL labor, because SPL labor appears explicitly as the productivity input `F`. If the Finance extract already subtracts SPL labor, either add it back for this model or use a separately named contribution measure, so the same input is not subtracted in the numerator and divided in the denominator.

All revenue and cost must share the same pod or project assignment, accounting period, recognition convention, currency and cost boundary. Do not label `Y` as official company gross profit unless Finance's cost boundary matches.

```math
P_{pt}=\frac{Y_{pt}}{F_{pt}}
```

This is contribution dollars supported per SPL FTE. It captures both channels automation could work through: more output with the same SPL resources, or the same output with fewer.

The ratio embeds a substantive restriction:

```math
\ln(P_{pt})=\ln(Y_{pt})-\ln(F_{pt})
```

A log-ratio regression therefore fixes the elasticity of output with respect to SPL labor at one. Always show a robustness model that estimates that elasticity instead of assuming it:

```math
\ln(Y_{pt}) = \alpha_p+\lambda_t+\tau Z_{pt}+\gamma\ln(F_{pt})+\delta'X_{pt}+\varepsilon_{pt}
```

If staffing changes because of treatment, realized `F_pt` is a post-treatment mechanism, not a confounder. The ratio is a policy-relevant total-leverage outcome; the production model is a conditional-output specification. Report both and label the distinction rather than treating them as interchangeable.

Fallback outcomes, in descending order of preference:

```math
P^{Revenue}_{pt}=\frac{R_{pt}}{F_{pt}}, \qquad P^{Projects}_{pt}=\frac{\mathrm{ComparableActiveProjects}_{pt}}{F_{pt}}
```

Revenue per SPL is easier to construct but ignores delivery cost. Projects per SPL needs a defensible complexity adjustment, and is the most likely to respond within the study window for the reason given in section 3.10.

For investment decisions rather than operational leverage, use a dollar net-value measure:

```math
NV_{pt}=Y_{pt}-c^{SPL}_tF_{pt}-Cost^{tool}_{pt}-Cost^{implementation}_{pt}
```

`NV` answers whether the intervention paid for itself. `P` answers whether an SPL supports more value. These are different questions.

### 5.7 Human attention

```math
H_{pwt}=\frac{SPLMinutes_{pwt}}{CompletedWorkflowUnits_{pwt}}
```

This measures the scarce input automation is intended to reduce. Exception handling, quality review and rework minutes must stay in the numerator, or the metric rewards automations that merely shift effort downstream.

### 5.8 Estimands

#### Primary: intention to treat

```math
\ln(P_{pt}) = \alpha_p+\lambda_t+\tau Z_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

```math
\mathrm{RolloutLift}=100\left(e^{\tau}-1\right)\%
```

`tau` estimates the effect of being assigned the rollout, regardless of adoption. This is preferred because `Z` is randomized and has a common definition, while the six surface rates do not share a unit. Assignment is also not selected by performance, whereas observed usage is: high-performing pods can choose to adopt more.

#### Surface first stages

```math
A^s_{pt} = \alpha^s_p+\lambda^s_t+\pi_s Z_{pt}+\theta_s'X_{pt}+\nu^s_{pt}
```

`pi_s` is the rollout-induced percentage-point change on surface `s`. Report the full prespecified set, adjusting for multiple testing, or declare one primary surface before seeing outcomes based on the intervention's intended mechanism.

#### Summary first stage

```math
U_{pt}=\alpha_p+\lambda_t+\pi_UZ_{pt}+\theta'X_{pt}+\nu_{pt}
```

`pi_U` is measured in baseline standard deviations, not percentage points.

#### Secondary: rollout-instrumented automation effect

Use instrumental variables only with a prespecified, substantively credible scalar exposure: `A^time`, one primary surface, or clearly labeled `U`.

```math
A^*_{pt}=\alpha_p+\lambda_t+\pi Z_{pt}+\theta'X_{pt}+\nu_{pt}
```

```math
\ln(P_{pt}) = \alpha_p+\lambda_t+\beta\widehat A^*_{pt}+\delta'X_{pt}+\varepsilon_{pt}
```

`beta` is the local average treatment effect among pods whose exposure responds to assignment, under the standard relevance, exclusion, independence and monotonicity assumptions. Because `A*` is a share and is not logged, `beta` is a semi-elasticity, not an elasticity. The familiar expression

```math
\mathrm{Lift}_{10pp}=100\left(e^{0.10\beta}-1\right)\%
```

is valid only when `A*` is a 0-to-1 share, and approximately `10 beta` percent for small effects. It is not valid for the standardized index `U`.

#### Mechanism

```math
\ln(H_{pwt}) = \alpha_{pw}+\lambda_t+\tau_HZ_{pt}+\delta'X_{pwt}+\varepsilon_{pwt}
```

Successful labor-saving rollout implies `tau_H < 0`.

#### Dynamic effects

Expect learning and organizational adjustment, so estimate an event study around assigned rollout:

```math
\ln(P_{pt}) = \alpha_p+\lambda_t +\sum_{k\neq-1}\beta_k\,1[t-T_p=k] +\delta'X_{pt}+\varepsilon_{pt}
```

Pre-treatment coefficients examine parallel trends and anticipation. Post-treatment coefficients show whether effects appear immediately or only after workflows and staffing adapt.

### 5.9 Why log, and when not to log

For a positive outcome,

```math
\ln(P_1)-\ln(P_0)=\ln\left(\frac{P_1}{P_0}\right)
```

so the estimand is proportional rather than dollar-level, which is more comparable across pods of different sizes, and usually reduces right skew. With a binary randomized treatment, exact percent lift is `100(e^tau - 1)`.

Do not log `P <= 0`. Prespecify one of: a levels model for contribution per SPL; inverse hyperbolic sine as a sensitivity analysis, interpreted carefully; a positive operational outcome such as revenue or completed quality-adjusted units; or a two-part analysis separating the probability of positive contribution from its magnitude. Never drop non-positive observations silently.

### 5.10 Guardrails

For each guardrail `j`:

```math
g_j\!\left(E[Q^j_{pt}]\right) = \alpha^j_p+\lambda^j_t+\tau^j_QZ_{pt}+\delta_j'X_{pt}
```

| Outcome | Suggested form | Desired direction |
|---|---|---|
| One-shot acceptance | Binomial/logit or linear probability | Non-negative |
| Delivery yield | Binomial/logit or linear probability | Non-negative |
| Rework rate | Binomial/logit | Non-positive |
| Failures and escalations | Poisson or negative binomial where variance supports it | Non-positive |
| QC score | Levels model | Non-negative |
| Expert NPS | Levels model with respondent and composition checks | Non-negative |

Preserve every quality numerator and denominator. Do not average unlike guardrails into an unvalidated quality-adjusted composite.

### 5.11 Controls and fixed effects

`alpha_p` removes time-invariant pod differences such as persistent client mix or baseline operating style. `lambda_t` absorbs firm-wide changes, seasonality and shared product releases. `X_pt` holds prespecified time-varying factors such as maturity, pricing or externally driven demand.

Avoid controlling for variables caused by treatment when estimating a total treatment effect. SPL hours, staffing changes, workflow volume and demand served may be mechanisms rather than confounders.

---

## 6. Experiment design

### 6.1 Objective

Estimate whether an intervention that increases SPL automation causes:

1. higher Coil involvement on the prespecified Hex surfaces;
2. lower human attention per workflow;
3. higher contribution output supported per SPL;
4. no deterioration in quality, delivery or expert experience.

Estimands are specified in section 5.8. Rollout mechanics are in section 7.

### 6.2 Treatment definition

Record each of these separately, because collapsing them is what makes a rollout uninterpretable afterwards:

- eligibility;
- assigned rollout cohort and date;
- actual access or enabled date;
- intervention type and intensity;
- actual adoption and automation;
- cross-pod sharing or contamination.

Do not define treatment solely as observed usage. High-performing pods may self-select into adoption, so a usage-defined treatment measures selection as much as effect.

### 6.3 Outcome hierarchy

**Primary.** Contribution output before SPL labor cost, per SPL FTE — subject to the pricing check in section 3.10, which may promote an operational outcome to primary instead.

**Mechanism.** Human attention per completed workflow; rework-inclusive SPL minutes; manual interventions per workflow.

**Secondary.** Revenue per SPL FTE; comparable projects supported per SPL; setup, ramp and cycle time; capacity released and redeployed.

**Guardrails.** One-shot acceptance; QC score and rework; delivery yield and SLA performance; expert NPS and satisfaction; client escalations; automation failure and human override rates.

### 6.4 Minimum viable rollout

Before launch, require only:

1. versioned assignment and rollout dates;
2. stable effective-dated pod and project mapping;
3. preserved raw automation events;
4. SPL allocation or FTE;
5. one viable economic or operational outcome;
6. one quality guardrail.

Workflow taxonomy can be constructed later; manual-minute weights cannot, because a weight measured after treatment is endogenous to it. New survey questions and app-time measurement must be in field before treatment if they are needed for baseline comparison. The full split is in section 4.

### 6.5 Main threats

| Threat | Consequence | Mitigation |
|---|---|---|
| Spillovers | Controls receive treatment indirectly | Cluster randomization; track sharing |
| Adoption selection | Strong pods both adopt and perform better | Use assigned rollout, not usage alone |
| Changing pod membership | Misattributes events and outcomes | Effective-dated mappings |
| Incommensurate surface units | A combined rate is dominated by arbitrary query, message or window volume | Separate first stages; optional standardized index; no summed rate |
| Surface measurement error | Attenuates or distorts the automation effect | Versioned definitions; surface validation; workflow and time subsample |
| Snapshot coverage gaps | Missing days are mistaken for zero usage | Coverage flags; common loaded-day windows; do not impute zero |
| Current roster applied historically | Reorganizations misclassify past departments | Effective-dated pod and person mapping |
| Anticipation | Pods change before their assigned date | Conceal timing where practical; inspect pre-treatment leads |
| Attrition and reorganization | Composition changes after treatment | Preserve assignment; report balance and attrition |
| Outcome lag | Revenue does not react immediately | Mechanism outcomes plus event-study horizon |
| Revenue insensitive to SPL effort | The primary economic outcome cannot respond within the window, so a null reflects pricing rather than productivity | Classify pods by pricing model; lead with an effort-responsive operational primary and treat contribution per FTE as confirmatory |
| Few randomized units | Cluster-robust standard errors over-reject and results look more significant than they are | Randomization inference as the primary test; stratify for balance |
| Shared access credential | Assignment and realized access diverge unobservably; borrowed access is indistinguishable from non-adoption | Identity-based gating with access logging; assignment frozen independently of the gate |
| Multiple testing | Selective positive findings | Prespecify primary outcome and guardrails |
| Low power | Noisy pod metrics hide real effects | Power analysis using pre-period variance |

### 6.6 Decision rule

Do not commit to a full workflow telemetry build before confirming all four of these:

- the rollout moves at least one prespecified surface metric or the adoption index;
- pod mapping and SPL denominators are sufficiently reliable;
- a plausible primary outcome has adequate variation and power;
- the result would change a product or deployment decision.

---

## 7. Rollout mechanics

The batched rollout is the simplest part of this study, and it stays simple as long as three decisions are made deliberately: what gets randomized, how access is gated, and how inference is done given how few units there are.

### 7.1 Unit of randomization

The working proposal is to take the pool of SPLs and randomize with respect to project and account. That is right, with one distinction that decides the whole design: whether project and account are **strata**, with individuals randomized and balanced across them, or the **randomized unit** itself, with whole projects assigned together.

The difference only matters when a project has more than one SPL. If two SPLs on the same project land in opposite arms, the treated one shares prompts, agents and templates with the control one, and the control is no longer a control.

So the choice is an empirical question, answerable today:

| Finding | Unit | Reason |
|---|---|---|
| Most projects have one SPL | Individual SPL, stratified by project type, account and maturity | Individual assignment already is cluster assignment; maximum power |
| Many projects have several SPLs | Project or account cluster | Within-project contamination would otherwise destroy the contrast |
| Mixed | Cluster on project, stratify on account and maturity | Safe under both; costs some power |

**Action:** count SPLs per project and per account over the last complete quarter. That distribution picks the unit, and nothing else about the design depends on the choice.

Regardless of unit, stratify on the variables that predict the outcome — project maturity, project type, scale and baseline adoption — and randomize rollout timing within strata.

### 7.2 Access gating

Password protection is a reasonable instinct and the wrong mechanism, for a reason that has nothing to do with security.

A shared password cannot tell you who used the tool. It cannot distinguish an SPL who was assigned access and chose not to use it from an SPL who borrowed a colleague's password, and those two cases pull the estimate in opposite directions. Passwords also get shared, which is not a hypothetical failure in a population that collaborates by design.

Gate on identity instead, using a per-SPL feature flag or entitlement with access logged:

- every access attempt is attributed to a person, so contamination becomes an observed variable rather than an assumption to argue about;
- exact first-access timestamps per person are recorded, which is the input the event study in section 5.8 needs anyway;
- revoking or extending access for one person does not require re-gating everyone.

This is not more work than a password. It is the same gate keyed to the identity that already exists.

One rule holds whichever gate is chosen: **the assignment record must be frozen independently of the gate.** Access gates get adjusted ad hoc by whoever administers them, and if assignment is inferred from the gate's current state, the study loses its intention-to-treat basis. Record assignment once and never overwrite it with realized access.

### 7.3 Waves

Use a stepped-wedge or batched rollout in which every eligible unit is eventually treated. This is worth preferring on two grounds beyond the statistical ones: nobody is asked to be permanently excluded from a tool their peers have, and each unit contributes both treated and untreated periods, which absorbs persistent unit-level differences.

Practical rules:

- randomize timing within strata, not across the whole pool;
- keep the assigned date even if a unit is slow to adopt;
- avoid announcing individual dates far in advance, so units do not change behavior before treatment starts;
- inspect pre-treatment event-study coefficients for anticipation regardless.

### 7.4 Inference with few units

This is the part most likely to be underestimated. The SPL pool is small, and cluster-robust standard errors are badly behaved with few clusters: they over-reject, so results look more significant than they are. Roughly forty clusters is where the usual asymptotics start to be trusted, and this study may have fewer.

Use randomization inference as the primary basis for p-values:

1. hold the realized outcomes fixed;
2. re-draw assignment thousands of times using the exact randomization procedure, strata included;
3. compare the realized estimate to the resulting distribution.

This is exact under the sharp null and does not depend on cluster counts. Report cluster-robust standard errors alongside it for readability, not as the primary test.

Two supporting choices matter at this scale. Stratification buys more through balance than through power, so stratify on anything that plausibly predicts the outcome. And prespecify the primary outcome and guardrails before assignment, since with few units the temptation to search across outcomes is strongest and the cost of doing so is highest.

### 7.5 Power, and what is needed to compute it

Power can be computed now, from existing data, because the only inputs that matter are the pre-period variance of the chosen primary outcome and the number of units. Neither requires the intervention to exist.

For a clustered design with `J` units, `m` periods each, and intra-cluster correlation `rho`:

```math
\mathrm{MDE} = \left(z_{1-\alpha/2}+z_{\mathrm{power}}\right) \sqrt{\frac{\sigma^2}{J\,\bar\pi(1-\bar\pi)}} \sqrt{\frac{1+(m-1)\rho}{m}}
```

where `sigma^2` is the residual variance of the outcome after unit and period fixed effects, and `pi-bar` is the share of unit-periods treated under the wave schedule.

| Input | Where it comes from |
|---|---|
| `J` | Unit count from the SPL-per-project distribution in 7.1 |
| `m` | Study length in weeks |
| `sigma^2` | Residual variance of the primary outcome in the pre-period |
| `rho` | Within-unit correlation in the pre-period |
| `pi-bar` | Wave schedule |

Run this for each candidate primary outcome before choosing one. An outcome whose MDE exceeds any effect size worth acting on should not be the primary outcome, however much it is the one people want to see. This is the same test applied to expert NPS in section 3.2, and it should be applied to the economic outcome too.

### 7.6 Pre-launch checklist

1. SPL-per-project distribution computed; randomization unit chosen.
2. Strata defined from pre-treatment variables only.
3. Identity-based access gating in place, with access logging.
4. Assignment table frozen, independent of the gate.
5. Effective-dated person, pod and project capture running.
6. Bucket C measures in field: baseline manual minutes, added survey items, workflow eligibility.
7. Power computed per candidate outcome; primary outcome and guardrails prespecified.
8. Randomization script saved, so the same procedure can be replayed for inference.

---

## 8. Engineering data contract

This section translates the design into datasets engineers can build and economists can audit. The core rule is that every estimate must be reproducible from immutable source events plus effective-dated mappings.

### 8.1 Canonical grains

| Dataset | One row per | Purpose |
|---|---|---|
| `raw_surface_event` | emitted native or Coil source event | Preserve immutable source telemetry |
| `surface_unit` | canonical query, message, or surface-specific 5-minute window | Apply comparable within-surface numerator and denominator logic |
| `workflow_occurrence` | completed SPL workflow unit | Connect usage to an eligible job-to-be-done and its outcome |
| `person_pod_assignment` | person × pod × effective interval | Allocate SPL labor and events without duplicating people |
| `experiment_assignment` | randomized unit × rollout wave | Preserve intention-to-treat assignment |
| `pod_week_finance` | pod × accounting week | Supply revenue and consistently bounded variable cost |
| `pod_week_quality` | pod × week × quality measure | Supply guardrails without collapsing unlike outcomes |
| `pod_week_analysis` | pod × week | Final economic estimation panel |

The minimum viable study needs the assignment, mapping, raw-surface-event, canonical-surface-unit, finance, quality and analysis tables. `workflow_occurrence` is the richer second phase.

### 8.2 Minimum viable schemas

#### `experiment_assignment`

| Field | Type | Rule |
|---|---|---|
| `randomized_unit_id` | string | Stable pod, project or person identifier used at assignment |
| `pod_id` | string | Nullable only if project or person is the randomized unit |
| `project_id` | string | Nullable only if pod or person is the randomized unit |
| `rollout_wave` | string | Prespecified batch or cohort |
| `assigned_treatment` | boolean | Never replace with realized usage |
| `assignment_at` | timestamp | Frozen assignment time |
| `eligible_at_assignment` | boolean | Defined before outcomes are observed |
| `strata` | object or string | Variables used in randomization |

#### `person_pod_assignment`

| Field | Type | Rule |
|---|---|---|
| `person_id` | string | Stable SPL identifier |
| `pod_id` | string | Stable pod identifier |
| `role` | string | Allows explicit SPL filtering |
| `effective_start` | timestamp | Inclusive |
| `effective_end` | timestamp | Exclusive; null only for current assignment |
| `allocation_share` | decimal | Between 0 and 1 |
| `source_system` | string | Staffing system, time system or approved manual map |
| `mapping_version` | string | Reproducibility and backfill tracking |

For a fully allocated SPL over an overlapping interval, allocation shares across pods should sum to 1. Temporary under-allocation may be allowed but must be flagged.

#### `raw_surface_event`

| Field | Type | Rule |
|---|---|---|
| `event_id` | string | Unique, immutable identifier |
| `event_at` | timestamp | UTC source time |
| `person_id` | string | Actor responsible for the work |
| `surface` | string | Slack, Google Docs, Snowflake, and so on |
| `tool_name` | string | Canonical tool identifier |
| `source_marker` | string | Native, MCP, queue, OAuth client, and so on |
| `is_bot` | boolean | Bots excluded or reported separately by policy |
| `success` | boolean | Call-level reliability measure |
| `classification_version` | string | Prevents silent historical changes |
| `workflow_occurrence_id` | string | Nullable in the MVP; required for the workflow model |

#### `surface_unit`

| Field | Type | Rule |
|---|---|---|
| `surface_unit_id` | string | Stable key after surface-specific deduplication and sessionization |
| `surface` | string | Snowflake, Sheets, Docs, Slack, Team Platform or Studio |
| `unit_type` | string | Query, posted message, or 5-minute window |
| `unit_start_at` | timestamp | UTC; window floor where applicable |
| `person_id`, `account_id`, `actor_id` | string | Preserve the identities each surface definition requires |
| `numerator_flag` | boolean | Unit satisfies the documented Coil-involvement rule |
| `denominator_flag` | boolean | Unit is in the documented opportunity set |
| `definition_version` | string | Must change when eligibility, deduplication or markers change |
| `loaded_date` | date | Enables coverage and gap checks |

The precise rules differ by surface; see section 2.3. A single generic `is_automated` classifier is not sufficient to reconstruct the saved snapshot.

#### `pod_week_finance`

| Field | Type | Rule |
|---|---|---|
| `pod_id` | string | Same canonical ID used by mappings |
| `week_start` | date | Same calendar used throughout the panel |
| `recognized_revenue` | currency decimal | Document the recognition convention |
| `non_spl_variable_cost` | currency decimal | Explicit cost boundary |
| `currency` | string | Convert using a versioned FX table if needed |
| `finance_close_version` | string | Supports restatements and auditability |

#### `pod_week_quality`

Store one row per metric rather than forcing unlike measures into a composite.

| Field | Type | Rule |
|---|---|---|
| `pod_id`, `week_start` | keys | Match the analysis panel |
| `metric_name` | string | QC, rework, one-shot acceptance, SLA, NPS, and so on |
| `numerator`, `denominator` | numeric | Preserve the counts behind rates where applicable |
| `metric_value` | numeric | Published value |
| `source_system` | string | Lineage |
| `definition_version` | string | Definition stability |

### 8.3 Source-to-model lineage

| Source | Staging | Intermediate | Mart |
|---|---|---|---|
| ClickHouse, Snowflake, Datadog, Aurora events | `stg_raw_surface_event` | `int_surface_unit` → `int_surface_pod_week` | `pod_week_analysis` |
| Org and staffing mappings | `stg_person_pod_assignment` | `int_surface_pod_week` | `pod_week_analysis` |
| Finance and project data | `stg_pod_finance` | — | `pod_week_analysis` |
| QC and delivery systems | `stg_pod_quality` | — | `pod_week_analysis` |
| Rollout assignment | `stg_experiment_assignment` | — | `pod_week_analysis` |
| JTBD taxonomy and time study | `stg_workflow_occurrence` | `int_workflow_automation` | `pod_week_analysis` |
| Raw surface events (second pass) | `stg_raw_surface_event` | `int_workflow_automation` | `pod_week_analysis` |

#### Join order

1. Join each person-level event to `person_pod_assignment` using both `person_id` and the event's effective timestamp.
2. If a person has simultaneous pod allocations, multiply attributed event and time measures by `allocation_share`, unless a direct project or pod tag gives a stronger assignment.
3. Convert raw events to canonical surface units using the exact query, message or window rule for that surface.
4. Aggregate to pod-week only after bot policy, identity matching, deduplication, coverage, definition version and failures are explicit.
5. Join finance, quality and rollout tables at their declared pod-week grain.
6. Preserve unmatched records in audit tables; do not silently discard them.

### 8.4 Metric transformations

Construct one rate per surface from its canonical units:

```math
A^s_{pt} = \frac{\sum_{u\in(s,p,t)}\mathbf{1}(numerator_u=1)}{\sum_{u\in(s,p,t)}\mathbf{1}(denominator_u=1)}
```

Do not aggregate `N_s` or `D_s` across surfaces. Publish six separate rates. If a single compliance outcome is needed, compute the standardized index from section 5.4 in the analysis layer, freezing the relevant surface set and the standardization moments before treatment.

The pod-week analysis mart should expose the untransformed components as well as the ratios:

- numerator and denominator count for every surface;
- canonical unit type, inclusion and exclusion waterfall, loaded days, and definition version;
- qualifying four-or-more-day active-user count and full-time roster denominator;
- SPL hours and allocation-derived FTE;
- recognized revenue and each included cost component;
- six surface rates, optional standardized adoption index, contribution output, and output per SPL FTE;
- quality numerators and denominators;
- rollout assignment and realized access.

Econometric transforms such as `ln(P)` belong in the analysis layer, not the canonical warehouse mart. This keeps the raw business metric interpretable and makes non-positive values visible.

### 8.5 Required validation tests

**Identity and range.** `event_id` is unique and non-null. Effective assignment intervals for a person and pod do not overlap unexpectedly. `0 <= allocation_share <= 1`, and overlapping shares do not exceed 1 beyond a documented tolerance. `0 <= surface_share <= 1` for every surface. Rate numerators never exceed denominators.

**Reconciliation.** Raw source events reconcile to each surface's canonical units through a documented deduplication and sessionization waterfall. Saved-snapshot checks reconcile to the published September 2026 `N`, `D`, rate and loaded-day totals in section 2.5. Finance components reconcile to the approved finance extract at project and period level. Pod-week SPL FTE reconciles to the staffing total. Bot exclusion, failure handling and each surface's contribution are shown as waterfall counts.

**Experiment integrity.** One immutable assignment per randomized unit. No pre-assignment outcomes attributed to treatment. Treatment and control balance on prespecified baseline covariates. Missing mappings and missing outcomes reported by arm. Spillovers and cross-pod SPL assignments flagged.

**Definition stability.** Every backfill records source and classifier versions. Historical values do not change without a versioned restatement. All dashboard labels include numerator, denominator, exclusions, grain and refresh date.

### 8.6 Staged implementation

**Phase 0, audit what exists.** Freeze the saved Hex snapshot and document all six source universes. Reconcile each surface to its published numerator, denominator, rate and coverage checks. Version the bot, failure, scheduling, OAuth, queue-marker, eligible-query, union-window and roster policies. Produce the effective-dated SPL-to-pod mapping.

**Phase 1, minimum viable causal panel.** Build `experiment_assignment`, `person_pod_assignment`, `surface_unit` and `pod_week_analysis`. Add SPL FTE, finance contribution output, and at least one operational quality guardrail. Estimate intention to treat first; treat event automation as a secondary mediator.

**Phase 2, validate the usage proxy.** Compare each surface proxy with short time-use modules and sampled task audits. Estimate first stages separately by surface, using the standardized index only as a clearly labeled summary. Retain raw telemetry so metrics can be reconstructed once definitions mature.

**Phase 3, workflow production system.** Define mutually exclusive eligible workflows from the JTBD taxonomy. Collect pre-treatment manual minutes and workflow volume. Estimate displaced labor share, attention per completed unit, and workflow-level quality.

---

## 9. Variable catalog

### 9.1 Status vocabulary

- **Measured:** directly observed in a source system.
- **Derived:** calculated from measured variables.
- **Proxy:** observable but imperfect substitute for the intended construct.
- **Proposed:** requires a new mapping, field, survey or instrumentation path.
- **Under revision:** exists, but should not currently be treated as source of truth.

### 9.2 Inventory

| Symbol / variable | Meaning | Role | Status | Current or candidate source | Grain | Proxy for, or limitation |
|---|---|---|---|---|---|---|
| `tool_calls` | Total agent tool-call events | Adoption diagnostic | Measured | ClickHouse and Snowflake tool-call telemetry | Event; user-day or week | Activity, not productivity or labor displacement |
| `DAU` | Daily active agent users | Adoption diagnostic | Derived | User-level telemetry | Day | Breadth of adoption, not depth or value |
| `weekly_calls` | Calls per user per week | Adoption diagnostic | Derived | Tool-call telemetry | User-week | Usage intensity; affected by surface event volume |
| `tool_breadth` | Distinct tools used | Adoption diagnostic | Derived | Tool-call telemetry | User-week | Breadth of use, not automation |
| `failure_rate` | Failed calls over attempted calls | Reliability guardrail | Derived | Tool-call telemetry | Surface-week | Technical success, not task success |
| `N^SF`, `D^SF`, `A^SF` | MCP-tagged eligible queries, all eligible native queries, and their ratio | Surface adoption | Measured and derived | Panther native query history; `mcp` source tag | Query; pod or group-week | Query-type and eligible-account pruning must be versioned |
| `N^Sheets`, `D^Sheets`, `A^Sheets` | Coil Sheets windows, union of Coil and native windows, and ratio | Surface adoption | Measured and derived | ClickHouse allowlisted writes; Panther Drive spreadsheet edits | User/account × 5-min window | Union and sessionization reconcile sampling rates but do not measure labor saved |
| `N^Docs`, `D^Docs`, `A^Docs` | Coil Docs windows, union of Coil and native windows, and ratio | Surface adoption | Measured and derived | Successful `docs.documents.batchUpdate`; Panther Drive document edits | User/account × 5-min window | Only 28 of 90 snapshot history days were loaded |
| `C^Slack`, `N^Slack`, `A^Slack` | Qualifying Coil sends, native and non-Coil messages, and `C/(C+N)` | Surface adoption | Measured and derived | Slack member analytics; Snowflake MCP and queue send data | Posted message; pod or group-week | Request and queue dedup; scheduling excluded |
| `N^TP`, `D^TP`, `A^TP` | Automated-origin JobEvent windows, all JobEvent actor-windows, and ratio | Surface adoption | Measured and derived | Aurora JobEvents and ActionsQueue via Fivetran and Snowflake | Actor × 5-min window | Sessionization avoids weighting one task by emitted event count |
| `N^Studio`, `D^Studio`, `A^Studio` | Coil-OAuth native auth windows, all native auth windows, and ratio | Surface adoption | Measured and derived | Datadog auth logs plus saved native-account cohort | Account × 5-min window | Includes reads, polling, setup, and later-failed requests |
| `U_pt` | Mean pre-treatment-standardized rate across a frozen surface set | Compliance summary | Derived and proposed | Six surface rates | Pod-week | Baseline-SD index, not percent of work automated |
| `surface_coverage` | Loaded days over selected days | Data validity | Derived | Snapshot load calendar | Surface-period | Missing days are gaps, not zeros |
| `surface_active_user` | Positive surface numerator on at least four distinct loaded UTC days in a saved week | Adoption breadth | Derived | Surface numerator plus employee roster | Person-surface-week | Cannot qualify on missing days |
| `surface_breadth` | Qualifying active users over full-time salaried roster | Adoption breadth | Derived | Surface activity plus roster | Group-surface-week | Snapshot uses 2026-09-10 labels for historical activity |
| `sub_department` | Organizational grouping | Join and control | Measured | User and org mapping | User-date | Current grouping is broader than pod |
| `pod_id` | Stable user or SPL to pod mapping | Required join key | Proposed and incomplete | Mapping work; project and org data | User-date | Pods and project assignments change over time |
| `workflow_id` | Mutually exclusive SPL task or workflow | Measurement unit | Proposed | SPL JTBD workbook and workflow classification | Workflow occurrence | Current telemetry is not consistently classified into workflows |
| `eligible_w` | Whether workflow `w` should be automated | Denominator rule | Proposed and derived | SPL JTBD review | Workflow-version | Must exclude intentional human judgment |
| `V_pwt` | Eligible workflow occurrence count | Automation weight and output | Proposed | Workflow and event pipeline | Pod-workflow-week | Requires non-overlapping occurrence definitions |
| `M_w` | Pre-treatment manual minutes per workflow occurrence | Automation weight | Proposed | Time-use study, telemetry validation | Workflow-version | Must be fixed pre-treatment to avoid endogenous weights |
| `S_pwt` | Fraction of baseline labor displaced by automation | Automation exposure | Proposed | Event state plus time validation | Pod-workflow-week | AI assistance is not automatically labor displacement |
| `time_survey` | Self-reported SPL time allocation | Mechanism and proxy | Measured but noisy | Weekly SPL time-use survey | SPL-week | Recall error and category inconsistency; see section 3.3 |
| `app_time` | Time spent in relevant apps and workflows | Mechanism and proxy | Proposed or partially measured | App telemetry; Insightful time logs | User-session | App-open time may not equal active work |
| `L_pt` | SPL labor hours assigned to pod | Labor input | Proposed and derived | Staffing allocation or time records | Pod-week | Requires valid allocation across concurrent pods |
| `F_pt` | SPL full-time equivalents assigned to pod | Denominator | Derived | SPL hours or allocation shares | Pod-week | Headcount without allocation overcounts shared SPLs |
| `R_pt` | Revenue attributable to pod | Economic input | Proposed join | Finance and project data | Pod-week or month | Must align recognition period and project ownership |
| `C_pt` | Non-SPL variable delivery costs | Economic input | Proposed join | Finance and project data | Pod-week or month | Cost boundaries must be documented and stable |
| `Y_pt` | Revenue minus non-SPL variable delivery costs | Contribution output | Derived | `R_pt - C_pt` | Pod-week or month | Not official gross profit unless Finance's boundary matches |
| `P_pt` | Contribution output supported per SPL FTE | Primary outcome | Derived | Finance plus staffing | Pod-week or month | Coarse; does not identify the workflow mechanism; see section 3.10 |
| `H_pwt` | SPL minutes per completed workflow unit | Mechanism outcome | Proposed | Time survey or telemetry plus workflow counts | Pod-workflow-week | Requires comparable output-unit definitions |
| `project_maturity` | Ramp or steady-state stage | Stratifier and control | Proposed join | Project metadata | Project-week | Treatment effects may differ sharply during ramp |
| `project_type` | Work or project category | Stratifier and control | Proposed join | Project metadata | Project | Must be known before treatment |
| `pricing_model` | How the project is priced | Stratifier and validity check | Proposed join | Finance and contracts | Project-period | Determines whether revenue can respond to SPL effort at all |
| `demand_volume` | Requested work volume | Control and context | Proposed join | Project and task systems | Pod-week | May itself respond to improved capacity over longer horizons |
| `team_mix` | SPL tenure, staffing and expert scale | Control and heterogeneity | Proposed join | HR, staffing and project data | Pod-week | Avoid post-treatment staffing controls in total-effect models |
| `Z_pt` | Randomized rollout assignment | Instrument and treatment | Proposed | Experiment assignment table | Pod or person-date | Must be assigned before outcomes and protected from spillovers |
| `Q_pt` | QC, yield, rework, satisfaction, SLA or escalation outcome | Guardrail | Mixed | Operational systems; expert NPS | Pod-week | Each quality measure needs its own model and direction |
| `expert_NPS` | Weekly expert recommendation score | Experience guardrail | Measured but noisy | Weekly expert NPS | Pod-week or respondent | Likely low power; composition and nonresponse sensitive; see section 3.2 |
| `spl_output_units` | Delivered or accepted work units attributable to a pod-week | Candidate primary outcome | Proposed | Delivery and QC systems | Pod-week | Currently absent; the main gap in the existing metric set |

### 9.3 Required keys

Every analytical row should be joinable through effective-dated keys, with the temporal constraint in section 4.6. A current-state org chart is insufficient for reconstructing past pod membership.

### 9.4 Source hierarchy

1. **Existing telemetry:** six separate surface metrics with distinct query, message and window definitions; tool calls, users and failure state.
2. **Existing surveys and operations:** SPL time-use survey, expert NPS, task quality, handling time, delivery and rework.
3. **New joins:** stable pod and project mapping, staffing allocation, finance outcomes, pricing model.
4. **New measurement:** workflow classification, baseline manual minutes, fraction of labor displaced.
5. **Experiment metadata:** assignment unit, rollout cohort, assignment date, eligibility, compliance.

### 9.5 Data preservation requirement

Retain raw, timestamped event data and versioned mappings even if the final workflow taxonomy is not ready before rollout. Historical reconstruction is possible only when raw events, stable IDs, classification versions and effective dates are all preserved. See section 4 for which variables this actually protects and which it does not.

---

## 10. Decisions required

### 10.1 Needed before the next sync

1. **Randomization unit, waves and intervention components.** Resolved by the SPL-per-project count in section 7.1.
2. **Effective-dated person, pod and project mapping, plus the SPL allocation source.**
3. **Finance numerator:** revenue recognition grain, and exactly which variable costs enter `C`.
4. **Primary economic outcome, primary Hex first stage, and the quality non-inferiority guardrail** — chosen after the MDE calculation in section 7.5 and the pricing-model check in section 3.10.

### 10.2 Owners and deadlines

| Decision | Proposed owner | Needed before |
|---|---|---|
| Canonical pod and project mapping | Research engineering plus data engineering | Phase 1 |
| Six versioned surface numerator and denominator definitions | Hex owner plus data engineering | Phase 1 |
| Finance cost boundary and recognition grain | Finance plus economist | Phase 1 |
| Pricing-model classification of eligible pods | Finance plus economist | Analysis plan freeze |
| Randomization unit, waves and eligibility | Economist plus program owner | Rollout |
| Identity-based access gating and access logging | Program owner plus engineering | Rollout |
| Retention audit and bucket B capture jobs | Data engineering | Rollout |
| Baseline manual minutes and survey additions | SPL operations plus research | Rollout |
| Primary quality guardrail | Operations plus economist | Analysis plan freeze |
| Workflow taxonomy | SPL operations plus research | Phase 3 |

---

## Appendix A. Sources and snapshot caveats

### Source material

- [Economics SSOT](https://docs.google.com/document/d/16jbeq72m4u3CS1JMkH2qZyb7a8ApT9O0ByHrtbZEnUc/edit)
- [SPL JTBD workbook](https://docs.google.com/spreadsheets/d/1uIXvx8xJy8CgHKKigtqQ2rNHvxBYeXmNlYw7zTmKNO0/edit)
- [Coil surface activity, saved snapshot, September 2026](https://app.hex.tech/500e8e3f-f94b-4ca6-9ba1-d07bdc8e4dfb/hex/Coil-surface-activity-saved-snapshot-September-2026-034Ni63vTasQW1Fe7W7I7w/draft/logic?threadLayout=collapsed&projectView=app&view=app)
- [Rex / Adina FDE sync](https://notes.granola.ai/t/ad9534c2-a48e-430d-9af0-f25d1a856894-008umkv4)
- Repository: `adinapak-mercor/spl-automation-economics`

### Standing caveats on the Hex snapshot

The September 2026 saved snapshot is not a live source. Its surface histories end on different dates. Missing days are gaps and must not be imputed as zero activity. Department and title labels as of 2026-09-10 are applied retrospectively to historical activity, so departmental breakouts can be misclassified across reorganizations. The snapshot itself states that units differ across surfaces and that there is no combined rate.
