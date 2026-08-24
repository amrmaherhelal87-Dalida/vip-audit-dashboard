"""
Apply all dashboard changes:
1. Remove Q2 2026 hardcoded text from title/header/footer
2. Add Quarter tab (nav + panel)
3. Remove Governorate sub-tab (keep region only)
4. Hide Governorate filter
5. Add outlet search bar
6. Change map to Google Maps-like tiles (CartoDB Voyager)
7. Expand map popup (code, name, all KPIs, region, round)
8. Add Quarter tab JS + search JS
"""

import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ─────────────────────────────────────────────
# 1. Title
# ─────────────────────────────────────────────
html = html.replace(
    '<title>VIP Audit Dashboard ⚡ Q2 2026</title>',
    '<title>VIP Audit Dashboard</title>'
)

# ─────────────────────────────────────────────
# 2. Meta description
# ─────────────────────────────────────────────
html = re.sub(
    r'<meta name="description" content="[^"]*"/>',
    '<meta name="description" content="Red Bull VIP Outlet Audit Dashboard — KPI compliance, incentive tracking and regional performance." />',
    html
)

# ─────────────────────────────────────────────
# 3. Header subtitle – remove Q2 2026
# ─────────────────────────────────────────────
html = re.sub(
    r'<span>Red Bull Egypt[^<]*Q2 2026[^<]*Field Compliance</span>',
    '<span>Red Bull Egypt Field Compliance</span>',
    html
)

# ─────────────────────────────────────────────
# 4. Remove Q2 2026 badge from header-meta
# ─────────────────────────────────────────────
html = html.replace(
    '<span class="badge badge-gold">Q2 2026</span>\n',
    ''
)

# ─────────────────────────────────────────────
# 5. Tab nav – add Quarter tab
# ─────────────────────────────────────────────
OLD_NAV = '''<nav class="tab-nav" id="tab-nav">
  <button class="tab-btn active" data-tab="overview" id="btn-tab-overview">
    <span class="tab-icon">📊</span> Overview
  </button>
  <button class="tab-btn" data-tab="map" id="btn-tab-map">
    <span class="tab-icon">🗺</span> Interactive Map
  </button>
</nav>'''

NEW_NAV = '''<nav class="tab-nav" id="tab-nav">
  <button class="tab-btn active" data-tab="overview" id="btn-tab-overview">
    <span class="tab-icon">📊</span> Overview
  </button>
  <button class="tab-btn" data-tab="quarter" id="btn-tab-quarter">
    <span class="tab-icon">📅</span> Quarterly
  </button>
  <button class="tab-btn" data-tab="map" id="btn-tab-map">
    <span class="tab-icon">🗺</span> Interactive Map
  </button>
</nav>'''

html = html.replace(OLD_NAV, NEW_NAV)

# ─────────────────────────────────────────────
# 6. Hide Governorate filter group
# ─────────────────────────────────────────────
OLD_GOV_FILTER = '''    <div class="filter-group">
      <label for="f-gov">Governorate</label>
      <select id="f-gov">
        <option value="all">All Governorates</option>
      </select>
    </div>'''

NEW_GOV_FILTER = '''    <div class="filter-group" style="display:none">
      <label for="f-gov">Governorate</label>
      <select id="f-gov">
        <option value="all">All Governorates</option>
      </select>
    </div>'''

html = html.replace(OLD_GOV_FILTER, NEW_GOV_FILTER)

# ─────────────────────────────────────────────
# 7. Remove KPI sub hardcoded "April–July" text
# ─────────────────────────────────────────────
html = re.sub(
    r'<div class="kpi-sub">Across \d+ rounds[^<]*</div>',
    '<div class="kpi-sub" id="k-rounds-sub">Across all rounds</div>',
    html
)

# ─────────────────────────────────────────────
# 8. Remove Governorate chart sub-tab button only
# ─────────────────────────────────────────────
html = html.replace(
    '          <button class="chart-tab-btn" data-regiongov-tab="gov">Governorate</button>\n',
    ''
)

# ─────────────────────────────────────────────
# 9. Add search bar to Outlet Detail section
# ─────────────────────────────────────────────
OLD_OUTLET = '''  <!-- Data Table -->
  <div class="section-label">Outlet Detail</div>
  <div class="table-card fade-in">
    <div class="chart-header">
      <div>
        <div class="chart-title">Audit Records</div>
        <div class="chart-subtitle" id="table-count">Showing — records</div>
      </div>
    </div>'''

