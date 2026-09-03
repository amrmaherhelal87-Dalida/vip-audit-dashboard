with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ══════════════════════════════════════════════════════════════════
# 1. ADD SheetJS CDN (for Excel export) after Chart.js CDN
# ══════════════════════════════════════════════════════════════════
OLD_CDN = '<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>'
NEW_CDN = OLD_CDN + '\n  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>'
if OLD_CDN in html:
    html = html.replace(OLD_CDN, NEW_CDN, 1)
    fixes += 1
    print("CDN: SheetJS added")

# ══════════════════════════════════════════════════════════════════
# 2. ADD CSS for export button + dropdown
# ══════════════════════════════════════════════════════════════════
EXPORT_CSS = """
    /* ── Export Button & Dropdown ── */
    .export-wrap { position: relative; display: inline-block; }
    #btn-export {
      background: rgba(16,185,129,.12);
      border: 1px solid rgba(16,185,129,.35);
      color: #10b981;
      padding: 8px 16px;
      border-radius: 8px;
      font-family: inherit;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all .2s;
      display: flex; align-items: center; gap: 6px;
    }
    #btn-export:hover {
      background: rgba(16,185,129,.22);
      border-color: #10b981;
      box-shadow: 0 0 12px rgba(16,185,129,.2);
    }
    .export-menu {
      display: none;
      position: absolute;
      top: calc(100% + 6px);
      right: 0;
      background: #1e293b;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 10px;
      padding: 6px;
      z-index: 9999;
      min-width: 170px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }
    .export-wrap.open .export-menu { display: block; }
    .export-item {
      display: flex; align-items: center; gap: 10px;
      padding: 9px 14px;
      border-radius: 7px;
      cursor: pointer;
      color: #94a3b8;
      font-size: 13px;
      font-weight: 500;
      transition: background .15s;
      border: none; background: none; width: 100%; font-family: inherit;
      text-align: left;
    }
    .export-item:hover { background: rgba(255,255,255,0.06); color: #e2e8f0; }
    .export-item .ei-icon { font-size: 16px; }
"""
html = html.replace('.tab-nav {', EXPORT_CSS + '\n    .tab-nav {', 1)
fixes += 1
print("CSS: export button styles added")

# ══════════════════════════════════════════════════════════════════
# 3. REPLACE "↺ Reset" button → "Clear Filters" + add Export button
# ══════════════════════════════════════════════════════════════════
OLD_RESET_BTN = '    <button id="btn-reset">↺ Reset</button>\n  </div>'
NEW_RESET_BTN = """    <div style="display:flex;gap:8px;align-items:center;margin-left:auto">
      <button id="btn-reset">✕ Clear Filters</button>
      <div class="export-wrap" id="export-wrap">
        <button id="btn-export" onclick="toggleExportMenu()">
          <span>⬇ Export</span><span style="font-size:10px">▼</span>
        </button>
        <div class="export-menu">
          <button class="export-item" onclick="exportData('csv')">
            <span class="ei-icon">📄</span> Export as CSV
          </button>
          <button class="export-item" onclick="exportData('excel')">
            <span class="ei-icon">📊</span> Export as Excel
          </button>
        </div>
      </div>
    </div>
  </div>"""

if OLD_RESET_BTN in html:
    html = html.replace(OLD_RESET_BTN, NEW_RESET_BTN, 1)
    fixes += 1
    print("HTML: Reset → Clear Filters + Export button added")
else:
    print("WARN: Reset button not found")

# ══════════════════════════════════════════════════════════════════
# 4. ALSO rename map Reset button
# ══════════════════════════════════════════════════════════════════
html = html.replace('>↺ Reset</button>', '>✕ Clear Filters</button>', 1)
print("HTML: Map Reset → Clear Filters")

