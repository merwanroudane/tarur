"""
TARUR Core Module
=================
Base classes for test results, critical values, and common utilities.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Literal


# ---------------------------------------------------------------------------
# Critical‑Value Container
# ---------------------------------------------------------------------------

@dataclass
class CriticalValues:
    """Container for asymptotic / finite‑sample critical values."""

    values: Dict[str, float]          # e.g. {"1%": -3.48, "5%": -2.93, "10%": -2.66}
    sample_size: Optional[int] = None # None → asymptotic
    source: str = ""                  # e.g. "Kruse (2011), Table 1"

    # Convenience helpers
    @property
    def cv1(self) -> float:
        return self.values.get("1%", np.nan)

    @property
    def cv5(self) -> float:
        return self.values.get("5%", np.nan)

    @property
    def cv10(self) -> float:
        return self.values.get("10%", np.nan)


# ---------------------------------------------------------------------------
# Model Summary
# ---------------------------------------------------------------------------

@dataclass
class ModelSummary:
    """Lightweight summary of the estimated auxiliary regression."""

    coefficients: pd.DataFrame       # columns: estimate, std_err, t_stat, p_value
    residuals: np.ndarray
    r_squared: float = 0.0
    adj_r_squared: float = 0.0
    aic: float = 0.0
    bic: float = 0.0
    nobs: int = 0
    df_resid: int = 0


# ---------------------------------------------------------------------------
# TestResult — The Unified Output Object
# ---------------------------------------------------------------------------

@dataclass
class TestResult:
    """
    Universal result container returned by every TARUR test.

    Attributes
    ----------
    test_name : str
        Human‑readable name, e.g. "KSS (2003) Nonlinear Unit Root Test".
    statistic_name : str
        Label for the test statistic, e.g. "tNL", "τ", "F_AE".
    statistic : float
        Computed test statistic value.
    critical_values : CriticalValues
        Relevant critical values for comparison.
    selected_lag : int
        Optimal lag order selected by the chosen criterion.
    lag_method : str
        Lag selection method used ("AIC", "BIC", "t-stat").
    case : str
        Deterministic specification ("raw", "demeaned", "detrended").
    null_hypothesis : str
        Statement of H₀.
    alt_hypothesis : str
        Statement of H₁.
    decision : Dict[str, bool]
        Rejection decisions at each significance level.
    interpretation : str
        One‑line plain‑English interpretation.
    model_summary : Optional[ModelSummary]
        Regression details (if available).
    reference : str
        Full citation.
    extra : Dict
        Any test‑specific extra outputs.
    """

    test_name: str = ""
    statistic_name: str = ""
    statistic: float = np.nan
    critical_values: CriticalValues = field(default_factory=lambda: CriticalValues({}))
    selected_lag: int = 0
    lag_method: str = ""
    case: str = ""
    null_hypothesis: str = "Unit root (nonstationary)"
    alt_hypothesis: str = "Globally stationary nonlinear process"
    decision: Dict[str, bool] = field(default_factory=dict)
    interpretation: str = ""
    model_summary: Optional[ModelSummary] = None
    reference: str = ""
    extra: Dict = field(default_factory=dict)

    # ── Decision logic ────────────────────────────────────────────────
    def _make_decisions(self, tail: str = "left"):
        """
        Populate ``self.decision`` and ``self.interpretation``.

        Parameters
        ----------
        tail : str
            "left"  → reject when stat < CV  (t‑type tests)
            "right" → reject when stat > CV  (F / Wald / χ² tests)
        """
        cv = self.critical_values.values
        self.decision = {}
        reject_level = None

        for level_str in ("1%", "5%", "10%"):
            if level_str not in cv:
                continue
            if tail == "left":
                rejected = self.statistic < cv[level_str]
            else:
                rejected = self.statistic > cv[level_str]
            self.decision[level_str] = rejected
            if rejected:
                reject_level = level_str

        if reject_level:
            self.interpretation = (
                f"Reject H0 at the {reject_level} significance level. "
                f"{self.alt_hypothesis}."
            )
        else:
            self.interpretation = (
                "Fail to reject H0 at conventional significance levels. "
                f"{self.null_hypothesis}."
            )

    # ── Pretty printing ───────────────────────────────────────────────
    def __str__(self) -> str:
        from tarur.tables import format_result
        return format_result(self)

    def __repr__(self) -> str:
        return (
            f"TestResult(test='{self.test_name}', "
            f"stat={self.statistic:.4f}, "
            f"decision={self.decision})"
        )

    # ── Export helpers ─────────────────────────────────────────────────
    def to_dict(self) -> dict:
        """Flat dictionary suitable for a DataFrame row."""
        d = {
            "test": self.test_name,
            "statistic_name": self.statistic_name,
            "statistic": self.statistic,
            "selected_lag": self.selected_lag,
            "lag_method": self.lag_method,
            "case": self.case,
        }
        for k, v in self.critical_values.values.items():
            d[f"cv_{k}"] = v
        for k, v in self.decision.items():
            d[f"reject_{k}"] = v
        d["interpretation"] = self.interpretation
        return d

    def to_latex(self) -> str:
        """Return a LaTeX‑formatted results table snippet."""
        from tarur.tables import result_to_latex
        return result_to_latex(self)

    def plot(self, ax=None):
        """Quick visual of statistic vs critical‑value bands."""
        from tarur.visualization import plot_test_result
        return plot_test_result(self, ax=ax)


# ---------------------------------------------------------------------------
# BatchResult — for run_all_tests()
# ---------------------------------------------------------------------------

@dataclass
class BatchResult:
    """Container for results from multiple tests on the same series."""

    results: List[TestResult] = field(default_factory=list)

    def summary(self) -> pd.DataFrame:
        """Return a comparison DataFrame."""
        rows = [r.to_dict() for r in self.results]
        return pd.DataFrame(rows)

    def __str__(self) -> str:
        from tarur.tables import format_batch
        return format_batch(self)

    def to_latex(self) -> str:
        from tarur.tables import batch_to_latex
        return batch_to_latex(self)

    def plot(self):
        from tarur.visualization import plot_batch
        return plot_batch(self)


# ---------------------------------------------------------------------------
# Helpers shared across tests
# ---------------------------------------------------------------------------

def _validate_series(x, min_length: int = 20) -> np.ndarray:
    """Convert input to 1‑D float64 array and validate."""
    x = np.asarray(x, dtype=np.float64).squeeze()
    if x.ndim != 1:
        raise ValueError(f"Expected a 1-D series, got shape {x.shape}")
    if len(x) < min_length:
        raise ValueError(
            f"Series length {len(x)} is below minimum {min_length}"
        )
    if np.any(np.isnan(x)):
        raise ValueError("Series contains NaN values. Please clean data first.")
    return x


def _prepare_case(x: np.ndarray, case: str) -> np.ndarray:
    """
    Apply deterministic adjustment.

    Parameters
    ----------
    case : str
        "raw"       → no adjustment
        "demeaned"  → subtract OLS mean
        "detrended" → subtract OLS linear trend
    """
    case = case.lower().strip()
    if case in ("raw", "none", "1"):
        return x.copy()
    elif case in ("demeaned", "demean", "constant", "2"):
        return x - np.mean(x)
    elif case in ("detrended", "detrend", "trend", "3"):
        n = len(x)
        trend = np.arange(n, dtype=np.float64)
        ones = np.ones(n)
        X = np.column_stack([ones, trend])
        beta = np.linalg.lstsq(X, x, rcond=None)[0]
        return x - X @ beta
    else:
        raise ValueError(f"Unknown case '{case}'. Use 'raw', 'demeaned', or 'detrended'.")


def _ols(y: np.ndarray, X: np.ndarray) -> dict:
    """
    Minimal OLS with full diagnostics.

    Returns dict with keys: beta, residuals, se, t_stats, p_values,
    sigma2, aic, bic, r2, r2_adj, nobs, k
    """
    from scipy import stats as sp_stats

    n, k = X.shape
    beta, residuals_sum, rank, sv = np.linalg.lstsq(X, y, rcond=None)
    fitted = X @ beta
    resid = y - fitted
    df = n - k

    sigma2 = np.sum(resid ** 2) / df if df > 0 else np.inf
    cov = sigma2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    t_stats = beta / se
    p_values = 2.0 * sp_stats.t.sf(np.abs(t_stats), df)

    ss_res = np.sum(resid ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    r2_adj = 1 - (1 - r2) * (n - 1) / df if df > 0 else 0.0

    ll = -0.5 * n * (np.log(2 * np.pi * ss_res / n) + 1)
    aic = -2 * ll + 2 * k
    bic = -2 * ll + k * np.log(n)

    return {
        "beta": beta,
        "residuals": resid,
        "fitted": fitted,
        "se": se,
        "t_stats": t_stats,
        "p_values": p_values,
        "sigma2": sigma2,
        "aic": aic,
        "bic": bic,
        "r2": r2,
        "r2_adj": r2_adj,
        "nobs": n,
        "k": k,
        "df": df,
    }


def _make_model_summary(ols_result: dict, var_names: list) -> ModelSummary:
    """Build a ModelSummary from _ols() output."""
    coef_df = pd.DataFrame({
        "estimate": ols_result["beta"],
        "std_err": ols_result["se"],
        "t_stat": ols_result["t_stats"],
        "p_value": ols_result["p_values"],
    }, index=var_names)

    return ModelSummary(
        coefficients=coef_df,
        residuals=ols_result["residuals"],
        r_squared=ols_result["r2"],
        adj_r_squared=ols_result["r2_adj"],
        aic=ols_result["aic"],
        bic=ols_result["bic"],
        nobs=ols_result["nobs"],
        df_resid=ols_result["df"],
    )
