SMOOTH_SECTION = """
<section class="section section-alt" id="smooth">
<div class="container">
<div class="section-tag">Category 2</div>
<h2 class="section-title">Smooth Transition Unit Root Tests</h2>
<p class="section-sub">These tests first estimate a nonlinear smooth transition deterministic trend via NLS, subtract it, then apply an ADF test to the residuals. <strong>Each test has its own distinct critical values</strong> from its original paper — they are not interchangeable.</p>

<!-- LNV -->
<div class="theory-card">
  <h3><span class="theory-num">5</span> LNV (1998) — Single Logistic Smooth Transition</h3>
  <div class="theory-ref">Leybourne, S., Newbold, P., &amp; Vougas, D. (1998). <em>Unit roots and smooth transitions.</em> JTSA, 19(1), 83–97.</div>
  <p>The logistic transition function: $S_t(\\gamma,\\tau) = \\bigl[1 + \\exp(-\\gamma(t - \\tau T))\\bigr]^{-1}$ smoothly shifts from 0 to 1. Three models:</p>
  <div class="math-block">$$\\text{Model A: }\\; y_t = \\alpha_1 + \\alpha_2 S_t + \\nu_t$$</div>
  <div class="math-block">$$\\text{Model B: }\\; y_t = \\alpha_1 + \\beta_1 t + \\alpha_2 S_t + \\nu_t$$</div>
  <div class="math-block">$$\\text{Model C: }\\; y_t = \\alpha_1 + \\beta_1 t + \\alpha_2 S_t + \\beta_2 t\\, S_t + \\nu_t$$</div>
  <p>NLS estimates $\\gamma$ and $\\tau$, then the ADF $t$-statistic on the detrended residuals $\\hat{\\nu}_t$ is compared to LNV Table I (not ADF tables!).</p>
  <table class="cv-table" style="max-width:600px;">
    <thead><tr><th>T</th><th colspan="3">Model A</th><th colspan="3">Model B</th></tr>
    <tr><th></th><th>1%</th><th>5%</th><th>10%</th><th>1%</th><th>5%</th><th>10%</th></tr></thead>
    <tbody>
      <tr><td>50</td><td>-5.10</td><td>-4.36</td><td>-4.01</td><td>-5.77</td><td>-5.05</td><td>-4.64</td></tr>
      <tr><td>100</td><td>-4.88</td><td>-4.23</td><td>-3.91</td><td>-5.48</td><td>-4.77</td><td>-4.43</td></tr>
      <tr><td>200</td><td>-4.76</td><td>-4.16</td><td>-3.85</td><td>-5.20</td><td>-4.63</td><td>-4.34</td></tr>
      <tr><td>500</td><td>-4.69</td><td>-4.10</td><td>-3.80</td><td>-5.14</td><td>-4.57</td><td>-4.28</td></tr>
    </tbody>
  </table>
  <pre>result = tarur.lnv_test(y, model='A', max_lags=12)  # model: 'A', 'B', or 'C'</pre>
</div>

<!-- VOUGAS -->
<div class="theory-card">
  <h3><span class="theory-num">6</span> Vougas (2006) — Extended Single Transition (5 Models)</h3>
  <div class="theory-ref">Vougas, D. (2006). <em>On unit root testing with smooth transitions.</em> Computational Statistics &amp; Data Analysis, 51(2), 797–800.</div>
  <p>Extends LNV with five functional forms (Models A–E), including trend-only transition and exponential transition. Each model has a distinct CV table. Model A mirrors LNV but with updated CVs from Vougas (2006) Table 1.</p>
  <pre>for m in ['A','B','C','D','E']:
    r = tarur.vougas_test(y, model=m, max_lags=12)
    print(f"Model {m}: t={r.statistic:.3f}, CV(5%)={r.critical_values.cv5:.3f}, {r.decision}")</pre>
</div>

<!-- HARVEY MILLS -->
<div class="theory-card">
  <h3><span class="theory-num">7</span> Harvey &amp; Mills (2002) — Double Smooth Transition</h3>
  <div class="theory-ref">Harvey, D.I., &amp; Mills, T.C. (2002). <em>Unit roots and double smooth transitions.</em> J. Applied Statistics, 29(5), 675–683.</div>
  <p>Allows <strong>two</strong> smooth transitions (two structural breaks). The double transition function is:</p>
  <div class="math-block">$$y_t = \\alpha_1 + \\alpha_2 S_t^{(1)} + \\alpha_3 S_t^{(2)} + \\nu_t \\ \\ \\text{(Model A)}$$</div>
  <p>The CVs are <strong>substantially larger</strong> in absolute value than LNV because the more flexible double-transition alternative shifts the null distribution. Using LNV CVs here would lead to over-rejection.</p>
  <table class="cv-table" style="max-width:500px;">
    <thead><tr><th>T</th><th>1%</th><th>5%</th><th>10%</th></tr></thead>
    <tbody>
      <tr><td>50</td><td>-6.49</td><td>-5.73</td><td>-5.33</td></tr>
      <tr><td>100</td><td>-6.05</td><td>-5.37</td><td>-5.04</td></tr>
      <tr><td>200</td><td>-5.80</td><td>-5.20</td><td>-4.90</td></tr>
      <tr><td>1000</td><td>-5.64</td><td>-5.07</td><td>-4.79</td></tr>
    </tbody>
  </table>
  <pre>result = tarur.harvey_mills_test(y, model='A', max_lags=12)</pre>
</div>
</div>
</section>
"""
print("Smooth section done")
