# A tail of labor supply and a tale of monetary policy

Dear Editor,
This note reports our responses to the feedback redecived from Refine.ink on 2026-02-18 with details of the minor changes we have made to the manuscript as a result

We report the original feedback plus our responses below.
**Legend**: **Done** = fully implemented. **Partial** = partially implemented. 


---

## Overall Feedback

Here are some overall reactions to the document.

**Defining the left-tail object under cyclical re-ranking**

A central challenge for the paper’s core narrative is establishing that the "left-tail" response is a behavior of low-income workers rather than a mechanical artifact of cyclical sorting. Because the headline evidence in Figure 2 relies on cumulative bins ($P_{\le J}$) constructed from monthly cross-sections (Section 2.1), the composition of these bins changes endogenously with the shock. A skeptical reader might wonder if the result is driven by workers moving *into* the bottom percentiles during a contraction, rather than the workers *at* the bottom increasing hours. This concern is particularly acute given that the ranking variable is an hourly wage observed in the ORG, and the Kansas Fed matched-CPS exercise relies on an imputation/ranking procedure (Appendix A) that could itself be cyclical.

To secure the "labor supply" interpretation against demand-side composition stories, the empirical design needs to isolate the estimand more rigorously. The current "supply vs. demand" discussion in Section 2.3 relies on the inverse movement of wages and hours, but in a re-ranked cross-section, this sign pattern can still arise from selection (e.g., job-mix changes or survivorship bias). The panel evidence in Figure 5 is a step in the right direction, but the argument would be much more persuasive if the estimand were explicitly defined using a "fixed/pre-shock rank" design. If the authors can demonstrate the same sign pattern when bins are defined by worker characeristics fixed *prior* to the shock, the interpretation of the mechanism would be significantly more robust.

**Structural isolation within the FAVAR architecture**

The FAVAR architecture described in Section 2.2 raises a question regarding the separation of the information set from the measurement targets. Currently, the factor-extraction panel $X_t$ appears to include the specific CPS distributional hours and earnings series that are also the outcomes of interest. There is a risk that the factor space becomes partially defined by these idiosyncratic distributional movements, potentially contaminating the macro factors and the VAR residuals used for proxy-IV identification. This is a subtle but critical issue when the main contribution is the *shape* of a distributional IRF.

It would be prudent to audit the sensitivity of the results to this design choice. A clean split-sample approach—estimating factors on a standard macro set (like FRED-MD) while excluding the CPS block, and then recovering the CPS IRFs via the measurement equation—would demonstrate that the results are not driven by "state definition." Furthermore, given the reliance on proxy-IV, the paper would benefit from a transparent audit of instrument relevance in the policy equation and sensitivity to the factor number $K$ relative to the generated regressor uncertainty, specifically for this application.

**Formalizing the contribution to the aggregate**

The claims regarding the "importance of the tail" in Section 2.3 could be tightened by moving from variance shares to a formal decomposition. Statements such as "16% of aggregate hours" or the comparison in Figure 3 (aggregate vs. aggregate excluding bottom 20%) are conceptually slippery because dropping a subgroup is not a valid general equilibrium counterfactual; it mechanically alters the level and composition of the aggregate. Without a precise identity-based decomposition, it is difficult to evaluate the claim that the tail "substantially dampens" the aggregate response.

A more effective presentation would decompose the *aggregate hours IRF* into non-overlapping group contributions, explicitly separating intensive-margin hours (conditional on employment) from employment-share movements. Since the structural section connects this mechanism to MPC and sacrifice-ratio differences, establishing a precise accounting identity in the empirical section is necessary to support the policy conclusions.

**Aligning the model-data mapping and policy counterfactuals**

The transition from the empirical "fact" to the structural model (Section 3) introduces several moving parts that make the comparison difficult to assess. First, the mapping between data bins and model groups is not immediate: the empirical section uses hourly-earnings percentiles ($P_{\le 5}$), while the model sorts agents by endogenous objects like productivity $e$ and assets $a$ (Figures 6–8). Since agents in the model re-rank after shocks, comparing model groups to data bins requires the same "fixed-rank" discipline mentioned earlier.

