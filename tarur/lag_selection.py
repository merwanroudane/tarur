"""
TARUR — Lag Selection Utilities
================================
AIC, BIC, and t‑stat‑based automatic lag‑length selection.
"""

from __future__ import annotations

import numpy as np
from tarur.core import _ols


def select_lag(
    z: np.ndarray,
    x: np.ndarray,
    build_X_func,
    max_lags: int,
    method: str = "aic",
) -> int:
    """
    Select optimal lag length for unit‑root test regressions.

    Parameters
    ----------
    z : array
        First difference of the series.
    x : array
        The (possibly transformed) level series.
    build_X_func : callable
        ``build_X_func(z, x, lag)`` → (y_dep, X_reg, var_names).
    max_lags : int
        Maximum lag to consider.
    method : str
        "aic", "bic", or "t-stat" (general‑to‑specific).

    Returns
    -------
    int : optimal lag order (0 ≤ lag ≤ max_lags).
    """
    method = method.lower().strip()
    if method in ("aic", "bic"):
        return _info_criterion_lag(z, x, build_X_func, max_lags, method)
    elif method in ("t-stat", "tstat", "t_stat", "t"):
        return _tstat_lag(z, x, build_X_func, max_lags)
    else:
        raise ValueError(f"Unknown lag method '{method}'. Use 'aic', 'bic', or 't-stat'.")


def _info_criterion_lag(z, x, build_X_func, max_lags, criterion):
    """Select lag that minimizes AIC or BIC."""
    best_ic = np.inf
    best_lag = 0

    for lag in range(max_lags + 1):
        try:
            y_dep, X_reg, _ = build_X_func(z, x, lag)
            result = _ols(y_dep, X_reg)
            ic = result["aic"] if criterion == "aic" else result["bic"]
            if ic < best_ic:
                best_ic = ic
                best_lag = lag
        except Exception:
            continue

    return best_lag


def _tstat_lag(z, x, build_X_func, max_lags):
    """
    General‑to‑specific: start from max_lags, drop last lag if its
    p‑value > 0.10, repeat.
    """
    for lag in range(max_lags, 0, -1):
        try:
            y_dep, X_reg, _ = build_X_func(z, x, lag)
            result = _ols(y_dep, X_reg)
            # Check p‑value of the last lagged‑difference coefficient
            last_p = result["p_values"][-1]
            if last_p <= 0.10:
                return lag
        except Exception:
            continue

    return 0


# ═══════════════════════════════════════════════════════════════════════════
# Common regression builders used across tests
# ═══════════════════════════════════════════════════════════════════════════

def _embed_diff_lags(z: np.ndarray, lag: int):
    """
    Create lagged‑difference matrix (equivalent to R's embed).

    Returns (z_dep, z_diff_lags) both trimmed to same length.
    z_dep = z[lag:]
    z_diff_lags = [z[lag-1:-(1)], z[lag-2:-(2)], ...] if lag > 0
    """
    n = len(z)
    if lag == 0:
        return z, np.empty((n, 0))

    z_dep = z[lag:]
    lags_list = []
    for i in range(1, lag + 1):
        lags_list.append(z[lag - i : n - i])
    z_diff_lags = np.column_stack(lags_list)
    return z_dep, z_diff_lags
