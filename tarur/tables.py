"""TARUR — Rich Table Formatting & LaTeX Export."""
from __future__ import annotations
from tarur.core import TestResult

def format_result(r: TestResult) -> str:
    w=60;cv=r.critical_values.values
    lines=[]
    lines.append("="*w)
    lines.append(f"  {r.test_name}".center(w))
    lines.append("="*w)
    lines.append(f"  H0: {r.null_hypothesis}")
    lines.append(f"  H1: {r.alt_hypothesis}")
    lines.append("-"*w)
    lines.append(f"  Test Statistic ({r.statistic_name}){' '*(20-len(r.statistic_name))}| {r.statistic:.4f}")
    lines.append(f"  Selected Lag                  | {r.selected_lag} ({r.lag_method})")
    lines.append(f"  Case                          | {r.case}")
    lines.append("-"*w)
    cv_str = "  Critical Values: " + " | ".join(f"{k}: {v:.3f}" for k,v in cv.items() if k!="p-value")
    lines.append(cv_str)
    if r.critical_values.source:
        lines.append(f"  Source: {r.critical_values.source}")
    lines.append("-"*w)
    for level,rejected in r.decision.items():
        mark = "[REJECT]" if rejected else "[ACCEPT]"
        lines.append(f"  {level}: {mark} H0")
    lines.append("-"*w)
    lines.append(f"  >> {r.interpretation}")
    lines.append("="*w)
    return "\n".join(lines)

def format_batch(batch) -> str:
    from tarur.core import BatchResult
    lines=["","="*80,"  TARUR — Nonlinear Unit Root Test Battery".center(80),"="*80,""]
    header=f"{'Test':<42} {'Stat':>8} {'CV 5%':>8} {'Decision':>10}"
    lines.append(header);lines.append("-"*72)
    for r in batch.results:
        cv5=r.critical_values.values.get("5%",float('nan'))
        dec="REJECT" if r.decision.get("5%",False) else "ACCEPT"
        lines.append(f"  {r.test_name:<40} {r.statistic:>8.3f} {cv5:>8.3f} {dec:>10}")
    lines.append("="*80)
    return "\n".join(lines)

def result_to_latex(r: TestResult) -> str:
    cv=r.critical_values.values
    lines=[r"\\begin{table}[htbp]",r"\\centering",
        f"\\\\caption{{{r.test_name}}}",r"\\begin{tabular}{lc}",r"\\hline\\hline",
        f"Test Statistic (${r.statistic_name}$) & {r.statistic:.4f} \\\\\\\\",
        f"Selected Lag & {r.selected_lag} \\\\\\\\",r"\\hline"]
    for k,v in cv.items():
        if k!="p-value": lines.append(f"CV ({k}) & {v:.3f} \\\\\\\\")
    dec="Reject $H_0$" if r.decision.get("5%",False) else "Fail to reject $H_0$"
    lines+=[r"\\hline",f"Decision (5\\%) & {dec} \\\\\\\\",r"\\hline\\hline",
        r"\\end{tabular}",r"\\end{table}"]
    return "\n".join(lines)

def batch_to_latex(batch) -> str:
    lines=[r"\\begin{table}[htbp]",r"\\centering",
        r"\\caption{Nonlinear Unit Root Test Results}",
        r"\\begin{tabular}{lccc}",r"\\hline\\hline",
        r"Test & Statistic & CV (5\\%) & Decision \\\\",r"\\hline"]
    for r in batch.results:
        cv5=r.critical_values.values.get("5%",float('nan'))
        dec="Reject" if r.decision.get("5%",False) else "Accept"
        lines.append(f"{r.test_name} & {r.statistic:.3f} & {cv5:.3f} & {dec} \\\\\\\\")
    lines+=[r"\\hline\\hline",r"\\end{tabular}",r"\\end{table}"]
    return "\n".join(lines)
