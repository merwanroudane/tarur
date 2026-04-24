# TARUR

**Nonlinear Unit Root Testing Library for Python**

*17+ tests · Embedded critical values · Automatic decisions · Publication-quality output*

[![PyPI](https://img.shields.io/pypi/v/tarur?color=%2334D058&label=PyPI)](https://pypi.org/project/tarur/)
[![Python](https://img.shields.io/pypi/pyversions/tarur)](https://pypi.org/project/tarur/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/merwanroudane/tarur/blob/main/LICENSE)

---

## Why TARUR?

Most nonlinear unit root test implementations in R (e.g., `NonlinearTSA`) **do not include critical values**, forcing researchers to manually look them up in the original papers every single time. This is tedious, error-prone, and slows empirical research.

**TARUR** solves this by providing:

- **Embedded CVs** — All critical values from the original papers (asymptotic + finite-sample)
- **Auto decisions** — Reject / fail-to-reject at 1%, 5%, 10% — no manual comparison
- **One-line API** — `tarur.kss_test(y)` gives you everything
- **Full battery** — `tarur.run_all_tests(y)` runs 11+ tests at once
- **Bug fixes** — Corrects errors in R implementations (Kruse, Hu-Chen, Sollis 2009)
- **LaTeX export** — Publication-ready tables for your papers

---

## Installation

```bash
pip install tarur
```

From source:

```bash
git clone https://github.com/merwanroudane/tarur.git
cd tarur && pip install -e .
```

**Dependencies:** `numpy`, `scipy`, `pandas`, `matplotlib` (all standard scientific stack).

---

## Quick Start

```python
import numpy as np
import tarur

# Load your time series (level, not differenced)
y = np.log(your_price_series)

# Single test
result = tarur.kss_test(y, case='demeaned', max_lags=8)
print(result)

# Full battery — all 11 tests at once
batch = tarur.run_all_tests(y, case='demeaned', max_lags=8)
```

**Output:**

```
============================================================
         KSS (2003) Nonlinear Unit Root Test
============================================================
  H0: Unit root (linear random walk)
  H1: Globally stationary ESTAR process
------------------------------------------------------------
  Test Statistic (tNL)          | -4.127
  Selected Lag                  | 4 (AIC)
  Case                          | demeaned
------------------------------------------------------------
  Critical Values: 1%: -3.930 | 5%: -3.400 | 10%: -3.130
  Source: Kapetanios, Shin & Snell (2003), Table 1
------------------------------------------------------------
  1%: [REJECT] H0
  5%: [REJECT] H0
  10%: [REJECT] H0
------------------------------------------------------------
  >> Reject H0 at the 1% significance level.
     Globally stationary ESTAR process.
============================================================
```

---

## Complete Test Catalog

### ESTAR-Based Unit Root Tests

| Test | Function | Statistic | Tail | Key Feature |
|------|----------|-----------|------|-------------|
| **KSS (2003)** | `kss_test()` | tNL | Left | Foundational ESTAR test using cubic auxiliary |
| **Kruse (2011)** | `kruse_test()` | Modified Wald τ | Right | Allows nonzero location parameter c |
| **Sollis (2009)** | `sollis2009_test()` | F_AE + Fas | Right | Tests asymmetric vs symmetric ESTAR |
| **Hu & Chen (2016)** | `hu_chen_test()` | 3-param Wald τ | Right | Locally explosive, globally stationary |

### Threshold / Asymmetric Tests

| Test | Function | Statistic | Tail | Key Feature |
|------|----------|-----------|------|-------------|
| **Enders & Granger (1998)** | `enders_granger_test()` | Φ (F-type) | Right | MTAR with momentum indicator |
| **Sollis (2004)** | `sollis2004_test()` | F_TAR | Right | ST-TAR with smooth transition detrending |
| **Cook & Vougas (2009)** | `cook_vougas_test()` | F_MTAR | Right | ST-MTAR combining NLS + asymmetry |

### Smooth Transition Unit Root Tests

| Test | Function | Statistic | Tail | Key Feature |
|------|----------|-----------|------|-------------|
| **LNV (1998)** | `lnv_test()` | t_ADF | Left | Single logistic transition (3 models) |
| **Vougas (2006)** | `vougas_test()` | t_ADF | Left | 5 functional forms (Models A–E) |
| **Harvey & Mills (2002)** | `harvey_mills_test()` | t_ADF | Left | Double smooth transition (2 breaks) |

### Grid-Search Tests

| Test | Function | Statistic | Tail | Key Feature |
|------|----------|-----------|------|-------------|
| **Kılıç (2011)** | `kilic_test()` | inf-t | Left | Grid search over transition parameter γ |
| **Park & Shintani (2016)** | `park_shintani_test()` | inf-t | Left | Transitional autoregressive model |

### Extended Tests

| Test | Function | Statistic | Tail | Key Feature |
|------|----------|-----------|------|-------------|
| **Pascalau (2007)** | `pascalau_test()` | F | Right | Asymmetric NLSTAR with y⁴ terms |
| **Cuestas & Garratt (2011)** | `cuestas_garratt_test()` | χ² | Right | Cubic polynomial detrending |
| **Cuestas & Ordóñez (2014)** | `cuestas_ordonez_test()` | tNL | Left | NLS logistic detrending + KSS |

### Cointegration Tests

| Test | Function | Description |
|------|----------|-------------|
| **KSS (2006)** | `kss_cointegration_test()` | Nonlinear cointegration via ESTAR residuals |
| **Enders & Siklos (2001)** | `enders_siklos_test()` | Threshold cointegration with asymmetric ECM |

### Linearity & Diagnostics

| Test | Function | Description |
|------|----------|-------------|
| **Teräsvirta (1994)** | `terasvirta_test()` | Linearity test + LSTAR vs ESTAR selection |
| **ARCH** | `arch_test()` | Engle (1982) LM test for ARCH effects |
| **McLeod-Li** | `mcleod_li_test()` | Portmanteau test on squared residuals |

---

## Detailed Test Guide

### KSS (2003) — The Foundational Test

The KSS test uses a cubic auxiliary regression derived from a Taylor expansion of the ESTAR transition function:

```
Δyₜ = β₁ yₜ₋₁³ + Σ ρᵢ Δyₜ₋ᵢ + uₜ
```

- **H₀**: Unit root (β₁ = 0)
- **H₁**: Globally stationary ESTAR process (β₁ < 0)
- **Statistic**: tNL = β̂₁ / se(β̂₁), reject when tNL < CV

**Critical values (asymptotic, Table 1):**

| Case | 1% | 5% | 10% |
|------|-----|-----|------|
| Raw | −3.48 | −2.93 | −2.66 |
| Demeaned | −3.93 | −3.40 | −3.13 |
| Detrended | −3.40 | −2.93 | −2.66 |

```python
result = tarur.kss_test(y, case='demeaned', max_lags=12, lag_method='aic')
print(result)
```

---

### Kruse (2011) — Improved ESTAR Test

Kruse improves on KSS by allowing a nonzero location parameter *c*, adding a quadratic term:

```
Δyₜ = β₁ yₜ₋₁³ + β₂ yₜ₋₁² + Σ ρᵢ Δyₜ₋ᵢ + uₜ
```

The test statistic is a **Modified Wald τ** (not a standard Wald):

```
τ = t²(β₂⊥=0) + 𝟙(β̂₁ < 0) · t²(β₁=0)
```

> ⚠️ **Bug fix:** The R `NonlinearTSA` package uses a standard Chi-squared. TARUR implements the correct modified Wald τ with the indicator function from the paper.

**Critical values (asymptotic, T=1000, Table 1):**

| Case | 1% | 5% | 10% |
|------|------|------|------|
| Raw | 13.15 | 9.53 | 7.85 |
| Demeaned | 13.75 | 10.17 | 8.60 |
| Detrended | 17.10 | 12.82 | 11.10 |

```python
result = tarur.kruse_test(y, case='demeaned', max_lags=12)
```

---

### Sollis (2009) — Asymmetric ESTAR

Tests whether mean reversion is **symmetric or asymmetric**:

```
Δyₜ = φ₁ yₜ₋₁³ + φ₂ yₜ₋₁⁴ + Σ κᵢ Δyₜ₋ᵢ + ηₜ
```

Two statistics:
- **F_AE**: Joint test φ₁ = φ₂ = 0 (unit root test)
- **Fas**: Test φ₂ = 0 (symmetry test — if rejected, adjustment is asymmetric)

> ⚠️ **Bug fix:** The R code uses the wrong auxiliary regression variables.

```python
result = tarur.sollis2009_test(y, case='demeaned', max_lags=12)
print(f"Symmetry Fas: {result.extra['Fas']:.3f} (p={result.extra['Fas_pvalue']:.4f})")
print(f"  → {result.extra['symmetry_test']}")
```

---

### Enders & Granger (1998) — MTAR Test

Momentum Threshold Autoregression with asymmetric adjustment:

```
Δûₜ = Iₜ ρ⁺ ûₜ₋₁ + (1-Iₜ) ρ⁻ ûₜ₋₁ + Σ δᵢ Δûₜ₋ᵢ + εₜ
```

where Iₜ = 1 if Δyₜ₋₁ ≥ 0 (momentum indicator).

```python
result = tarur.enders_granger_test(y, case='demeaned', max_lags=12)
print(f"ρ⁺ = {result.extra['rho_pos']:.4f}")
print(f"ρ⁻ = {result.extra['rho_neg']:.4f}")
print(f"Symmetry F = {result.extra['F_symmetry']:.3f} (p={result.extra['F_sym_pvalue']:.4f})")
```

---

### Smooth Transition Tests (LNV / Vougas / Harvey-Mills)

These tests first fit a nonlinear smooth transition trend via NLS, then apply an ADF test on the residuals. **Each has its own distinct critical values** from its own paper.

**LNV (1998) critical values — Model A (Table I):**

| T | 1% | 5% | 10% |
|---|------|------|------|
| 25 | −5.67 | −4.75 | −4.28 |
| 50 | −5.10 | −4.36 | −4.01 |
| 100 | −4.88 | −4.23 | −3.91 |
| 200 | −4.76 | −4.16 | −3.85 |
| 500 | −4.69 | −4.10 | −3.80 |

**Harvey & Mills (2002) critical values — Model A (Table 1, double transition):**

| T | 1% | 5% | 10% |
|---|------|------|------|
| 50 | −6.49 | −5.73 | −5.33 |
| 100 | −6.05 | −5.37 | −5.04 |
| 200 | −5.80 | −5.20 | −4.90 |
| 1000 | −5.64 | −5.07 | −4.79 |

> **Note:** Harvey-Mills CVs are much larger in absolute value because the double-transition alternative is more flexible, shifting the null distribution substantially.

```python
result_lnv = tarur.lnv_test(y, model='A', max_lags=12)
result_vougas = tarur.vougas_test(y, model='A', max_lags=12)
result_hm = tarur.harvey_mills_test(y, model='A', max_lags=12)

# Test all Vougas models
for m in ['A', 'B', 'C', 'D', 'E']:
    r = tarur.vougas_test(y, model=m, max_lags=12)
    print(f"Model {m}: t={r.statistic:.3f}, CV(5%)={r.critical_values.cv5:.3f}")
```

---

### Cointegration Tests

```python
# Nonlinear cointegration
result = tarur.kss_cointegration_test(y1, y2, case='demeaned', max_lags=12)

# Threshold cointegration with asymmetric adjustment
result = tarur.enders_siklos_test(y1, y2, max_lags=12)
```

---

### Teräsvirta (1994) Linearity Test

Before applying nonlinear tests, verify that nonlinearity is present:

```python
result = tarur.terasvirta_test(np.diff(y), d=1)
print(f"Linearity p-value: {result.extra['p_linearity']:.4f}")
print(f"Suggested model: {result.extra['suggested_model']}")  # LSTAR or ESTAR
```

---

## API Reference

### Common Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| `case` | `'raw'`, `'demeaned'`, `'detrended'` | Deterministic terms |
| `max_lags` | integer (default 8) | Maximum lag order for augmentation |
| `lag_method` | `'aic'`, `'bic'`, `'t-stat'` | Automatic lag selection criterion |
| `model` | `'A'` to `'E'` | Smooth transition model specification |

### TestResult Object

Every test returns a `TestResult` with these attributes:

```python
result.statistic         # Test statistic value (float)
result.statistic_name    # Label: "tNL", "τ", "F_AE", etc.
result.critical_values   # CriticalValues with .cv1, .cv5, .cv10
result.decision          # {"1%": bool, "5%": bool, "10%": bool}
result.interpretation    # Plain-English sentence
result.selected_lag      # Optimal lag order (int)
result.case              # Specification used
result.model_summary     # Regression coefficients, R², AIC, BIC
result.extra             # Test-specific extras (dict)
result.reference         # Full citation

# Export
result.to_dict()         # Flat dictionary for DataFrame rows
result.to_latex()        # LaTeX table snippet
result.plot()            # Matplotlib visualization
print(result)            # Formatted terminal output
```

### BatchResult Object

```python
batch = tarur.run_all_tests(y, case='demeaned', max_lags=8)

batch.summary()          # pandas DataFrame with all results
batch.to_latex()         # Full LaTeX comparison table
batch.plot()             # Dashboard visualization
print(batch)             # Formatted comparison table
```

---

## Recommended Workflow

```python
import numpy as np
import tarur

# 1. Load data (use log-levels for financial series)
y = np.log(your_price_series)

# 2. Test for linearity first
lin = tarur.terasvirta_test(np.diff(y), d=1)
print(f"Linearity p-value: {lin.extra['p_linearity']:.4f}")
print(f"Suggested model: {lin.extra['suggested_model']}")

# 3. Run the full nonlinear unit root battery
batch = tarur.run_all_tests(y, case='demeaned', max_lags=12)

# 4. Summary table for your paper
df = batch.summary()
print(df[['test', 'statistic', 'cv_5%', 'reject_5%']].to_string(index=False))

# 5. Export LaTeX for publication
print(batch.to_latex())

# 6. Visualization
tarur.plot_series_analysis(y, title='My Series')
batch.plot()
```

---

## Critical Values — Complete Source Mapping

Every test uses **its own distinct critical values** from its original paper. No sharing, no approximations.

| Test | Paper Source | Table | Sample Sizes | Statistic Type |
|------|-------------|-------|--------------|----------------|
| KSS (2003) | KSS, Table 1 | Asymptotic | — | t-type (left) |
| Kruse (2011) | Kruse, Table 1 | T=1000 | — | Wald τ (right) |
| Sollis (2009) | Sollis, Table 1 | T=50,100,200 | Interpolated | F-type (right) |
| Hu & Chen (2016) | Hu & Chen, Table 1 | T=1000 | — | Wald τ (right) |
| Enders & Granger (1998) | E&G, Table 1 | Asymptotic | — | F-type (right) |
| LNV (1998) | LNV, Table I | T=25–500 | Interpolated | t-type (left) |
| Vougas (2006) | Vougas, Table 1 | T=25–500 | Interpolated | t-type (left) |
| Harvey & Mills (2002) | H&M, Table 1 | T=50–1000 | Interpolated | t-type (left) |
| Cook & Vougas (2009) | C&V, Table 1 | T=50–500 | Interpolated | F-type (right) |
| Sollis (2004) | Sollis, Table II | T=100 | — | F-type (right) |
| Kılıç (2011) | Kılıç, Table 1 | Asymptotic | — | t-type (left) |
| Park & Shintani (2016) | P&S, Table 1 | Asymptotic | — | t-type (left) |
| Pascalau (2007) | Pascalau | Simulated | — | F-type (right) |
| Cuestas & Garratt (2011) | C&G | Simulated | — | χ²-type (right) |

---

## Bug Fixes vs R NonlinearTSA Package

| Issue | R Code (Wrong) | TARUR (Correct) |
|-------|----------------|-----------------|
| **Kruse (2011)** | Standard Wald / Chi² | Modified Wald τ with indicator function |
| **Hu & Chen (2016)** | Same error as Kruse | 3-parameter modified Wald with orthogonalization |
| **Sollis (2009)** | Wrong auxiliary regression | Correct AESTAR formulation with y³ and y⁴ |
| **TAR/MTAR** | Depends on R `tsDyn` package | Fully native Python (zero R dependency) |
| **Critical values** | Not included in output | All embedded from original papers |

---

## Visualization

```python
# Series diagnostic plot (ACF, PACF, distribution)
tarur.plot_series_analysis(y, title='Real Exchange Rate')

# Individual test visualization
result = tarur.kss_test(y)
result.plot()

# Full battery dashboard
batch = tarur.run_all_tests(y)
batch.plot()
```

---

## Citation

If you use TARUR in your research, please cite:

```bibtex
@software{tarur2024,
  author = {Roudane, Merwan},
  title = {TARUR: Nonlinear Unit Root Testing Library for Python},
  year = {2024},
  url = {https://github.com/merwanroudane/tarur}
}
```

---

## References

- Kapetanios, G., Shin, Y., & Snell, A. (2003). Testing for a unit root in the nonlinear STAR framework. *Journal of Econometrics*, 112(2), 359–379.
- Kruse, R. (2011). A new unit root test against ESTAR based on a class of modified statistics. *Statistical Papers*, 52(1), 71–85.
- Sollis, R. (2009). A simple unit root test against asymmetric STAR nonlinearity. *Economic Modelling*, 26(1), 118–125.
- Sollis, R. (2004). Asymmetric adjustment and smooth transitions. *Journal of Time Series Analysis*, 25(3), 409–417.
- Hu, J., & Chen, Z. (2016). A unit root test against globally stationary ESTAR models. *Economics Letters*, 146, 89–94.
- Enders, W., & Granger, C.W.J. (1998). Unit-root tests and asymmetric adjustment. *JBES*, 16(3), 304–311.
- Enders, W., & Siklos, P.L. (2001). Cointegration and threshold adjustment. *JBES*, 19(2), 166–176.
- Leybourne, S., Newbold, P., & Vougas, D. (1998). Unit roots and smooth transitions. *JTSA*, 19(1), 83–97.
- Vougas, D. (2006). On unit root testing with smooth transitions. *CSDA*, 51(2), 797–800.
- Harvey, D.I., & Mills, T.C. (2002). Unit roots and double smooth transitions. *J. Applied Statistics*, 29(5), 675–683.
- Cook, S., & Vougas, D. (2009). Unit root testing against an ST–MTAR alternative. *Applied Economics*, 41(11), 1397–1404.
- Kılıç, R. (2011). Testing for a unit root in a stationary ESTAR process. *Econometric Reviews*, 30(3), 274–302.
- Park, J.Y., & Shintani, M. (2016). Testing for a unit root against transitional autoregressive models. *International Economic Review*, 57(2), 635–664.
- Pascalau, R. (2007). Unit root tests with smooth breaks. Working paper.
- Cuestas, J.C., & Garratt, D. (2011). Is real GDP per capita a stationary process? *Applied Economics*, 43(11), 1431–1437.
- Cuestas, J.C., & Ordóñez, J. (2014). Smooth transitions, asymmetric adjustment, and unit roots. *Applied Economics Letters*, 21(14), 969–972.
- Teräsvirta, T. (1994). Specification, estimation, and evaluation of smooth transition autoregressive models. *JASA*, 89(425), 208–218.

---

## Author

**Dr. Merwan Roudane**

📧 merwanroudane920@gmail.com

🔗 [github.com/merwanroudane/tarur](https://github.com/merwanroudane/tarur)

## License

MIT License — see [LICENSE](LICENSE) for details.
