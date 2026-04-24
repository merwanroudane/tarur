"""
Sollis (2009) — Asymmetric ESTAR (AESTAR) Unit Root Test
========================================================

Tests H₀: unit root vs H₁: globally stationary symmetric/asymmetric ESTAR.

Auxiliary regression:  Δyₜ = φ₁ y³ₜ₋₁ + φ₂ y⁴ₜ₋₁ + Σ κᵢ Δyₜ₋ᵢ + ηₜ

Test statistic: F_AE  (joint F‑test of φ₁=φ₂=0, reject when F > CV)

Additionally tests symmetric vs asymmetric: Fas (standard F on φ₂=0)

NOTE: The R code in NonlinearTSA is incomplete — it uses the same regression
as Kruse (y³, y⁴) but doesn't correctly derive from the AESTAR model.
This implementation follows the original paper exactly.

Reference
---------
Sollis, R. (2009). A simple unit root test against asymmetric STAR nonlinearity
with an application to real exchange rates in Nordic countries.
Economic Modelling, 26(1), 118-125.
"""

from __future__ import annotations

import numpy as np
from scipy import stats as sp_stats
from tarur.core import (
    TestResult, _validate_series, _prepare_case,
    _ols, _make_model_summary,
)
from tarur.lag_selection import select_lag, _embed_diff_lags
from tarur.critical_values import get_sollis2009_cv


def sollis2009_test(
    x,
    case: str = "demeaned",
    max_lags: int = 8,
    lag_method: str = "aic",
) -> TestResult:
    """
    Sollis (2009) AESTAR unit root test.

    Parameters
    ----------
    x : array-like
        Time series (level).
    case : str
        "raw", "demeaned", or "detrended".
    max_lags : int
        Maximum lag order.
    lag_method : str
        "aic", "bic", or "t-stat".

    Returns
    -------
    TestResult
        Contains F_AE (unit root test) and Fas (symmetry test) in extra.
    """
    x = _validate_series(x)
    x_adj = _prepare_case(x, case)

    z = np.diff(x_adj)
    n = len(z)

    def build_X(z, x_adj, lag):
        z_dep, z_lags = _embed_diff_lags(z, lag)
        m = len(z_dep)
        # From eq. (19): regressors are y³ₜ₋₁ and y⁴ₜ₋₁
        x_cube = x_adj[:n] ** 3
        x_four = x_adj[:n] ** 4
        x_lag1 = x_cube[lag: lag + m]
        x_lag2 = x_four[lag: lag + m]
        if lag == 0:
            X = np.column_stack([x_lag1, x_lag2])
            names = ["y3_lag1", "y4_lag1"]
        else:
            X = np.column_stack([x_lag1, x_lag2, z_lags])
            names = ["y3_lag1", "y4_lag1"] + [f"dz_lag{i+1}" for i in range(lag)]
        return z_dep, X, names

    opt_lag = select_lag(z, x_adj, build_X, max_lags, lag_method)

    # ── Unrestricted model (with y³ and y⁴) ──────────────────────────
    z_dep, X_u, var_names = build_X(z, x_adj, opt_lag)
    ols_u = _ols(z_dep, X_u)
    sse_u = np.sum(ols_u["residuals"] ** 2)

    # ── Restricted model (H₀: φ₁=φ₂=0, only lagged diffs) ───────────
    if opt_lag == 0:
        # Under H₀ the model is just Δyₜ = ηₜ (no regressors)
        sse_r = np.sum(z_dep ** 2)
        k_r = 0
    else:
        _, z_lags = _embed_diff_lags(z, opt_lag)
        ols_r = _ols(z_dep, z_lags)
        sse_r = np.sum(ols_r["residuals"] ** 2)
        k_r = z_lags.shape[1]

    # ── F‑statistic: F_AE ────────────────────────────────────────────
    m_restr = 2  # two restrictions (φ₁=0, φ₂=0)
    n_obs = len(z_dep)
    k_u = X_u.shape[1]
    df2 = n_obs - k_u

    F_AE = ((sse_r - sse_u) / m_restr) / (sse_u / df2) if df2 > 0 else 0.0

    # ── Symmetry test: Fas (standard F on φ₂=0) ─────────────────────
    # Restricted model: only y³ (no y⁴)
    z_dep2, z_lags2 = _embed_diff_lags(z, opt_lag)
    m2 = len(z_dep2)
    x_cube2 = x_adj[:n] ** 3
    x_lag1_only = x_cube2[opt_lag: opt_lag + m2]
    if opt_lag == 0:
        X_symm = x_lag1_only.reshape(-1, 1)
    else:
        X_symm = np.column_stack([x_lag1_only, z_lags2])
    ols_symm = _ols(z_dep2, X_symm)
    sse_symm = np.sum(ols_symm["residuals"] ** 2)

    Fas = ((sse_symm - sse_u) / 1) / (sse_u / df2) if df2 > 0 else 0.0
    Fas_pvalue = sp_stats.f.sf(Fas, 1, df2)

    # ── Critical values ──────────────────────────────────────────────
    cv = get_sollis2009_cv(case, len(x))

    # ── Decision on φ₁ sign (for symmetry test validity) ─────────────
    phi1_hat = ols_u["beta"][0]

    result = TestResult(
        test_name="Sollis (2009) Asymmetric ESTAR Unit Root Test",
        statistic_name="F_AE",
        statistic=F_AE,
        critical_values=cv,
        selected_lag=opt_lag,
        lag_method=lag_method.upper(),
        case=case,
        null_hypothesis="Unit root (linear random walk)",
        alt_hypothesis="Globally stationary symmetric or asymmetric ESTAR",
        model_summary=_make_model_summary(ols_u, var_names),
        reference=(
            "Sollis, R. (2009). A simple unit root test against asymmetric STAR "
            "nonlinearity with an application to real exchange rates in Nordic "
            "countries. Economic Modelling, 26(1), 118-125."
        ),
        extra={
            "phi1": phi1_hat,
            "phi2": ols_u["beta"][1],
            "F_AE": F_AE,
            "Fas": Fas,
            "Fas_pvalue": Fas_pvalue,
            "symmetry_test": (
                "Reject symmetry (asymmetric ESTAR)" if Fas_pvalue < 0.05
                else "Fail to reject symmetry (symmetric ESTAR)"
            ),
        },
    )
    result._make_decisions(tail="right")
    return result
