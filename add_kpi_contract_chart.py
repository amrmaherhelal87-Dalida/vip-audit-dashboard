with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ── 1. INSERT HTML: new chart section before "<!-- Charts Row 2 -->" ──────────
NEW_SECTION = '''
  <!-- KPI Compliance by Contract Type -->
  <div class="section-label" style="margin-top:8px">KPI Compliance by Contract Type</div>
  <div class="chart-card chart-wide fade-in" style="animation-delay:.18s">
    <div class="chart-header">
      <div>
        <div class="chart-title" id="kpi-contract-title">Impulse &amp; Grocery — KPI Compliance</div>
        <div class="chart-subtitle" id="kpi-contract-subtitle">Compliance % and total incentive EGP per KPI for this contract type</div>
      </div>
      <div class="chart-tabs">
        <button class="chart-tab-btn active" data-contract-tab="Impulse &amp; Grocery">Impulse &amp; Grocery</button>
        <button class="chart-tab-btn" data-contract-tab="Supermarket">Supermarket</button>
        <button class="chart-tab-btn" data-contract-tab="Gas Station">Gas Station</button>
        <button class="chart-tab-btn" data-contract-tab="Bazar">Bazar</button>
      </div>
    </div>
    <div class="chart-wrap" style="height:280px"><canvas id="c-kpi-contract"></canvas></div>
  </div>

'''

html = html.replace('  <!-- Charts Row 2 -->', NEW_SECTION + '  <!-- Charts Row 2 -->')
print("HTML section inserted")

# ── 2. ADD buildKPIContractChart() call inside render() ──────────────────────
OLD_RENDER_BODY = """  buildRegionChart(data);
  buildGovernorateChart(data);"""

NEW_RENDER_BODY = """  buildRegionChart(data);
  buildGovernorateChart(data);
  buildKPIContractChart(data);"""

html = html.replace(OLD_RENDER_BODY, NEW_RENDER_BODY)
print("render() updated")

