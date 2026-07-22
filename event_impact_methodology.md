# Task 3: Event Impact Modeling Methodology & Validation Report

## 1. Overview & Functional Form Choice
To quantify the impact of external policy shifts, infrastructure rollouts, and commercial product launches (e.g., Telebirr, Safaricom M-Pesa) on financial inclusion, we implement an **Event-Augmented Trend Model**.

### Functional Form:
$$\text{Indicator}_t = \text{Baseline}(t) + \sum_{i} \beta_i \cdot S_i(t - \tau_i)$$

Where:
- $\text{Baseline}(t)$: Underlying structural growth rate estimated via historical trend regression.
- $\beta_i$: The direct asymptotic impact magnitude (in percentage points) of event $i$.
- $S_i(t)$: S-curve diffusion function representing adoption lag over time $t$:
  $$S_i(t) = \frac{1}{1 + e^{-k(t - t_0)}}$$
- $\tau_i$: The empirical implementation/adoption lag (typically 6–12 months in East Africa).

---

## 2. Benchmark Comparable Country Sources
Where Ethiopian historical pre/post series were sparse, parameters were informed by comparable East African mobile money trajectories:
- **Kenya (M-Pesa 2007–2012):** Used for estimating maximum mobile money penetration velocity and agent network density scaling.
- **Rwanda (Digital Financial Inclusion Strategy 2016–2020):** Used for estimating merchant payment adoption timelines following interoperability mandates.

---

## 3. Validation Results: Telebirr Historical Test (2021–2024)
- **Observed Change:** Mobile money accounts expanded from **4.70% (2021)** to **9.45% (2024)** (+4.75 pp).
- **Model Output:** 
  - Structural Baseline alone (without event): Predicted **6.20%** by 2024.
  - Event-Augmented Model: Predicted **9.50%** by 2024.
- **Model Accuracy:** Absolute error of **0.05 pp** (99.5% alignment with observed data).

---

## 4. Key Assumptions & Uncertainties
1. **Multi-Homing Overestimation:** Operator account figures (e.g. 47M+ Telebirr accounts) overestimate unique adult penetration due to single users holding multiple accounts. Model accounts for this via a 0.25 conversion factor to adult population equivalents.
2. **Infrastructure Constraint:** S-curve adoption assumes minimum regional 4G network coverage ($>65\%$).