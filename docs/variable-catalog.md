# Variable catalog and lineage

## Status vocabulary

- **Measured:** directly observed in a source system.
- **Derived:** calculated from measured variables.
- **Proxy:** observable but imperfect substitute for the intended construct.
- **Proposed:** requires a new mapping, field, survey, or instrumentation path.
- **Under revision:** exists, but should not currently be treated as source-of-truth.

## Current variables

| Symbol / variable | Meaning | Role | Status | Current or candidate source | Grain | Proxy for / limitation |
|---|---|---|---|---|---|---|
| `tool_calls` | Total agent tool-call events | Adoption diagnostic | Measured | ClickHouse/Snowflake tool-call telemetry | Event; user-day/week | Activity, not productivity or labor displacement |
| `DAU` | Daily active agent users | Adoption diagnostic | Derived | User-level telemetry | Day | Breadth of adoption, not depth or value |
| `weekly_calls` | Calls per user per week | Adoption diagnostic | Derived | Tool-call telemetry | User-week | Usage intensity; affected by surface event volume |
| `tool_breadth` | Distinct tools used | Adoption diagnostic | Derived | Tool-call telemetry | User-week | Breadth of use, not automation |
| `failure_rate` | Failed calls divided by attempted calls | Reliability guardrail | Derived | Tool-call telemetry | Surface-week | Technical success, not task success |
| `N^SF`, `D^SF`, `A^SF` | MCP-tagged eligible queries, all eligible native queries, and their ratio | Surface adoption | Measured/derived | Panther native query history; `mcp` source tag | Query; pod/group-week | Query-type and eligible-account pruning must be versioned |
| `N^Sheets`, `D^Sheets`, `A^Sheets` | Coil Sheets windows, union of Coil/native spreadsheet windows, and ratio | Surface adoption | Measured/derived | ClickHouse allowlisted writes; Panther Drive spreadsheet edits | User/account × 5-minute UTC window | Union/sessionization reconciles sampling rates but does not measure labor saved |
| `N^Docs`, `D^Docs`, `A^Docs` | Coil Docs windows, union of Coil/native document windows, and ratio | Surface adoption | Measured/derived | Successful `docs.documents.batchUpdate`; Panther Drive document edits | User/account × 5-minute UTC window | Only 28/90 snapshot history days were loaded |
| `C^Slack`, `N^Slack`, `A^Slack` | Qualifying Coil sends, native/non-Coil messages, and `C/(C+N)` | Surface adoption | Measured/derived | Slack member analytics and Snowflake MCP/queue send data | Posted message; pod/group-week | Request/queue dedup; scheduling excluded |
| `N^TP`, `D^TP`, `A^TP` | Automated-origin JobEvent windows, all JobEvent actor-windows, and ratio | Surface adoption | Measured/derived | Aurora JobEvents/ActionsQueue via Fivetran/Snowflake | Actor × 5-minute UTC window | Sessionization avoids weighting one task by emitted event count |
| `N^Studio`, `D^Studio`, `A^Studio` | Coil-OAuth native auth windows, all native auth windows, and ratio | Surface adoption | Measured/derived | Datadog auth logs plus saved native-account cohort | Account × 5-minute UTC window | Includes reads, polling, setup, and later-failed requests |
| `U_pt` | Mean pre-treatment-standardized rate across a frozen relevant surface set | Compliance summary | Derived/proposed | Six surface rates | Pod-week | Baseline-SD index, not percent of work automated |
| `surface_coverage` | Loaded days divided by selected days | Data validity | Derived | Snapshot load calendar | Surface-period | Missing days are gaps, not zeros |
| `surface_active_user` | Positive surface numerator on at least 4 distinct loaded UTC days in saved week | Adoption breadth | Derived | Surface numerator plus employee roster | Person-surface-week | Cannot qualify on missing days |
| `surface_breadth` | Qualifying active users divided by full-time salaried roster | Adoption breadth | Derived | Surface activity plus roster | Group-surface-week | Snapshot uses 2026-09-10 labels for historical activity |
| `sub_department` | Organizational grouping | Join/control | Measured | User/org mapping | User-date | Current grouping is broader than pod |
| `pod_id` | Stable user/SPL-to-pod mapping | Required join key | Proposed/incomplete | Rex mapping work; project/org data | User-date | Pods and project assignments change over time |
| `workflow_id` | Mutually exclusive SPL task/workflow | Measurement unit | Proposed | SPL JTBD workbook and workflow classification | Workflow occurrence | Current telemetry is not consistently classified into workflows |
| `eligible_w` | Whether workflow `w` should be automated | Denominator rule | Proposed/derived | SPL JTBD review | Workflow-version | Must exclude intentionally human judgment |
| `V_pwt` | Eligible workflow occurrence count | Automation weight/output | Proposed | Workflow/event pipeline | Pod-workflow-week | Requires non-overlapping occurrence definitions |
| `M_w` | Pre-treatment manual minutes per workflow occurrence | Automation weight | Proposed | Time-use study, telemetry validation | Workflow-version | Must be fixed pre-treatment to avoid endogenous weights |
| `S_pwt` | Fraction of baseline labor displaced by automation | Automation exposure | Proposed | Event state plus time validation | Pod-workflow-week | AI assistance is not automatically labor displacement |
| `time_survey` | Self-reported SPL time allocation | Mechanism/proxy | Measured but noisy | Weekly SPL time-use survey | SPL-week | Recall error and category inconsistency |
| `app_time` | Time spent in relevant apps/workflows | Mechanism/proxy | Proposed or partially measured | App telemetry / Insightful time logs | User-session | App-open time may not equal active work |
| `L_pt` | SPL labor hours assigned to pod | Labor input | Proposed/derived | Staffing allocation or time records | Pod-week | Requires valid allocation across concurrent pods |
| `FTE_pt` | SPL full-time equivalents assigned to pod | Denominator | Derived | SPL hours or allocation shares | Pod-week | Headcount without allocation overcounts shared SPLs |
| `R_pt` | Revenue attributable to pod | Economic input | Proposed join | Finance/project data | Pod-week/month | Must align recognition period and project ownership |
| `C_pt` | Non-SPL variable delivery costs | Economic input | Proposed join | Finance/project data | Pod-week/month | Cost boundaries must be documented and stable |
| `Y_pt` | Revenue minus non-SPL variable delivery costs | Contribution output | Derived | `R_pt - C_pt` | Pod-week/month | Not official gross profit unless Finance's boundary matches |
| `P_pt` | Contribution output supported per SPL FTE | Primary outcome | Derived | Finance plus staffing | Pod-week/month | Coarse; does not identify the workflow mechanism |
| `H_pwt` | SPL minutes per completed workflow unit | Mechanism outcome | Proposed | Time survey/telemetry plus workflow counts | Pod-workflow-week | Requires comparable output-unit definitions |
| `project_maturity` | Ramp or steady-state stage | Stratifier/control | Proposed join | Project metadata | Project-week | Treatment effects may differ sharply during ramp |
| `project_type` | Work/project category | Stratifier/control | Proposed join | Project metadata | Project | Must be known before treatment |
| `demand_volume` | Requested work volume | Control/context | Proposed join | Project/task systems | Pod-week | May itself respond to improved capacity over longer horizons |
| `pricing` | Customer price or revenue model | Control | Proposed join | Finance/contracts | Project-period | Pricing changes affect output independently of automation |
| `team_mix` | SPL tenure, staffing and expert scale | Control/heterogeneity | Proposed join | HR/staffing/project data | Pod-week | Avoid post-treatment staffing controls in total-effect models |
| `Z_pt` | Randomized Studio/Monk rollout assignment | Instrument/treatment | Proposed | Experiment assignment table | Pod-date/week | Must be assigned before outcomes and protected from spillovers |
| `Q_pt` | QC, yield, rework, satisfaction, SLA or escalation outcome | Guardrail | Mixed | Operational systems; expert NPS | Pod-week | Each quality measure needs its own model and direction |
| `expert_NPS` | Weekly expert recommendation score | Experience guardrail | Measured but noisy | Weekly expert NPS | Pod/week or respondent | Likely low power and affected by composition/nonresponse |

