with open('index.html', encoding='utf-8') as f:
    html = f.read()
import re

fixes = 0

# ══════════════════════════════════════════════════════════════════
# FIX 1 — Score bar: add display:block to .score-bar-fill
# ══════════════════════════════════════════════════════════════════
html = html.replace(
    '.score-bar-fill { height: 100%; border-radius: 4px; transition: width .3s; }',
    '.score-bar-fill { display:block; height: 100%; border-radius: 4px; transition: width .3s; }'
)
fixes += 1
print("FIX 1: score-bar-fill display:block added")

# ══════════════════════════════════════════════════════════════════
# FIX 2 — Add Price to Impulse & Grocery in OUTLET_KPIS (table)
# ══════════════════════════════════════════════════════════════════
html = html.replace(
    """    'Impulse & Grocery': [
      {label:'Avail',  key:'avail_compliance'},
      {label:'SoS',    key:'sos_compliance'},
      {label:'SZ',     key:'sz_compliance'},
      {label:'L.Cooler',key:'large_cooler_compliance'},
    ],""",
    """    'Impulse & Grocery': [
      {label:'Avail',  key:'avail_compliance'},
      {label:'SoS',    key:'sos_compliance'},
      {label:'SZ',     key:'sz_compliance'},
      {label:'Price',  key:'price_compliance'},
      {label:'L.Cooler',key:'large_cooler_compliance'},
    ],"""
)
fixes += 1
print("FIX 2: Price added to Impulse & Grocery OUTLET_KPIS")

# ══════════════════════════════════════════════════════════════════
# FIX 3 — Add Price to Impulse in KPI_BY_CONTRACT (contract chart)
# ══════════════════════════════════════════════════════════════════
OLD_KPI_CONTRACT = """{ id:'impulse', label:'Impulse & Grocery',
    kpis:[
      { label:'Availability',   comp:'avail_compliance',        inc:'avail_incentive' },
      { label:'Share of Shelf', comp:'sos_compliance',          inc:'sos_incentive' },
      { label:'Strike Zone',    comp:'sz_compliance',           inc:'sz_incentive' },
      { label:'Large Cooler',   comp:'large_cooler_compliance', inc:'large_cooler_incentive' },
    ]
  },"""

NEW_KPI_CONTRACT = """{ id:'impulse', label:'Impulse & Grocery',
    kpis:[
      { label:'Availability',   comp:'avail_compliance',        inc:'avail_incentive' },
      { label:'Share of Shelf', comp:'sos_compliance',          inc:'sos_incentive' },
      { label:'Strike Zone',    comp:'sz_compliance',           inc:'sz_incentive' },
      { label:'Price',          comp:'price_compliance',        inc:'price_incentive' },
      { label:'Large Cooler',   comp:'large_cooler_compliance', inc:'large_cooler_incentive' },
    ]
  },"""

if OLD_KPI_CONTRACT in html:
    html = html.replace(OLD_KPI_CONTRACT, NEW_KPI_CONTRACT, 1)
    fixes += 1
    print("FIX 3: Price added to Impulse KPI_BY_CONTRACT")
else:
    # Try with different whitespace
    m = re.search(r"id:'impulse'.*?label:'Large Cooler'.*?\},\s*\]\s*\},", html, re.DOTALL)
    if m:
        old_block = m.group(0)
        # Insert Price before Large Cooler
        new_block = old_block.replace(
            "{ label:'Large Cooler',",
            "{ label:'Price',          comp:'price_compliance',        inc:'price_incentive' },\n      { label:'Large Cooler',"
        )
        html = html.replace(old_block, new_block, 1)
        fixes += 1
        print("FIX 3: Price added to Impulse KPI_BY_CONTRACT (via regex)")
    else:
        print("WARN FIX 3: KPI_BY_CONTRACT Impulse block not found")

