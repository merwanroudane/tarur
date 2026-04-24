"""LNV (1998) — Leybourne, Newbold & Vougas Unit Root Test with Smooth Transition."""
from __future__ import annotations
import numpy as np
from scipy.optimize import least_squares
from tarur.core import TestResult, _validate_series, _ols, _make_model_summary
from tarur.lag_selection import select_lag, _embed_diff_lags
from tarur.critical_values import get_lnv_cv

def _logistic(t, gamma, tau, n): return 1.0/(1.0+np.exp(-gamma*(t - tau*n)))

def _nls_detrend(x, model):
    n = len(x); t = np.arange(n, dtype=np.float64)
    if model in ("A","1"):
        def resid(p): return x - (p[0] + p[1]*_logistic(t,p[2],p[3],n))
        p0 = [np.mean(x), 0.0, 1.0, 0.5]
    elif model in ("B","2"):
        def resid(p): return x - (p[0] + p[1]*_logistic(t,p[2],p[3],n) + p[4]*t)
        p0 = [np.mean(x), 0.0, 1.0, 0.5, 0.0]
    else:
        def resid(p): return x - (p[0] + p[1]*_logistic(t,p[2],p[3],n) + p[4]*t + p[5]*t*_logistic(t,p[2],p[3],n))
        p0 = [np.mean(x), 0.0, 1.0, 0.5, 0.0, 0.0]
    try:
        sol = least_squares(resid, p0, method='lm', max_nfev=2000)
        return sol.fun
    except: return x - np.mean(x)

def lnv_test(x, model="A", max_lags=8, lag_method="aic"):
    x = _validate_series(x)
    res = _nls_detrend(x, model)
    z = np.diff(res); nz = len(z)
    def build_X(z, res, lag):
        zd, zl = _embed_diff_lags(z, lag); m = len(zd)
        xl = res[:nz][lag:lag+m]
        if lag==0: return zd, xl.reshape(-1,1), ["y_lag1"]
        return zd, np.column_stack([xl,zl]), ["y_lag1"]+[f"dz{i+1}" for i in range(lag)]
    opt = select_lag(z, res, build_X, max_lags, lag_method)
    zd, X, vn = build_X(z, res, opt); o = _ols(zd, X)
    t = o["t_stats"][0]; cv = get_lnv_cv(model, len(x))
    r = TestResult(test_name=f"LNV (1998) Model {model}", statistic_name="t_ADF",
        statistic=t, critical_values=cv, selected_lag=opt, lag_method=lag_method.upper(),
        case=f"NLS Model {model}", null_hypothesis="Unit root",
        alt_hypothesis="Stationary around smooth logistic transition",
        model_summary=_make_model_summary(o,vn),
        reference="Leybourne, Newbold & Vougas (1998). J. Time Series Analysis, 19(1), 83-97.")
    r._make_decisions(tail="left"); return r
