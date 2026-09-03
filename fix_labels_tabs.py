with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ── 1. Add datalabels plugin CDN after Chart.js ───────────────────────────────
OLD_CDN = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>'
NEW_CDN = '''<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>'''
html = html.replace(OLD_CDN, NEW_CDN, 1)
fixes += 1
print("CDN: datalabels plugin added")

# ── 2. Register plugin + set global defaults right after <script> main block start
# Find where the main script starts (after the CDN scripts)
OLD_SCRIPT_START = "const ALL_DATA_KEYS = null;"
NEW_SCRIPT_START = """Chart.register(ChartDataLabels);
// Global defaults: datalabels OFF everywhere unless explicitly enabled per dataset
Chart.defaults.set('plugins.datalabels', { display: false });

const ALL_DATA_KEYS = null;"""
if OLD_SCRIPT_START in html:
    html = html.replace(OLD_SCRIPT_START, NEW_SCRIPT_START, 1)
    fixes += 1
    print("JS: ChartDataLabels registered globally, default OFF")
else:
    print("WARN: script start anchor not found")

# ── 3. Change q-pill → chart-tab-btn in HTML ─────────────────────────────────
html = html.replace('class="q-pill active"', 'class="chart-tab-btn active"')
html = html.replace('class="q-pill"', 'class="chart-tab-btn"')
fixes += 1
print("HTML: q-pill → chart-tab-btn")

# ── 4. Remove q-pill CSS (no longer needed, using chart-tab-btn) ──────────────
import re
html = re.sub(r'\.q-pill \{.*?\}\.q-pill:hover \{.*?\}\.q-pill\.active \{.*?\}', '', html, flags=re.DOTALL)
# Also remove via explicit block
old_qpill_css = '''.q-pill {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  color: #94a3b8;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: all .2s;
  white-space: nowrap;
}
.q-pill:hover { border-color: rgba(232,0,28,.4); color: #e8001c; }
.q-pill.active {
  background: rgba(232,0,28,.15);
  border-color: rgba(232,0,28,.6);
  color: #e8001c;
}
'''
if old_qpill_css in html:
    html = html.replace(old_qpill_css, '')
    print("CSS: q-pill styles removed")
    fixes += 1

# ── 5. Add datalabels to buildRegionChart bars ────────────────────────────────
OLD_REGION_DS = """          data: regionScores,
          backgroundColor: barColors.map(c=>c+'bb'),
          borderColor: barColors,
          borderWidth:2, borderRadius:6,
          yAxisID:'yLeft', order:2"""
NEW_REGION_DS = """          data: regionScores,
          backgroundColor: barColors.map(c=>c+'bb'),
          borderColor: barColors,
          borderWidth:2, borderRadius:6,
          yAxisID:'yLeft', order:2,
          datalabels: {
            display: true, anchor:'end', align:'top',
            color:'#cbd5e1', font:{size:10,weight:'600'},
            formatter: v => v.toFixed(1)+'%'
          }"""
if OLD_REGION_DS in html:
    html = html.replace(OLD_REGION_DS, NEW_REGION_DS, 1)
    fixes += 1
    print("JS: datalabels added to Region chart bars")
else:
    print("WARN: Region chart dataset not found")

# ── 6. Add datalabels to buildGovernorateChart bars ──────────────────────────
OLD_GOV_DS = """          data: govScores,
          backgroundColor: barColors.map(c=>c+'bb'),
          borderColor: barColors,
          borderWidth:2, borderRadius:6,
          yAxisID:'yLeft', order:2"""
NEW_GOV_DS = """          data: govScores,
          backgroundColor: barColors.map(c=>c+'bb'),
          borderColor: barColors,
          borderWidth:2, borderRadius:6,
          yAxisID:'yLeft', order:2,
          datalabels: {
            display: true, anchor:'end', align:'top',
            color:'#cbd5e1', font:{size:10,weight:'600'},
            formatter: v => v.toFixed(1)+'%'
          }"""
if OLD_GOV_DS in html:
    html = html.replace(OLD_GOV_DS, NEW_GOV_DS, 1)
    fixes += 1
    print("JS: datalabels added to Governorate chart bars")
