"""
KSS (2003) — Kapetanios, Shin & Snell Nonlinear Unit Root Test
================================================================

Tests H₀: unit root (linear) vs H₁: globally stationary ESTAR process.

Auxiliary regression:  Δyₜ = β₁ y³ₜ₋₁ + Σ ρᵢ Δyₜ₋ᵢ + uₜ

Test statistic: tNL = β̂₁ / se(β̂₁)  (t‑type, reject when tNL < CV)

Reference
---------
Kapetanios, G., Shin, Y., & Snell, A. (2003). Testing for a unit root
in the nonlinear STAR framework. Journal of Econometrics, 112(2), 359-379.
"""

from __future__ import annotations

import numpy as np
from tarur.core import (
    TestResult, _validate_series, _prepare_case,
    _ols, _make_model_summary,
)
from tarur.lag_selection import select_lag, _embed_diff_lags
from tarur.critical_values import get_kss_cv


def kss_test(
    x,
    case: str = "demeaned",
    max_lags: int = 8,
    lag_method: str = "aic",
) -> TestResult:
    """
    Kapetanios, Shin & Snell (2003) nonlinear unit root test.

    Parameters
    ----------
    x : array-like
        Time series (level).
    case : str
        "raw", "demeaned", or "detrended".
    max_lags : int
        Maximum lag order for augmented regression.
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
        x_cube = x_adj[: n] ** 3
        x_lag1 = x_cube[lag: lag + m]
        if lag == 0:
            X = x_lag1.reshape(-1, 1)
            names = ["y3_lag1"]
        else:
            X = np.column_stack([x_lag1, z_lags])
            names = ["y3_lag1"] + [f"dz_lag{i+1}" for i in range(lag)]
        return z_dep, X, names

    # Select lag
    opt_lag = select_lag(z, x_adj, build_X, max_lags, lag_method)

    # Estimate final model
    z_dep, X, var_names = build_X(z, x_adj, opt_lag)
    ols = _ols(z_dep, X)

    # t‑statistic on β₁ (first coefficient)
    t_stat = ols["t_stats"][0]

    # Critical values
    cv = get_kss_cv(case)

    # Build result
    result = TestResult(
        test_name="KSS (2003) Nonlinear Unit Root Test",
        statistic_name="tNL",
        statistic=t_stat,
        critical_values=cv,
        selected_lag=opt_lag,
        lag_method=lag_method.upper(),
        case=case,
        null_hypothesis="Unit root (linear random walk)",
        alt_hypothesis="Globally stationary ESTAR process",
        model_summary=_make_model_summary(ols, var_names),
        reference=(
            "Kapetanios, G., Shin, Y., & Snell, A. (2003). "
            "Testing for a unit root in the nonlinear STAR framework. "
            "Journal of Econometrics, 112(2), 359-379."
        ),
    )
    result._make_decisions(tail="left")
    return result