Second, the comparison between the heterogeneous labor supply model and the homogeneous benchmark (Tables 2–3) appears to change multiple parameters jointly ($\beta$, $\varphi$, $B$) and potentially the shock process itself. This opens the door to the critique that the differences in MPCs and sacrifice ratios are artifacts of retuning or closure choices rather than labor supply heterogeneity per se. The policy conclusions would be more compelling if the "like-for-like" comparison were more tightly controlled—holding steady-state targets and shock paths fixed where possible—and if the model's intensive-margin mechanism were explicitly reconciled with the extensive-margin dynamics (unemployment) observed in Figure 1.

[Sections separated by two newlines]

**Status**: [Partially addressed]

**Response**:
Added robustness recalibrating HANK-HomL by matching impact (period 0) aggregate labor L in HANK ; recomputed sacrifice ratios; added appendix table + main-text footnote linking to appendix (Appendix G.4). See also new footnote 25.
Regarding the fixed-rank mapping and broader empirical/model alignment points, we believe we have done our best give the data constraints we have.

---

## Detailed Comments (17)

### 1. Calibration of the Homogeneous Labor counterfactual

**Status**: [Addressed]

**Quote**:
> To ensure comparability, we calibrate both models to match the labor supply response of the median agent... Comparing this specification to a model with a homogeneous labor supply, we find that labor supply heterogeneity reduces the aggregate MPC and attenuates the transmission of monetary policy through aggregate demand. As a result, the output cost of disinflation is lower

**Feedback**:
The quantitative comparison between HANK and HANK-HomL hinges on the specific “comparability” criterion: calibrating HANK-HomL to match the *median* agent’s labor-supply response in HANK. This is a defensible way to isolate the left-tail mechanism, but it also means the sacrifice-ratio and aggregate-hours differences should be interpreted conditional on that targeting choice. It would help to clarify (and/or check robustness) how much of the “lower output cost of disinflation” result persists under alternative calibration targets more directly tied to aggregates (e.g., matching aggregate hours or output responses).

**Response**:
Done. Added robustness recalibrating HANK-HomL by matching impact (period 0) aggregate labor L in HANK ; recomputed sacrifice ratios; added appendix table + main-text footnote linking to appendix (Appendix G.4). See also new footnote 25.

---

### 2. Inconsistency in calibration of earnings risk and discount factor

**Status**: [Addressed]

**Quote**:
> Table 1: One-asset HANK calibration

**Feedback**:
There is an apparent mismatch in the definition of $\sigma_e$ between equation (6) and Table 1. Equation (6) defines $\sigma_e$ as the innovation standard deviation in $\log e_{it}=\rho_e \log e_{it-1}+\sigma_e \epsilon_{it}$ with $\epsilon_{it}\sim\mathcal N(0,1)$, while Table 1 labels $\sigma_e$ as the cross-sectional (stationary) standard deviation of log earnings (value 0.5). With $\rho_e=0.966$, these correspond to very different magnitudes (innovation SD around 0.13 vs unconditional SD around 1.9, depending on interpretation). It would help to clarify which object is being calibrated/used in the discretization and verify the implied stationary dispersion of log earnings used in the quantitative results.

**Response**:
Done. Clarified $\sigma_e$ definition in footnote 17. Table 1 reports stationary dispersion $\text{Std}(\log e)=\sigma_e$ and mapping to innovation SD $\sigma_{\epsilon,e}=\sigma_e\sqrt{1-\rho_e^2}$ (baseline $\approx 0.13$).

---

### 3. Inconsistent steady-state calibration parameters

**Status**: [Addressed]

**Quote**:
> | $\beta$ | Discount factor | 0.98 | $r=0.005$ |

