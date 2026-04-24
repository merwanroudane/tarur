"""
TARUR — Nonlinear Unit Root Testing Library
============================================

A comprehensive Python library implementing 17+ nonlinear unit root,
cointegration, and linearity tests with embedded critical values,
automatic decision rules, and publication-quality output.

Author: Dr. Merwan Roudane (merwanroudane920@gmail.com)
"""

from tarur._version import __version__

# ── Unit Root Tests ──────────────────────────────────────────────────
from tarur.unit_root.kss import kss_test
from tarur.unit_root.kruse import kruse_test
from tarur.unit_root.sollis2009 import sollis2009_test
from tarur.unit_root.sollis2004 import sollis2004_test
from tarur.unit_root.enders_granger import enders_granger_test
from tarur.unit_root.hu_chen import hu_chen_test
from tarur.unit_root.lnv import lnv_test
from tarur.unit_root.vougas import vougas_test
from tarur.unit_root.harvey_mills import harvey_mills_test
from tarur.unit_root.cook_vougas import cook_vougas_test
from tarur.unit_root.kilic import kilic_test, park_shintani_test
from tarur.unit_root.pascalau import pascalau_test
from tarur.unit_root.cuestas_garratt import cuestas_garratt_test
from tarur.unit_root.cuestas_ordonez import cuestas_ordonez_test

# ── Cointegration Tests ──────────────────────────────────────────────
from tarur.cointegration.tests import kss_cointegration_test, enders_siklos_test

# ── Linearity & Diagnostics ─────────────────────────────────────────
from tarur.linearity.tests import terasvirta_test, arch_test, mcleod_li_test

# ── Visualization ────────────────────────────────────────────────────
from tarur.visualization import plot_series_analysis

# ── Core ─────────────────────────────────────────────────────────────
from tarur.core import TestResult, BatchResult


def run_all_tests(x, case="demeaned", max_lags=8, lag_method="aic",
                  verbose=True) -> BatchResult:
    """
    Run a comprehensive battery of nonlinear unit root tests.

    Parameters
    ----------
    x : array-like
        Time series (level).
    case : str
        "raw", "demeaned", or "detrended".
    max_lags : int
        Maximum lag order.
    lag_method : str
        "aic", "bic", or "t-stat".
    verbose : bool
        Print results table.

    Returns
    -------
    BatchResult with all test outcomes.
    """
    import warnings
    warnings.filterwarnings("ignore")

    tests = [
        ("KSS", lambda: kss_test(x, case, max_lags, lag_method)),
        ("Kruse", lambda: kruse_test(x, case, max_lags, lag_method)),
        ("Sollis2009", lambda: sollis2009_test(x, case, max_lags, lag_method)),
        ("HuChen", lambda: hu_chen_test(x, case, max_lags, lag_method)),
        ("Pascalau", lambda: pascalau_test(x, case, max_lags, lag_method)),
        ("CuestasGarratt", lambda: cuestas_garratt_test(x, max_lags, lag_method)),
        ("CuestasOrdonez", lambda: cuestas_ordonez_test(x, max_lags, lag_method)),
        ("EndersGranger", lambda: enders_granger_test(x, case, max_lags, lag_method)),
        ("LNV_A", lambda: lnv_test(x, "A", max_lags, lag_method)),
        ("Vougas_A", lambda: vougas_test(x, "A", max_lags, lag_method)),
        ("HarveyMills_A", lambda: harvey_mills_test(x, "A", max_lags, lag_method)),
    ]

    batch = BatchResult()
    for name, fn in tests:
        try:
            result = fn()
            batch.results.append(result)
        except Exception as e:
            if verbose:
                print(f"  [SKIP] {name}: {e}")

    if verbose:
        print(batch)

    return batch


__all__ = [
    "__version__",
    # Unit root
    "kss_test", "kruse_test", "sollis2009_test", "sollis2004_test",
    "enders_granger_test", "hu_chen_test", "lnv_test", "vougas_test",
    "harvey_mills_test", "cook_vougas_test", "kilic_test", "park_shintani_test",
    "pascalau_test", "cuestas_garratt_test", "cuestas_ordonez_test",
    # Cointegration
    "kss_cointegration_test", "enders_siklos_test",
    # Linearity & diagnostics
    "terasvirta_test", "arch_test", "mcleod_li_test",
    # Utilities
    "run_all_tests", "plot_series_analysis",
    "TestResult", "BatchResult",
]
