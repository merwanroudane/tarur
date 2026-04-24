"""TARUR — Publication-Quality Visualizations."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({"font.family":"serif","font.size":11,
    "axes.spines.top":False,"axes.spines.right":False})

def plot_test_result(r, ax=None):
    """Plot test statistic vs critical value bands."""
    if ax is None: fig,ax=plt.subplots(figsize=(8,3))
    cv=r.critical_values.values
    colors={"1%":"#e74c3c","5%":"#e67e22","10%":"#f1c40f"}
    # Bar for statistic
    bar_color="#2ecc71" if r.decision.get("5%",False) else "#95a5a6"
    ax.barh(0,r.statistic,height=0.4,color=bar_color,alpha=0.8,edgecolor="white",label=f"{r.statistic_name}={r.statistic:.3f}")
    for i,(k,v) in enumerate(cv.items()):
        if k=="p-value":continue
        ax.axvline(v,color=colors.get(k,"gray"),linestyle="--",lw=1.5,label=f"CV {k}: {v:.3f}")
    ax.set_yticks([]);ax.set_xlabel("Test Statistic")
    ax.set_title(r.test_name,fontsize=12,fontweight="bold")
    ax.legend(loc="best",fontsize=8);plt.tight_layout()
    return ax

def plot_batch(batch):
    """Dashboard comparing all test results."""
    n=len(batch.results)
    fig,axes=plt.subplots(n,1,figsize=(10,max(3,n*1.2)),sharex=False)
    if n==1:axes=[axes]
    for ax,r in zip(axes,batch.results):
        plot_test_result(r,ax=ax)
    plt.tight_layout();return fig

def plot_series_analysis(x, title="Series Analysis"):
    """Plot series with level, differences, and ACF."""
    x=np.asarray(x)
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    axes[0,0].plot(x,color="#2c3e50",lw=0.8);axes[0,0].set_title("Level",fontweight="bold")
    axes[0,0].fill_between(range(len(x)),x,alpha=0.1,color="#3498db")
    d=np.diff(x);axes[0,1].plot(d,color="#e74c3c",lw=0.6);axes[0,1].set_title("First Difference",fontweight="bold")
    axes[0,1].axhline(0,color="gray",lw=0.5)
    # ACF
    from numpy.fft import fft,ifft
    n=len(x);xd=x-np.mean(x);r_full=np.real(ifft(np.abs(fft(xd,2*n))**2))[:n]/np.sum(xd**2)
    lags_show=min(40,n//2);axes[1,0].bar(range(lags_show),r_full[:lags_show],color="#3498db",alpha=0.7,width=0.6)
    ci=1.96/np.sqrt(n);axes[1,0].axhline(ci,color="red",ls="--",lw=0.8);axes[1,0].axhline(-ci,color="red",ls="--",lw=0.8)
    axes[1,0].set_title("ACF (Level)",fontweight="bold")
    # Histogram
    axes[1,1].hist(x,bins=30,color="#9b59b6",alpha=0.7,edgecolor="white")
    axes[1,1].set_title("Distribution",fontweight="bold")
    fig.suptitle(title,fontsize=14,fontweight="bold",y=1.01)
    plt.tight_layout();return fig