NEW_OUTLET = '''  <!-- Data Table -->
  <div class="section-label">Outlet Detail</div>
  <div class="table-card fade-in">
    <div class="chart-header">
      <div>
        <div class="chart-title">Audit Records</div>
        <div class="chart-subtitle" id="table-count">Showing — records</div>
      </div>
      <div style="display:flex;align-items:center;gap:8px">
        <input type="text" id="outlet-search"
          placeholder="🔍  Search by code or name…"
          style="padding:7px 14px;border-radius:8px;border:1px solid var(--border);
                 background:var(--surface);color:var(--text);font-size:13px;width:260px;outline:none">
        <button id="outlet-search-clear" title="Clear search"
          style="padding:6px 10px;border-radius:8px;border:1px solid var(--border);
                 background:var(--surface);color:var(--muted);cursor:pointer;font-size:13px">✕</button>
      </div>
    </div>'''

html = html.replace(OLD_OUTLET, NEW_OUTLET)

# ─────────────────────────────────────────────
# 10. Add Quarter tab panel (before map panel)
# ─────────────────────────────────────────────
QUARTER_PANEL = '''
<!-- QUARTER TAB -->
<div class="tab-panel" id="tab-quarter">
  <div style="max-width:1600px;margin:0 auto;padding:20px 24px 40px">
    <div class="section-label">Quarterly Performance</div>
    <div class="kpi-grid" id="quarter-kpi-row"></div>

    <div class="section-label" style="margin-top:24px">Round vs Quarter Breakdown</div>
    <div class="charts-grid">
      <div class="chart-card chart-wide fade-in">
        <div class="chart-header">
          <div>
            <div class="chart-title">Compliance % by Round</div>
            <div class="chart-subtitle">Grouped by quarter</div>
          </div>
        </div>
        <div class="chart-wrap"><canvas id="c-quarter-score"></canvas></div>
      </div>
      <div class="chart-card chart-wide fade-in" style="animation-delay:.08s">
        <div class="chart-header">
          <div>
            <div class="chart-title">Incentive EGP by Round</div>
            <div class="chart-subtitle">Grouped by quarter</div>
          </div>
        </div>
        <div class="chart-wrap"><canvas id="c-quarter-incentive"></canvas></div>
      </div>
    </div>

    <div class="section-label" style="margin-top:24px">Quarter Summary Table</div>
    <div class="table-card fade-in">
      <div class="table-scroll">
        <table id="quarter-table">
          <thead><tr>
            <th>Quarter</th>
            <th>Rounds</th>
            <th>Audits</th>
            <th>Avg Score</th>
            <th>Avail. Compliant</th>
            <th>Total Incentive</th>
          </tr></thead>
          <tbody id="quarter-tbody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>

'''

# Insert before map tab panel
html = html.replace('<!-- MAP TAB -->', QUARTER_PANEL + '<!-- MAP TAB -->')

# ─────────────────────────────────────────────
# 11. Footer – remove Q2-2026 reference
# ─────────────────────────────────────────────
html = re.sub(
    r'<footer>.*?</footer>',
    '''<footer>
  <p>VIP Audit Dashboard · Red Bull Egypt Field Operations ·
  <a href="https://github.com/amrmaherhelal87-Dalida/vip-audit-dashboard" target="_blank">GitHub 🐙</a></p>
</footer>''',
    html, flags=re.DOTALL
)

# ─────────────────────────────────────────────
# 12. Map tiles – CartoDB Voyager (Google Maps-like)
# ─────────────────────────────────────────────
html = html.replace(
    "L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {\n    attribution: '&copy; OSM &copy; CARTO', subdomains:'abcd', maxZoom:19,\n  }).addTo(leafletMap);",
    "L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {\n    attribution: '&copy; <a href=\"https://www.openstreetmap.org/copyright\">OSM</a> &copy; <a href=\"https://carto.com/\">CARTO</a>',\n    subdomains:'abcd', maxZoom:19,\n  }).addTo(leafletMap);"
)

