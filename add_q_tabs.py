with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ── 1. ADD Q-FILTER SUB-TABS to Quarter panel HTML ────────────────────────────
OLD_QH = '''<div class="tab-panel" id="tab-quarter">
  <div style="max-width:1600px;margin:0 auto;padding:20px 24px 40px">
    <div class="section-label">Quarterly Performance</div>
    <div class="kpi-grid" id="quarter-kpi-row"></div>'''

NEW_QH = '''<div class="tab-panel" id="tab-quarter">
  <div style="max-width:1600px;margin:0 auto;padding:20px 24px 40px">

    <!-- Q1 / Q2 / Q3 / Q4 filter tabs -->
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:24px;flex-wrap:wrap">
      <span style="color:var(--muted);font-size:13px;font-weight:600;margin-right:4px">Filter by Quarter:</span>
      <button class="chart-tab-btn active" data-q-tab="all"  style="min-width:90px">All</button>
      <button class="chart-tab-btn"        data-q-tab="Q1"   style="min-width:70px">Q1</button>
      <button class="chart-tab-btn"        data-q-tab="Q2"   style="min-width:70px">Q2</button>
      <button class="chart-tab-btn"        data-q-tab="Q3"   style="min-width:70px">Q3</button>
      <button class="chart-tab-btn"        data-q-tab="Q4"   style="min-width:70px">Q4</button>
      <span id="q-filter-label" style="margin-left:auto;color:var(--muted);font-size:12px"></span>
    </div>

    <div class="section-label">Quarterly Performance</div>
    <div class="kpi-grid" id="quarter-kpi-row"></div>'''

if OLD_QH in html:
    html = html.replace(OLD_QH, NEW_QH)
    fixes += 1
    print("HTML: Q filter tabs added")
else:
    print("WARN: Quarter HTML target not found")

# ── 2. REPLACE buildQuarterTab to accept qFilter param ────────────────────────
OLD_FN_SIG = "function buildQuarterTab(data) {"
NEW_FN_SIG = "function buildQuarterTab(data, qFilter) {"

html = html.replace(OLD_FN_SIG, NEW_FN_SIG, 1)

# ── 3. ADD qFilter logic at top of function body (after opening brace) ─────────
OLD_BODY_START = """function buildQuarterTab(data, qFilter) {
  // Group data by quarter-year
  const quarters = {};
  data.forEach(r => {"""

NEW_BODY_START = """function buildQuarterTab(data, qFilter) {
  if (!qFilter) qFilter = 'all';

  // If a specific quarter selected, filter data to that quarter only
  const filtered = (qFilter === 'all')
    ? data
    : data.filter(r => (MONTH_TO_Q[r.month] || 'Unknown') === qFilter);

  // Update label
  const lbl = document.getElementById('q-filter-label');
  if (lbl) lbl.textContent = qFilter === 'all'
    ? filtered.length.toLocaleString() + ' total audits'
    : filtered.length.toLocaleString() + ' audits in ' + qFilter;

  // Replace data reference for all subsequent logic
  data = filtered;

  // Group data by quarter-year
  const quarters = {};
  data.forEach(r => {"""

if OLD_BODY_START in html:
    html = html.replace(OLD_BODY_START, NEW_BODY_START, 1)
    fixes += 1
    print("JS: qFilter logic added to buildQuarterTab")
else:
    print("WARN: buildQuarterTab body start not found")

# ── 4. UPDATE the quarter tab click wiring to support sub-tabs ─────────────────
OLD_WIRE = """// Wire up Quarter tab – build when first visited
let quarterBuilt = false;
document.getElementById('btn-tab-quarter')?.addEventListener('click', () => {
  if (!quarterBuilt) {
    buildQuarterTab(ALL_DATA);
    quarterBuilt = true;
  }
});"""

NEW_WIRE = """// ── Quarter main tab: build on first visit ──────────────────────────────────
let quarterBuilt   = false;
let activeQFilter  = 'all';

document.getElementById('btn-tab-quarter')?.addEventListener('click', () => {
  if (!quarterBuilt) {
    buildQuarterTab(ALL_DATA, activeQFilter);
    quarterBuilt = true;
  }
});

// ── Q1/Q2/Q3/Q4 sub-tab filter buttons ──────────────────────────────────────
document.querySelectorAll('[data-q-tab]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-q-tab]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeQFilter = btn.dataset.qTab;
    buildQuarterTab(ALL_DATA, activeQFilter);
    quarterBuilt = true;
  });
});"""

if OLD_WIRE in html:
    html = html.replace(OLD_WIRE, NEW_WIRE, 1)
    fixes += 1
    print("JS: Q sub-tab event listeners wired")
else:
    print("WARN: Quarter wire code not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes}  — Done.")
