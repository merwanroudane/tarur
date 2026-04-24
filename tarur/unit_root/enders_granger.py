"""Enders & Granger (1998) — MTAR Unit Root Test (native, no tsDyn)."""
from __future__ import annotations
import numpy as np
from scipy import stats as sp_stats
from tarur.core import TestResult, _validate_series, _prepare_case, _ols, _make_model_summary
from tarur.lag_selection import _embed_diff_lags
from tarur.critical_values import get_enders_granger_cv

def enders_granger_test(x, case="demeaned", max_lags=8, lag_method="aic"):
    x = _validate_series(x); x_adj = _prepare_case(x, case)
    z = np.diff(x_adj); n = len(z)
    inc_map = {"raw":"none","demeaned":"const","detrended":"both"}
    include = inc_map.get(case.lower(),"none")
    best_aic, opt_lag = np.inf, 1
    for lag in range(1, max_lags+1):
        try:
            zd, zl = _embed_diff_lags(z, lag); m = len(zd)
            xl = x_adj[:n][lag:lag+m]; dz = np.diff(x_adj[:n+1])
            It = (dz[lag-1:lag-1+m] >= 0).astype(float)
            pos = It*xl; neg = (1-It)*xl
            cols = [pos, neg]
            if include in ("const","both"): cols.append(np.ones(m))
            if include == "both": cols.append(np.arange(m, dtype=float))
            if lag > 0: cols.append(zl)
            X = np.column_stack(cols); o = _ols(zd, X)
            if o["aic"] < best_aic: best_aic = o["aic"]; opt_lag = lag
        except: continue
    zd, zl = _embed_diff_lags(z, opt_lag); m = len(zd)
    xl = x_adj[:n][opt_lag:opt_lag+m]; dz = np.diff(x_adj[:n+1])
    It = (dz[opt_lag-1:opt_lag-1+m] >= 0).astype(float)
    pos = It*xl; neg = (1-It)*xl
    cols = [pos, neg]; vn = ["rho_pos","rho_neg"]
    if include in ("const","both"): cols.append(np.ones(m)); vn.append("const")
    if include == "both": cols.append(np.arange(m,dtype=float)); vn.append("trend")
    if opt_lag > 0: cols.append(zl); vn += [f"dz{i+1}" for i in range(opt_lag)]
    X = np.column_stack(cols); o = _ols(zd, X)
    rho_p, rho_n = o["beta"][0], o["beta"][1]
    se_p, se_n = o["se"][0], o["se"][1]
    sse_u = np.sum(o["residuals"]**2)
    # Restricted (rho_p=rho_n=0)
    cols_r = [c for i,c in enumerate(cols) if i >= 2]
    if len(cols_r)==0: sse_r = np.sum(zd**2)
    else: sse_r = np.sum(_ols(zd, np.column_stack(cols_r))["residuals"]**2)
    df2 = m - X.shape[1]; Phi = ((sse_r-sse_u)/2)/(sse_u/df2) if df2>0 else 0
    # t-max
    t_p = rho_p/se_p; t_n = rho_n/se_n
    # Symmetry test (rho_p=rho_n)
    R = np.zeros(X.shape[1]); R[0]=1; R[1]=-1
    cov = o["sigma2"]*np.linalg.inv(X.T@X)
    F_sym = ((R@o["beta"])**2)/(R@cov@R) if (R@cov@R)>0 else 0
    F_sym_p = sp_stats.f.sf(F_sym, 1, df2)
    cv = get_enders_granger_cv(include)
    r = TestResult(test_name="Enders & Granger (1998) MTAR", statistic_name="Phi",
        statistic=Phi, critical_values=cv, selected_lag=opt_lag, lag_method=lag_method.upper(),
        case=case, null_hypothesis="Unit root",
        alt_hypothesis="MTAR stationary with asymmetric adjustment",
        model_summary=_make_model_summary(o,vn),
        reference="Enders & Granger (1998). JBES, 16(3), 304-311.",
        extra={"rho_pos":rho_p,"rho_neg":rho_n,"t_pos":t_p,"t_neg":t_n,
               "F_symmetry":F_sym,"F_sym_pvalue":F_sym_p})
    r._make_decisions(tail="right"); return r
