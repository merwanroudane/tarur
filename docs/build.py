"""Combine all guide parts into docs/guide.html and generate docs/api.html."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from parts.shared import NAV, FOOTER
from parts.guide_hero import HERO, TOC
from parts.guide_estar import ESTAR_SECTION
from parts.guide_smooth import SMOOTH_SECTION
from parts.guide_tar import TAR_SECTION, GRID_SECTION
from parts.guide_rest import EXT_SECTION, COINT_SECTION, LIN_SECTION, CV_TABLE_SECTION

guide_html = (
    NAV.format(title="Theory Guide", g='class="active"', a='', r='') +
    HERO + TOC +
    ESTAR_SECTION + SMOOTH_SECTION + TAR_SECTION + GRID_SECTION +
    EXT_SECTION + COINT_SECTION + LIN_SECTION + CV_TABLE_SECTION +
    FOOTER
)

with open("docs/guide.html", "w", encoding="utf-8") as f:
    f.write(guide_html)
print(f"guide.html written ({len(guide_html)//1024} KB)")

# ── API Reference page ──────────────────────────────────────────────
API_HTML = NAV.format(title="API Reference", g='', a='class="active"', r='') + """
<section style="background:linear-gradient(135deg,#f0f7ff,#e8f4ff,#f0fdf8);padding:4rem 2rem 3rem;text-align:center;border-bottom:1px solid var(--border);">
  <div class="section-tag">API Reference</div>
  <h1 style="font-size:2.5rem;font-weight:700;letter-spacing:-.03em;margin-bottom:.5rem;">Complete API Documentation</h1>
  <p style="color:var(--text2);max-width:700px;margin:0 auto;">All functions, parameters, and return types for the TARUR library.</p>
</section>

<section class="section">
<div class="container">
<div class="section-tag">Core Objects</div>
<h2 class="section-title" id="testresult">TestResult</h2>
<p style="color:var(--text2);margin-bottom:1.5rem;">Every test returns a <code>TestResult</code> dataclass containing all outputs.</p>
<div class="api-card">
  <div class="api-header"><code>TestResult</code><span class="ret">dataclass</span></div>
  <div class="api-body">
    <table class="param-table">
      <thead><tr><th>Attribute</th><th>Type</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td>statistic</td><td>float</td><td>Computed test statistic value</td></tr>
        <tr><td>statistic_name</td><td>str</td><td>Label: "tNL", "&#964;", "F_AE", "inf_t", etc.</td></tr>
        <tr><td>critical_values</td><td>CriticalValues</td><td>Object with .cv1, .cv5, .cv10 and .source</td></tr>
        <tr><td>decision</td><td>dict</td><td>{"1%": bool, "5%": bool, "10%": bool}</td></tr>
        <tr><td>interpretation</td><td>str</td><td>Plain-English interpretation sentence</td></tr>
        <tr><td>selected_lag</td><td>int</td><td>Optimal lag order selected</td></tr>
        <tr><td>lag_method</td><td>str</td><td>"AIC", "BIC", or "t-stat"</td></tr>
        <tr><td>case</td><td>str</td><td>Deterministic specification used</td></tr>
        <tr><td>model_summary</td><td>ModelSummary</td><td>Regression coefficients, R&sup2;, AIC, BIC</td></tr>
        <tr><td>extra</td><td>dict</td><td>Test-specific extras (e.g., Fas, rho_pos, symmetry_test)</td></tr>
        <tr><td>reference</td><td>str</td><td>Full citation string</td></tr>
      </tbody>
    </table>
    <pre style="margin-top:1rem;"><span class="c"># Methods</span>
result.<span class="fn2">to_dict</span>()    <span class="c"># Flat dict for DataFrame rows</span>
result.<span class="fn2">to_latex</span>()  <span class="c"># LaTeX table snippet</span>
result.<span class="fn2">plot</span>()       <span class="c"># Matplotlib visualization</span>
<span class="fn2">print</span>(result)      <span class="c"># Formatted terminal output</span></pre>
  </div>
</div>

<h2 class="section-title" style="margin-top:2rem;" id="batchresult">BatchResult</h2>
<div class="api-card">
  <div class="api-header"><code>BatchResult</code><span class="ret">dataclass</span></div>
  <div class="api-body">
    <pre><span class="c"># Run all available tests at once</span>
batch = tarur.<span class="fn2">run_all_tests</span>(y, case=<span class="st">'demeaned'</span>, max_lags=<span class="nm">12</span>)

batch.<span class="fn2">summary</span>()    <span class="c"># pandas DataFrame with all results</span>
batch.<span class="fn2">to_latex</span>()  <span class="c"># Full LaTeX comparison table</span>
batch.<span class="fn2">plot</span>()       <span class="c"># Dashboard visualization</span>
<span class="fn2">print</span>(batch)       <span class="c"># Formatted comparison table</span></pre>
  </div>
