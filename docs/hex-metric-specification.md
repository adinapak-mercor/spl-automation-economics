# Hex surface metrics: exact definitions and research use

Source: [Coil surface activity · saved snapshot · September 2026](https://app.hex.tech/500e8e3f-f94b-4ca6-9ba1-d07bdc8e4dfb/hex/Coil-surface-activity-saved-snapshot-September-2026-034Ni63vTasQW1Fe7W7I7w/draft/logic?threadLayout=collapsed&projectView=app&view=app)

This is a saved snapshot, not a live source. Its surface histories end on different dates, missing days remain gaps, and current department/title labels as of 2026-09-10 are applied to historical activity.

## The most important implication

There is no mathematically defensible combined Hex automation percentage in this snapshot. Each surface has a different observational unit:

```math
A_{spt}=\frac{N_{spt}}{D_{spt}},\qquad s\in
\{\mathrm{Snowflake,Sheets,Docs,Slack,TeamPlatform,Studio}\}
```

`N_s` and `D_s` are valid only within surface `s`. Adding them across surfaces would treat one SQL query, one message, and one five-minute account window as interchangeable units.

Therefore:

- use the six `A_s` measures separately as adoption/compliance outcomes;
- use randomized access `Z` as the primary causal treatment;
- do not describe a weighted or standardized Hex index as “percent of work automated”;
- reserve that interpretation for a workflow-time measure whose numerator and denominator are both minutes of eligible work.

## Surface formula table

| Surface | Unit `u_s` | Numerator `N_s` | Denominator `D_s` | Surface rate |
|---|---|---|---|---|
| Snowflake | eligible native query record | query carries the `mcp` source tag | native query is in an eligible account and passes query-type pruning, excluding types such as `ALTER_SESSION` | `A^{SF}=N^{mcp-query}/D^{eligible-query}` |
| Google Sheets | user/account × five-minute UTC window | union window contains a successful allowlisted Coil Sheets write from ClickHouse | distinct union of Coil Sheets windows and native Drive spreadsheet-edit windows from Panther | `A^{Sheets}=N^{Coil-window}/D^{union-window}` |
| Google Docs | user/account × five-minute UTC window | union window contains a successful `docs.documents.batchUpdate` Coil call | distinct union of Coil Docs windows and native Drive document-edit windows from Panther | `A^{Docs}=N^{Coil-window}/D^{union-window}` |
| Slack | posted message | selected status-OK MCP send or executed queue send, deduplicated by request/queue ID; scheduled sends excluded | Coil-attributed sends plus native/non-Coil messages after compatible attribution and deduplication | `A^{Slack}=C/(C+N)` |
| Team Platform | non-null actor × five-minute UTC window | JobEvent window has any linked queue marker with source type `automation`, `agent`, or `external` | distinct actor-windows on nondeleted JobEvents | `A^{TP}=N^{automated-origin-window}/D^{jobevent-window}` |
| Studio v1 | native Studio account × five-minute UTC window | window contains any authentication with the Coil Okta OAuth client ID | distinct account-windows with any native authentication across API routes | `A^{Studio}=N^{Coil-OAuth-window}/D^{native-auth-window}` |

### Snowflake

Let `q` index native query records:

```math
D^{SF}_{pt}=\sum_q
\mathbf 1\{q\text{ belongs to }(p,t),\ q\text{ is eligible}\}
```

```math
N^{SF}_{pt}=\sum_q
\mathbf 1\{q\text{ is eligible},\ \mathrm{source}(q)=\texttt{mcp}\}
```

```math
A^{SF}_{pt}=\frac{N^{SF}_{pt}}{D^{SF}_{pt}}
```

The newer method expands what counts as automated because the older implementation discarded some MCP Snowflake calls. This means changes across methodology versions are not behavioral changes unless recomputed on a common definition.

### Google Sheets and Google Docs

Let `b=(i,a,k)` be a person/account/five-minute-UTC window. For surface `s`:

```math
C^s_b=\mathbf 1\{\text{a qualifying Coil event occurs in }b\}
```

```math
G^s_b=\mathbf 1\{\text{a qualifying native Drive edit occurs in }b\}
```

```math
N^s_{pt}=\sum_{b\in(p,t)}C^s_b,
\qquad
D^s_{pt}=\sum_{b\in(p,t)}\mathbf 1\{C^s_b=1\lor G^s_b=1\}
```

```math
A^s_{pt}=\frac{N^s_{pt}}{D^s_{pt}},
\qquad s\in\{\mathrm{Sheets,Docs}\}
```

The union denominator prevents a window present in both systems from being counted twice. Five-minute sessionization reduces distortion from different sampling/emission rates in ClickHouse and the native Drive API. It does not prove that a Coil window replaced all manual labor in the window.

### Slack

Let `C_pt` be qualifying Coil sends and `N_pt` compatible native/non-Coil posted messages after attribution and deduplication:

```math
A^{Slack}_{pt}=\frac{C_{pt}}{C_{pt}+N_{pt}}
```

The older method did not include Coil sends in the total message opportunity set. Scheduling is excluded, so this rate should not be used as a measure of scheduled-agent adoption.

### Team Platform

Let `b=(actor,five-minute-window)`:

```math
J_b=\mathbf 1\{\text{at least one nondeleted JobEvent occurs in }b\}
```

```math
K_b=\mathbf 1\{\text{a linked queue marker has source in }
\{automation,agent,external\}\}
```

```math
A^{TP}_{pt}
=
\frac{\sum_{b\in(p,t)}J_bK_b}
{\sum_{b\in(p,t)}J_b}
```

Sessionization prevents one automated task that emits many JobEvents from mechanically receiving more weight.

### Studio v1

Let `b=(native-account,five-minute-window)`:

```math
T_b=\mathbf 1\{\text{any native Studio authentication occurs in }b\}
```

```math
O_b=\mathbf 1\{\text{any authentication in }b\text{ bears the Coil OAuth client ID}\}
```

```math
A^{Studio}_{pt}
=
\frac{\sum_{b\in(p,t)}T_bO_b}
{\sum_{b\in(p,t)}T_b}
```

The denominator includes reads, polling, setup, and requests that later fail. This is specifically the share of authenticated Studio activity with Coil OAuth involvement, not the share of successful Studio work automated.

## Active-user and roster formulas

For person `i`, surface `s`, and saved week `t`, define a qualifying active user as someone with a positive surface numerator on at least four distinct loaded UTC days:

```math
Active_{ist}
=
\mathbf 1\left\{
\sum_{d\in t}\mathbf 1(N_{isd}>0)\geq4
\right\}
```

Department active users are:

```math
AU_{gst}=\sum_i
\mathbf 1\{group_i=g,\ matchedFTE_i=1\}\,Active_{ist}
```

`People_g` is the full-time salaried roster count, including employees without recorded activity. A useful breadth measure is:

```math
Breadth_{gst}=\frac{AU_{gst}}{People_g}
```

Because missing days cannot qualify, compare active-user breadth only for complete saved weeks. The 2026-09-10 roster is applied retrospectively, so historical department breakouts can be misclassified after reorganizations.

## Coverage and freshness

For a requested date set `T`:

```math
Coverage_s(T)
=
\frac{\sum_{d\in T}\mathbf 1\{\text{surface }s\text{ loaded on }d\}}
{|T|}
```

Missing days must remain missing; they are not zero-activity days. Do not compare surfaces on a nominal calendar period unless the actual loaded-day intersection is used or missingness is explicitly modeled.

## Saved snapshot values

These are descriptive checks, not model constants.

| Surface | Latest saved 7-day period | `N / D` | Rate | History loaded |
|---|---:|---:|---:|---:|
| Snowflake | 2026-09-04–2026-09-10 | 1,087,475 / 1,270,690 | 85.6% | 89/90 days |
| Google Sheets | 2026-09-04–2026-09-10 | 18,212 / 65,437 | 27.8% | 28/90 days |
| Google Docs | 2026-09-04–2026-09-10 | 1,456 / 28,811 | 5.1% | 28/90 days |
| Slack | 2026-09-03–2026-09-09 | 142,768 / 507,419 | 28.1% | 90/90 days |
| Team Platform | 2026-09-04–2026-09-10 | 4,155 / 7,173 | 57.9% | 90/90 days |
| Studio v1 | 2026-09-07–2026-09-13 | 15,640 / 155,645 | 10.0% | 89/90 days |

Studio's displayed 90-day summary is 129,316 Coil OAuth windows over 1,504,297 total windows, or 8.6%, across 655 accounts with activity from 2026-06-16 through 2026-09-13.

## What each metric can and cannot identify

| Metric | Defensible interpretation | Not defensible |
|---|---|---|
| `A_s` | Within-surface share of observed eligible activity carrying the specified Coil marker | Percent of SPL labor automated |
| `Breadth_s` | Share of rostered employees using the surface numerator on 4+ loaded days | Share of employees made productive |
| `N_s` | Volume of Coil-attributed units under that surface definition | Hours saved |
| `D_s` | Surface-specific observed opportunity set | A common opportunity set across surfaces |
| `Coverage_s` | Completeness of the saved time series | Evidence that missing days had zero activity |

## Research-safe ways to use the Hex data

### Primary: separate first stages

```math
A^s_{pt}
=
\alpha^s_p+\lambda^s_t+\pi_s Z_{pt}+\theta_s'X_{pt}+\nu^s_{pt}
```

Report `pi_s` for every prespecified surface and adjust for multiple testing or declare one primary surface based on the intervention's intended mechanism.

### Secondary: standardized compliance index

If one scalar is needed for power or summary, standardize every surface using only pre-treatment control-period moments:

```math
\widetilde A^s_{pt}
=
\frac{A^s_{pt}-\mu^s_0}{\sigma^s_0}
```

```math
U_{pt}=\frac{1}{|\mathcal S^0_p|}
\sum_{s\in\mathcal S^0_p}\widetilde A^s_{pt}
```

`S^0_p` is the pod's prespecified, pre-treatment relevant surface set. `U` is an adoption index measured in baseline standard deviations. It is not an automation percentage, so the expression “10-percentage-point increase in `U`” is invalid.

### Long-run target: common labor unit

Only the workflow-time construction supports a cross-surface percentage interpretation:

```math
A^{time}_{pt}
=
\frac{\sum_w V_{pwt}M_wS_{pwt}}
{\sum_w V_{pwt}M_w}
```

Both numerator and denominator are minutes of eligible baseline manual work, making the sum dimensionally coherent.