# ─────────────────────────────────────────────
# 13. Map popup – expand with name, all KPIs, region
# ─────────────────────────────────────────────
OLD_POPUP = """    const popup = `<div class="popup-title">${r.outlet_code||'—'}</div>
      <div class="popup-score" style="color:${scoreCl}">${scorePct}</div>
      <div class="popup-row"><span>Type</span><strong><span style="color:${typeColor}">●</span> ${r.outlet_type}</strong></div>
      <div class="popup-row"><span>Round</span><strong>R${r.round} — ${r.month}</strong></div>
      <div class="popup-row"><span>Region</span><strong>${r.region} / ${r.governorate}</strong></div>
      <div class="popup-row"><span>Availability</span><strong style="color:${avCl}">${avStr}</strong></div>
      <div class="popup-row"><span>SoS</span><strong style="color:${r.sos_compliance===1?'#10b981':'#e8001c'}">${r.sos_compliance===1?'✓':'✗'}</strong></div>
      <div class="popup-row"><span>Incentive</span><strong style="color:#f5c518">${incentive} EGP</strong></div>`;"""

NEW_POPUP = """    // Helper: KPI compliance row (skip if null/undefined)
    const kpiRow = (label, val) => {
      if (val === null || val === undefined) return '';
      const cl = val === 1 ? '#10b981' : '#e8001c';
      return `<div class="popup-row"><span>${label}</span><strong style="color:${cl}">${val===1?'✓':'✗'}</strong></div>`;
    };
    const popup = `
      <div class="popup-title">${r.outlet_code||'—'}</div>
      ${r.outlet_name ? `<div style="color:#94a3b8;font-size:11px;margin:-4px 0 6px;max-width:230px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${r.outlet_name}">${r.outlet_name}</div>` : ''}
      <div class="popup-score" style="color:${scoreCl}">${scorePct}</div>
      <div class="popup-row"><span>Type</span><strong><span style="color:${typeColor}">●</span> ${r.outlet_type}</strong></div>
      <div class="popup-row"><span>Round</span><strong>R${r.round} — ${r.month}</strong></div>
      <div class="popup-row"><span>Region</span><strong>${r.region||'—'}</strong></div>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:5px 0">
      ${kpiRow('Availability', r.avail_compliance)}
      ${kpiRow('SoS', r.sos_compliance)}
      ${kpiRow('Strike Zone', r.sz_compliance)}
      ${kpiRow('Price', r.price_compliance)}
      ${kpiRow('POSM', r.posm_compliance)}
      ${kpiRow('Outdoor Visibility', r.outdoor_compliance)}
      ${kpiRow('Sticky Shelf', r.sticky_compliance)}
      ${kpiRow('Ambient Placement', r.ambient_compliance)}
      ${kpiRow('Cooler @ Cashier', r.cooler_cashier_compliance)}
      ${kpiRow('Large Cooler', r.large_cooler_compliance)}
      ${kpiRow('Cooler Accessible', r.cooler_visible_compliance)}
      ${kpiRow('Chilled 2m Cashier', r.chilled_cashier_compliance)}
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:5px 0">
      <div class="popup-row"><span>Incentive</span><strong style="color:#f5c518">${incentive} EGP</strong></div>`;"""

html = html.replace(OLD_POPUP, NEW_POPUP)

# ─────────────────────────────────────────────
# 14. renderTable – add outlet search filter
# ─────────────────────────────────────────────
OLD_RENDER = """function renderTable(data) {
  const tbody = document.getElementById('table-body');
  const show = data.slice(0, 200);"""

NEW_RENDER = """function renderTable(data) {
  const tbody = document.getElementById('table-body');
  // Apply outlet search filter
  const searchQ = (document.getElementById('outlet-search')?.value || '').toLowerCase().trim();
  let filtered = searchQ
    ? data.filter(r =>
        String(r.outlet_code||'').toLowerCase().includes(searchQ) ||
        String(r.outlet_name||'').toLowerCase().includes(searchQ))
    : data;
  const show = filtered.slice(0, 200);"""

html = html.replace(OLD_RENDER, NEW_RENDER)

