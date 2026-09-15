# Notion-ready equation blocks

Paste each block into a Notion equation block. The prose labels explain the role of each measure.

## 1. Measurement system

```latex
\begin{gathered}
\textbf{Measured system:}\quad Z_{pt},\ \{A^s_{pt}\}_{s\in\mathcal S},\ H_{pt},\ P_{pt},\ Q_{pt}\\[8pt]
Z_{pt}=\text{rollout assignment},\quad
A^s_{pt}=\text{surface-specific Coil involvement},\quad
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

## 3. Hex surface metrics

```latex
\begin{gathered}
\boxed{A^s_{pt}=\frac{N^s_{pt}}{D^s_{pt}}},\qquad
s\in\{\mathrm{Snowflake,Sheets,Docs,Slack,TeamPlatform,Studio}\}\\[8pt]
[D^{SF}]=\mathrm{queries},\quad[D^{Slack}]=\mathrm{messages},\quad
[D^{other}]=\mathrm{surface\!\text{-}specific\ five\!\text{-}minute\ windows}\\[8pt]
\text{The six rates are valid within surface but cannot be pooled into one percentage.}
\end{gathered}
```

## 4. Ideal workflow-weighted automation measure

```latex
\begin{gathered}
\mathrm{EligibleManualMinutes}_{pt}=\sum_{w\in\mathcal E}V_{pwt}M_w\\[4pt]
\mathrm{DisplacedManualMinutes}_{pt}=\sum_{w\in\mathcal E}V_{pwt}M_wS_{pwt}\\[8pt]
\boxed{A^{time}_{pt}=\frac{\sum_{w\in\mathcal E}V_{pwt}M_wS_{pwt}}
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
\boxed{\ln(P_{pt})=\alpha_p+\lambda_t+\tau Z_{pt}+\delta'X_{pt}+\varepsilon_{pt}}\\[8pt]
\boxed{\mathrm{RolloutLift}=100\left(e^{\tau}-1\right)\%}\\[8pt]
\alpha_p=\text{pod fixed effects},\quad
\lambda_t=\text{week fixed effects},\\
X_{pt}=\text{prespecified time-varying confounders},\quad
Z_{pt}=\text{randomized assigned access}\\[8pt]
\text{The log converts level differences into proportional changes; }\tau\text{ is the ITT effect.}
\end{gathered}
```

## 7. Rollout and IV estimate

```latex
\begin{gathered}
\textbf{Intention-to-treat:}\qquad
\ln(P_{pt})=\alpha_p+\lambda_t+\tau Z_{pt}+\delta'X_{pt}+\varepsilon_{pt}\\[8pt]
\textbf{Surface first stages:}\qquad
A^s_{pt}=\alpha^s_p+\lambda^s_t+\pi_s Z_{pt}+\delta_s'X_{pt}+\nu^s_{pt}\\[8pt]
\textbf{Second stage:}\qquad
\boxed{\ln(P_{pt})=\alpha_p+\lambda_t+\beta\widehat A^{time}_{pt}+\delta'X_{pt}+\varepsilon_{pt}}\\[8pt]
\tau=\text{effect of offering access},\quad
\pi_s=\text{effect of rollout on surface }s,\quad
\beta=\text{effect for workflow-time-responsive units}
\end{gathered}
```

## 8. Human-attention mechanism

```latex
\begin{gathered}
\boxed{H_{pwt}=\frac{\mathrm{SPLMinutes}_{pwt}}
{\mathrm{CompletedWorkflowUnits}_{pwt}}}\\[8pt]
\ln(H_{pwt})=\alpha_{pw}+\lambda_t+\tau_HZ_{pt}+\delta'X_{pwt}+\varepsilon_{pwt}\\[6pt]
\text{Successful labor-saving rollout implies }\tau_H<0.
\end{gathered}
```

## 9. Quality guardrails

```latex
\begin{gathered}
g\!\left(\mathbb E[Q_{pt}]\right)
=\alpha_p+\lambda_t+\tau_QZ_{pt}+\delta'X_{pt}\\[8pt]
Q_{pt}\in\{\text{one-shot acceptance, rework, delivery yield, QC, SLA, expert outcomes}\}\\[4pt]
g=\text{identity for continuous outcomes, logit for binary/rate outcomes,}\\
\text{and Poisson or negative binomial links for counts when appropriate.}
\end{gathered}
```