## Required keys

Every analytical row should ultimately be joinable through effective-dated keys:

```text
person_id → SPL assignment → pod_id → project_id → client/account_id
```

Required temporal constraint:

```text
assignment_start <= event_time < assignment_end
```

A current-state org chart is insufficient for reconstructing past pod membership.

## Source hierarchy

1. **Existing telemetry:** six separate surface metrics with distinct query/message/window definitions; tool calls, users and failure state.
2. **Existing surveys/operations:** SPL time-use survey, expert NPS, task quality, AHT, delivery and rework.
3. **New joins:** stable pod/project mapping, staffing allocation and finance outcomes.
4. **New measurement:** workflow classification, baseline manual minutes and fraction of labor displaced.
5. **Experiment metadata:** assignment unit, rollout cohort, assignment date, eligibility and compliance.

## Data preservation requirement

Retain raw, timestamped event data and versioned mappings even if the final workflow taxonomy is not ready before rollout. Historical reconstruction is possible only when raw events, stable IDs, classification versions and effective dates are preserved.

## Hex snapshot caveat

The September 2026 saved snapshot explicitly states that units differ and there is no combined rate. Use [`hex-metric-specification.md`](hex-metric-specification.md) as the source for exact surface numerators, denominators, snapshot periods, history coverage, active-user logic, and definition differences from the original Hex.
