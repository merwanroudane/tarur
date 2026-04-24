"""KSS (2006) Nonlinear Cointegration & Enders-Siklos (2001) TAR Cointegration."""
from __future__ import annotations
import numpy as np
from tarur.core import TestResult,_validate_series,_ols,_make_model_summary
from tarur.lag_selection import select_lag,_embed_diff_lags
from tarur.critical_values import get_kss_cv,get_enders_siklos_cv

def kss_cointegration_test(y,x,case="demeaned",max_lags=8,lag_method="aic"):
    y=_validate_series(y);x=_validate_series(x)
    res=y-np.linalg.lstsq(np.column_stack([np.ones(len(x)),x]),y,rcond=None)[0]@np.column_stack([np.ones(len(x)),x]).T@np.ones(1) if False else None
    X_coint=np.column_stack([np.ones(len(x)),x])
    beta=np.linalg.lstsq(X_coint,y,rcond=None)[0]
    res=y-X_coint@beta
    from tarur.unit_root.kss import kss_test
    r=kss_test(res,case=case,max_lags=max_lags,lag_method=lag_method)
    r.test_name="KSS (2006) Nonlinear Cointegration Test"
    r.null_hypothesis="No cointegration (residuals have unit root)"
    r.alt_hypothesis="Nonlinear cointegration (ESTAR stationary residuals)"
    r.reference="Kapetanios, Shin & Snell (2006). Econometric Theory, 22(2), 279-303."
    return r

def enders_siklos_test(y,x,max_lags=8):
    y=_validate_series(y);x=_validate_series(x)
    X_c=np.column_stack([np.ones(len(x)),x])
    beta=np.linalg.lstsq(X_c,y,rcond=None)[0]
    res=y-X_c@beta
    from tarur.unit_root.enders_granger import enders_granger_test
    r=enders_granger_test(res,case="raw",max_lags=max_lags)
    r.test_name="Enders & Siklos (2001) TAR Cointegration Test"
    r.null_hypothesis="No cointegration"
    r.alt_hypothesis="Threshold cointegration with asymmetric adjustment"
    r.reference="Enders & Siklos (2001). JBES, 19(2), 166-176."
    r.critical_values=get_enders_siklos_cv("none")
    return r
