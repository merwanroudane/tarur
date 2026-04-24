"""Extract all text/table outputs from the executed tutorial notebook."""
import json, html as html_mod

with open('tarur_tutorial.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

outputs_data = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell.get('source', [])).strip()[:80]
    for out in cell.get('outputs', []):
        otype = out.get('output_type', '')
        if otype in ('stream', 'execute_result', 'display_data'):
            text = out.get('text', '') or out.get('data', {}).get('text/plain', '')
            if isinstance(text, list):
                text = ''.join(text)
            if text.strip() and len(text) > 80:
                outputs_data.append({'cell': i, 'src': src, 'text': text})

# Write as HTML snippets file
sections_html = ""
labels = {
    5:  "Dataset sizes",
    9:  "KSS (2003) result — EUR/USD",
    11: "Kruse (2011) result — EUR/USD",
    13: "Sollis (2009) result — EUR/USD",
    15: "Hu & Chen (2016) result — EUR/USD",
    17: "Enders & Granger (1998) result — Gold",
    19: "LNV (1998) result — Gold",
    21: "Vougas (2006) result — Gold",
    23: "Harvey & Mills (2002) result — Gold",
    27: "Terasvirta linearity test — EUR/USD returns",
    29: "Full battery — EUR/USD",
    31: "Full battery — Gold",
    33: "Full battery — S&P 500",
    35: "Summary DataFrame — all series",
    43: "Cointegration — EUR/USD vs Gold",
    47: "Monte Carlo validation summary",
}

for o in outputs_data:
    label = labels.get(o['cell'], f"Output (Cell {o['cell']})")
    escaped = html_mod.escape(o['text'])
    sections_html += f"""
<div class="output-block">
  <div class="output-label">{label}</div>
  <pre class="output-pre">{escaped}</pre>
</div>
"""
    print(f"Cell {o['cell']:3d} | {len(o['text']):5d} chars | {label}")

with open('docs/parts/nb_outputs_html.py', 'w', encoding='utf-8') as f:
    f.write(f'NB_OUTPUTS_HTML = """{sections_html}"""\n')

print(f"\nExtracted {len(outputs_data)} outputs → docs/parts/nb_outputs_html.py")
