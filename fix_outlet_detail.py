with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ══════════════════════════════════════════════════════════════════
# 1. MAKE MAIN FILTERS-BAR STICKY (bring to front on scroll)
# ══════════════════════════════════════════════════════════════════
OLD_FILTER_CSS = """    .filters-bar {
      display: flex; flex-wrap: wrap; gap: 12px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px 20px;
      margin-bottom: 28px;
      align-items: center;
    }"""

NEW_FILTER_CSS = """    .filters-bar {
      display: flex; flex-wrap: wrap; gap: 12px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px 20px;
      margin-bottom: 28px;
      align-items: center;
    }
    /* Sticky main filter bar */
    #tab-overview > .filters-bar {
      position: sticky;
      top: 0;
      z-index: 500;
      backdrop-filter: blur(10px);
      background: rgba(15,23,42,0.95);
      border-radius: 0 0 var(--radius) var(--radius);
      border-top: none;
      margin-bottom: 20px;
    }"""

if OLD_FILTER_CSS in html:
    html = html.replace(OLD_FILTER_CSS, NEW_FILTER_CSS, 1)
    fixes += 1
    print("CSS: main filter bar is now sticky")
else:
    print("WARN: filters-bar CSS not found")

# ══════════════════════════════════════════════════════════════════
# 2. ADD "Outlet Name" column to table thead
# ══════════════════════════════════════════════════════════════════
OLD_THEAD = """            <th data-col="serial">#</th>
            <th data-col="round">Round</th>
            <th data-col="month">Month</th>
            <th data-col="outlet_code">Code</th>
            <th data-col="outlet_type">Type</th>
            <th data-col="region">Region</th>
            <th data-col="governorate">Gov.</th>
            <th data-col="overall_score">Score</th>
            <th data-col="avail_compliance">Avail.</th>
            <th data-col="sos_compliance">SoS</th>
            <th data-col="sz_compliance">Strike</th>
            <th data-col="total_incentive">Incentive</th>"""

NEW_THEAD = """            <th data-col="serial">#</th>
            <th data-col="round">Round</th>
            <th data-col="outlet_code">Code</th>
            <th data-col="outlet_name">Name</th>
            <th data-col="outlet_type">Type</th>
            <th data-col="region">Region</th>
            <th data-col="overall_score">Score</th>
            <th>KPI Compliance</th>
            <th data-col="total_incentive">Incentive</th>"""

if OLD_THEAD in html:
    html = html.replace(OLD_THEAD, NEW_THEAD, 1)
    fixes += 1
    print("HTML: table thead updated with Name + KPI Compliance column")
else:
    print("WARN: thead not found")

# ══════════════════════════════════════════════════════════════════
# 3. UPDATE renderTable() rows to show KPI badges per outlet type
# ══════════════════════════════════════════════════════════════════
OLD_RENDER_ROWS = """  tbody.innerHTML = show.map(r => `<tr>
    <td style="color:var(--muted)">${r.serial||'—'}</td>
    <td><span class="badge badge-gold" style="font-size:10px">R${r.round||'—'}</span></td>
    <td style="color:var(--muted)">${r.month||'—'}</td>
    <td style="font-family:monospace;color:var(--muted)">${r.outlet_code||'—'}</td>
    <td>${outletPill(r.outlet_type)}</td>
    <td>${r.region||'—'}</td>
    <td>${r.governorate||'—'}</td>
    <td>${scoreFill(r.overall_score)}</td>
    <td>${compPill(r.avail_compliance)}</td>
    <td>${compPill(r.sos_compliance)}</td>
    <td>${compPill(r.sz_compliance)}</td>
    <td style="color:var(--gold);font-weight:600">${typeof r.total_incentive === 'number' ? r.total_incentive.toFixed(1) + ' EGP' : '—'}</td>
  </tr>`).join('');"""

NEW_RENDER_ROWS = """  // KPI map per outlet type (same as KPI_BY_CONTRACT)
  const OUTLET_KPIS = {
    'Impulse & Grocery': [
      {label:'Avail',  key:'avail_compliance'},
      {label:'SoS',    key:'sos_compliance'},
      {label:'SZ',     key:'sz_compliance'},
      {label:'L.Cooler',key:'large_cooler_compliance'},
    ],
    'Supermarket': [
      {label:'Avail',  key:'avail_compliance'},
      {label:'SoS',    key:'sos_compliance'},
      {label:'SZ',     key:'sz_compliance'},
      {label:'Price',  key:'price_compliance'},
      {label:'Ambient',key:'ambient_compliance'},
      {label:'Cooler@Cash',key:'cooler_cashier_compliance'},
    ],
    'Gas Station': [
      {label:'Avail',  key:'avail_compliance'},
      {label:'SoS',    key:'sos_compliance'},
      {label:'SZ',     key:'sz_compliance'},
      {label:'Price',  key:'price_compliance'},
      {label:'Sticky', key:'sticky_compliance'},
      {label:'Chilled',key:'chilled_cashier_compliance'},
      {label:'Brand Vis',key:'posm_compliance'},
    ],
    'Bazar': [
      {label:'Avail',  key:'avail_compliance'},
      {label:'Outdoor',key:'outdoor_compliance'},
      {label:'Price',  key:'price_compliance'},
      {label:'Cooler', key:'cooler_visible_compliance'},
    ],
  };

  function kpiChips(r) {
    const kpis = OUTLET_KPIS[r.outlet_type] || [
      {label:'Avail',key:'avail_compliance'},
      {label:'SoS',  key:'sos_compliance'},
      {label:'SZ',   key:'sz_compliance'},
    ];
    return kpis.map(k => {
      const v = r[k.key];
      if (v === 1) return `<span style="background:rgba(16,185,129,.18);color:#10b981;border:1px solid rgba(16,185,129,.3);border-radius:12px;padding:2px 8px;font-size:10px;font-weight:600;white-space:nowrap">✓ ${k.label}</span>`;
      if (v === 0) return `<span style="background:rgba(232,0,28,.12);color:#e8001c;border:1px solid rgba(232,0,28,.25);border-radius:12px;padding:2px 8px;font-size:10px;font-weight:600;white-space:nowrap">✗ ${k.label}</span>`;
      return `<span style="color:rgba(148,163,184,.4);font-size:10px;padding:2px 8px;border-radius:12px;border:1px solid rgba(255,255,255,.05)">— ${k.label}</span>`;
    }).join(' ');
  }

  tbody.innerHTML = show.map(r => `<tr>
    <td style="color:var(--muted)">${r.serial||'—'}</td>
    <td><span class="badge badge-gold" style="font-size:10px">R${r.round||'—'}</span></td>
    <td style="font-family:monospace;color:var(--muted);font-size:11px">${r.outlet_code||'—'}</td>
    <td style="max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${r.outlet_name||''}">${r.outlet_name||'—'}</td>
    <td>${outletPill(r.outlet_type)}</td>
    <td>${r.region||'—'}</td>
    <td>${scoreFill(r.overall_score)}</td>
    <td style="white-space:nowrap">${kpiChips(r)}</td>
    <td style="color:var(--gold);font-weight:600;white-space:nowrap">${typeof r.total_incentive === 'number' ? r.total_incentive.toFixed(1) + ' EGP' : '—'}</td>
  </tr>`).join('');"""

if OLD_RENDER_ROWS in html:
    html = html.replace(OLD_RENDER_ROWS, NEW_RENDER_ROWS, 1)
    fixes += 1
    print("JS: renderTable() updated with outlet name + KPI compliance chips")
else:
    print("WARN: renderTable rows not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes} — Done.")
