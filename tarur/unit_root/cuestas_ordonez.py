"""Cuestas & Ordonez (2014) — NLS detrending + KSS test."""
from __future__ import annotations
import numpy as np
from scipy.optimize import least_squares
from tarur.core import TestResult, _validate_series, _ols, _make_model_summary
from tarur.lag_selection import select_lag, _embed_diff_lags
from tarur.critical_values import get_cuestas_ordonez_cv

def cuestas_ordonez_test(x, max_lags=8, lag_method="aic"):
    x = _validate_series(x); n = len(x)
    trend = np.arange(n, dtype=np.float64)
    logistic = 1.0/(1.0+np.exp(-0.5*trend))
    X_nls = np.column_stack([np.ones(n), trend, logistic, trend*logistic])
    beta = np.linalg.lstsq(X_nls, x, rcond=None)[0]
    x_adj = x - X_nls @ beta
    z = np.diff(x_adj); nz = len(z)
    def build_X(z, xa, lag):
        zd, zl = _embed_diff_lags(z, lag); m = len(zd)
        xl = (xa[:nz]**3)[lag:lag+m]
        if lag==0: return zd, xl.reshape(-1,1), ["y3"]
        return zd, np.column_stack([xl,zl]), ["y3"]+[f"dz{i+1}" for i in range(lag)]
    opt = select_lag(z, x_adj, build_X, max_lags, lag_method)
    zd, X, vn = build_X(z, x_adj, opt); o = _ols(zd, X)
    t = o["t_stats"][0]; cv = get_cuestas_ordonez_cv()
    r = TestResult(test_name="Cuestas & Ordonez (2014)", statistic_name="tNL",
        statistic=t, critical_values=cv, selected_lag=opt, lag_method=lag_method.upper(),
        case="NLS detrended", null_hypothesis="Unit root",
        alt_hypothesis="Stationary after smooth transition detrending",
        model_summary=_make_model_summary(o,vn),
        reference="Cuestas & Ordonez (2014). Applied Economics Letters, 21(14), 969-972.")
    r._make_decisions(tail="left"); return r
