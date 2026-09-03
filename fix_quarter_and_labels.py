import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ══════════════════════════════════════════════════════════════════
# 1. REMOVE Quarter filter group from main Overview filter bar
# ══════════════════════════════════════════════════════════════════
OLD_Q_FILTER_GROUP = '''    <div class="filter-group" style="gap:4px;flex-direction:column">
      <label style="font-size:11px;margin-bottom:4px">Quarter</label>
      <div style="display:flex;gap:4px">
        <button class="chart-tab-btn active" data-q-filter="all">All</button>
        <button class="chart-tab-btn" data-q-filter="Q1">Q1</button>
        <button class="chart-tab-btn" data-q-filter="Q2">Q2</button>
        <button class="chart-tab-btn" data-q-filter="Q3">Q3</button>
        <button class="chart-tab-btn" data-q-filter="Q4">Q4</button>
      </div>
    </div>
    <button id="btn-reset">↺ Reset</button>
  </div>'''

NEW_BTN_RESET = '''    <button id="btn-reset">↺ Reset</button>
  </div>'''

if OLD_Q_FILTER_GROUP in html:
    html = html.replace(OLD_Q_FILTER_GROUP, NEW_BTN_RESET, 1)
    fixes += 1
    print("HTML: Quarter pills removed from main filter bar")
else:
    print("WARN: Quarter filter group not found in filter bar")

# ══════════════════════════════════════════════════════════════════
# 2. REPLACE Q-tab buttons inside Quarterly panel with a SELECT
# ══════════════════════════════════════════════════════════════════
OLD_Q_TABS_HTML = '''    <!-- Q1 / Q2 / Q3 / Q4 filter tabs -->
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:24px;flex-wrap:wrap">
      <span style="color:var(--muted);font-size:13px;font-weight:600;margin-right:4px">Filter by Quarter:</span>
      <button class="chart-tab-btn active" data-q-tab="all"  style="min-width:90px">All</button>
      <button class="chart-tab-btn"        data-q-tab="Q1"   style="min-width:70px">Q1</button>
      <button class="chart-tab-btn"        data-q-tab="Q2"   style="min-width:70px">Q2</button>
      <button class="chart-tab-btn"        data-q-tab="Q3"   style="min-width:70px">Q3</button>
      <button class="chart-tab-btn"        data-q-tab="Q4"   style="min-width:70px">Q4</button>
      <span id="q-filter-label" style="margin-left:auto;color:var(--muted);font-size:12px"></span>
    </div>'''

NEW_Q_SELECT_HTML = '''    <!-- Quarter SELECT filter -->
    <div class="filters-bar fade-in" style="margin-bottom:24px;padding:12px 16px">
      <div class="filter-group">
        <label for="q-select">Quarter</label>
        <select id="q-select">
          <option value="all">All Quarters</option>
          <option value="Q1">Q1</option>
          <option value="Q2">Q2</option>
          <option value="Q3">Q3</option>
          <option value="Q4">Q4</option>
        </select>
      </div>
      <span id="q-filter-label" style="color:var(--muted);font-size:12px;margin-left:8px;align-self:flex-end;padding-bottom:6px"></span>
    </div>'''

if OLD_Q_TABS_HTML in html:
    html = html.replace(OLD_Q_TABS_HTML, NEW_Q_SELECT_HTML, 1)
    fixes += 1
    print("HTML: Quarter tab buttons → SELECT dropdown in Quarterly panel")
else:
    print("WARN: Q tab buttons not found in quarterly panel")

# ══════════════════════════════════════════════════════════════════
# 3. REPLACE [data-q-tab] JS listeners with #q-select onChange
#    Also REMOVE globalQFilter from applyFilters (no longer needed)
# ══════════════════════════════════════════════════════════════════
OLD_Q_TAB_LISTENERS = """// ── Q1/Q2/Q3/Q4 sub-tab filter buttons ──────────────────────────────────────
document.querySelectorAll('[data-q-tab]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-q-tab]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeQFilter = btn.dataset.qTab;
    buildQuarterTab(ALL_DATA, activeQFilter);
    quarterBuilt = true;
  });
});"""

NEW_Q_SELECT_LISTENER = """// ── Quarter SELECT inside Quarterly tab ─────────────────────────────────────
document.getElementById('q-select')?.addEventListener('change', function() {
  activeQFilter = this.value;
  buildQuarterTab(ALL_DATA, activeQFilter);
  quarterBuilt = true;
});"""

