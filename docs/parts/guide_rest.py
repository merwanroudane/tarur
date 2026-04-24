EXT_SECTION = """
<section class="section" id="extended">
<div class="container">
<div class="section-tag">Category 5</div>
<h2 class="section-title">Extended Tests</h2>

<div class="theory-card">
  <h3><span class="theory-num">13</span> Pascalau (2007) — Asymmetric NLSTAR</h3>
  <div class="theory-ref">Pascalau, R. (2007). <em>Unit root tests with smooth breaks: an application to the Nelson-Plosser data set.</em> Working Paper.</div>
  <p>Extends the ESTAR auxiliary regression with additional polynomial terms ($y^4$), allowing for richer asymmetric dynamics:</p>
  <div class="math-block">$$\\Delta y_t = \\beta_1 y_{t-1}^2 + \\beta_2 y_{t-1}^3 + \\beta_3 y_{t-1}^4 + \\sum \\rho_i \\Delta y_{t-i} + u_t$$</div>
  <p>Joint $F$-test $H_0: \\beta_1=\\beta_2=\\beta_3=0$ (right-tailed). Simulated CVs: 1%: 9.35, 5%: 6.82, 10%: 5.68.</p>
  <pre>result = tarur.pascalau_test(y, case='demeaned', max_lags=12)</pre>
</div>

<div class="theory-card">
  <h3><span class="theory-num">14</span> Cuestas &amp; Garratt (2011) — Cubic Polynomial Detrending</h3>
  <div class="theory-ref">Cuestas, J.C., &amp; Garratt, D. (2011). <em>Is real GDP per capita a stationary process? Smooth transitions, nonlinear trends and unit root testing.</em> Applied Economics, 43(11), 1431–1437.</div>
  <p>Fits a cubic polynomial trend $\\mu(t) = c_0 + c_1 t + c_2 t^2 + c_3 t^3$, then applies a KSS-type test to the detrended series. The $\\chi^2$ statistic tests $H_0: \\beta_1=\\beta_2=0$ in the detrended auxiliary regression.</p>
  <pre>result = tarur.cuestas_garratt_test(y, max_lags=12)</pre>
</div>

<div class="theory-card">
  <h3><span class="theory-num">15</span> Cuestas &amp; Ordóñez (2014) — NLS Logistic Detrending + KSS</h3>
  <div class="theory-ref">Cuestas, J.C., &amp; Ordóñez, J. (2014). <em>Smooth transitions, asymmetric adjustment and unit roots.</em> Applied Economics Letters, 21(14), 969–972.</div>
  <p>First removes a smooth transition trend via NLS (logistic form), then applies the standard KSS test to the residuals. The paper shows that KSS critical values remain valid for the NLS-detrended residuals.</p>
  <pre>result = tarur.cuestas_ordonez_test(y, max_lags=12)</pre>
</div>
</div>
</section>
"""

COINT_SECTION = """
<section class="section section-alt" id="coint">
<div class="container">
<div class="section-tag">Category 6</div>
<h2 class="section-title">Nonlinear Cointegration Tests</h2>

<div class="theory-card">
  <h3><span class="theory-num">16</span> KSS Nonlinear Cointegration (2006)</h3>
  <div class="theory-ref">Kapetanios, G., Shin, Y., &amp; Snell, A. (2006). <em>Testing for cointegration in nonlinear smooth transition error correction models.</em> Econometric Theory, 22(2), 279–303.</div>
  <p>Estimate the static cointegrating regression $y_{1t} = \\alpha + \\beta y_{2t} + u_t$, then apply the KSS test to $\\hat{u}_t$. Under nonlinear cointegration, the equilibrium error is a globally stationary ESTAR process rather than a linear AR(1).</p>
  <pre>result = tarur.kss_cointegration_test(y1, y2, case='demeaned', max_lags=12)</pre>
</div>

<div class="theory-card">
  <h3><span class="theory-num">17</span> Enders &amp; Siklos (2001) — TAR Cointegration</h3>
  <div class="theory-ref">Enders, W., &amp; Siklos, P.L. (2001). <em>Cointegration and threshold adjustment.</em> JBES, 19(2), 166–176.</div>
  <p>Tests cointegration where the equilibrium error follows a TAR or MTAR process — adjustment toward equilibrium is faster in one direction than the other. The $\\Phi^*$ statistic tests $\\rho^+=\\rho^-=0$.</p>
  <pre>result = tarur.enders_siklos_test(y1, y2, max_lags=12)</pre>
</div>
</div>
</section>
"""

