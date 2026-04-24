"""
Kruse (2011) — Modified Wald‑Type Unit Root Test Against ESTAR
==============================================================

Tests H₀: unit root vs H₁: globally stationary ESTAR (with nonzero c).

Auxiliary regression:  Δyₜ = β₁ y³ₜ₋₁ + β₂ y²ₜ₋₁ + Σ ρᵢ Δyₜ₋ᵢ + uₜ

Test statistic:  τ = t²_{β⊥₂=0} + 𝟙(β̂₁<0) · t²_{β₁=0}
(Modified Wald, reject when τ > CV)

Reference
---------
Kruse, R. (2011). A new unit root test against ESTAR based on a class
of modified statistics. Statistical Papers, 52(1), 71-85.
"""

from __future__ import annotations

import numpy as np
from tarur.core import (
    TestResult, _validate_series, _prepare_case,
    _ols, _make_model_summary,
)
from tarur.lag_selection import select_lag, _embed_diff_lags
from tarur.critical_values import get_kruse_cv


def kruse_test(
    x,
    case: str = "demeaned",
    max_lags: int = 8,
    lag_method: str = "aic",
) -> TestResult:
    """
    Kruse (2011) modified Wald-type unit root test against ESTAR.

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
    """
    x = _validate_series(x)
    x_adj = _prepare_case(x, case)

    z = np.diff(x_adj)
    n = len(z)

    def build_X(z, x_adj, lag):
        z_dep, z_lags = _embed_diff_lags(z, lag)
        m = len(z_dep)
        x_cube = x_adj[:n] ** 3
        x_sq = x_adj[:n] ** 2
        x_lag1 = x_cube[lag: lag + m]
        x_lag2 = x_sq[lag: lag + m]
        if lag == 0:
            X = np.column_stack([x_lag1, x_lag2])
            names = ["y3_lag1", "y2_lag1"]
        else:
            X = np.column_stack([x_lag1, x_lag2, z_lags])
            names = ["y3_lag1", "y2_lag1"] + [f"dz_lag{i+1}" for i in range(lag)]
        return z_dep, X, names

    opt_lag = select_lag(z, x_adj, build_X, max_lags, lag_method)

    z_dep, X, var_names = build_X(z, x_adj, opt_lag)
    ols = _ols(z_dep, X)

    # ── Compute modified Wald τ statistic (Kruse 2011, eq. 5) ────────
    beta1 = ols["beta"][0]  # coefficient on y³
    beta2 = ols["beta"][1]  # coefficient on y²

    # Variance‑covariance of (β₁, β₂)
    sigma2 = ols["sigma2"]
    XtX_inv = np.linalg.inv(X.T @ X) * sigma2

    v11 = XtX_inv[0, 0]
    v22 = XtX_inv[1, 1]
    v12 = XtX_inv[0, 1]

    # Orthogonalized β₂⊥ = β₂ - β₁·v₂₁/v₁₁
    beta2_orth = beta2 - beta1 * v12 / v11
    var_beta2_orth = v22 - v12 ** 2 / v11

    # τ = t²_{β₂⊥=0} + 𝟙(β₁<0)·t²_{β₁=0}
    t2_beta2_orth = beta2_orth ** 2 / var_beta2_orth if var_beta2_orth > 0 else 0.0
    t2_beta1 = beta1 ** 2 / v11 if v11 > 0 else 0.0

    tau = t2_beta2_orth + (1.0 if beta1 < 0 else 0.0) * t2_beta1

    cv = get_kruse_cv(case)

    result = TestResult(
        test_name="Kruse (2011) Modified Wald Unit Root Test",
        statistic_name="\u03c4",  # τ
        statistic=tau,
        critical_values=cv,
        selected_lag=opt_lag,
        lag_method=lag_method.upper(),
        case=case,
        null_hypothesis="Unit root (linear random walk)",
        alt_hypothesis="Globally stationary ESTAR (nonzero location c)",
        model_summary=_make_model_summary(ols, var_names),
        reference=(
            "Kruse, R. (2011). A new unit root test against ESTAR based on a class "
            "of modified statistics. Statistical Papers, 52(1), 71-85."
        ),
        extra={"beta1_y3": beta1, "beta2_y2": beta2, "indicator": beta1 < 0},
    )
    result._make_decisions(tail="right")
    return result