# ══════════════════════════════════════════════════════════════════
# FIX 4 — Add Price to Impulse in map POPUP_KPIS
# ══════════════════════════════════════════════════════════════════
html = html.replace(
    """    'Impulse & Grocery': [
      {l:'Avail',k:'avail_compliance'},{l:'SoS',k:'sos_compliance'},
      {l:'Strike',k:'sz_compliance'},{l:'L.Cooler',k:'large_cooler_compliance'},
    ],""",
    """    'Impulse & Grocery': [
      {l:'Avail',k:'avail_compliance'},{l:'SoS',k:'sos_compliance'},
      {l:'Strike',k:'sz_compliance'},{l:'Price',k:'price_compliance'},
      {l:'L.Cooler',k:'large_cooler_compliance'},
    ],"""
)
fixes += 1
print("FIX 4: Price added to Impulse map POPUP_KPIS")

# ══════════════════════════════════════════════════════════════════
# FIX 5 — Add Round 83 (August) to filter dropdowns
# ══════════════════════════════════════════════════════════════════
# Overview filter
html = html.replace(
    '<label class="ms-opt"><input type="checkbox" value="83" onchange="msOptChange(\'ms-round\')"> Round 83 — August</label>',
    '<label class="ms-opt"><input type="checkbox" value="83" onchange="msOptChange(\'ms-round\')"> Round 83 — August</label>'
)
# Check if Round 83 already exists
if 'Round 83' not in html:
    html = html.replace(
        '<label class="ms-opt"><input type="checkbox" value="82" onchange="msOptChange(\'ms-round\')"> Round 82 — July</label>\n          </div>',
        '<label class="ms-opt"><input type="checkbox" value="82" onchange="msOptChange(\'ms-round\')"> Round 82 — July</label>\n          <label class="ms-opt"><input type="checkbox" value="83" onchange="msOptChange(\'ms-round\')"> Round 83 — August</label>\n          </div>'
    )
    fixes += 1
    print("FIX 5: Round 83 added to overview filter")
else:
    print("FIX 5: Round 83 already in filter")

# Map filter
if 'ms-m-round' in html and 'Round 83' not in html.split('ms-m-round')[1][:500]:
    html = html.replace(
        '<label class="ms-opt"><input type="checkbox" value="82" onchange="msOptChange(\'ms-m-round\')"> Round 82 — July</label>',
        '<label class="ms-opt"><input type="checkbox" value="82" onchange="msOptChange(\'ms-m-round\')"> Round 82 — July</label>\n          <label class="ms-opt"><input type="checkbox" value="83" onchange="msOptChange(\'ms-m-round\')"> Round 83 — August</label>'
    )
    fixes += 1
    print("FIX 5b: Round 83 added to map filter")

# ══════════════════════════════════════════════════════════════════
# FIX 6 — MERGE charts: remove Trend card, make Outlet Type chart wider
#          + add Overall as line in buildOutletChart
# ══════════════════════════════════════════════════════════════════
# Remove the standalone "Compliance Trend by Round" chart card
OLD_TREND_CARD = """    <!-- Round trend -->
    <div class="chart-card fade-in">
      <div class="chart-header">
        <div>
          <div class="chart-title">Compliance Trend by Round</div>
          <div class="chart-subtitle">Average score per audit round (April \u2192 July)</div>
        </div>
      </div>
      <div class="chart-wrap"><canvas id="c-trend"></canvas></div>
    </div>"""

if OLD_TREND_CARD in html:
    html = html.replace(OLD_TREND_CARD, '    <!-- Compliance Trend merged into Outlet Type chart below -->', 1)
    fixes += 1
    print("FIX 6: Trend chart card removed (merged into outlet chart)")
else:
    print("WARN FIX 6: Trend card not found — may have different text")

# Make outlet chart full-width (add chart-wide class)
html = html.replace(
    '<div class="chart-card fade-in" style="animation-delay:.1s">\n      <div class="chart-header">\n        <div>\n          <div class="chart-title">Compliance by Outlet Type</div>',
    '<div class="chart-card chart-wide fade-in" style="animation-delay:.1s">\n      <div class="chart-header">\n        <div>\n          <div class="chart-title">Compliance &amp; Trend by Outlet Type</div>'
)
# Update subtitle
html = html.replace(
    '<div class="chart-subtitle">Monthly compliance % per outlet type + overall total</div>',
    '<div class="chart-subtitle">Monthly compliance % per outlet type — bars by type, line = overall trend + audit count</div>'
)
fixes += 1
print("FIX 6b: Outlet chart made full-width with updated title")