**Feedback**:
Table 1 reports $\beta=0.98$ with a target $r=0.005$, which may confuse readers because (under a certainty representative-agent Euler equation) these numbers would not line up. In a HANK model with idiosyncratic risk and borrowing constraints, $r$ need not satisfy $1=\beta(1+r)$, and the table may also be mixing annual vs per-period conventions. It would help to clarify (i) the model period/annualization used for $\beta$ and $r$, and (ii) what exactly the “$r=0.005$” target refers to (e.g., an annualized real rate, or the equilibrium risk-free rate implied by the full heterogeneous-agent steady state).


**Response**:
Done. Clarified and modified accordingly Table 1.

---

### 4. Contradictory definition of earnings vs. wages

**Status**: [Addressed]

**Quote**:
> In each month of the sample that runs from 1985 to 2019, we extract individual-level data on hours worked and hourly real wages, with individuals sorted on labor earnings. ${ }^{6}$ Our measure of hours corresponds to hours worked in the previous week in all jobs. We use the consistent series for hourly wages in 2019 dollars created by CEPR as our measure of earnings.

**Feedback**:
The sorting variable is described inconsistently here: “sorted on labor earnings” usually means total labor income (e.g., $w\times h$), but the next sentence indicates you use a CEPR hourly wage series “as our measure of earnings,” and the bin definition later refers to “percentile of hourly earnings.” Since sorting on hourly wage versus total earnings can select different workers in the bottom tail, it would be helpful to state explicitly whether the bins are based on the hourly wage (hourly earnings) or on total labor income, and then use consistent terminology (“wage” vs “earnings/income”) throughout this subsection.

**Response**:
Done. Clarified that we use the consistent series for hourly wages in 2019 dollars created by CEPR as our measure of wage. Also clarified that the bins are based on labor earnings.

---

### 5. Mechanism of interest rate transmission to constrained agents

**Status**: [Addressed]

**Quote**:
> In particular, constrained or hand-to-mouth (HTM) households face a tighter intertemporal budget constraint and a wedge in their Euler equation, making their marginal utility of consumption highly sensitive to income fluctuations. By analyzing how borrowing constraints and the curvature of the utility function with respect to consumption affect the optimal choices of consumption and leisure, we show that monetary policy shocks can generate an increase in labor supply among constrained households, driven by income effects.

**Feedback**:
The “Euler-wedge/HTM” intuition risks being read as saying that constrained households’ labor supply reacts directly to the contemporaneous policy rate via the Euler equation. In the model timing, a strictly binding borrowing constraint shuts down the usual intertemporal-substitution margin, so the relevant link from monetary policy to poor households’ labor supply should be stated in terms of contemporaneous disposable income/cash-flow effects (e.g., via wages/transfers and via the realized real return on predetermined nominal asset/debt positions through inflation). It would help to clarify which of these channels is intended when attributing the result to the Euler wedge and “higher rates.”

**Response**:
Done. Reworded the HTM/Euler-wedge intuition to emphasize that when the borrowing constraint binds, the key link is contemporaneous cash-flow/wealth effects (wages/transfers and real return/burden on existing positions), not intertemporal substitution.

---

### 6. Interpretation of Real Rate channel in decomposition

**Status**: [Addressed]

**Quote**:
> The real rate (blue bars), instead, pushes aggregate labor supply up during the first two quarters. This is mainly due to the standard intertemporal substitution effect-less consumption today (more labor supply) versus more tomorrow. But there is also another channel through which higher rates increase labor supply today: an increase in the interest repayment of existing debt induces agents to work more.

**Feedback**:
The interpretation of the “real rate” (blue) contribution would benefit from a sharper distinction between (i) intertemporal-substitution effects operating through the Euler equation and (ii) contemporaneous cash-flow/wealth effects of $r_t$ on existing nominal asset/debt positions (and related fiscal flows). The text notes both, but for low-income/near-HTM bins it is easy to misread the blue bars as primarily “substitution,” whereas the debt-repayment / real burden channel is likely the key driver there. Clarifying what is included in the SSJ “real rate” input and how to interpret it across the distribution would reduce confusion.