LIN_SECTION = """
<section class="section" id="linearity">
<div class="container">
<div class="section-tag">Category 7</div>
<h2 class="section-title">Linearity &amp; Diagnostic Tests</h2>

<div class="theory-card">
  <h3><span class="theory-num">18</span> Teräsvirta (1994) — Linearity Test</h3>
  <div class="theory-ref">Teräsvirta, T. (1994). <em>Specification, estimation, and evaluation of smooth transition autoregressive models.</em> JASA, 89(425), 208–218.</div>
  <p>Tests $H_0$: linearity against a STAR alternative via a third-order Taylor expansion. The sequential procedure also distinguishes between LSTAR and ESTAR:</p>
  <div class="math-block">$$H_{01}: \\delta_3=0,\\quad H_{02}: \\delta_2=0|\\delta_3=0,\\quad H_{03}: \\delta_1=0|\\delta_2=\\delta_3=0$$</div>
  <ul style="margin:.5rem 0 .5rem 1.5rem;color:var(--text2);font-size:.92rem;line-height:2;">
    <li>If $H_{02}$ is rejected most strongly → <strong>ESTAR</strong></li>
    <li>If $H_{01}$ or $H_{03}$ rejected most strongly → <strong>LSTAR</strong></li>
  </ul>
  <pre>result = tarur.terasvirta_test(np.diff(y), d=1)
print(f"p-value: {result.extra['p_linearity']:.4f}")
print(f"Suggested: {result.extra['suggested_model']}")
print(f"H01 F={result.extra['H01']:.3f}, H02 F={result.extra['H02']:.3f}, H03 F={result.extra['H03']:.3f}")</pre>
</div>
</div>
</section>
"""

CV_TABLE_SECTION = """
<section class="section section-alt" id="cvtable">
<div class="container">
<div class="section-tag">Reference</div>
<h2 class="section-title">Critical Value Master Table</h2>
<p class="section-sub">Every test in TARUR uses its own critical values from its original paper. The table below maps each test to its source, table number, sample sizes, and tail direction.</p>
<div class="test-table-wrap">
<table class="test-table">
<thead><tr><th>Test</th><th>Paper Source</th><th>Table</th><th>T (sample sizes)</th><th>Tail</th><th>Type</th></tr></thead>
<tbody>
<tr><td>KSS (2003)</td><td>KSS (2003)</td><td>Table 1</td><td>Asymptotic</td><td class="tag tag-left">Left</td><td>t-type</td></tr>
<tr><td>Kruse (2011)</td><td>Kruse (2011)</td><td>Table 1</td><td>T=1000</td><td class="tag tag-right">Right</td><td>Wald &#964;</td></tr>
<tr><td>Sollis (2009)</td><td>Sollis (2009)</td><td>Table 1</td><td>50,100,200 (interp.)</td><td class="tag tag-right">Right</td><td>F-type</td></tr>
<tr><td>Hu &amp; Chen (2016)</td><td>Hu &amp; Chen (2016)</td><td>Table 1</td><td>T=1000</td><td class="tag tag-right">Right</td><td>Wald &#964;</td></tr>
<tr><td>LNV (1998)</td><td>LNV (1998)</td><td>Table I</td><td>25–500 (interp.)</td><td class="tag tag-left">Left</td><td>t-type</td></tr>
<tr><td>Vougas (2006)</td><td>Vougas (2006)</td><td>Table 1</td><td>25–500 (interp.)</td><td class="tag tag-left">Left</td><td>t-type</td></tr>
<tr><td>Harvey &amp; Mills (2002)</td><td>H&amp;M (2002)</td><td>Table 1</td><td>50–1000 (interp.)</td><td class="tag tag-left">Left</td><td>t-type</td></tr>
<tr><td>Enders &amp; Granger (1998)</td><td>E&amp;G (1998)</td><td>Table 1</td><td>Asymptotic</td><td class="tag tag-right">Right</td><td>F-type</td></tr>
<tr><td>Cook &amp; Vougas (2009)</td><td>C&amp;V (2009)</td><td>Table 1</td><td>50–500 (interp.)</td><td class="tag tag-right">Right</td><td>F-type</td></tr>
<tr><td>Sollis (2004)</td><td>Sollis (2004)</td><td>Table II</td><td>T=100</td><td class="tag tag-right">Right</td><td>F-type</td></tr>
<tr><td>Kili&#231; (2011)</td><td>Kili&#231; (2011)</td><td>Table 1</td><td>Asymptotic</td><td class="tag tag-left">Left</td><td>t-type</td></tr>
<tr><td>Park &amp; Shintani (2016)</td><td>P&amp;S (2016)</td><td>Table 1</td><td>Asymptotic</td><td class="tag tag-left">Left</td><td>t-type</td></tr>
<tr><td>Pascalau (2007)</td><td>Pascalau (2007)</td><td>Simulated</td><td>Simulated</td><td class="tag tag-right">Right</td><td>F-type</td></tr>
<tr><td>Cuestas &amp; Garratt (2011)</td><td>C&amp;G (2011)</td><td>Simulated</td><td>Simulated</td><td class="tag tag-right">Right</td><td>&#967;&#178;-type</td></tr>
</tbody>
</table>
</div>
<div class="alert alert-info" style="margin-top:1.5rem;">
<span>ℹ</span>
<span><strong>Finite-sample interpolation:</strong> For tests with multiple T entries, TARUR automatically linearly interpolates between the two closest available sample sizes to your actual T.</span>
</div>
</div>
</section>
"""
print("Extended, cointegration, linearity, CV master table parts done")