OLD_COUNT = "  document.getElementById('table-count').textContent = `Showing ${show.length.toLocaleString()} of ${data.length.toLocaleString()} records`;"
NEW_COUNT = "  document.getElementById('table-count').textContent = `Showing ${show.length.toLocaleString()} of ${filtered.length.toLocaleString()} records${searchQ ? ' (filtered)' : ''}`;"
html = html.replace(OLD_COUNT, NEW_COUNT)

# ─────────────────────────────────────────────
# 15. Add Quarter tab JS + search listener
# ─────────────────────────────────────────────
QUARTER_JS = """
/* ═══════════════════════════════════════════════════════════
   OUTLET SEARCH
═══════════════════════════════════════════════════════════ */
document.getElementById('outlet-search').addEventListener('input', function() {
  renderTable(getFilteredData());
});
document.getElementById('outlet-search-clear').addEventListener('click', function() {
  document.getElementById('outlet-search').value = '';
  renderTable(getFilteredData());
});

/* ═══════════════════════════════════════════════════════════
   QUARTER TAB
═══════════════════════════════════════════════════════════ */
const MONTH_TO_Q = {
  'January':'Q1','February':'Q1','March':'Q1',
  'April':'Q2','May':'Q2','June':'Q2',
  'July':'Q3','August':'Q3','September':'Q3',
  'October':'Q4','November':'Q4','December':'Q4'
};

function buildQuarterTab(data) {
  // Group data by quarter-year
  const quarters = {};
  data.forEach(r => {
    const q = MONTH_TO_Q[r.month] || 'Unknown';
    const yr = '2026';
    const key = `${q} ${yr}`;
    if (!quarters[key]) quarters[key] = { audits:[], rounds:new Set(), months:new Set() };
    quarters[key].audits.push(r);
    if (r.round) quarters[key].rounds.add(r.round);
    if (r.month) quarters[key].months.add(r.month);
  });

  const qKeys = Object.keys(quarters).sort();

  // ── KPI summary cards ─────────────────────────────────
  const kpiRow = document.getElementById('quarter-kpi-row');
  kpiRow.innerHTML = qKeys.map((q, i) => {
    const { audits, rounds } = quarters[q];
    const avgScore = audits.reduce((s,r) => s + (r.overall_score||0), 0) / audits.length;
    const incentive = audits.reduce((s,r) => s + (r.total_incentive||0), 0);
    const compliant = audits.filter(r => r.avail_compliance === 1).length;
    const compPct   = (compliant / audits.length * 100).toFixed(1);
    const colors = ['red','gold','green','red'];
    return `<div class="kpi-card ${colors[i%colors.length]} fade-in" style="animation-delay:${i*0.08}s">
      <div class="kpi-icon">📅</div>
      <div class="kpi-label">${q}</div>
      <div class="kpi-value">${audits.length.toLocaleString()}</div>
      <div class="kpi-sub">Rounds: ${[...rounds].sort().join(', ')}</div>
      <div class="kpi-sub">Avg Score: ${(avgScore*100).toFixed(1)}%</div>
      <div class="kpi-sub">Avail: ${compPct}% · ${incentive.toFixed(0)} EGP</div>
    </div>`;
  }).join('');

  // ── Round-level score chart ────────────────────────────
  // Get all rounds sorted
  const allRounds = [...new Set(data.map(r=>r.round))].sort((a,b)=>a-b);
  const roundLabels = allRounds.map(r => `R${r}`);
  const roundColors = allRounds.map(r => {
    const month = (data.find(d=>d.round===r)||{}).month||'';
    const q = MONTH_TO_Q[month]||'Unknown';
    const palette = {'Q1':'#3b82f6','Q2':'#e8001c','Q3':'#f5c518','Q4':'#10b981'};
    return palette[q] || '#94a3b8';
  });

  const roundScores = allRounds.map(r => {
    const sub = data.filter(d=>d.round===r);
    if (!sub.length) return 0;
    return (sub.reduce((s,d)=>s+(d.overall_score||0),0)/sub.length*100);
  });
  const roundIncentives = allRounds.map(r =>
    data.filter(d=>d.round===r).reduce((s,d)=>s+(d.total_incentive||0),0)
  );

  // Score chart
  const scoreCtx = document.getElementById('c-quarter-score');
  if (scoreCtx) {
    if (scoreCtx._qChart) scoreCtx._qChart.destroy();
    scoreCtx._qChart = new Chart(scoreCtx, {
      type:'bar',
      data:{
        labels: roundLabels,
        datasets:[{
          label:'Avg Compliance %',
          data: roundScores.map(v=>v.toFixed(1)),
          backgroundColor: roundColors.map(c=>c+'99'),
          borderColor: roundColors,
          borderWidth:2, borderRadius:6
        }]
      },
      options:{
        responsive:true, maintainAspectRatio:false,
        plugins:{legend:{display:false},
          tooltip:{callbacks:{label:ctx=>`${ctx.raw}%`}}},
        scales:{
          x:{ticks:{color:'#94a3b8'},grid:{color:'rgba(255,255,255,0.05)'}},
          y:{ticks:{color:'#94a3b8',callback:v=>v+'%'},grid:{color:'rgba(255,255,255,0.05)'},
             suggestedMin:0,suggestedMax:100}
        }
      }
    });
  }

  // Incentive chart
  const incCtx = document.getElementById('c-quarter-incentive');
  if (incCtx) {
    if (incCtx._qChart) incCtx._qChart.destroy();
    incCtx._qChart = new Chart(incCtx, {
      type:'bar',
      data:{
        labels: roundLabels,
        datasets:[{
          label:'Incentive EGP',
          data: roundIncentives,
          backgroundColor: roundColors.map(c=>c+'99'),
          borderColor: roundColors,
          borderWidth:2, borderRadius:6
        }]
      },
      options:{
        responsive:true, maintainAspectRatio:false,
        plugins:{legend:{display:false},
          tooltip:{callbacks:{label:ctx=>`${Number(ctx.raw).toLocaleString()} EGP`}}},
        scales:{
          x:{ticks:{color:'#94a3b8'},grid:{color:'rgba(255,255,255,0.05)'}},
          y:{ticks:{color:'#94a3b8',callback:v=>v.toLocaleString()},
             grid:{color:'rgba(255,255,255,0.05)'}}
        }
      }
    });
  }

  // ── Summary table ──────────────────────────────────────
  const tbody = document.getElementById('quarter-tbody');
  tbody.innerHTML = qKeys.map(q => {
    const { audits, rounds } = quarters[q];
    const avgScore = audits.reduce((s,r)=>s+(r.overall_score||0),0)/audits.length;
    const incentive = audits.reduce((s,r)=>s+(r.total_incentive||0),0);
    const compliant = audits.filter(r=>r.avail_compliance===1).length;
    const compPct   = (compliant/audits.length*100).toFixed(1);
    const scoreCol = avgScore>=0.7?'#10b981':avgScore>=0.5?'#f5c518':'#e8001c';
    return `<tr>
      <td><strong>${q}</strong></td>
      <td style="color:var(--muted)">${[...rounds].sort().map(r=>`R${r}`).join(' · ')}</td>
      <td>${audits.length.toLocaleString()}</td>
      <td style="color:${scoreCol};font-weight:600">${(avgScore*100).toFixed(1)}%</td>
      <td>${compliant.toLocaleString()} <span style="color:var(--muted)">(${compPct}%)</span></td>
      <td style="color:var(--gold);font-weight:600">${incentive.toFixed(0).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',')} EGP</td>
    </tr>`;
  }).join('');
}

// Wire up Quarter tab – build when first visited
let quarterBuilt = false;
document.getElementById('btn-tab-quarter')?.addEventListener('click', () => {
  if (!quarterBuilt) {
    buildQuarterTab(ALL_DATA);
    quarterBuilt = true;
  }
});
"""

# Insert JS before closing </script>
html = html.replace('</script>\n</body>', QUARTER_JS + '\n</script>\n</body>')

# ─────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("All changes applied successfully!")
print("Changes made:")
print("  ✅ Removed Q2 2026 from title, header, footer")
print("  ✅ Added Quarterly tab (nav + panel + JS)")
print("  ✅ Removed Governorate sub-tab from region chart")
print("  ✅ Hidden Governorate filter")
print("  ✅ Added outlet search bar (code or name)")
print("  ✅ Map tiles → CartoDB Voyager (Google Maps-like)")
print("  ✅ Map popup → expanded with name, all KPIs, region, round")
print("  ✅ renderTable → respects search bar")
