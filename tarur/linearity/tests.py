"""Terasvirta (1994) Linearity Test & ARCH/McLeod-Li Diagnostics."""
from __future__ import annotations
import numpy as np
from scipy import stats as sp_stats
from tarur.core import TestResult,_validate_series,_ols

def terasvirta_test(x,d=1,max_p=4):
    x=_validate_series(x)
    if d>max_p: raise ValueError("d must be <= max_p")
    # Select AR order by AIC
    best_aic=np.inf;best_p=1
    for p in range(1,max_p+1):
        X_embed=np.column_stack([x[p-j:len(x)-j] for j in range(p)])
        y=x[p:];o=_ols(y,X_embed)
        if o["aic"]<best_aic:best_aic=o["aic"];best_p=p
    p=best_p;y=x[p:];X=np.column_stack([x[p-j:len(x)-j] for j in range(p)])
    ytd=x[p-d:len(x)-d];ytd2=ytd**2;ytd3=ytd**3
    a=X*ytd[:,None];b=X*ytd2[:,None];c=X*ytd3[:,None]
    # Linearity test
    Xu=np.column_stack([X,a,b,c]);ou=_ols(y,Xu);SSEu=np.sum(ou["residuals"]**2)
    Xr=X;o_r=_ols(y,Xr);SSEr=np.sum(o_r["residuals"]**2)
    h1=a.shape[1]+b.shape[1]+c.shape[1];h2=len(y)-Xu.shape[1]
    F_lin=((SSEr-SSEu)/h1)/(SSEu/h2) if h2>0 else 0
    p_lin=sp_stats.f.sf(F_lin,h1,h2)
    # H01-H03 sequential tests
    ou1=_ols(y,np.column_stack([X,a]));sse1=np.sum(ou1["residuals"]**2)
    h1a=a.shape[1];h2a=len(y)-X.shape[1]-a.shape[1]
    H01=((SSEr-sse1)/h1a)/(sse1/h2a) if h2a>0 else 0;pH01=sp_stats.f.sf(H01,h1a,h2a)
    ou2=_ols(y,np.column_stack([X,a,b]));sse2=np.sum(ou2["residuals"]**2)
    h1b=b.shape[1];h2b=len(y)-X.shape[1]-a.shape[1]-b.shape[1]
    H02=((sse1-sse2)/h1b)/(sse2/h2b) if h2b>0 else 0;pH02=sp_stats.f.sf(H02,h1b,h2b)
    H03=((sse2-SSEu)/c.shape[1])/(SSEu/h2) if h2>0 else 0;pH03=sp_stats.f.sf(H03,c.shape[1],h2)
    # Model selection: LSTAR vs ESTAR
    if pH02<pH01 and pH02<pH03: model_type="ESTAR"
    else: model_type="LSTAR"
    from tarur.core import CriticalValues
    r=TestResult(test_name="Terasvirta (1994) Linearity Test",statistic_name="F_LIN",
        statistic=F_lin,critical_values=CriticalValues({"p-value":p_lin}),
        selected_lag=p,case=f"d={d}",null_hypothesis="Linear AR model",
        alt_hypothesis=f"Nonlinear STAR model (suggested: {model_type})",
        reference="Terasvirta (1994). JASA, 89(425), 208-218.",
        extra={"F_linearity":F_lin,"p_linearity":p_lin,
               "H01":H01,"pH01":pH01,"H02":H02,"pH02":pH02,"H03":H03,"pH03":pH03,
               "suggested_model":model_type,"AR_order":p})
    r.decision={"5%":p_lin<0.05,"10%":p_lin<0.10,"1%":p_lin<0.01}
    r.interpretation=f"{'Reject' if p_lin<0.05 else 'Fail to reject'} linearity (p={p_lin:.4f}). Suggested: {model_type}"
    return r

def arch_test(x,lags=4):
    x=_validate_series(x);e2=x**2;n=len(e2)
    y=e2[lags:];X=np.column_stack([e2[lags-i:n-i] for i in range(1,lags+1)])
    X=np.column_stack([np.ones(len(y)),X])
    o=_ols(y,X);LM=len(y)*o["r2"]
    p=sp_stats.chi2.sf(LM,lags)
    from tarur.core import CriticalValues
    r=TestResult(test_name="Engle ARCH Test",statistic_name="LM",
        statistic=LM,critical_values=CriticalValues({"p-value":p}),
        selected_lag=lags,null_hypothesis="No ARCH effects",
        alt_hypothesis="ARCH effects present",
        reference="Engle, R. (1982). Econometrica, 50(4), 987-1007.")
    r.decision={"5%":p<0.05,"10%":p<0.10,"1%":p<0.01}
    r.interpretation=f"{'Reject' if p<0.05 else 'Fail to reject'} no ARCH (p={p:.4f})"
    return r

def mcleod_li_test(x,lags=12):
    x=_validate_series(x);e2=x**2;n=len(e2);m=np.mean(e2)
    acf_vals=[]
    for k in range(1,lags+1):
        acf_vals.append(np.sum((e2[:n-k]-m)*(e2[k:]-m))/np.sum((e2-m)**2))
    Q=n*(n+2)*sum(a**2/(n-k) for k,a in enumerate(acf_vals,1))
    p=sp_stats.chi2.sf(Q,lags)
    from tarur.core import CriticalValues
    r=TestResult(test_name="McLeod-Li Test",statistic_name="Q",
        statistic=Q,critical_values=CriticalValues({"p-value":p}),
        selected_lag=lags,null_hypothesis="No nonlinear dependence",
        alt_hypothesis="Nonlinear dependence in squared residuals",
        reference="McLeod & Li (1983). J. Time Series Analysis, 4(4), 269-273.")
    r.decision={"5%":p<0.05,"10%":p<0.10,"1%":p<0.01}
    r.interpretation=f"{'Reject' if p<0.05 else 'Fail to reject'} no nonlinearity (p={p:.4f})"
    return r