# ══════════════════════════════════════════════════════════════════
# 5. ADD Export JS functions before closing </script>
# ══════════════════════════════════════════════════════════════════
EXPORT_JS = """
/* ── Export Functions ────────────────────────────────────────────────────── */
function toggleExportMenu() {
  const wrap = document.getElementById('export-wrap');
  wrap.classList.toggle('open');
}

// Close export menu on outside click
document.addEventListener('click', e => {
  if (!e.target.closest('#export-wrap')) {
    document.getElementById('export-wrap')?.classList.remove('open');
  }
});

function getExportData() {
  // Use currently filtered data
  const data = applyFilters(ALL_DATA);
  return data.map((r, i) => ({
    '#':              i + 1,
    'Round':          r.round || '',
    'Month':          r.month || '',
    'Outlet Code':    r.outlet_code || '',
    'Outlet Name':    r.outlet_name || '',
    'Outlet Type':    r.outlet_type || '',
    'Region':         r.region || '',
    'Governorate':    r.governorate || '',
    'Overall Score':  typeof r.overall_score === 'number' ? +(r.overall_score * 100).toFixed(1) : '',
    'Avail. %':       r.avail_compliance === 1 ? 100 : r.avail_compliance === 0 ? 0 : '',
    'SoS %':          r.sos_compliance   === 1 ? 100 : r.sos_compliance   === 0 ? 0 : '',
    'Strike Zone %':  r.sz_compliance    === 1 ? 100 : r.sz_compliance    === 0 ? 0 : '',
    'Price %':        r.price_compliance === 1 ? 100 : r.price_compliance === 0 ? 0 : '',
    'Sticky Shelf %': r.sticky_compliance=== 1 ? 100 : r.sticky_compliance=== 0 ? 0 : '',
    'Ambient %':      r.ambient_compliance===1 ? 100 : r.ambient_compliance===0 ? 0 : '',
    'Cooler@Cashier %': r.cooler_cashier_compliance===1?100:r.cooler_cashier_compliance===0?0:'',
    'Chilled Cashier %':r.chilled_cashier_compliance===1?100:r.chilled_cashier_compliance===0?0:'',
    'Outdoor %':      r.outdoor_compliance===1?100:r.outdoor_compliance===0?0:'',
    'Brand Vis. %':   r.posm_compliance===1?100:r.posm_compliance===0?0:'',
    'Large Cooler %': r.large_cooler_compliance===1?100:r.large_cooler_compliance===0?0:'',
    'Cooler Visible %':r.cooler_visible_compliance===1?100:r.cooler_visible_compliance===0?0:'',
    'Total Incentive (EGP)': typeof r.total_incentive === 'number' ? +r.total_incentive.toFixed(2) : '',
  }));
}

function exportData(type) {
  document.getElementById('export-wrap').classList.remove('open');
  const rows = getExportData();
  if (!rows.length) { alert('No data to export with current filters.'); return; }

  const now = new Date();
  const stamp = `${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}`;
  const filename = `VIP_Audit_${stamp}`;

  if (type === 'csv') {
    const headers = Object.keys(rows[0]);
    const csv = [
      headers.join(','),
      ...rows.map(r => headers.map(h => {
        const v = r[h] ?? '';
        return typeof v === 'string' && (v.includes(',') || v.includes('"'))
          ? `"${v.replace(/"/g, '""')}"` : v;
      }).join(','))
    ].join('\\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename + '.csv';
    a.click();
    URL.revokeObjectURL(a.href);

  } else if (type === 'excel') {
    if (typeof XLSX === 'undefined') { alert('Excel library loading… try again in a moment.'); return; }
    const ws = XLSX.utils.json_to_sheet(rows);
    // Style header row width
    const cols = Object.keys(rows[0]).map(k => ({ wch: Math.max(k.length, 12) }));
    ws['!cols'] = cols;
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'VIP Audit Data');
    XLSX.writeFile(wb, filename + '.xlsx');
  }
}
"""

html = html.replace('</script>\n</body>', EXPORT_JS + '\n</script>\n</body>', 1)
fixes += 1
print("JS: Export functions added")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes} — Done.")
