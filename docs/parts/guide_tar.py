TAR_SECTION = """
<section class="section" id="tar">
<div class="container">
<div class="section-tag">Category 3</div>
<h2 class="section-title">Asymmetric / TAR Unit Root Tests</h2>
<p class="section-sub">Threshold autoregressive models allow the speed of adjustment to depend on whether the deviation from equilibrium is positive or negative — a key feature of many commodity prices and real exchange rates.</p>

<!-- ENDERS GRANGER -->
<div class="theory-card">
  <h3><span class="theory-num">8</span> Enders &amp; Granger (1998) — MTAR Test</h3>
  <div class="theory-ref">Enders, W., &amp; Granger, C.W.J. (1998). <em>Unit-root tests and asymmetric adjustment with an example using the term structure of interest rates.</em> JBES, 16(3), 304–311.</div>
  <p>The Momentum Threshold Autoregression (MTAR) model uses the sign of $\\Delta y_{t-1}$ as the threshold indicator:</p>
  <div class="math-block">$$I_t = \\begin{cases} 1 & \\text{if } \\Delta y_{t-1} \\geq 0 \\\\ 0 & \\text{if } \\Delta y_{t-1} &lt; 0 \\end{cases}$$</div>
  <div class="math-block">$$\\Delta \\hat{u}_t = I_t \\rho^+ \\hat{u}_{t-1} + (1-I_t) \\rho^- \\hat{u}_{t-1} + \\sum_{i=1}^{p} \\delta_i \\Delta \\hat{u}_{t-i} + \\varepsilon_t$$</div>
  <p><strong>$\\Phi$ statistic:</strong> Joint $F$-test $H_0: \\rho^+=\\rho^-=0$ (right-tailed). A second symmetry test checks $H_0: \\rho^+=\\rho^-$.</p>
  <pre>result = tarur.enders_granger_test(y, case='demeaned', max_lags=12)
print(f"rho+ = {result.extra['rho_pos']:.4f}, rho- = {result.extra['rho_neg']:.4f}")
print(f"Symmetry F = {result.extra['F_symmetry']:.3f}, p = {result.extra['F_sym_pvalue']:.4f}")</pre>
</div>

<!-- SOLLIS 2004 -->
<div class="theory-card">
  <h3><span class="theory-num">9</span> Sollis (2004) — ST-TAR Test</h3>
  <div class="theory-ref">Sollis, R. (2004). <em>Asymmetric adjustment and smooth transitions.</em> Journal of Time Series Analysis, 25(3), 409–417.</div>
  <p>Combines logistic smooth transition detrending with TAR-type asymmetric adjustment. The smooth transition removes a structural break in the deterministic component before testing for a unit root.</p>
  <pre>result = tarur.sollis2004_test(y, model='A', max_lags=12)</pre>
</div>

<!-- COOK VOUGAS -->
<div class="theory-card">
  <h3><span class="theory-num">10</span> Cook &amp; Vougas (2009) — ST-MTAR Test</h3>
  <div class="theory-ref">Cook, S., &amp; Vougas, D. (2009). <em>Unit root testing against an ST-MTAR alternative.</em> Applied Economics, 41(11), 1397–1404.</div>
  <p>Combines smooth transition detrending with MTAR asymmetric adjustment. The critical values are from <strong>Cook &amp; Vougas (2009) Table 1</strong> — they are substantially different from Sollis (2004) and must not be shared.</p>
  <table class="cv-table" style="max-width:560px;">
    <thead><tr><th>T</th><th colspan="3">Model A (F*&#945;)</th><th colspan="3">Model B (F*&#945;(&#946;))</th></tr>
    <tr><th></th><th>1%</th><th>5%</th><th>10%</th><th>1%</th><th>5%</th><th>10%</th></tr></thead>
    <tbody>
      <tr><td>50</td><td>13.27</td><td>10.06</td><td>8.62</td><td>16.79</td><td>13.20</td><td>11.55</td></tr>
      <tr><td>100</td><td>12.92</td><td>9.65</td><td>8.34</td><td>15.40</td><td>12.18</td><td>10.75</td></tr>
      <tr><td>250</td><td>12.02</td><td>9.33</td><td>8.08</td><td>14.18</td><td>11.52</td><td>10.32</td></tr>
    </tbody>
  </table>
  <pre>result = tarur.cook_vougas_test(y, model='A', max_lags=12)</pre>
</div>
</div>
</section>
"""

GRID_SECTION = """
<section class="section section-alt" id="grid">
<div class="container">
<div class="section-tag">Category 4</div>
<h2 class="section-title">Grid-Search Tests</h2>
<p class="section-sub">Rather than fixing the transition parameter, these tests search over a grid of values and take the infimum of the $t$-statistic, which gives higher power against ESTAR alternatives.</p>

<!-- KILIC -->
<div class="theory-card">
  <h3><span class="theory-num">11</span> Kılıç (2011) — inf-t Grid Search</h3>
  <div class="theory-ref">Kılıç, R. (2011). <em>Testing for a unit root in a stationary ESTAR process.</em> Econometric Reviews, 30(3), 274–302.</div>
  <p>For each $\\gamma$ in a grid $\\Gamma$, the KSS $t$-statistic is computed. The test statistic is the infimum:</p>
  <div class="math-block">$$\\inf_{\\gamma \\in \\Gamma}\\; t_{NL}(\\gamma)$$</div>
  <p>Because of the grid search, the null distribution differs from KSS — the critical values are <strong>larger in absolute value</strong>.</p>
  <table class="cv-table" style="max-width:400px;">
    <thead><tr><th>Case</th><th>1%</th><th>5%</th><th>10%</th></tr></thead>
    <tbody>
      <tr><td>Raw</td><td>-3.78</td><td>-3.22</td><td>-2.93</td></tr>
      <tr><td>Demeaned</td><td>-4.29</td><td>-3.71</td><td>-3.42</td></tr>
      <tr><td>Detrended</td><td>-4.73</td><td>-4.17</td><td>-3.88</td></tr>
    </tbody>
  </table>
  <pre>result = tarur.kilic_test(y, case='demeaned', max_lags=12)
print(f"Optimal gamma: {result.extra['optimal_gamma']:.4f}")</pre>
</div>

<!-- PARK SHINTANI -->
<div class="theory-card">
  <h3><span class="theory-num">12</span> Park &amp; Shintani (2016) — Transitional AR</h3>
  <div class="theory-ref">Park, J.Y., &amp; Shintani, M. (2016). <em>Testing for a unit root against transitional autoregressive models.</em> International Economic Review, 57(2), 635–664.</div>
  <p>A more general grid-search approach that nests the ESTAR model and allows a broader class of transition functions. Asymptotic critical values are tabulated in Park &amp; Shintani (2016) Table 1.</p>
  <pre>result = tarur.park_shintani_test(y, case='raw', max_lags=12)</pre>
</div>
</div>
</section>
"""
print("TAR + Grid sections done")
