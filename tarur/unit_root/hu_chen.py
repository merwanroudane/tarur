"""
Hu & Chen (2016) — Modified Wald Unit Root Test (3‑parameter)
=============================================================

Tests H₀: unit root vs H₁: locally explosive/unit root but globally
stationary ESTAR.

Auxiliary regression:  Δyₜ = β₁ yₜ₋₁ + β₂ y²ₜ₋₁ + β₃ y³ₜ₋₁ + Σ ρᵢ Δyₜ₋ᵢ + uₜ

Test statistic:  τ = τ²_I + 𝟙(β̂₃<0)·t²_{β₃=0}
(Modified Wald with one one‑sided + two two‑sided parameters)

Reference
---------
Hu, J., & Chen, Z. (2016). A unit root test against globally stationary
ESTAR models when local condition is non-stationary.
Economics Letters, 146, 89-94.
"""

from __future__ import annotations

import numpy as np
from tarur.core import (
    TestResult, _validate_series, _prepare_case,
    _ols, _make_model_summary,
)
from tarur.lag_selection import select_lag, _embed_diff_lags
from tarur.critical_values import get_hu_chen_cv


def hu_chen_test(
    x,
    case: str = "demeaned",
    max_lags: int = 8,
    lag_method: str = "aic",
) -> TestResult:
    """
    Hu & Chen (2016) modified Wald unit root test.

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
        x1 = x_adj[:n][lag: lag + m]       # yₜ₋₁
        x2 = x_adj[:n][lag: lag + m] ** 2  # y²ₜ₋₁
        x3 = x_adj[:n][lag: lag + m] ** 3  # y³ₜ₋₁
        if lag == 0:
            X = np.column_stack([x1, x2, x3])
            names = ["y_lag1", "y2_lag1", "y3_lag1"]
        else:
            X = np.column_stack([x1, x2, x3, z_lags])
            names = ["y_lag1", "y2_lag1", "y3_lag1"] + [f"dz_lag{i+1}" for i in range(lag)]
        return z_dep, X, names

    opt_lag = select_lag(z, x_adj, build_X, max_lags, lag_method)

    z_dep, X, var_names = build_X(z, x_adj, opt_lag)
    ols = _ols(z_dep, X)

    # ── Compute modified Wald τ (Hu & Chen 2016) ─────────────────────
    beta = ols["beta"][:3]  # β₁, β₂, β₃
    sigma2 = ols["sigma2"]
    XtX_inv = np.linalg.inv(X.T @ X) * sigma2

    # Extract 3×3 block for (β₁, β₂, β₃)
    V = XtX_inv[:3, :3]
    v33 = V[2, 2]
    V_I = V[:2, :2]
    V_I3 = V[:2, 2]

    # Orthogonalized: β_I·3 = β_I - β₃ · V_I3 / v33
    beta_I = beta[:2]
    beta3 = beta[2]
    beta_I_orth = beta_I - beta3 * V_I3 / v33

    # Variance of orthogonalized: V_I·3 = V_I - V_I3 V_I3' / v33
    V_I_orth = V_I - np.outer(V_I3, V_I3) / v33

    # τ²_I = β_I·3' V_I·3⁻¹ β_I·3
    try:
        V_I_orth_inv = np.linalg.inv(V_I_orth)
        tau_I_sq = beta_I_orth @ V_I_orth_inv @ beta_I_orth
    except np.linalg.LinAlgError:
        tau_I_sq = 0.0

    # t²_{β₃=0}
    t2_beta3 = beta3 ** 2 / v33 if v33 > 0 else 0.0

    # τ = τ²_I + 𝟙(β₃<0) · t²_{β₃=0}
    tau = tau_I_sq + (1.0 if beta3 < 0 else 0.0) * t2_beta3

    cv = get_hu_chen_cv(case)

    result = TestResult(
        test_name="Hu & Chen (2016) Modified Wald Unit Root Test",
        statistic_name="\u03c4",  # τ
        statistic=tau,
        critical_values=cv,
        selected_lag=opt_lag,
        lag_method=lag_method.upper(),
        case=case,
        null_hypothesis="Unit root (linear random walk)",
        alt_hypothesis="Locally explosive but globally stationary ESTAR",
        model_summary=_make_model_summary(ols, var_names),
        reference=(
            "Hu, J., & Chen, Z. (2016). A unit root test against globally "
            "stationary ESTAR models when local condition is non-stationary. "
            "Economics Letters, 146, 89-94."
        ),
        extra={
            "beta1_y": beta[0],
            "beta2_y2": beta[1],
            "beta3_y3": beta[2],
            "indicator": beta[2] < 0,
        },
    )
    result._make_decisions(tail="right")
    return result
