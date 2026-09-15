# Notion-ready equation blocks

Paste each block into a Notion equation block. The prose labels explain the role of each measure.

## 1. Measurement system

```latex
\begin{gathered}
\textbf{Causal chain:}\quad Z_{pt}\rightarrow A_{pt}\rightarrow H_{pt}\rightarrow P_{pt},\qquad Q_{pt}\text{ is a guardrail}\\[8pt]
Z_{pt}=\text{rollout assignment},\quad
A_{pt}=\text{automation exposure},\quad
H_{pt}=\text{human attention},\\
P_{pt}=\text{economic output per SPL},\quad
Q_{pt}=\text{quality/delivery outcome}
\end{gathered}
```

## 2. Main business metric

```latex
\begin{gathered}
GP_{pt}=R_{pt}-C_{pt}\\[6pt]
\boxed{P_{pt}=\frac{GP_{pt}}{\mathrm{SPL\ FTE}_{pt}}}\\[8pt]
R_{pt}=\text{recognized pod revenue},\qquad
C_{pt}=\text{non-SPL variable delivery cost}\\
P_{pt}=\text{pod contribution supported per full-time-equivalent SPL}
\end{gathered}
```

## 3. Minimum viable automation proxy

```latex
\begin{gathered}
\boxed{A^{\mathrm{Hex}}_{pt}
=\frac{\mathrm{AutomatedEvents}_{pt}}
{\mathrm{AutomatedEvents}_{pt}+\mathrm{ManualComparatorEvents}_{pt}}}\\[8pt]
\text{Interpretation: share of comparable observed events classified as automated.}\\
\text{Limitation: event counts do not necessarily represent comparable workflows or labor saved.}
\end{gathered}
```

## 4. Ideal workflow-weighted automation measure

```latex
\begin{gathered}
\mathrm{EligibleManualMinutes}_{pt}=\sum_{w\in\mathcal E}V_{pwt}M_w\\[4pt]
\mathrm{DisplacedManualMinutes}_{pt}=\sum_{w\in\mathcal E}V_{pwt}M_wS_{pwt}\\[8pt]
\boxed{A_{pt}=\frac{\sum_{w\in\mathcal E}V_{pwt}M_wS_{pwt}}
{\sum_{w\in\mathcal E}V_{pwt}M_w}}\\[8pt]
V_{pwt}=\text{workflow volume},\quad
M_w=\text{pre-treatment manual minutes per unit},\\
S_{pwt}=\text{fraction of baseline manual labor displaced},\quad
0\leq A_{pt}\leq1
\end{gathered}
```

## 5. SPL labor denominator

```latex
\begin{gathered}
\mathrm{SPL\ FTE}_{pt}=\sum_i a_{ipt},\qquad
\sum_p a_{ipt}=1\ \text{for a fully allocated SPL}\\[8pt]
\text{or}\qquad
\mathrm{SPL\ FTE}_{pt}=\frac{\sum_i L_{ipt}}{\mathrm{StandardHours}_t}
\end{gathered}
```

## 6. Primary causal model

```latex
\begin{gathered}
\boxed{\ln(P_{pt})=\alpha_p+\lambda_t+\beta\widehat A_{pt}+\delta'X_{pt}+\varepsilon_{pt}}\\[8pt]
\boxed{\mathrm{Lift}_{10pp}=100\left(e^{0.10\beta}-1\right)\%}\\[8pt]
\alpha_p=\text{pod fixed effects},\quad
\lambda_t=\text{week fixed effects},\\
X_{pt}=\text{prespecified time-varying confounders},\quad
\widehat A_{pt}=\text{automation induced by rollout}\\[8pt]
\text{The log converts level differences into proportional changes; }\beta\text{ is a semi-elasticity.}
\end{gathered}
```

## 7. Rollout and IV estimate

```latex
\begin{gathered}
\textbf{Intention-to-treat:}\qquad
\ln(P_{pt})=\alpha_p+\lambda_t+\tau Z_{pt}+\delta'X_{pt}+\varepsilon_{pt}\\[8pt]
\textbf{First stage:}\qquad
A_{pt}=\alpha_p+\lambda_t+\pi Z_{pt}+\delta'X_{pt}+\nu_{pt}\\[8pt]
\textbf{Second stage:}\qquad
\boxed{\ln(P_{pt})=\alpha_p+\lambda_t+\beta\widehat A_{pt}+\delta'X_{pt}+\varepsilon_{pt}}\\[8pt]
\tau=\text{effect of offering access},\quad
\pi=\text{effect of rollout on automation},\quad
\beta=\text{effect for rollout-responsive units}
\end{gathered}
```

## 8. Human-attention mechanism

```latex
\begin{gathered}
\boxed{H_{pwt}=\frac{\mathrm{SPLMinutes}_{pwt}}
{\mathrm{CompletedWorkflowUnits}_{pwt}}}\\[8pt]
\ln(H_{pwt})=\alpha_{pw}+\lambda_t+\beta_HA_{pwt}+\delta'X_{pwt}+\varepsilon_{pwt}\\[6pt]
\text{Successful labor-saving automation implies }\beta_H<0.
\end{gathered}
```

## 9. Quality guardrails

```latex
\begin{gathered}
g\!\left(\mathbb E[Q_{pt}]\right)
=\alpha_p+\lambda_t+\beta_QA_{pt}+\delta'X_{pt}\\[8pt]
Q_{pt}\in\{\text{one-shot acceptance, rework, delivery yield, QC, SLA, expert outcomes}\}\\[4pt]
g=\text{identity for continuous outcomes, logit for binary/rate outcomes,}\\
\text{and Poisson or negative binomial links for counts when appropriate.}
\end{gathered}
```
