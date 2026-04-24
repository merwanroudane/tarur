ESTAR_SECTION = """
<section class="section" id="estar">
<div class="container">
<div class="section-tag">Category 1</div>
<h2 class="section-title">ESTAR-Based Unit Root Tests</h2>
<p class="section-sub">All four tests derive from a Taylor expansion of the ESTAR model:
$y_t = y_{t-1} + \\phi y_{t-1}\\,[1 - e^{-\\theta y_{t-1}^2}] + \\varepsilon_t$,
where under $H_0: \\theta=0$ the process is a unit root and under $H_1: \\theta>0$ it is globally stationary with nonlinear mean reversion.</p>

<!-- KSS -->
<div class="theory-card">
  <h3><span class="theory-num">1</span> KSS (2003) — Nonlinear ESTAR Unit Root Test</h3>
  <div class="theory-ref">Kapetanios, G., Shin, Y., &amp; Snell, A. (2003). <em>Testing for a unit root in the nonlinear STAR framework.</em> Journal of Econometrics, 112(2), 359–379.</div>
  <p>Taking a first-order Taylor expansion of the transition function around $\\theta=0$ gives the auxiliary regression:</p>
  <div class="math-block">$$\\Delta y_t = \\beta_1 y_{t-1}^3 + \\sum_{i=1}^{p} \\rho_i \\Delta y_{t-i} + u_t$$</div>
  <p><strong>Test statistic:</strong> $t_{NL} = \\hat{\\beta}_1 / \\text{se}(\\hat{\\beta}_1)$ — a standard $t$-ratio on the cubic term. <strong>Reject $H_0$ when $t_{NL} &lt; \\text{CV}$</strong> (left-tailed).</p>
  <p><strong>Case specification:</strong> <em>raw</em> — no adjustment; <em>demeaned</em> — subtract OLS mean; <em>detrended</em> — subtract OLS linear trend. The demeaned case is most common for exchange rates and commodity prices.</p>
  <table class="cv-table" style="max-width:500px;">
    <thead><tr><th>Case</th><th>1%</th><th>5%</th><th>10%</th></tr></thead>
    <tbody>
      <tr><td>Raw</td><td>-3.48</td><td>-2.93</td><td>-2.66</td></tr>
      <tr><td>Demeaned</td><td>-3.93</td><td>-3.40</td><td>-3.13</td></tr>
      <tr><td>Detrended</td><td>-3.40</td><td>-2.93</td><td>-2.66</td></tr>
    </tbody>
  </table>
  <pre style="margin-top:.75rem;">result = tarur.kss_test(y, case='demeaned', max_lags=12, lag_method='aic')
print(result)  # statistic, CVs, decision, interpretation</pre>
</div>

<!-- KRUSE -->
<div class="theory-card">
  <h3><span class="theory-num">2</span> Kruse (2011) — Modified Wald τ Test</h3>
  <div class="theory-ref">Kruse, R. (2011). <em>A new unit root test against ESTAR based on a class of modified statistics.</em> Statistical Papers, 52(1), 71–85.</div>
  <div class="fix-badge">⚠ Bug Fix: R NonlinearTSA uses standard Chi-squared — TARUR implements the correct modified Wald τ</div>
  <p>KSS restricts the ESTAR location parameter $c=0$. Kruse relaxes this, giving auxiliary regression:</p>
  <div class="math-block">$$\\Delta y_t = \\beta_1 y_{t-1}^3 + \\beta_2 y_{t-1}^2 + \\sum_{i=1}^{p} \\rho_i \\Delta y_{t-i} + u_t$$</div>
  <p>The test statistic is <strong>not</strong> a standard Wald. It is the modified Wald:</p>
  <div class="math-block">$$\\tau = t^2_{\\hat{\\beta}_{2\\perp}=0} + \\mathbf{1}(\\hat{\\beta}_1 &lt; 0)\\cdot t^2_{\\hat{\\beta}_1=0}$$</div>
  <p>The indicator $\\mathbf{1}(\\hat{\\beta}_1 &lt; 0)$ implements the one-sided alternative. <strong>Reject $H_0$ when $\\tau &gt; \\text{CV}$</strong> (right-tailed).</p>
  <table class="cv-table" style="max-width:500px;">
    <thead><tr><th>Case</th><th>1%</th><th>5%</th><th>10%</th></tr></thead>
    <tbody>
      <tr><td>Raw</td><td>13.15</td><td>9.53</td><td>7.85</td></tr>
      <tr><td>Demeaned</td><td>13.75</td><td>10.17</td><td>8.60</td></tr>
      <tr><td>Detrended</td><td>17.10</td><td>12.82</td><td>11.10</td></tr>
    </tbody>
  </table>
  <pre>result = tarur.kruse_test(y, case='demeaned', max_lags=12)</pre>
</div>

<!-- SOLLIS 2009 -->
<div class="theory-card">
  <h3><span class="theory-num">3</span> Sollis (2009) — Asymmetric ESTAR Test</h3>
  <div class="theory-ref">Sollis, R. (2009). <em>A simple unit root test against asymmetric STAR nonlinearity.</em> Economic Modelling, 26(1), 118–125.</div>
  <div class="fix-badge">⚠ Bug Fix: R code uses wrong auxiliary regression — TARUR implements the correct AESTAR formulation</div>
  <p>Extends ESTAR to allow <strong>asymmetric adjustment</strong>: upward and downward departures from equilibrium revert at different speeds. Auxiliary regression:</p>
  <div class="math-block">$$\\Delta y_t = \\phi_1 y_{t-1}^3 + \\phi_2 y_{t-1}^4 + \\sum_{i=1}^{p} \\kappa_i \\Delta y_{t-i} + \\eta_t$$</div>
  <p>Two statistics are computed:</p>
  <ul style="margin:.5rem 0 .5rem 1.5rem;color:var(--text2);font-size:.92rem;line-height:2;">
    <li><strong>$F_{AE}$</strong>: Joint $F$-test of $H_0: \\phi_1=\\phi_2=0$ — the unit root test (reject when $F_{AE} &gt; \\text{CV}$)</li>
    <li><strong>$F_{as}$</strong>: $F$-test of $H_0: \\phi_2=0$ — symmetry test (reject $\\Rightarrow$ asymmetric mean reversion)</li>
  </ul>
  <pre>result = tarur.sollis2009_test(y, case='demeaned', max_lags=12)
print(f"Symmetry Fas: {result.extra['Fas']:.3f}  p={result.extra['Fas_pvalue']:.4f}")
print(result.extra['symmetry_test'])</pre>
</div>

<!-- HU CHEN -->
<div class="theory-card">
  <h3><span class="theory-num">4</span> Hu &amp; Chen (2016) — 3-Parameter Modified Wald</h3>
  <div class="theory-ref">Hu, J., &amp; Chen, Z. (2016). <em>A unit root test against globally stationary ESTAR models when local condition is non-stationary.</em> Economics Letters, 146, 89–94.</div>
  <div class="fix-badge">⚠ Bug Fix: R code applies same error as Kruse — TARUR uses correct 3-parameter orthogonalized Wald</div>
  <p>Allows a locally non-stationary (explosive) but globally stationary ESTAR process. Auxiliary regression adds the linear term:</p>
  <div class="math-block">$$\\Delta y_t = \\beta_1 y_{t-1} + \\beta_2 y_{t-1}^2 + \\beta_3 y_{t-1}^3 + \\sum_{i=1}^{p} \\rho_i \\Delta y_{t-i} + u_t$$</div>
  <p>The 3-parameter modified Wald statistic (right-tailed) has higher power than KSS when the data-generating process is locally explosive.</p>
  <pre>result = tarur.hu_chen_test(y, case='demeaned', max_lags=12)</pre>
</div>

</div>
</section>
"""
print("ESTAR section done")
