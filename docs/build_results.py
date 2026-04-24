"""Build docs/results.html — all notebook outputs (text + plots) in one page."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts.shared import NAV, FOOTER
from parts.nb_outputs_html import NB_OUTPUTS_HTML

# Extra CSS for output blocks
EXTRA_CSS = """
<style>
.output-block {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 1.5rem;
  overflow: hidden;
  box-shadow: var(--shadow);
}
.output-label {
  background: var(--bg3);
  border-bottom: 1px solid var(--border);
  padding: .55rem 1rem;
  font-size: .82rem;
  font-weight: 700;
  color: var(--text2);
  letter-spacing: .04em;
  text-transform: uppercase;
}
.output-pre {
  background: #1e293b;
  color: #e2e8f0;
  padding: 1rem 1.25rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: .78rem;
  line-height: 1.7;
  overflow-x: auto;
  margin: 0;
  border-radius: 0;
  box-shadow: none;
  white-space: pre;
}
.gallery-2col {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}
.plot-card {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
  background: #fff;
  transition: all .2s;
}
.plot-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.plot-card img { width: 100%; display: block; }
.plot-card .cap {
  padding: .65rem 1rem;
  font-size: .83rem;
  color: var(--text2);
  border-top: 1px solid var(--border);
  font-style: italic;
}
.results-toc {
  background: var(--primary-light);
  border: 1px solid #bfdbfe;
  border-radius: var(--radius);
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  font-size: .9rem;
}
.results-toc h4 { color: var(--primary); margin-bottom: .5rem; font-size: .9rem; }
.results-toc a { color: var(--primary); margin-right: 1rem; text-decoration: none; }
.results-toc a:hover { text-decoration: underline; }
</style>
"""

PLOTS = [
    ("plot_00.png", "EUR/USD, Gold, and S&amp;P 500 — Level (log) and daily returns (2010–2024)"),
    ("plot_01.png", "EUR/USD — Full nonlinear unit root battery: statistic vs. 5% CV"),
    ("plot_02.png", "Gold prices — Full battery with reject/accept decisions"),
    ("plot_03.png", "S&amp;P 500 — Expected unit root: most tests correctly accept H₀"),
    ("plot_04.png", "Decision heatmap — All tests × All series at 1%, 5%, 10%"),
    ("plot_05.png", "EUR/USD — Diagnostic dashboard (level, ACF, PACF, histogram, QQ)"),
    ("plot_06.png", "Monte Carlo — ESTAR process (stationary) vs. Random Walk (non-stationary)"),
]

plots_html = '<div class="gallery-2col">'
for fname, cap in PLOTS:
    plots_html += f"""
<div class="plot-card">
  <img src="assets/img/{fname}" alt="{cap}" loading="lazy"/>
  <div class="cap">{cap}</div>
</div>"""
plots_html += "</div>"

page = (
    NAV.format(title="Results", g='', a='', r='class="active"') +
    EXTRA_CSS +
    """
<section style="background:linear-gradient(135deg,#f0f7ff,#e8f4ff,#f0fdf8);
  padding:4rem 2rem 3rem;text-align:center;border-bottom:1px solid var(--border);">
  <div class="section-tag">Empirical Results</div>
  <h1 style="font-size:2.5rem;font-weight:700;letter-spacing:-.03em;margin-bottom:.5rem;">
    Tutorial Outputs — Real Data</h1>
  <p style="color:var(--text2);max-width:700px;margin:0 auto;">
    All outputs from the
    <a href="https://github.com/merwanroudane/tarur/blob/main/tarur_tutorial.ipynb"
       target="_blank" style="color:var(--primary);font-weight:600;">tutorial notebook</a>
    — test result tables and visualizations using EUR/USD, Gold, and S&amp;P 500
    data (2010–2024). Run the notebook yourself with
    <code style="background:var(--bg3);padding:.1rem .4rem;border-radius:4px;">pip install tarur==1.0.1</code>.
  </p>
</section>

<section class="section">
<div class="container">

<div class="results-toc">
  <h4>Quick Navigation</h4>
  <a href="#plots">📊 Visualizations</a>
  <a href="#individual">🔬 Individual Tests</a>
  <a href="#battery">⚡ Full Battery</a>
  <a href="#summary">📋 Summary Table</a>
  <a href="#coint">🔗 Cointegration</a>
  <a href="#montecarlo">🎲 Monte Carlo</a>
</div>

<!-- PLOTS -->
<h2 class="section-title anchor" id="plots" style="margin-bottom:1rem;">📊 Visualizations</h2>
""" + plots_html + """

<!-- TEXT OUTPUTS -->
<h2 class="section-title anchor" id="individual"
  style="margin-top:2.5rem;margin-bottom:1rem;">🔬 Individual Test Outputs</h2>
<p style="color:var(--text2);margin-bottom:1.5rem;font-size:.93rem;">
  Each test prints its statistic, critical values from the original paper, and an
  automatic reject/accept decision at 1%, 5%, and 10% significance levels.
</p>
""" + NB_OUTPUTS_HTML + """

</div>
</section>
""" + FOOTER
)

with open("docs/results.html", "w", encoding="utf-8") as f:
    f.write(page)
print(f"results.html written ({len(page)//1024} KB)")
