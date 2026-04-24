"""Kilic (2011) and Park & Shintani (2016) inf-t unit root tests."""
from __future__ import annotations
import numpy as np
from tarur.core import TestResult,_validate_series,_prepare_case,_ols,_make_model_summary
from tarur.lag_selection import select_lag,_embed_diff_lags
from tarur.critical_values import get_kilic_cv,get_park_shintani_cv

def _inf_t_test(x, case, max_lags, lag_method, cv_func, name, ref, alt):
    x=_validate_series(x);x_adj=_prepare_case(x,case)
    z=np.diff(x_adj);sd_z=np.std(z)+1e-12;n=len(z)
    lo=1/(100*sd_z);hi=min(100/sd_z,5.0);step=max((hi-lo)/200,0.005)
    best_t=-np.inf;best_gamma=lo
    # Grid search for optimal gamma
    zd1,zl1=_embed_diff_lags(z,1);m1=len(zd1)
    xl1=x_adj[:n][1:1+m1]
    for gamma in np.arange(lo,hi,step):
        G=1.0-np.exp(-gamma*zl1[:,0]**2)
        X=np.column_stack([xl1*G,zl1])
        try:
            o=_ols(zd1,X);ts=o["t_stats"][0]
            if ts>best_t:best_t=ts;best_gamma=gamma
        except:continue
    # Select lag with optimal gamma
    def build_X(z,xa,lag):
        zd,zl=_embed_diff_lags(z,lag);m=len(zd)
        xl=xa[:n][lag:lag+m]
        if lag==0:
            G=np.ones(m);X=np.column_stack([xl*G]);nn=["xG"]
        else:
            G=1.0-np.exp(-best_gamma*zl[:,0]**2)
            X=np.column_stack([xl*G,zl]);nn=["xG"]+[f"dz{i+1}" for i in range(lag)]
        return zd,X,nn
    opt=select_lag(z,x_adj,build_X,max_lags,lag_method)
    zd,X,vn=build_X(z,x_adj,opt);o=_ols(zd,X);t=o["t_stats"][0]
    cv=cv_func(case)
    r=TestResult(test_name=name,statistic_name="inf_t",statistic=t,
        critical_values=cv,selected_lag=opt,lag_method=lag_method.upper(),
        case=case,null_hypothesis="Unit root",alt_hypothesis=alt,
        model_summary=_make_model_summary(o,vn),reference=ref,
        extra={"optimal_gamma":best_gamma})
    r._make_decisions(tail="left");return r

def kilic_test(x,case="demeaned",max_lags=8,lag_method="aic"):
    return _inf_t_test(x,case,max_lags,lag_method,get_kilic_cv,
        "Kilic (2011) inf-t Unit Root Test",
        "Kilic (2011). Econometric Reviews, 30(3), 274-302.",
        "Stationary ESTAR process")

def park_shintani_test(x,case="raw",max_lags=8,lag_method="aic"):
    return _inf_t_test(x,case,max_lags,lag_method,get_park_shintani_cv,
        "Park & Shintani (2016) inf-t Unit Root Test",
        "Park & Shintani (2016). International Economic Review, 57(2), 635-664.",
        "Transitional autoregressive stationary process")