**Response**:
Done. Clarified the SSJ “real rate” channel: the $r$ input holds $w$, Div, Tax fixed and combines substitution for unconstrained agents with cash-flow/debt-service effects for constrained agents (dominant in low-income bins).

---

### 7. Sign error in goods market clearing condition

**Status**: [Addressed]

**Quote**:
> $$Y_{t}=\int_{0}^{1} c_{i t} d i-\psi_{t}$$

**Feedback**:
The goods-market clearing condition appears to have the wrong sign on Rotemberg adjustment costs. With $\psi_t\ge 0$ defined as a real resource cost and with dividends defined as $d_t=Y_t-w_tH_t-\psi_t$, aggregate accounting implies $C_t=Y_t-\psi_t$, i.e. $Y_t=C_t+\psi_t$ (abstracting from government spending/investment). As written, $Y_t=\int_0^1 c_{it}di-\psi_t$ would instead imply $C_t=Y_t+\psi_t$, which treats adjustment costs as adding resources.

**Response**:
Done. Fixed the sign in the goods-market clearing condition so Rotemberg costs use resources ($Y=C+\psi$).

---

### 8. Counter-intuitive HTM share response in Figure G.22

**Status**: [Addressed]

**Quote**:
> Figure G.22: Impulse Responses of Core Macroeconomic Variables: HANK-HomL vs HANK

**Feedback**:
The “Hand-to-Mouth” panel in Figure G.22 is surprising: HTM share rises sharply in HANK while staying near flat in HANK-HomL, even though low-income households’ ability to raise hours in HANK helps dampen the aggregate consumption decline. This may be consistent with households defending consumption by dissaving (or with debt-service effects pushing more agents to the constraint), but the appendix does not define precisely how HTM is measured or which households drive the change. It would be useful to (i) confirm the model labels in this panel and (ii) clarify the HTM definition/mechanism behind the larger increase in HANK.

**Response**:
Done. Defined HTM explicitly as the fraction at the borrowing limit $a=\underline{a}$ and explained that this pattern is consistent with households smoothing the contraction by dissaving/borrowing, which shifts more mass to the constraint even as low-income households increase labor effort.

---

### 9. Potential weighting bias in FAVAR factor extraction

**Status**: [Addressed]

**Quote**:
> We construct a pseudo panel using earning percentile groups. We split the population into two groups, $P_{\leq J}$ and $P_{>J}$ where $J$ ranges from 5 to 95 with increments of 5. For example, when $J=5, P_{\leq 5}$ refers to the group that consists of respondents who fall below that 5th percentile of hourly earnings. Our panel includes $P_{\leq J}$ for $J=5, \ldots 95$ capturing the cumulative distribution.
[^2]We also include quintile bins

**Feedback**:
The pseudo-panel construction uses overlapping cumulative groups $P_{\le J}$ (and the footnote mentions also quintile bins). It is not fully clear which of these series are included in $X_t$ for factor estimation, and if cumulative bins are included, the survey block becomes highly collinear/redundant. Depending on scaling/standardization, this could affect the estimated factor space and how “common” versus group-specific movements are separated. It would help to clarify exactly which percentile-group series enter $X_t$ for PCA and whether the results are robust to using only mutually exclusive bins (e.g., quintiles/deciles) rather than many cumulative cutoffs.

**Response**:
Done. Clarified that the dataset used for estimation combines aggregate and income-group-level data, considering one percentile split at a time, i.e. $P_{\leq 5}$ and $P_{> 5}$. We therefore estimate a separate empirical model for each percentile split.

---

### 10. Mismatch between text/title and figure content in G.25

**Status**: [Addressed]

**Quote**:
> Figure G.25: Contribution of each income bin to the aggregate response.
(b) Contribution of each income bin to the aggregate response.
![](/documents/ae22fb7f-bd18-48e2-8232-3906368397f1/images/image_047.jpg)