# ── 3. INSERT JS for buildKPIContractChart before closing </script> of main block ──
KPI_CONTRACT_JS = '''

/* ═══════════════════════════════════════════════
   KPI COMPLIANCE BY CONTRACT TYPE
   Bar chart (compliance %) + Line (incentive EGP)
   Same format as Regional Performance chart.
   4 tabs: Impulse & Grocery | Supermarket | Gas Station | Bazar
═══════════════════════════════════════════════ */

const KPI_BY_CONTRACT = {
  'Impulse & Grocery': [
    { label: 'Availability',   comp: 'avail_compliance',           inc: 'avail_incentive' },
    { label: 'Share of Shelf', comp: 'sos_compliance',             inc: 'sos_incentive' },
    { label: 'Strike Zone',    comp: 'sz_compliance',              inc: 'sz_incentive' },
    { label: 'Large Cooler',   comp: 'large_cooler_compliance',    inc: 'large_cooler_incentive' },
  ],
  'Supermarket': [
    { label: 'Availability',      comp: 'avail_compliance',          inc: 'avail_incentive' },
    { label: 'Share of Shelf',    comp: 'sos_compliance',            inc: 'sos_incentive' },
    { label: 'Strike Zone',       comp: 'sz_compliance',             inc: 'sz_incentive' },
    { label: 'Price',             comp: 'price_compliance',          inc: 'price_incentive' },
    { label: 'POSM',              comp: 'posm_compliance',           inc: 'posm_incentive' },
    { label: 'Ambient Placement', comp: 'ambient_compliance',        inc: 'ambient_incentive' },
    { label: 'Cooler @ Cashier',  comp: 'cooler_cashier_compliance', inc: 'cooler_cashier_incentive' },
  ],
  'Gas Station': [
    { label: 'Availability',      comp: 'avail_compliance',             inc: 'avail_incentive' },
    { label: 'Share of Shelf',    comp: 'sos_compliance',               inc: 'sos_incentive' },
    { label: 'Strike Zone',       comp: 'sz_compliance',                inc: 'sz_incentive' },
    { label: 'Price',             comp: 'price_compliance',             inc: 'price_incentive' },
    { label: 'Sticky Shelf',      comp: 'sticky_compliance',            inc: 'sticky_incentive' },
    { label: 'Chilled 2m Cashier',comp: 'chilled_cashier_compliance',   inc: 'chilled_cashier_incentive' },
  ],
  'Bazar': [
    { label: 'Availability',         comp: 'avail_compliance',          inc: 'avail_incentive' },
    { label: 'Share of Shelf',       comp: 'sos_compliance',            inc: 'sos_incentive' },
    { label: 'Strike Zone',          comp: 'sz_compliance',             inc: 'sz_incentive' },
    { label: 'Outdoor Visibility',   comp: 'outdoor_compliance',        inc: 'outdoor_incentive' },
    { label: 'POSM',                 comp: 'posm_compliance',           inc: 'posm_incentive' },
    { label: 'Cooler Accessible',    comp: 'cooler_visible_compliance',  inc: 'cooler_visible_incentive' },
  ],
};

const CONTRACT_COLORS = {
  'Impulse & Grocery': ['#e8001c','#c0392b','#e74c3c','#ff6b6b'],
  'Supermarket':       ['#f5c518','#f39c12','#e67e22','#d35400','#f5c518','#f39c12','#e67e22'],
  'Gas Station':       ['#3b82f6','#2563eb','#1d4ed8','#60a5fa','#3b82f6','#2563eb'],
  'Bazar':             ['#8b5cf6','#7c3aed','#6d28d9','#a78bfa','#8b5cf6','#7c3aed'],
};

let kpiContractChart = null;
let activeContractType = 'Impulse & Grocery';

function buildKPIContractChart(data) {
  const type  = activeContractType;
  const kpis  = KPI_BY_CONTRACT[type] || [];
  const colors = CONTRACT_COLORS[type] || ['#94a3b8'];

  // Filter to this outlet type only
  const sub = data.filter(r => r.outlet_type === type);
  const n   = sub.length;

  // Compute compliance % and total incentive per KPI
  const labels  = kpis.map(k => k.label);
  const compPct = kpis.map(k => {
    const valid = sub.filter(r => r[k.comp] === 0 || r[k.comp] === 1);
    if (!valid.length) return 0;
    return parseFloat((valid.filter(r => r[k.comp] === 1).length / valid.length * 100).toFixed(1));
  });
  const incVals = kpis.map(k =>
    sub.reduce((s, r) => s + (typeof r[k.inc] === 'number' ? r[k.inc] : 0), 0)
  );

  const ctx = document.getElementById('c-kpi-contract');
  if (!ctx) return;
  if (kpiContractChart) { kpiContractChart.destroy(); kpiContractChart = null; }

  kpiContractChart = new Chart(ctx, {
    data: {
      labels,
      datasets: [
        {
          type: 'bar',
          label: 'Avg Compliance %',
          data: compPct,
          backgroundColor: colors.map(c => c + 'bb'),
          borderColor: colors,
          borderWidth: 2,
          borderRadius: 6,
          yAxisID: 'yLeft',
          order: 2,
        },
        {
          type: 'line',
          label: 'Total Incentive (EGP)',
          data: incVals,
          borderColor: '#f5c518',
          backgroundColor: 'rgba(245,197,24,0.08)',
          pointBackgroundColor: '#f5c518',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 8,
          tension: 0.35,
          fill: false,
          yAxisID: 'yRight',
          order: 1,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          display: true,
          labels: { color: '#94a3b8', usePointStyle: true, padding: 20, font: { size: 12 } }
        },
        tooltip: {
          callbacks: {
            label: ctx => ctx.dataset.label === 'Avg Compliance %'
              ? `Compliance %: ${ctx.raw}%`
              : `Total Incentive (EGP): ${Number(ctx.raw).toLocaleString(undefined,{maximumFractionDigits:0})}`
          }
        }
      },
      scales: {
        x: {
          ticks: { color: '#94a3b8', font: { size: 12 } },
          grid:  { color: 'rgba(255,255,255,0.05)' }
        },
        yLeft: {
          type: 'linear', position: 'left',
          min: 0, max: 100,
          ticks: { color: '#94a3b8', callback: v => v + '%' },
          grid:  { color: 'rgba(255,255,255,0.05)' },
          title: { display: false }
        },
        yRight: {
          type: 'linear', position: 'right',
          ticks: { color: '#f5c518', callback: v => v.toLocaleString() },
          grid:  { drawOnChartArea: false }
        }
      }
    }
  });

  // Update header text
  const titleEl    = document.getElementById('kpi-contract-title');
  const subtitleEl = document.getElementById('kpi-contract-subtitle');
  if (titleEl)    titleEl.textContent    = type + ' — KPI Compliance';
  if (subtitleEl) subtitleEl.textContent =
    n.toLocaleString() + ' outlets · Compliance % and incentive EGP per monitored KPI';
}

// Wire up the 4 contract-type tabs
document.querySelectorAll('[data-contract-tab]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-contract-tab]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeContractType = btn.dataset.contractTab;
    buildKPIContractChart(getFilteredData ? getFilteredData() : ALL_DATA);
  });
});
'''

# Insert before the first </script> that closes the main block (after init())
# The main script block ends with: init();\n</script>
html = html.replace('init();\n</script>', 'init();\n' + KPI_CONTRACT_JS + '\n</script>', 1)
print("JS inserted")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done - all changes written to index.html")
