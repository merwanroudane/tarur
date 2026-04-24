"""Cook & Vougas (2009) — Smooth Transition MTAR Test."""
from __future__ import annotations
import numpy as np
from scipy.optimize import least_squares
from tarur.core import TestResult,_validate_series,_ols,_make_model_summary
from tarur.lag_selection import _embed_diff_lags
from tarur.critical_values import get_cook_vougas_cv

def _logistic(t,g,tau,n): return 1.0/(1.0+np.exp(-g*(t-tau*n)))
def _nls(x,model):
    n=len(x);t=np.arange(n,dtype=np.float64)
    if model in("A","1"):
        r=lambda p:x-(p[0]+p[1]*_logistic(t,p[2],p[3],n));p0=[np.mean(x),0,1,0.5]
    elif model in("B","2"):
        r=lambda p:x-(p[0]+p[1]*_logistic(t,p[2],p[3],n)+p[4]*t);p0=[np.mean(x),0,1,0.5,0]
    elif model in("C","3"):
        r=lambda p:x-(p[0]+p[1]*_logistic(t,p[2],p[3],n)+p[4]*t+p[5]*t*_logistic(t,p[2],p[3],n));p0=[np.mean(x),0,1,0.5,0,0]
    else:
        r=lambda p:x-(p[0]+p[3]*t*_logistic(t,p[1],p[2],n));p0=[np.mean(x),1,0.5,0]
    try: return least_squares(r,p0,method='lm',max_nfev=2000).fun
    except: return x-np.mean(x)

def cook_vougas_test(x,model="A",max_lags=8):
    x=_validate_series(x);res=_nls(x,model)
    z=np.diff(res);nz=len(z);best_aic=np.inf;opt=1
    for lag in range(1,max_lags+1):
        zd,zl=_embed_diff_lags(z,lag);m=len(zd)
        xl=res[:nz][lag:lag+m];dres=np.diff(res[:nz+1])
        It=(dres[lag-1:lag-1+m]>=0).astype(float)
        pos=It*xl;neg=(1-It)*xl
        X=np.column_stack([pos,neg,zl]) if lag>0 else np.column_stack([pos,neg])
        try:
            o=_ols(zd,X)
            if o["aic"]<best_aic:best_aic=o["aic"];opt=lag
        except:continue
    zd,zl=_embed_diff_lags(z,opt);m=len(zd)
    xl=res[:nz][opt:opt+m];dres=np.diff(res[:nz+1])
    It=(dres[opt-1:opt-1+m]>=0).astype(float)
    pos=It*xl;neg=(1-It)*xl
    vn=["rho_pos","rho_neg"]
    X=np.column_stack([pos,neg,zl]) if opt>0 else np.column_stack([pos,neg])
    if opt>0: vn+=[f"dz{i+1}" for i in range(opt)]
    o=_ols(zd,X);sse_u=np.sum(o["residuals"]**2)
    if opt>0:sse_r=np.sum(_ols(zd,zl)["residuals"]**2)
    else:sse_r=np.sum(zd**2)
    df2=m-X.shape[1];F=((sse_r-sse_u)/2)/(sse_u/df2) if df2>0 else 0
    cv=get_cook_vougas_cv(model, len(x))
    r=TestResult(test_name=f"Cook & Vougas (2009) Model {model}",statistic_name="F_MTAR",
        statistic=F,critical_values=cv,selected_lag=opt,lag_method="AIC",
        case=f"ST-MTAR Model {model}",null_hypothesis="Unit root",
        alt_hypothesis="Stationary around smooth transition with asymmetric adjustment",
        model_summary=_make_model_summary(o,vn),
        reference="Cook & Vougas (2009).")
    r._make_decisions(tail="right");return r
