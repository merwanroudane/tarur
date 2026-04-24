"""
TARUR — Critical Values Database
=================================
All critical values extracted from the original academic papers.
Finite‑sample values are interpolated when the exact sample size is unavailable.
"""

from __future__ import annotations

import numpy as np
from tarur.core import CriticalValues

# ═══════════════════════════════════════════════════════════════════════════
# KSS (2003) — Kapetanios, Shin & Snell
# Source: KSS (2003), Table 1 — asymptotic critical values
# Test statistic: t‑type (reject when tNL < CV)
# ═══════════════════════════════════════════════════════════════════════════

KSS_CV = {
    "raw": {"1%": -3.48, "5%": -2.93, "10%": -2.66},
    "demeaned": {"1%": -3.93, "5%": -3.40, "10%": -3.13},
    "detrended": {"1%": -3.40, "5%": -2.93, "10%": -2.66},
}


def get_kss_cv(case: str) -> CriticalValues:
    key = _norm_case(case)
    return CriticalValues(
        values=KSS_CV[key],
        source="Kapetanios, Shin & Snell (2003), Table 1 (asymptotic)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Kruse (2011) — Modified Wald τ
# Source: Kruse (2011), Table 1 — asymptotic (T=1000, 20 000 replications)
# Test statistic: τ (reject when τ > CV)
# ═══════════════════════════════════════════════════════════════════════════

KRUSE_CV = {
    "raw":       {"1%": 13.15, "5%": 9.53, "10%": 7.85},
    "demeaned":  {"1%": 13.75, "5%": 10.17, "10%": 8.60},
    "detrended": {"1%": 17.10, "5%": 12.82, "10%": 11.10},
}


def get_kruse_cv(case: str) -> CriticalValues:
    key = _norm_case(case)
    return CriticalValues(
        values=KRUSE_CV[key],
        source="Kruse (2011), Table 1 (asymptotic, T=1000)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sollis (2009) — Asymmetric ESTAR F‑test
# Source: Sollis (2009), Table 1 — finite‑sample + asymptotic
# Test statistic: F_AE (reject when F > CV)
# ═══════════════════════════════════════════════════════════════════════════

SOLLIS2009_CV = {
    "raw": {
        50:   {"10%": 3.577, "5%": 4.464, "1%": 6.781},
        100:  {"10%": 3.527, "5%": 4.365, "1%": 6.272},
        200:  {"10%": 3.496, "5%": 4.297, "1%": 6.066},
        None: {"10%": 1.837, "5%": 2.505, "1%": 4.241},  # asymptotic
    },
    "demeaned": {
        50:   {"10%": 4.009, "5%": 4.886, "1%": 6.891},
        100:  {"10%": 4.157, "5%": 4.954, "1%": 6.883},
        200:  {"10%": 4.173, "5%": 4.971, "1%": 6.806},
        None: {"10%": 3.725, "5%": 4.557, "1%": 6.236},
    },
    "detrended": {
        50:   {"10%": 5.415, "5%": 6.546, "1%": 8.799},
        100:  {"10%": 5.460, "5%": 6.463, "1%": 8.531},
        200:  {"10%": 5.590, "5%": 6.597, "1%": 8.954},
        None: {"10%": 5.372, "5%": 6.292, "1%": 8.344},
    },
}


def get_sollis2009_cv(case: str, T: int) -> CriticalValues:
    key = _norm_case(case)
    table = SOLLIS2009_CV[key]
    cv, src_size = _interpolate_cv(table, T)
    return CriticalValues(
        values=cv,
        sample_size=src_size,
        source=f"Sollis (2009), Table 1 (T={src_size or 'asymptotic'})",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Hu & Chen (2016) — Modified Wald τ (3‑parameter)
# Source: Hu & Chen (2016), Table 1 — asymptotic (T=1000, 50 000 reps)
# Test statistic: τ (reject when τ > CV)
# ═══════════════════════════════════════════════════════════════════════════

HU_CHEN_CV = {
    "raw":       {"1%": 15.12, "5%": 11.22, "10%": 9.49},
    "demeaned":  {"1%": 15.62, "5%": 11.86, "10%": 10.12},
    "detrended": {"1%": 18.62, "5%": 14.39, "10%": 12.42},
}


def get_hu_chen_cv(case: str) -> CriticalValues:
    key = _norm_case(case)
    return CriticalValues(
        values=HU_CHEN_CV[key],
        source="Hu & Chen (2016), Table 1 (asymptotic, T=1000)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Cuestas & Garratt (2011) — Chi‑squared test
# Source: Paper + R code hardcoded values
# Test statistic: χ² (reject when χ² > CV)
# ═══════════════════════════════════════════════════════════════════════════

CUESTAS_GARRATT_CV = {"1%": 22.44, "5%": 17.27, "10%": 14.97}


def get_cuestas_garratt_cv() -> CriticalValues:
    return CriticalValues(
        values=CUESTAS_GARRATT_CV,
        source="Cuestas & Garratt (2011) — simulated critical values",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Vougas (2006) — ADF on NLS residuals
# Source: Vougas (2006), Table 1 — finite‑sample CVs
# 5 models (A–E) × 5 sample sizes × 3 significance levels
# Test statistic: t‑type (reject when t < CV)
# ═══════════════════════════════════════════════════════════════════════════

VOUGAS_CV = {
    "A": {
        25:  {"1%": -4.67, "5%": -3.82, "10%": -3.41},
        50:  {"1%": -4.38, "5%": -3.69, "10%": -3.37},
        100: {"1%": -4.24, "5%": -3.63, "10%": -3.34},
        250: {"1%": -4.17, "5%": -3.60, "10%": -3.32},
        500: {"1%": -4.15, "5%": -3.59, "10%": -3.32},
    },
    "B": {
        25:  {"1%": -4.99, "5%": -4.19, "10%": -3.77},
        50:  {"1%": -4.71, "5%": -4.03, "10%": -3.69},
        100: {"1%": -4.54, "5%": -3.96, "10%": -3.66},
        250: {"1%": -4.48, "5%": -3.93, "10%": -3.64},
        500: {"1%": -4.47, "5%": -3.93, "10%": -3.64},
    },
    "C": {
        25:  {"1%": -5.13, "5%": -4.33, "10%": -3.92},
        50:  {"1%": -4.83, "5%": -4.16, "10%": -3.83},
        100: {"1%": -4.68, "5%": -4.08, "10%": -3.78},
        250: {"1%": -4.60, "5%": -4.04, "10%": -3.76},
        500: {"1%": -4.58, "5%": -4.04, "10%": -3.76},
    },
    "D": {
        25:  {"1%": -4.44, "5%": -3.57, "10%": -3.14},
        50:  {"1%": -4.10, "5%": -3.43, "10%": -3.09},
        100: {"1%": -3.97, "5%": -3.38, "10%": -3.08},
        250: {"1%": -3.90, "5%": -3.35, "10%": -3.06},
        500: {"1%": -3.88, "5%": -3.34, "10%": -3.06},
    },
    "E": {
        25:  {"1%": -4.90, "5%": -4.06, "10%": -3.66},
        50:  {"1%": -4.56, "5%": -3.91, "10%": -3.59},
        100: {"1%": -4.42, "5%": -3.86, "10%": -3.56},
        250: {"1%": -4.38, "5%": -3.83, "10%": -3.55},
        500: {"1%": -4.36, "5%": -3.82, "10%": -3.54},
    },
}


def get_vougas_cv(model: str, T: int) -> CriticalValues:
    model = model.upper()
    if model not in VOUGAS_CV:
        raise ValueError(f"Vougas model must be A–E, got '{model}'")
    table = VOUGAS_CV[model]
    cv, src_size = _interpolate_cv(table, T)
    return CriticalValues(
        values=cv,
        sample_size=src_size,
        source=f"Vougas (2006), Table 1 (Model {model}, T={src_size})",
    )


# ═══════════════════════════════════════════════════════════════════════════
# LNV (1998) — Leybourne, Newbold & Vougas
# Source: LNV (1998), Table I — DISTINCT from Vougas (2006)
# sα = Model A, sα(β) = Model B, sαβ = Model C
# Test statistic: t-type (reject when t < CV)
# ═══════════════════════════════════════════════════════════════════════════

LNV_CV = {
    "A": {  # sα
        25:  {"1%": -5.669, "5%": -4.750, "10%": -4.280},
        50:  {"1%": -5.095, "5%": -4.363, "10%": -4.009},
        100: {"1%": -4.882, "5%": -4.232, "10%": -3.909},
        200: {"1%": -4.761, "5%": -4.161, "10%": -3.851},
        500: {"1%": -4.685, "5%": -4.103, "10%": -3.797},
    },
    "B": {  # sα(β)
        25:  {"1%": -6.561, "5%": -5.583, "10%": -5.097},
        50:  {"1%": -5.770, "5%": -5.053, "10%": -4.636},
        100: {"1%": -5.479, "5%": -4.771, "10%": -4.427},
        200: {"1%": -5.201, "5%": -4.629, "10%": -4.337},
        500: {"1%": -5.141, "5%": -4.565, "10%": -4.277},
    },
    "C": {  # sαβ
        25:  {"1%": -7.152, "5%": -6.054, "10%": -5.555},
        50:  {"1%": -6.135, "5%": -5.395, "10%": -4.990},
        100: {"1%": -5.650, "5%": -5.011, "10%": -4.697},
        200: {"1%": -5.435, "5%": -4.867, "10%": -4.572},
        500: {"1%": -5.420, "5%": -4.825, "10%": -4.552},
    },
}


def get_lnv_cv(model: str, T: int) -> CriticalValues:
    model = model.upper()
    if model not in LNV_CV:
        raise ValueError(f"LNV model must be A–C, got '{model}'")
    table = LNV_CV[model]
    cv, src_size = _interpolate_cv(table, T)
    return CriticalValues(
        values=cv,
        sample_size=src_size,
        source=f"Leybourne, Newbold & Vougas (1998), Table I (Model {model}, T={src_size})",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Enders & Granger (1998) — TAR / MTAR unit root
# Source: Enders & Granger (1998), Table 1
# Test statistic: Φ (F‑type, reject when Φ > CV)
# ═══════════════════════════════════════════════════════════════════════════

ENDERS_GRANGER_CV = {
    "none": {"1%": 7.85, "5%": 5.67, "10%": 4.71},    # no deterministics
    "const": {"1%": 8.78, "5%": 6.41, "10%": 5.39},    # with constant
    "both": {"1%": 9.69, "5%": 7.16, "10%": 6.07},     # constant + trend
}


def get_enders_granger_cv(include: str) -> CriticalValues:
    include = include.lower()
    if include not in ENDERS_GRANGER_CV:
        raise ValueError(f"include must be 'none', 'const', or 'both', got '{include}'")
    return CriticalValues(
        values=ENDERS_GRANGER_CV[include],
        source="Enders & Granger (1998), Table 1",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Enders & Siklos (2001) — TAR / MTAR cointegration
# Source: Enders & Siklos (2001), Table 1
# Same Φ critical values as Enders & Granger (for residual‑based tests)
# ═══════════════════════════════════════════════════════════════════════════

ENDERS_SIKLOS_CV = ENDERS_GRANGER_CV


def get_enders_siklos_cv(include: str = "none") -> CriticalValues:
    include = include.lower()
    cv = ENDERS_SIKLOS_CV.get(include, ENDERS_SIKLOS_CV["none"])
    return CriticalValues(
        values=cv,
        source="Enders & Siklos (2001), Table 1",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sollis (2004) — ST‑TAR unit root
# Source: Sollis (2004), Table II — simulated CVs (T=100, 1000 reps)
# Test statistic: F_p1=p2=0 (reject when F > CV)
# ═══════════════════════════════════════════════════════════════════════════

SOLLIS2004_CV = {
    "A": {"1%": 8.14, "5%": 5.89, "10%": 4.87},    # Model with intercept
    "B": {"1%": 9.02, "5%": 6.56, "10%": 5.44},    # Model with trend
    "C": {"1%": 9.87, "5%": 7.22, "10%": 6.02},    # Model with trend*function
}


def get_sollis2004_cv(model: str) -> CriticalValues:
    model = model.upper()
    if model not in ("A", "B", "C"):
        model_map = {"1": "A", "2": "B", "3": "C"}
        model = model_map.get(str(model), "A")
    return CriticalValues(
        values=SOLLIS2004_CV.get(model, SOLLIS2004_CV["A"]),
        source=f"Sollis (2004), Table II (Model {model}, T=100)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Pascalau (2007) — Asymmetric NLSTAR
# Source: Pascalau (2007, working paper), simulated CVs
# Test statistic: F (reject when F > CV)
# ═══════════════════════════════════════════════════════════════════════════

PASCALAU_CV = {
    "raw":       {"1%": 8.50, "5%": 6.18, "10%": 5.12},
    "demeaned":  {"1%": 9.35, "5%": 6.82, "10%": 5.68},
    "detrended": {"1%": 10.21, "5%": 7.48, "10%": 6.25},
}


def get_pascalau_cv(case: str) -> CriticalValues:
    key = _norm_case(case)
    return CriticalValues(
        values=PASCALAU_CV[key],
        source="Pascalau (2007) — simulated critical values",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Harvey & Mills (2002) — Double smooth transition
# Source: Harvey & Mills (2002), Table 1 — DISTINCT from LNV/Vougas
# σ²α = Model A, σ²α(β) = Model B, σ²αβ = Model C
# Test statistic: t-type (reject when t < CV)
# NOTE: These CVs are LARGER in absolute value than LNV because the
# double-transition alternative is more flexible.
# ═══════════════════════════════════════════════════════════════════════════

HARVEY_MILLS_CV = {
    "A": {  # σ²α (double transition, intercept only)
        50:  {"1%": -6.49, "5%": -5.73, "10%": -5.33},
        100: {"1%": -6.05, "5%": -5.37, "10%": -5.04},
        150: {"1%": -5.84, "5%": -5.27, "10%": -4.94},
        200: {"1%": -5.80, "5%": -5.20, "10%": -4.90},
        1000:{"1%": -5.64, "5%": -5.07, "10%": -4.79},
    },
    "B": {  # σ²α(β) (double transition, intercept + fixed trend)
        50:  {"1%": -7.37, "5%": -6.48, "10%": -6.07},
        100: {"1%": -6.64, "5%": -5.97, "10%": -5.64},
        150: {"1%": -6.39, "5%": -5.80, "10%": -5.50},
        200: {"1%": -6.36, "5%": -5.74, "10%": -5.44},
        1000:{"1%": -6.05, "5%": -5.53, "10%": -5.25},
    },
    "C": {  # σ²αβ (double transition, intercept + trend transition)
        50:  {"1%": -8.14, "5%": -7.16, "10%": -6.74},
        100: {"1%": -7.25, "5%": -6.55, "10%": -6.20},
        150: {"1%": -6.90, "5%": -6.32, "10%": -6.02},
        200: {"1%": -6.79, "5%": -6.21, "10%": -5.93},
        1000:{"1%": -6.59, "5%": -6.01, "10%": -5.74},
    },
}


def get_harvey_mills_cv(model: str, T: int) -> CriticalValues:
    model = model.upper()
    if model not in HARVEY_MILLS_CV:
        model_map = {"1": "A", "2": "B", "3": "C"}
        model = model_map.get(str(model), "A")
    table = HARVEY_MILLS_CV.get(model, HARVEY_MILLS_CV["A"])
    cv, src_size = _interpolate_cv(table, T)
    return CriticalValues(
        values=cv,
        sample_size=src_size,
        source=f"Harvey & Mills (2002), Table 1 (Model {model}, T={src_size})",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Cook & Vougas (2009) — Smooth transition MTAR
# Source: Cook & Vougas (2009), Table 1 — DISTINCT from Sollis (2004)
# F-statistic CVs for ST-MTAR (not TAR)
# Test statistic: F_MTAR (reject when F > CV)
# ═══════════════════════════════════════════════════════════════════════════

COOK_VOUGAS_CV = {
    "A": {  # F*α (Model A — intercept transition)
        50:  {"1%": 13.269, "5%": 10.063, "10%": 8.620},
        100: {"1%": 12.917, "5%": 9.653,  "10%": 8.335},
        250: {"1%": 12.018, "5%": 9.329,  "10%": 8.077},
        500: {"1%": 11.611, "5%": 9.022,  "10%": 7.935},
    },
    "B": {  # F*α(β) (Model B — intercept + fixed trend)
        50:  {"1%": 16.792, "5%": 13.197, "10%": 11.553},
        100: {"1%": 15.400, "5%": 12.177, "10%": 10.754},
        250: {"1%": 14.180, "5%": 11.524, "10%": 10.315},
        500: {"1%": 14.176, "5%": 11.541, "10%": 10.138},
    },
    "C": {  # F*αβ (Model C — intercept + trend transition)
        50:  {"1%": 19.008, "5%": 14.937, "10%": 13.037},
        100: {"1%": 16.994, "5%": 13.663, "10%": 12.091},
        250: {"1%": 16.154, "5%": 13.057, "10%": 11.670},
        500: {"1%": 15.507, "5%": 12.721, "10%": 11.400},
    },
    "D": {  # F*β (Model D — trend transition only)
        50:  {"1%": 12.924, "5%": 9.434,  "10%": 7.948},
        100: {"1%": 12.223, "5%": 9.029,  "10%": 7.713},
        250: {"1%": 11.323, "5%": 8.699,  "10%": 7.416},
        500: {"1%": 11.111, "5%": 8.450,  "10%": 7.282},
    },
}


def get_cook_vougas_cv(model: str, T: int = 100) -> CriticalValues:
    model = model.upper()
    if model not in COOK_VOUGAS_CV:
        model_map = {"1": "A", "2": "B", "3": "C", "4": "D"}
        model = model_map.get(str(model), "A")
    table = COOK_VOUGAS_CV.get(model, COOK_VOUGAS_CV["A"])
    cv, src_size = _interpolate_cv(table, T)
    return CriticalValues(
        values=cv,
        sample_size=src_size,
        source=f"Cook & Vougas (2009), Table 1 (Model {model}, T={src_size})",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Park & Shintani (2016) — inf‑t test
# Source: Park & Shintani (2016), Table 1
# Test statistic: inf t (reject when t < CV)
# ═══════════════════════════════════════════════════════════════════════════

PARK_SHINTANI_CV = {
    "raw":       {"1%": -3.78, "5%": -3.19, "10%": -2.89},
    "demeaned":  {"1%": -4.23, "5%": -3.64, "10%": -3.34},
    "detrended": {"1%": -4.66, "5%": -4.07, "10%": -3.77},
}


def get_park_shintani_cv(case: str = "raw") -> CriticalValues:
    key = _norm_case(case)
    return CriticalValues(
        values=PARK_SHINTANI_CV[key],
        source="Park & Shintani (2016), Table 1 (asymptotic)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Kılıç (2011) — inf‑t with ESTAR
# Source: Kılıç (2011), Table 1 — Distinct from KSS CVs
# The inf-t test uses a grid search over gamma, so its
# null distribution differs from the standard KSS t-statistic.
# Test statistic: inf t (reject when t < CV)
# ═══════════════════════════════════════════════════════════════════════════

KILIC_CV = {
    "raw":       {"1%": -3.78, "5%": -3.22, "10%": -2.93},
    "demeaned":  {"1%": -4.29, "5%": -3.71, "10%": -3.42},
    "detrended": {"1%": -4.73, "5%": -4.17, "10%": -3.88},
}


def get_kilic_cv(case: str) -> CriticalValues:
    key = _norm_case(case)
    return CriticalValues(
        values=KILIC_CV[key],
        source="Kilic (2011), Table 1 (asymptotic, grid-search over gamma)",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Cuestas & Ordonez (2014) — uses KSS CVs on NLS residuals
# ═══════════════════════════════════════════════════════════════════════════

def get_cuestas_ordonez_cv() -> CriticalValues:
    return CriticalValues(
        values=KSS_CV["raw"],
        source="Cuestas & Ordonez (2014) — KSS (2003) CVs applied to NLS residuals",
    )


# ═══════════════════════════════════════════════════════════════════════════
# Internal helpers
# ═══════════════════════════════════════════════════════════════════════════

def _norm_case(case: str) -> str:
    """Normalize case string to 'raw', 'demeaned', or 'detrended'."""
    case = str(case).lower().strip()
    mapping = {
        "1": "raw", "raw": "raw", "none": "raw",
        "2": "demeaned", "demeaned": "demeaned", "demean": "demeaned",
        "constant": "demeaned", "const": "demeaned",
        "3": "detrended", "detrended": "detrended", "detrend": "detrended",
        "trend": "detrended",
    }
    return mapping.get(case, "raw")


def _interpolate_cv(table: dict, T: int) -> tuple:
    """
    Pick the best matching sample‑size entry from a CV table.

    Returns (cv_dict, source_size).
    """
    finite_sizes = sorted(k for k in table if k is not None)

    if not finite_sizes:
        return table[None], None

    # Exact match
    if T in table:
        return table[T], T

    # Use closest finite‑sample entry
    closest = min(finite_sizes, key=lambda s: abs(s - T))

    # If T is very large (>= largest * 1.5), use asymptotic if available
    if T >= finite_sizes[-1] * 1.5 and None in table:
        return table[None], None

    return table[closest], closest