if OLD_Q_TAB_LISTENERS in html:
    html = html.replace(OLD_Q_TAB_LISTENERS, NEW_Q_SELECT_LISTENER, 1)
    fixes += 1
    print("JS: q-tab listeners → q-select onChange")
else:
    print("WARN: Q tab listeners not found")

# ══════════════════════════════════════════════════════════════════
# 4. REMOVE globalQFilter from applyFilters
# ══════════════════════════════════════════════════════════════════
OLD_GLOBAL_Q = """    if (globalQFilter !== 'all') {
      const rq = MONTH_TO_Q[r.month] || 'Unknown';
      if (rq !== globalQFilter) return false;
    }
    return true;"""

NEW_NO_Q = "    return true;"

if OLD_GLOBAL_Q in html:
    html = html.replace(OLD_GLOBAL_Q, NEW_NO_Q, 1)
    fixes += 1
    print("JS: globalQFilter removed from applyFilters")

# Also remove globalQFilter variable and q-filter event listener
OLD_GQVAR = "let globalQFilter = 'all';\n\n"
html = html.replace(OLD_GQVAR, '', 1)

OLD_GQLISTENER = """// ── Global Quarter pill filter (in main filter bar) ──────────────────────────
document.querySelectorAll('[data-q-filter]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-q-filter]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    globalQFilter = btn.dataset.qFilter;
    render();
    // Also rebuild quarterly tab if already built
    if (quarterBuilt) {
      buildQuarterTab(applyFilters(ALL_DATA), activeQFilter);
    }
  });
});"""
if OLD_GQLISTENER in html:
    html = html.replace(OLD_GQLISTENER, '', 1)
    print("JS: global q-filter listener removed")

# Fix Reset to not reference globalQFilter anymore
OLD_RESET_Q = """  globalQFilter = 'all';
  document.querySelectorAll('[data-q-filter]').forEach(b => b.classList.toggle('active', b.dataset.qFilter === 'all'));
  render();"""
NEW_RESET_Q = "  render();"
if OLD_RESET_Q in html:
    html = html.replace(OLD_RESET_Q, NEW_RESET_Q, 1)
    print("JS: Reset cleaned up")

# ══════════════════════════════════════════════════════════════════
# 5. ADD datalabels to buildKPICombo bar dataset (Deep Dive charts)
# ══════════════════════════════════════════════════════════════════
OLD_KPI_BAR = """    label:'Avg Compliance %', data:avgs,
    backgroundColor:colorBar+'88', borderColor:colorBar,
    borderWidth:2, borderRadius:8, yAxisID:'y',"""

NEW_KPI_BAR = """    label:'Avg Compliance %', data:avgs,
    backgroundColor:colorBar+'88', borderColor:colorBar,
    borderWidth:2, borderRadius:8, yAxisID:'y',
    datalabels: {
      display: true, anchor:'end', align:'top',
      color:'#cbd5e1', font:{size:11,weight:'600'},
      formatter: v => v+'%'
    },"""

if OLD_KPI_BAR in html:
    html = html.replace(OLD_KPI_BAR, NEW_KPI_BAR, 1)
    fixes += 1
    print("JS: datalabels added to buildKPICombo bars (Deep Dive)")
else:
    print("WARN: buildKPICombo bar dataset not found")

# ══════════════════════════════════════════════════════════════════
# 6. UPDATE q-select label update in buildQuarterTab
# ══════════════════════════════════════════════════════════════════
# The label update already references 'q-filter-label' which still exists in HTML
# Also sync the select dropdown value when tab is opened
OLD_Q_WIRE = """document.getElementById('btn-tab-quarter')?.addEventListener('click', () => {
  if (!quarterBuilt) {
    buildQuarterTab(ALL_DATA, activeQFilter);
    quarterBuilt = true;
  }
});"""

NEW_Q_WIRE = """document.getElementById('btn-tab-quarter')?.addEventListener('click', () => {
  if (!quarterBuilt) {
    buildQuarterTab(ALL_DATA, activeQFilter);
    quarterBuilt = true;
  }
  // Sync select to activeQFilter
  const qs = document.getElementById('q-select');
  if (qs) qs.value = activeQFilter;
});"""

if OLD_Q_WIRE in html:
    html = html.replace(OLD_Q_WIRE, NEW_Q_WIRE, 1)
    fixes += 1
    print("JS: q-select synced on tab open")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes} — Done.")
