"""Pascalau (2007) Asymmetric NLSTAR Unit Root Test."""
from __future__ import annotations
import numpy as np
from tarur.core import TestResult, _validate_series, _prepare_case, _ols, _make_model_summary
from tarur.lag_selection import select_lag, _embed_diff_lags
from tarur.critical_values import get_pascalau_cv

def pascalau_test(x, case="demeaned", max_lags=8, lag_method="aic"):
    x = _validate_series(x); x_adj = _prepare_case(x, case)
    z = np.diff(x_adj); n = len(z)
    def build_X(z, x_adj, lag):
        zd, zl = _embed_diff_lags(z, lag); m = len(zd)
        x4 = (x_adj[:n]**4)[lag:lag+m]; x3 = (x_adj[:n]**3)[lag:lag+m]; x2 = (x_adj[:n]**2)[lag:lag+m]
        if lag == 0: return zd, np.column_stack([x4,x3,x2]), ["y4","y3","y2"]
        return zd, np.column_stack([x4,x3,x2,zl]), ["y4","y3","y2"]+[f"dz{i+1}" for i in range(lag)]
    opt = select_lag(z, x_adj, build_X, max_lags, lag_method)
    zd, X, vn = build_X(z, x_adj, opt)
    ou = _ols(zd, X); sse_u = np.sum(ou["residuals"]**2)
    if opt == 0: sse_r = np.sum(zd**2)
    else:
        _, zl = _embed_diff_lags(z, opt); sse_r = np.sum(_ols(zd, zl)["residuals"]**2)
    F = ((sse_r-sse_u)/3)/(sse_u/(len(zd)-X.shape[1])) if (len(zd)-X.shape[1])>0 else 0
    cv = get_pascalau_cv(case)
    r = TestResult(test_name="Pascalau (2007) Asymmetric NLSTAR", statistic_name="F",
        statistic=F, critical_values=cv, selected_lag=opt, lag_method=lag_method.upper(),
        case=case, null_hypothesis="Unit root", alt_hypothesis="Asymmetric NLSTAR stationary",
        model_summary=_make_model_summary(ou,vn),
        reference="Pascalau, R. (2007). Testing for a unit root in the asymmetric nonlinear smooth transition framework.")
    r._make_decisions(tail="right"); return r
