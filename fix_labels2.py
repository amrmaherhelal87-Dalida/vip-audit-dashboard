with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ── 1. Register ChartDataLabels after ALL_DATA declaration ───────────────────
OLD_ANCHOR = "let ALL_DATA = [];"
NEW_ANCHOR = """let ALL_DATA = [];

// Register datalabels plugin; defaults to OFF globally
Chart.register(ChartDataLabels);
Chart.defaults.set('plugins.datalabels', { display: false });
"""
if OLD_ANCHOR in html:
    html = html.replace(OLD_ANCHOR, NEW_ANCHOR, 1)
    fixes += 1
    print("JS: ChartDataLabels registered")
else:
    print("WARN: let ALL_DATA anchor not found")

# ── 2. Region chart bar dataset - add datalabels ─────────────────────────────
OLD_REGION = """        backgroundColor: barColors.map(c=>c+'88'),
        borderColor: barColors,
        borderWidth: 2, borderRadius: 8,
        y"""
NEW_REGION = """        backgroundColor: barColors.map(c=>c+'88'),
        borderColor: barColors,
        borderWidth: 2, borderRadius: 8,
        datalabels: {
          display: true, anchor:'end', align:'top',
          color:'#cbd5e1', font:{size:10,weight:'600'},
          formatter: v => v+'%'
        },
        y"""
if OLD_REGION in html:
    html = html.replace(OLD_REGION, NEW_REGION, 1)
    fixes += 1
    print("JS: datalabels added to Region chart")
else:
    print("WARN: Region chart dataset not found")

# ── 3. Find and fix Gov chart similarly ──────────────────────────────────────
OLD_GOV = "function buildGovernorateChart(data) {"
idx = html.find(OLD_GOV)
if idx > 0:
    chunk = html[idx:idx+2000]
    OLD_IN_CHUNK = """        backgroundColor: barColors.map(c=>c+'88'),
        borderColor: barColors,
        borderWidth: 2, borderRadius: 8,
        y"""
    if OLD_IN_CHUNK in chunk:
        new_chunk = chunk.replace(OLD_IN_CHUNK, """        backgroundColor: barColors.map(c=>c+'88'),
        borderColor: barColors,
        borderWidth: 2, borderRadius: 8,
        datalabels: {
          display: true, anchor:'end', align:'top',
          color:'#cbd5e1', font:{size:10,weight:'600'},
          formatter: v => v+'%'
        },
        y""", 1)
        html = html[:idx] + new_chunk + html[idx+2000:]
        fixes += 1
        print("JS: datalabels added to Gov chart")
    else:
        # Try alternate structure
        if "borderRadius: 8" in chunk:
            print("WARN: Gov chart structure slightly different, checking...")
            import re
            m = re.search(r'borderRadius: 8,\n', chunk)
            if m:
                print(repr(chunk[m.start():m.start()+200]))

# ── 4. Round chart in overview tab (buildRoundChart / buildTrend) ─────────────
OLD_TREND = "function buildRoundChart(data) {"
idx2 = html.find(OLD_TREND)
if idx2 < 0:
    OLD_TREND = "function buildTrend(data) {"
    idx2 = html.find(OLD_TREND)

if idx2 > 0:
    chunk2 = html[idx2:idx2+2000]
    if "borderRadius" in chunk2:
        # Add datalabels to first bar dataset in this function
        old_in = "borderWidth: 2, borderRadius: 6,"
        new_in = """borderWidth: 2, borderRadius: 6,
          datalabels: {
            display: true, anchor:'end', align:'top',
            color:'#cbd5e1', font:{size:10,weight:'600'},
            formatter: v => v
          },"""
        if old_in in chunk2:
            new_chunk2 = chunk2.replace(old_in, new_in, 1)
            html = html[:idx2] + new_chunk2 + html[idx2+2000:]
            fixes += 1
            print("JS: datalabels added to Trend/Round chart")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal additional fixes: {fixes}")