</div>
</div>
</section>

<section class="section section-alt">
<div class="container">
<div class="section-tag">Common Parameters</div>
<h2 class="section-title" id="params">Shared Parameters</h2>
<div class="api-card">
  <div class="api-body">
    <table class="param-table">
      <thead><tr><th>Parameter</th><th>Default</th><th>Description</th></tr></thead>
      <tbody>
        <tr><td>case</td><td>'demeaned'</td><td>'raw' (no adjustment) | 'demeaned' (subtract mean) | 'detrended' (subtract linear trend)</td></tr>
        <tr><td>max_lags</td><td>8</td><td>Maximum lag order for ADF augmentation. Rule of thumb: int(12*(T/100)^0.25)</td></tr>
        <tr><td>lag_method</td><td>'aic'</td><td>'aic' | 'bic' | 't-stat' — automatic lag selection criterion</td></tr>
        <tr><td>model</td><td>'A'</td><td>'A'–'E' for smooth transition model specification (LNV, Vougas, Harvey-Mills, Cook-Vougas)</td></tr>
      </tbody>
    </table>
  </div>
</div>

<h2 class="section-title" style="margin-top:2rem;" id="functions">All Functions</h2>
<div class="api-card">
  <div class="api-header"><code>tarur.kss_test(y, case, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>KSS (2003) nonlinear ESTAR unit root test. Left-tailed t-statistic on the cubic term y³.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.kruse_test(y, case, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Kruse (2011) modified Wald &#964; — allows nonzero ESTAR location parameter. Right-tailed.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.sollis2009_test(y, case, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Sollis (2009) asymmetric ESTAR. Returns F_AE (unit root) and Fas (symmetry) in result.extra.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.hu_chen_test(y, case, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Hu &amp; Chen (2016) 3-parameter modified Wald for locally explosive ESTAR.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.lnv_test(y, model, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>LNV (1998) single logistic smooth transition. model: 'A', 'B', or 'C'.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.vougas_test(y, model, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Vougas (2006) extended smooth transition. model: 'A', 'B', 'C', 'D', or 'E'.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.harvey_mills_test(y, model, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Harvey &amp; Mills (2002) double smooth transition. Uses own CV table (larger than LNV).</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.enders_granger_test(y, case, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Enders &amp; Granger (1998) MTAR test. result.extra contains rho_pos, rho_neg, F_symmetry.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.sollis2004_test(y, model, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Sollis (2004) ST-TAR unit root test.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.cook_vougas_test(y, model, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Cook &amp; Vougas (2009) ST-MTAR. Uses Cook &amp; Vougas Table 1 CVs (not Sollis).</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.kilic_test(y, case, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Kılıç (2011) inf-t grid search. result.extra['optimal_gamma'] gives the optimal transition speed.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.park_shintani_test(y, case, max_lags, lag_method)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Park &amp; Shintani (2016) transitional autoregressive grid-search test.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.pascalau_test(y, case, max_lags)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Pascalau (2007) asymmetric NLSTAR with y&#178;, y&#179;, y&#8308; terms. Right-tailed F-test.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.cuestas_garratt_test(y, max_lags)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Cuestas &amp; Garratt (2011) cubic polynomial detrending + KSS. &#967;&#178;-type statistic.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.cuestas_ordonez_test(y, max_lags)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Cuestas &amp; Ordóñez (2014) NLS logistic detrending then KSS test on residuals.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.kss_cointegration_test(y1, y2, case, max_lags)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>KSS (2006) nonlinear cointegration. Tests whether cointegrating residuals are ESTAR-stationary.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.enders_siklos_test(y1, y2, max_lags)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Enders &amp; Siklos (2001) threshold cointegration with asymmetric error-correction.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.terasvirta_test(y, d)</code><span class="ret">→ TestResult</span></div>
  <div class="api-body"><p>Teräsvirta (1994) linearity test. result.extra['suggested_model'] → 'ESTAR' or 'LSTAR'.</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.run_all_tests(y, case, max_lags, lag_method)</code><span class="ret">→ BatchResult</span></div>
  <div class="api-body"><p>Runs all available unit root tests at once. Returns a BatchResult with .summary(), .to_latex(), .plot().</p></div>
</div>
<div class="api-card">
  <div class="api-header"><code>tarur.plot_series_analysis(y, title)</code><span class="ret">→ Figure</span></div>
  <div class="api-body"><p>Diagnostic dashboard: level, first differences, ACF, PACF, histogram, QQ-plot.</p></div>
</div>
</div>
</section>
""" + FOOTER

with open("docs/api.html", "w", encoding="utf-8") as f:
    f.write(API_HTML)
print(f"api.html written ({len(API_HTML)//1024} KB)")

print("All pages generated successfully!")