(c) Consumption
![](/documents/ae22fb7f-bd18-48e2-8232-3906368397f1/images/image_048.jpg)

**Feedback**:
The description around Figure G.25 suggests a decomposition of the aggregate impact into contributions from different income bins. However, the figure title/panel labels as shown here do not make clear where the income-bin dimension is represented, and (depending on the embedded plot’s legend/axes) it may instead look like the standard marginal-channel decomposition (e.g., $r$, $w$, Div+Tax) rather than a breakdown by income group. Please ensure Figure G.25 unambiguously indicates whether it is decomposing the response by income bins, by channels, or by income bins further decomposed into channels.

**Response**:
Done. Fixed the caption and the subfigure labels in Figure G.25 to make clear that it is decomposing the response by income bins.

---

### 11. Sign inconsistency in Figure G.25(b)

**Status**: [Addressed]

**Quote**:
> Figure G. 25 presents the results.

**Feedback**:
The stacked-bar decomposition in Figure G.25(b) is hard to reconcile at a glance with Figure G.23, where the lowest income bins’ hours rise in HANK. If Figure G.25(b) is intended to plot signed contributions of the form $\omega_i \Delta L_i$ (for the same model/aggregation concept as in Figure G.23), then the bottom bins’ contributions should be positive and partly offset the negative contributions from higher bins. If instead the bars reflect a different convention (e.g., contributions to the aggregate decline, efficiency-units labor, or the HomL model), it would help to clarify that and to double-check that the plotted signs match the intended accounting identity.

**Response**:
Done. The wrong caption in the old version confused the reader (see point 17). Now the figure is clear and indeed in G.25(b) the bottom bins' contributions are positive as expected.

---

### 12. Incorrect time indices in aggregate condition

**Status**: [Addressed]

**Quote**:
> Combining the aggregate conditions we have

$$
\begin{gathered}
\lambda \gamma \hat{c}_{t+1}^{B}+(1-\lambda \gamma) \hat{c}_{t+1}^{S}=\lambda \hat{H}_{t+1}^{B}+(1-\lambda) \hat{H}_{t+1}^{S} \\
\lambda \gamma\left[\frac{\sigma(1+\nu(1+\bar{D} \kappa))}{\gamma \sigma-1-\bar{D} \kappa} \hat{H}_{t}^{B}+\frac{\bar{D}^{2} \sigma \nu \lambda \kappa \beta}{e_{1} e_{0}} \epsilon_{t}^{m}\right]+(1-\lambda \gamma)\left[-\sigma \epsilon_{t}^{m}\right]
\end{gathered}
$$

**Feedback**:
The aggregate-clearing step in the “Derivation of Proposition 1” appears to have inconsistent time indices: the displayed identity is written with $t+1$ subscripts (e.g., $\hat c_{t+1}^B,\hat c_{t+1}^S,\hat H_{t+1}^B,\hat H_{t+1}^S$), but the substitutions immediately below use the time-$t$ policy rules just derived (e.g., $\hat c_t^S=-\sigma\epsilon_t^m$ and $\hat c_t^B$ as a function of $\hat H_t^B$). It seems the aggregate condition intended here is the time-$t$ one (or else the subsequent substitutions would need to be re-indexed consistently).

**Response**:
Done. Fixed the time indices in the aggregate condition to be consistent with the substitutions immediately below.

---

### 13. Contradiction between Figure 7 legend and text description

**Status**: [Addressed]

**Quote**:
> Figure 7 plots the impact responses of labor supply for households across seven income groups (from P0_2 to P98_100), under the six different model calibrations. Solid lines correspond to the baseline borrowing constraint calibration $\underline{a}=-0.5$, allowing limited debt, while dashed lines represent a tighter borrowing constraint $\underline{a}=0$ (no debt allowed).