else:
    print("WARN: Gov chart dataset not found")

# ── 7. Add datalabels to buildOutletChart bars ───────────────────────────────
# Find outlet chart bar dataset
OLD_OUTLET = """          borderRadius:6,
          borderWidth:2"""
# This is too generic, let's find specifically outlet chart
# Let's look for 'buildOutletChart'
idx = html.find('function buildOutletChart')
if idx > 0:
    chunk = html[idx:idx+1500]
    # Find borderRadius:6 in this chunk
    if 'borderRadius:6' in chunk:
        # Replace first occurrence in this chunk
        new_chunk = chunk.replace(
            'borderRadius:6,\n          borderWidth:2',
            'borderRadius:6,\n          borderWidth:2,\n          datalabels: {\n            display: true, anchor:\'end\', align:\'top\',\n            color:\'#cbd5e1\', font:{size:10,weight:\'600\'},\n            formatter: v => Number(v).toFixed(0)\n          }',
            1
        )
        html = html[:idx] + new_chunk + html[idx+1500:]
        fixes += 1
        print("JS: datalabels added to Outlet chart bars")

# ── 8. Add datalabels to KPI Contract chart bars ─────────────────────────────
OLD_CONTRACT_BAR = """          yAxisID: 'yLeft',
          order: 2,
        },"""
NEW_CONTRACT_BAR = """          yAxisID: 'yLeft',
          order: 2,
          datalabels: {
            display: true, anchor:'end', align:'top',
            color:'#cbd5e1', font:{size:10,weight:'600'},
            formatter: v => v+'%'
          },
        },"""
if OLD_CONTRACT_BAR in html:
    html = html.replace(OLD_CONTRACT_BAR, NEW_CONTRACT_BAR, 1)
    fixes += 1
    print("JS: datalabels added to KPI Contract chart bars")
else:
    print("WARN: KPI Contract bar dataset not found")

# ── 9. Add datalabels to Quarter score & incentive charts ─────────────────────
OLD_Q_SCORE = """          borderWidth:2, borderRadius:6
        }]
      },
      options:{
        responsive:true, maintainAspectRatio:false,
        plugins:{legend:{display:false},
          tooltip:{callbacks:{label:ctx=>`${ctx.raw}%`}}},"""
NEW_Q_SCORE = """          borderWidth:2, borderRadius:6,
          datalabels: {
            display: true, anchor:'end', align:'top',
            color:'#cbd5e1', font:{size:11,weight:'600'},
            formatter: v => parseFloat(v).toFixed(1)+'%'
          }
        }]
      },
      options:{
        responsive:true, maintainAspectRatio:false,
        plugins:{legend:{display:false},
          tooltip:{callbacks:{label:ctx=>`${ctx.raw}%`}}},"""
if OLD_Q_SCORE in html:
    html = html.replace(OLD_Q_SCORE, NEW_Q_SCORE, 1)
    fixes += 1
    print("JS: datalabels added to Quarter score chart")
else:
    print("WARN: Quarter score chart dataset not found")

OLD_Q_INC = """          borderWidth:2, borderRadius:6
        }]
      },
      options:{
        responsive:true, maintainAspectRatio:false,
        plugins:{legend:{display:false},
          tooltip:{callbacks:{label:ctx=>`${Number(ctx.raw).toLocaleString()} EGP`}}},"""
NEW_Q_INC = """          borderWidth:2, borderRadius:6,
          datalabels: {
            display: true, anchor:'end', align:'top',
            color:'#f5c518', font:{size:10,weight:'600'},
            formatter: v => Number(v).toLocaleString(undefined,{maximumFractionDigits:0})
          }
        }]
      },
      options:{
        responsive:true, maintainAspectRatio:false,
        plugins:{legend:{display:false},
          tooltip:{callbacks:{label:ctx=>`${Number(ctx.raw).toLocaleString()} EGP`}}},"""
if OLD_Q_INC in html:
    html = html.replace(OLD_Q_INC, NEW_Q_INC, 1)
    fixes += 1
    print("JS: datalabels added to Quarter incentive chart")
else:
    print("WARN: Quarter incentive chart dataset not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes} — Done.")
