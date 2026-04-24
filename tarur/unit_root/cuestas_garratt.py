"""Cuestas & Garratt (2011) Nonlinear Unit Root Test."""
from __future__ import annotations
import numpy as np
from tarur.core import TestResult, _validate_series, _ols, _make_model_summary
from tarur.lag_selection import select_lag, _embed_diff_lags
from tarur.critical_values import get_cuestas_garratt_cv

def cuestas_garratt_test(x, max_lags=8, lag_method="aic"):
    x = _validate_series(x)
    n = len(x)
    trend = np.arange(n, dtype=np.float64)
    X_det = np.column_stack([np.ones(n), trend, trend**2, trend**3])
    x_adj = x - X_det @ np.linalg.lstsq(X_det, x, rcond=None)[0]
    z = np.diff(x_adj); nz = len(z)

    def build_X(z, x_adj, lag):
        z_dep, z_lags = _embed_diff_lags(z, lag)
        m = len(z_dep)
        xl1 = (x_adj[:nz]**3)[lag:lag+m]
        xl2 = (x_adj[:nz]**2)[lag:lag+m]
        if lag == 0:
            return z_dep, np.column_stack([xl1, xl2]), ["y3","y2"]
        return z_dep, np.column_stack([xl1, xl2, z_lags]), ["y3","y2"]+[f"dz{i+1}" for i in range(lag)]

    opt = select_lag(z, x_adj, build_X, max_lags, lag_method)
    z_dep, X, vn = build_X(z, x_adj, opt)
    o = _ols(z_dep, X)
    b = o["beta"][:2]; V = np.linalg.inv(X.T@X)*o["sigma2"]
    chi2 = float(b @ np.linalg.inv(V[:2,:2]) @ b)
    cv = get_cuestas_garratt_cv()
    r = TestResult(test_name="Cuestas & Garratt (2011)", statistic_name="chi2",
        statistic=chi2, critical_values=cv, selected_lag=opt, lag_method=lag_method.upper(),
        case="cubic detrended", null_hypothesis="Unit root",
        alt_hypothesis="Globally stationary nonlinear", model_summary=_make_model_summary(o,vn),
        reference="Cuestas & Garratt (2011). Empirical Economics, 41(3), 555-563.")
    r._make_decisions(tail="right"); return r
