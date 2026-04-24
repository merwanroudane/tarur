NB_OUTPUTS_HTML = """
<div class="output-block">
  <div class="output-label">Dataset sizes</div>
  <pre class="output-pre">EUR/USD: 3907 observations
Gold:    3770 observations
S&amp;P500:  3773 observations
</pre>
</div>

<div class="output-block">
  <div class="output-label">KSS (2003) result — EUR/USD</div>
  <pre class="output-pre">============================================================
             KSS (2003) Nonlinear Unit Root Test            
============================================================
  H0: Unit root (linear random walk)
  H1: Globally stationary ESTAR process
------------------------------------------------------------
  Test Statistic (tNL)                 | -3.1823
  Selected Lag                  | 0 (AIC)
  Case                          | demeaned
------------------------------------------------------------
  Critical Values: 1%: -3.930 | 5%: -3.400 | 10%: -3.130
  Source: Kapetanios, Shin &amp; Snell (2003), Table 1 (asymptotic)
------------------------------------------------------------
  1%: [ACCEPT] H0
  5%: [ACCEPT] H0
  10%: [REJECT] H0
------------------------------------------------------------
  &gt;&gt; Reject H0 at the 10% significance level. Globally stationary ESTAR process.
============================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Kruse (2011) result — EUR/USD</div>
  <pre class="output-pre">============================================================
          Kruse (2011) Modified Wald Unit Root Test         
============================================================
  H0: Unit root (linear random walk)
  H1: Globally stationary ESTAR (nonzero location c)
------------------------------------------------------------
  Test Statistic (τ)                   | 10.4119
  Selected Lag                  | 0 (AIC)
  Case                          | demeaned
------------------------------------------------------------
  Critical Values: 1%: 13.750 | 5%: 10.170 | 10%: 8.600
  Source: Kruse (2011), Table 1 (asymptotic, T=1000)
------------------------------------------------------------
  1%: [ACCEPT] H0
  5%: [REJECT] H0
  10%: [REJECT] H0
------------------------------------------------------------
  &gt;&gt; Reject H0 at the 10% significance level. Globally stationary ESTAR (nonzero location c).
============================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Sollis (2009) result — EUR/USD</div>
  <pre class="output-pre">============================================================
        Sollis (2009) Asymmetric ESTAR Unit Root Test       
============================================================
  H0: Unit root (linear random walk)
  H1: Globally stationary symmetric or asymmetric ESTAR
------------------------------------------------------------
  Test Statistic (F_AE)                | 5.0873
  Selected Lag                  | 0 (AIC)
  Case                          | demeaned
------------------------------------------------------------
  Critical Values: 10%: 3.725 | 5%: 4.557 | 1%: 6.236
  Source: Sollis (2009), Table 1 (T=asymptotic)
------------------------------------------------------------
  1%: [ACCEPT] H0
  5%: [REJECT] H0
  10%: [REJECT] H0
------------------------------------------------------------
  &gt;&gt; Reject H0 at the 10% significance level. Globally stationary symmetric or asymmetric ESTAR.
============================================================

Symmetry test (Fas): 0.0500 (p=0.8230)
  → Fail to reject symmetry (symmetric ESTAR)
</pre>
</div>

<div class="output-block">
  <div class="output-label">Hu & Chen (2016) result — EUR/USD</div>
  <pre class="output-pre">============================================================
        Hu &amp; Chen (2016) Modified Wald Unit Root Test       
============================================================
  H0: Unit root (linear random walk)
  H1: Locally explosive but globally stationary ESTAR
------------------------------------------------------------
  Test Statistic (τ)                   | 11.9175
  Selected Lag                  | 0 (AIC)
  Case                          | demeaned
------------------------------------------------------------
  Critical Values: 1%: 15.620 | 5%: 11.860 | 10%: 10.120
  Source: Hu &amp; Chen (2016), Table 1 (asymptotic, T=1000)
------------------------------------------------------------
  1%: [ACCEPT] H0
  5%: [REJECT] H0
  10%: [REJECT] H0
------------------------------------------------------------
  &gt;&gt; Reject H0 at the 10% significance level. Locally explosive but globally stationary ESTAR.
============================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Enders & Granger (1998) result — Gold</div>
  <pre class="output-pre">============================================================
                 Enders &amp; Granger (1998) MTAR               
============================================================
  H0: Unit root
  H1: MTAR stationary with asymmetric adjustment
------------------------------------------------------------
  Test Statistic (Phi)                 | 0.1874
  Selected Lag                  | 1 (AIC)
  Case                          | demeaned
------------------------------------------------------------
  Critical Values: 1%: 8.780 | 5%: 6.410 | 10%: 5.390
  Source: Enders &amp; Granger (1998), Table 1
------------------------------------------------------------
  1%: [ACCEPT] H0
  5%: [ACCEPT] H0
  10%: [ACCEPT] H0
------------------------------------------------------------
  &gt;&gt; Fail to reject H0 at conventional significance levels. Unit root.
============================================================

Asymmetric adjustment: ρ⁺ = -0.0006, ρ⁻ = -0.0003
Symmetry F-test: 0.0354 (p=0.8508)
</pre>
</div>

<div class="output-block">
  <div class="output-label">LNV (1998) result — Gold</div>
  <pre class="output-pre">============================================================
                      LNV (1998) Model A                    
============================================================
  H0: Unit root
  H1: Stationary around smooth logistic transition
------------------------------------------------------------
  Test Statistic (t_ADF)               | -2.2350
  Selected Lag                  | 0 (AIC)
  Case                          | NLS Model A
------------------------------------------------------------
  Critical Values: 1%: -4.685 | 5%: -4.103 | 10%: -3.797
  Source: Leybourne, Newbold &amp; Vougas (1998), Table I (Model A, T=500)
------------------------------------------------------------
  1%: [ACCEPT] H0
  5%: [ACCEPT] H0
  10%: [ACCEPT] H0
------------------------------------------------------------
  &gt;&gt; Fail to reject H0 at conventional significance levels. Unit root.
============================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Output (Cell 20)</div>
  <pre class="output-pre">============================================================
                    Vougas (2006) Model A                   
============================================================
  H0: Unit root
  H1: Stationary around smooth transition
------------------------------------------------------------
  Test Statistic (t_ADF)               | -2.2350
  Selected Lag                  | 0 (AIC)
  Case                          | NLS Model A
------------------------------------------------------------
  Critical Values: 1%: -4.150 | 5%: -3.590 | 10%: -3.320
  Source: Vougas (2006), Table 1 (Model A, T=500)
------------------------------------------------------------
  1%: [ACCEPT] H0
  5%: [ACCEPT] H0
  10%: [ACCEPT] H0
------------------------------------------------------------
  &gt;&gt; Fail to reject H0 at conventional significance levels. Unit root.
============================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Vougas (2006) result — Gold</div>
  <pre class="output-pre">============================================================
                Harvey &amp; Mills (2002) Model A               
============================================================
  H0: Unit root
  H1: Stationary around double smooth transition
------------------------------------------------------------
  Test Statistic (t_ADF)               | -4.1185
  Selected Lag                  | 0 (AIC)
  Case                          | Double NLS Model A
------------------------------------------------------------
  Critical Values: 1%: -5.640 | 5%: -5.070 | 10%: -4.790
  Source: Harvey &amp; Mills (2002), Table 1 (Model A, T=1000)
------------------------------------------------------------
  1%: [ACCEPT] H0
  5%: [ACCEPT] H0
  10%: [ACCEPT] H0
------------------------------------------------------------
  &gt;&gt; Fail to reject H0 at conventional significance levels. Unit root.
============================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Harvey & Mills (2002) result — Gold</div>
  <pre class="output-pre">Linearity F-statistic: -810.5585
P-value: 1.000000
Suggested model: LSTAR

Sequential F-tests:
  H01 (linear terms):     F = -2433.310, p = 1.0000
  H02 (quadratic terms):  F = 0.000, p = 1.0000
  H03 (cubic terms):      F = 1.029, p = 0.3105
</pre>
</div>

<div class="output-block">
  <div class="output-label">Output (Cell 26)</div>
  <pre class="output-pre">======================================================================
  EUR/USD EXCHANGE RATE — Full Nonlinear Unit Root Test Battery
======================================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Output (Cell 26)</div>
  <pre class="output-pre">
================================================================================
                     TARUR — Nonlinear Unit Root Test Battery                   
================================================================================

Test                                           Stat    CV 5%   Decision
------------------------------------------------------------------------
  KSS (2003) Nonlinear Unit Root Test        -3.182   -3.400     ACCEPT
  Kruse (2011) Modified Wald Unit Root Test   10.412   10.170     REJECT
  Sollis (2009) Asymmetric ESTAR Unit Root Test    5.087    4.557     REJECT
  Hu &amp; Chen (2016) Modified Wald Unit Root Test   11.918   11.860     REJECT
  Pascalau (2007) Asymmetric NLSTAR           3.565    6.820     ACCEPT
  Cuestas &amp; Garratt (2011)                   14.880   17.270     ACCEPT
  Cuestas &amp; Ordonez (2014)                   -3.525   -2.930     REJECT
  Enders &amp; Granger (1998) MTAR                4.040    6.410     ACCEPT
  LNV (1998) Model A                         -3.802   -4.103     ACCEPT
  Vougas (2006) Model A                      -3.802   -3.590     REJECT
  Harvey &amp; Mills (2002) Model A              -4.615   -5.070     ACCEPT
================================================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Output (Cell 28)</div>
  <pre class="output-pre">======================================================================
  GOLD PRICES — Full Nonlinear Unit Root Test Battery
======================================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Output (Cell 28)</div>
  <pre class="output-pre">
================================================================================
                     TARUR — Nonlinear Unit Root Test Battery                   
================================================================================

Test                                           Stat    CV 5%   Decision
------------------------------------------------------------------------
  KSS (2003) Nonlinear Unit Root Test        -0.218   -3.400     ACCEPT
  Kruse (2011) Modified Wald Unit Root Test    4.186   10.170     ACCEPT
  Sollis (2009) Asymmetric ESTAR Unit Root Test    1.532    4.557     ACCEPT
  Hu &amp; Chen (2016) Modified Wald Unit Root Test    4.196   11.860     ACCEPT
  Pascalau (2007) Asymmetric NLSTAR           1.414    6.820     ACCEPT
  Cuestas &amp; Garratt (2011)                   12.865   17.270     ACCEPT
  Cuestas &amp; Ordonez (2014)                   -1.996   -2.930     ACCEPT
  Enders &amp; Granger (1998) MTAR                0.187    6.410     ACCEPT
  LNV (1998) Model A                         -2.235   -4.103     ACCEPT
  Vougas (2006) Model A                      -2.235   -3.590     ACCEPT
  Harvey &amp; Mills (2002) Model A              -4.119   -5.070     ACCEPT
================================================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Output (Cell 30)</div>
  <pre class="output-pre">======================================================================
  S&amp;P 500 INDEX — Full Nonlinear Unit Root Test Battery
======================================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Output (Cell 30)</div>
  <pre class="output-pre">
================================================================================
                     TARUR — Nonlinear Unit Root Test Battery                   
================================================================================

Test                                           Stat    CV 5%   Decision
------------------------------------------------------------------------
  KSS (2003) Nonlinear Unit Root Test        -0.434   -3.400     ACCEPT
  Kruse (2011) Modified Wald Unit Root Test    4.651   10.170     ACCEPT
  Sollis (2009) Asymmetric ESTAR Unit Root Test    1.926    4.557     ACCEPT
  Hu &amp; Chen (2016) Modified Wald Unit Root Test    4.706   11.860     ACCEPT
  Pascalau (2007) Asymmetric NLSTAR           1.577    6.820     ACCEPT
  Cuestas &amp; Garratt (2011)                   45.063   17.270     REJECT
  Cuestas &amp; Ordonez (2014)                   -6.482   -2.930     REJECT
  Enders &amp; Granger (1998) MTAR                0.048    6.410     ACCEPT
  LNV (1998) Model A                         -4.061   -4.103     ACCEPT
  Vougas (2006) Model A                      -4.061   -3.590     REJECT
  Harvey &amp; Mills (2002) Model A              -4.354   -5.070     ACCEPT
================================================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Output (Cell 32)</div>
  <pre class="output-pre">
==========================================================================================
  COMPREHENSIVE NONLINEAR UNIT ROOT TEST RESULTS
==========================================================================================
 Series                              Test Statistic CV (5%)  Lag Decision (5%)
EUR/USD              KSS (2003) Nonlinear    -3.182  -3.400    0   ✓ Accept H₀
EUR/USD                      Kruse (2011)    10.412  10.170    0   ✗ Reject H₀
EUR/USD    Sollis (2009) Asymmetric ESTAR     5.087   4.557    0   ✗ Reject H₀
EUR/USD                  Hu &amp; Chen (2016)    11.918  11.860    0   ✗ Reject H₀
EUR/USD Pascalau (2007) Asymmetric NLSTAR     3.565   6.820    0   ✓ Accept H₀
EUR/USD          Cuestas &amp; Garratt (2011)    14.880  17.270    0   ✓ Accept H₀
EUR/USD          Cuestas &amp; Ordonez (2014)    -3.525  -2.930    6   ✗ Reject H₀
EUR/USD      Enders &amp; Granger (1998) MTAR     4.040   6.410    1   ✓ Accept H₀
EUR/USD                LNV (1998) Model A    -3.802  -4.103    0   ✓ Accept H₀
EUR/USD             Vougas (2006) Model A    -3.802  -3.590    0   ✗ Reject H₀
EUR/USD     Harvey &amp; Mills (2002) Model A    -4.615  -5.070    0   ✓ Accept H₀
   Gold              KSS (2003) Nonlinear    -0.218  -3.400    0   ✓ Accept H₀
   Gold                      Kruse (2011)     4.186  10.170    0   ✓ Accept H₀
   Gold    Sollis (2009) Asymmetric ESTAR     1.532   4.557    0   ✓ Accept H₀
   Gold                  Hu &amp; Chen (2016)     4.196  11.860    0   ✓ Accept H₀
   Gold Pascalau (2007) Asymmetric NLSTAR     1.414   6.820    0   ✓ Accept H₀
   Gold          Cuestas &amp; Garratt (2011)    12.865  17.270    0   ✓ Accept H₀
   Gold          Cuestas &amp; Ordonez (2014)    -1.996  -2.930    1   ✓ Accept H₀
   Gold      Enders &amp; Granger (1998) MTAR     0.187   6.410    1   ✓ Accept H₀
   Gold                LNV (1998) Model A    -2.235  -4.103    0   ✓ Accept H₀
   Gold             Vougas (2006) Model A    -2.235  -3.590    0   ✓ Accept H₀
   Gold     Harvey &amp; Mills (2002) Model A    -4.119  -5.070    0   ✓ Accept H₀
S&amp;P 500              KSS (2003) Nonlinear    -0.434  -3.400    9   ✓ Accept H₀
S&amp;P 500                      Kruse (2011)     4.651  10.170    9   ✓ Accept H₀
S&amp;P 500    Sollis (2009) Asymmetric ESTAR     1.926   4.557    9   ✓ Accept H₀
S&amp;P 500                  Hu &amp; Chen (2016)     4.706  11.860    9   ✓ Accept H₀
S&amp;P 500 Pascalau (2007) Asymmetric NLSTAR     1.577   6.820    9   ✓ Accept H₀
S&amp;P 500          Cuestas &amp; Garratt (2011)    45.063  17.270    9   ✗ Reject H₀
S&amp;P 500          Cuestas &amp; Ordonez (2014)    -6.482  -2.930    9   ✗ Reject H₀
S&amp;P 500      Enders &amp; Granger (1998) MTAR     0.048   6.410    9   ✓ Accept H₀
S&amp;P 500                LNV (1998) Model A    -4.061  -4.103    9   ✓ Accept H₀
S&amp;P 500             Vougas (2006) Model A    -4.061  -3.590    9   ✗ Reject H₀
S&amp;P 500     Harvey &amp; Mills (2002) Model A    -4.354  -5.070    9   ✓ Accept H₀
</pre>
</div>

<div class="output-block">
  <div class="output-label">Cointegration — EUR/USD vs Gold</div>
  <pre class="output-pre">============================================================
  KSS (2006) Nonlinear Cointegration: EUR/USD ~ Gold
============================================================
============================================================
           KSS (2006) Nonlinear Cointegration Test          
============================================================
  H0: No cointegration (residuals have unit root)
  H1: Nonlinear cointegration (ESTAR stationary residuals)
------------------------------------------------------------
  Test Statistic (tNL)                 | -3.0346
  Selected Lag                  | 0 (AIC)
  Case                          | demeaned
------------------------------------------------------------
  Critical Values: 1%: -3.930 | 5%: -3.400 | 10%: -3.130
  Source: Kapetanios, Shin &amp; Snell (2003), Table 1 (asymptotic)
------------------------------------------------------------
  1%: [ACCEPT] H0
  5%: [ACCEPT] H0
  10%: [ACCEPT] H0
------------------------------------------------------------
  &gt;&gt; Fail to reject H0 at conventional significance levels. Unit root (linear random walk).
============================================================

============================================================
  Enders-Siklos (2001) TAR Cointegration: EUR/USD ~ Gold
============================================================
============================================================
        Enders &amp; Siklos (2001) TAR Cointegration Test       
============================================================
  H0: No cointegration
  H1: Threshold cointegration with asymmetric adjustment
------------------------------------------------------------
  Test Statistic (Phi)                 | 2.6885
  Selected Lag                  | 1 (AIC)
  Case                          | raw
------------------------------------------------------------
  Critical Values: 1%: 7.850 | 5%: 5.670 | 10%: 4.710
  Source: Enders &amp; Siklos (2001), Table 1
------------------------------------------------------------
  1%: [ACCEPT] H0
  5%: [ACCEPT] H0
  10%: [ACCEPT] H0
------------------------------------------------------------
  &gt;&gt; Fail to reject H0 at conventional significance levels. Unit root.
============================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Output (Cell 45)</div>
  <pre class="output-pre">% LaTeX table for EUR/USD results
% Copy this into your paper

\begin{table}[htbp]
\centering
\caption{Nonlinear Unit Root Test Results — EUR/USD Exchange Rate}
\label{tab:nonlinear_ur}
\begin{tabular}{lcccl}
\hline\hline
Test &amp; Statistic &amp; CV (5\%) &amp; Lag &amp; Decision \\
\hline
KSS &amp; -3.182 &amp; -3.400 &amp; 0 &amp; Accept \\
Kruse &amp; 10.412 &amp; 10.170 &amp; 0 &amp; Reject \\
Sollis &amp; 5.087 &amp; 4.557 &amp; 0 &amp; Reject \\
Hu &amp; Chen &amp; 11.918 &amp; 11.860 &amp; 0 &amp; Reject \\
Pascalau &amp; 3.565 &amp; 6.820 &amp; 0 &amp; Accept \\
Cuestas &amp; Garratt &amp; 14.880 &amp; 17.270 &amp; 0 &amp; Accept \\
Cuestas &amp; Ordonez &amp; -3.525 &amp; -2.930 &amp; 6 &amp; Reject \\
Enders &amp; Granger &amp; 4.040 &amp; 6.410 &amp; 1 &amp; Accept \\
LNV &amp; -3.802 &amp; -4.103 &amp; 0 &amp; Accept \\
Vougas &amp; -3.802 &amp; -3.590 &amp; 0 &amp; Reject \\
Harvey &amp; Mills &amp; -4.615 &amp; -5.070 &amp; 0 &amp; Accept \\
\hline\hline
\end{tabular}
\end{table}
</pre>
</div>

<div class="output-block">
  <div class="output-label">Monte Carlo validation summary</div>
  <pre class="output-pre">ESTAR Process (should reject H₀):
------------------------------------------------------------
</pre>
</div>

<div class="output-block">
  <div class="output-label">Monte Carlo validation summary</div>
  <pre class="output-pre">
================================================================================
                     TARUR — Nonlinear Unit Root Test Battery                   
================================================================================

Test                                           Stat    CV 5%   Decision
------------------------------------------------------------------------
  KSS (2003) Nonlinear Unit Root Test        -7.334   -3.400     REJECT
  Kruse (2011) Modified Wald Unit Root Test   54.373   10.170     REJECT
  Sollis (2009) Asymmetric ESTAR Unit Root Test   28.749    4.557     REJECT
  Hu &amp; Chen (2016) Modified Wald Unit Root Test   61.842   11.860     REJECT
  Pascalau (2007) Asymmetric NLSTAR          20.072    6.820     REJECT
  Cuestas &amp; Garratt (2011)                   57.091   17.270     REJECT
  Cuestas &amp; Ordonez (2014)                   -7.285   -2.930     REJECT
  Enders &amp; Granger (1998) MTAR               17.739    6.410     REJECT
  LNV (1998) Model A                         -6.322   -4.103     REJECT
  Vougas (2006) Model A                      -6.322   -3.590     REJECT
  Harvey &amp; Mills (2002) Model A              -6.733   -5.200     REJECT
================================================================================

Random Walk (should NOT reject H₀):
------------------------------------------------------------
</pre>
</div>

<div class="output-block">
  <div class="output-label">Monte Carlo validation summary</div>
  <pre class="output-pre">
================================================================================
                     TARUR — Nonlinear Unit Root Test Battery                   
================================================================================

Test                                           Stat    CV 5%   Decision
------------------------------------------------------------------------
  KSS (2003) Nonlinear Unit Root Test         0.015   -3.400     ACCEPT
  Kruse (2011) Modified Wald Unit Root Test    4.832   10.170     ACCEPT
  Sollis (2009) Asymmetric ESTAR Unit Root Test    0.677    4.557     ACCEPT
  Hu &amp; Chen (2016) Modified Wald Unit Root Test    5.409   11.860     ACCEPT
  Pascalau (2007) Asymmetric NLSTAR           2.266    6.820     ACCEPT
  Cuestas &amp; Garratt (2011)                   11.791   17.270     ACCEPT
  Cuestas &amp; Ordonez (2014)                   -2.208   -2.930     ACCEPT
  Enders &amp; Granger (1998) MTAR                2.457    6.410     ACCEPT
  LNV (1998) Model A                         -3.079   -4.103     ACCEPT
  Vougas (2006) Model A                      -3.079   -3.590     ACCEPT
  Harvey &amp; Mills (2002) Model A              -3.148   -5.200     ACCEPT
================================================================================
</pre>
</div>

<div class="output-block">
  <div class="output-label">Output (Cell 48)</div>
  <pre class="output-pre">
Validation Summary:
  ESTAR: 11/11 tests correctly reject H₀ at 5%
  RW:    11/11 tests correctly accept H₀ at 5%
</pre>
</div>
"""