**Feedback**:
The description of Figure 7 ties the solid lines to the baseline borrowing constraint $\underline a=-0.5$ (consistent with Table 1), but the figure’s legend appears to label the solid-line calibration as $a=-1$. This should be reconciled (either the legend, the text, or an explained difference in normalization) so readers can tell which borrowing limit was actually used for the plotted IRFs.

**Response**:
Done. Fixed the legend in Figure 7 to be consistent with the text description.

---

### 14. Incorrect distinction regarding data frequency of cited studies

**Status**: [Addressed]

**Quote**:
> Moreover, unlike most of these studies (except Broer et al. (2022)), we use data at monthly frequency, which allows us to exploit a longer time-series dimension to identify the transmission of monetary policy shocks.

**Feedback**:
The claim that only Broer et al. (2022) is an exception to “most of these studies” on using monthly-frequency data may read too strong to some readers, since at least some of the cited administrative-data papers are commonly understood to draw on monthly records (or monthly transition measures), even if they may differ in sample length and/or how much they exploit a long monthly time series for shock identification. It may help to qualify what you mean by “monthly frequency” here (e.g., monthly outcomes over a long span in a VAR/FAVAR-style time-series identification setting) and/or to soften the exclusivity of the parenthetical exception.

**Response**:
Done. Clarified that we use monthly outcomes, as in Broer et al. (2022), which allows us to exploit a longer time-series dimension to identify the transmission of monetary policy shocks.

---

### 15. Contradiction between Figure G.18 caption and notes

**Status**: [Addressed]

**Quote**:
> Figure G.18: Decomposition of consumption Response in HANK.
![](/documents/ae22fb7f-bd18-48e2-8232-3906368397f1/images/image_040.jpg)

Notes: Note: Percent deviation in aggregate labor hours from steady state

**Feedback**:
Figure G.18 has an internal labeling inconsistency: the caption refers to a decomposition of “consumption,” but the note describes the plot as “Percent deviation in aggregate labor hours from steady state.” Please reconcile the caption/notes so it is unambiguous which variable is being decomposed (and ensure the description matches the plotted object).

**Response**:
Done. Fixed Figure G.18 caption/notes inconsistency: notes now refer to consumption (not labor hours) and removed duplicated “Notes:”.

---

### 16. Logical inconsistency in discussion of income effects evidence

**Status**: [Addressed]

**Quote**:
> However, the empirical evidence supporting this view rarely focuses on business cycle shocks. Most estimates come from idiosyncratic income shocks, such as lottery winnings. For example, Cesarini, Lindqvist, Notowidigdo and Östling (2017) use Swedish administrative data and find modest income effects, while Golosov, Graber, Mogstad and Novgorodsky (2023), using U.S. data, argue that labor supply responses to lottery winnings are sizable and not negligible.

**Feedback**:
The opening phrase “empirical evidence supporting this view” is a bit awkward given that the examples that follow are explicitly mixed (one modest income effects; one sizable/not negligible). The logic of the paragraph seems to be that the evidence base on income effects largely comes from idiosyncratic shocks (often lottery-like), and it delivers mixed conclusions rather than uniformly supporting negligible income effects; it may be worth clarifying that framing to avoid a momentary contradiction in how the examples are introduced.

**Response**:
Done. Clarified that the empirical evidence supporting this view rarely focuses on business cycle shocks, eventually delivering mixed conclusions.

---

### 17. Mislabeled panels in Figure G.25

**Status**: [Addressed]

**Quote**:
> Figure G.25: Contribution of each income bin to the aggregate response.
(b) Contribution of each income bin to the aggregate response.

**Feedback**:
Figure G.25’s subpanel labeling/captioning appears inconsistent: the first shown panel is labeled “(b)” and the second “(c),” with no visible “(a).” This makes it unclear whether an initial panel is missing or whether the first panel is simply mislabeled.

**Response**:
Done. Fixed the subpanel labeling/captioning issue in Figure G.25 by removing the extra (misplaced) caption that caused (b)/(c) confusion.

---