# ══════════════════════════════════════════════════════════════════
# FIX 7 — Update buildOutletChart to include Audit Count line
#           (merging the old trend chart's audit count into outlet chart)
# ══════════════════════════════════════════════════════════════════
OLD_OUTLET_CHART_END = """  charts['c-outlet'] = new Chart(ctx('c-outlet'), {
    type: 'bar',
    data: { labels: months, datasets },
    options: {
      ...CHART_OPT,
      scales: {
        x: { grid:{color:'rgba(255,255,255,0.05)'}, ticks:{color:'#94a3b8'} },
        y: {
          min:0, max:100,
          grid:{color:'rgba(255,255,255,0.05)'},
          ticks:{color:'#94a3b8', callback:v=>v+'%'}
        }
      },
      plugins: {
        legend:{
          display: true,
          labels:{ color:'#94a3b8', boxWidth:12, padding:14, font:{size:11} }
        },
        tooltip:{
          callbacks:{
            label: c => ' ' + c.dataset.label + ': ' + (c.parsed.y != null ? c.parsed.y.toFixed(1)+'%' : 'N/A')
          }
        }
      }
    }
  });
}"""

NEW_OUTLET_CHART_END = """  // Overall line + audit count line (replaces the old Trend by Round chart)
  const overallData = months.map(m => {
    const sub = data.filter(r => r.month === m);
    return sub.length ? +(avgScore(sub)*100).toFixed(1) : null;
  });
  const auditCounts = months.map(m => data.filter(r => r.month === m).length);

  datasets.push({
    label: 'Overall %',
    type: 'line',
    data: overallData,
    borderColor: '#ffffff',
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderWidth: 2.5,
    pointBackgroundColor: '#ffffff',
    pointRadius: 5,
    pointHoverRadius: 7,
    fill: false,
    tension: 0.35,
    yAxisID: 'y',
    datalabels: {
      display: true, anchor:'end', align:'top',
      color:'#fff', font:{size:10, weight:'700'},
      formatter: v => v != null ? v+'%' : ''
    }
  });

  datasets.push({
    label: 'Audit Count',
    type: 'line',
    data: auditCounts,
    borderColor: '#f5c518',
    backgroundColor: 'rgba(245,197,24,0.1)',
    borderWidth: 2,
    borderDash: [5, 4],
    pointBackgroundColor: '#f5c518',
    pointRadius: 4,
    pointHoverRadius: 6,
    fill: false,
    tension: 0.35,
    yAxisID: 'y2',
    datalabels: { display: false }
  });

  charts['c-outlet'] = new Chart(ctx('c-outlet'), {
    type: 'bar',
    data: { labels: months, datasets },
    options: {
      ...CHART_OPT,
      scales: {
        x: { grid:{color:'rgba(255,255,255,0.05)'}, ticks:{color:'#94a3b8'} },
        y: {
          min:0, max:100, position:'left',
          grid:{color:'rgba(255,255,255,0.05)'},
          ticks:{color:'#94a3b8', callback:v=>v+'%'}
        },
        y2: {
          position:'right',
          grid:{display:false},
          ticks:{color:'#f5c518'},
          title:{display:true, text:'Audit Count', color:'#f5c518', font:{size:10}}
        }
      },
      plugins: {
        legend:{
          display: true,
          labels:{ color:'#94a3b8', boxWidth:12, padding:14, font:{size:11} }
        },
        tooltip:{
          callbacks:{
            label: c => {
              if (c.dataset.yAxisID === 'y2') return ' Audit Count: ' + c.parsed.y.toLocaleString();
              return ' ' + c.dataset.label + ': ' + (c.parsed.y != null ? c.parsed.y.toFixed(1)+'%' : 'N/A');
            }
          }
        }
      }
    }
  });
}"""

if OLD_OUTLET_CHART_END in html:
    html = html.replace(OLD_OUTLET_CHART_END, NEW_OUTLET_CHART_END, 1)
    fixes += 1
    print("FIX 7: buildOutletChart updated with Overall line + Audit Count")
else:
    print("WARN FIX 7: Old outlet chart end not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes}")
print(f"File lines: {len(html.splitlines())}")
