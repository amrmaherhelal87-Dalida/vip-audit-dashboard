with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ══════════════════════════════════════════════════════════════════
# 1. REPLACE Map m-round select → ms-wrap multi-select
# ══════════════════════════════════════════════════════════════════
OLD_M_ROUND = """      <div class="filter-group">
        <label for="m-round">Round</label>
        <select id="m-round">
          <option value="all">All Rounds</option>
          <option value="79">Round 79 — April</option>
          <option value="80">Round 80 — May</option>
          <option value="81">Round 81 — June</option>
          <option value="82">Round 82 — July</option>
        </select>
      </div>"""

NEW_M_ROUND = """      <div class="filter-group">
        <label>Round</label>
        <div class="ms-wrap" id="ms-m-round">
          <div class="ms-display" onclick="toggleMS('ms-m-round')">
            <span class="ms-label" id="ms-m-round-lbl">All Rounds</span>
            <span class="ms-arrow">&#9660;</span>
          </div>
          <div class="ms-panel">
            <label class="ms-opt all-opt"><input type="checkbox" value="all" checked onchange="msAllToggle('ms-m-round',this)"> All Rounds</label>
            <label class="ms-opt"><input type="checkbox" value="79" onchange="msOptChange('ms-m-round')"> Round 79 — April</label>
            <label class="ms-opt"><input type="checkbox" value="80" onchange="msOptChange('ms-m-round')"> Round 80 — May</label>
            <label class="ms-opt"><input type="checkbox" value="81" onchange="msOptChange('ms-m-round')"> Round 81 — June</label>
            <label class="ms-opt"><input type="checkbox" value="82" onchange="msOptChange('ms-m-round')"> Round 82 — July</label>
          </div>
        </div>
      </div>"""

if OLD_M_ROUND in html:
    html = html.replace(OLD_M_ROUND, NEW_M_ROUND, 1)
    fixes += 1
    print("HTML: Map Round → ms-wrap")
else:
    print("WARN: Map m-round not found")

# ══════════════════════════════════════════════════════════════════
# 2. REPLACE Map m-type select → ms-wrap multi-select
# ══════════════════════════════════════════════════════════════════
OLD_M_TYPE = """      <div class="filter-group">
        <label for="m-type">Outlet Type</label>
        <select id="m-type">
          <option value="all">All Types</option>
          <option value="Impulse &amp; Grocery">Impulse &amp; Grocery</option>
          <option value="Gas Station">Gas Station</option>
          <option value="Supermarket">Supermarket</option>
          <option value="Bazar">Bazar</option>
        </select>
      </div>"""

NEW_M_TYPE = """      <div class="filter-group">
        <label>Outlet Type</label>
        <div class="ms-wrap" id="ms-m-type">
          <div class="ms-display" onclick="toggleMS('ms-m-type')">
            <span class="ms-label" id="ms-m-type-lbl">All Types</span>
            <span class="ms-arrow">&#9660;</span>
          </div>
          <div class="ms-panel">
            <label class="ms-opt all-opt"><input type="checkbox" value="all" checked onchange="msAllToggle('ms-m-type',this)"> All Types</label>
            <label class="ms-opt"><input type="checkbox" value="Impulse &amp; Grocery" onchange="msOptChange('ms-m-type')"> Impulse &amp; Grocery</label>
            <label class="ms-opt"><input type="checkbox" value="Gas Station" onchange="msOptChange('ms-m-type')"> Gas Station</label>
            <label class="ms-opt"><input type="checkbox" value="Supermarket" onchange="msOptChange('ms-m-type')"> Supermarket</label>
            <label class="ms-opt"><input type="checkbox" value="Bazar" onchange="msOptChange('ms-m-type')"> Bazar</label>
          </div>
        </div>
      </div>"""

if OLD_M_TYPE in html:
    html = html.replace(OLD_M_TYPE, NEW_M_TYPE, 1)
    fixes += 1
    print("HTML: Map Outlet Type → ms-wrap")
else:
    print("WARN: Map m-type not found")

# ══════════════════════════════════════════════════════════════════
# 3. REPLACE Quarterly q-select → ms-wrap multi-select
# ══════════════════════════════════════════════════════════════════
OLD_Q_SELECT_HTML = """      <div class="filter-group">
        <label for="q-select">Quarter</label>
        <select id="q-select">
          <option value="all">All Quarters</option>
          <option value="Q1">Q1</option>
          <option value="Q2">Q2</option>
          <option value="Q3">Q3</option>
          <option value="Q4">Q4</option>
        </select>
      </div>"""

NEW_Q_SELECT_HTML = """      <div class="filter-group">
        <label>Quarter</label>
        <div class="ms-wrap" id="ms-quarter">
          <div class="ms-display" onclick="toggleMS('ms-quarter')">
            <span class="ms-label" id="ms-quarter-lbl">All Quarters</span>
            <span class="ms-arrow">&#9660;</span>
          </div>
          <div class="ms-panel">
            <label class="ms-opt all-opt"><input type="checkbox" value="all" checked onchange="msAllToggle('ms-quarter',this)"> All Quarters</label>
            <label class="ms-opt"><input type="checkbox" value="Q1" onchange="msOptChange('ms-quarter')"> Q1</label>
            <label class="ms-opt"><input type="checkbox" value="Q2" onchange="msOptChange('ms-quarter')"> Q2</label>
            <label class="ms-opt"><input type="checkbox" value="Q3" onchange="msOptChange('ms-quarter')"> Q3</label>
            <label class="ms-opt"><input type="checkbox" value="Q4" onchange="msOptChange('ms-quarter')"> Q4</label>
          </div>
        </div>
      </div>"""

if OLD_Q_SELECT_HTML in html:
    html = html.replace(OLD_Q_SELECT_HTML, NEW_Q_SELECT_HTML, 1)
    fixes += 1
    print("HTML: Quarterly Quarter → ms-wrap")
else:
    print("WARN: q-select not found")

# ══════════════════════════════════════════════════════════════════
# 4. UPDATE getMapFilters() to use getMSValues for round & type
# ══════════════════════════════════════════════════════════════════
OLD_GET_MAP = """function getMapFilters() {
  return {
    round:      document.getElementById('m-round').value,
    type:       document.getElementById('m-type').value,
    compliance: document.getElementById('m-compliance').value,
    colorBy:    document.getElementById('m-color').value,
  };
}"""

NEW_GET_MAP = """function getMapFilters() {
  return {
    round:      getMSValues('ms-m-round'),
    type:       getMSValues('ms-m-type'),
    compliance: document.getElementById('m-compliance').value,
    colorBy:    document.getElementById('m-color').value,
  };
}"""

if OLD_GET_MAP in html:
    html = html.replace(OLD_GET_MAP, NEW_GET_MAP, 1)
    fixes += 1
    print("JS: getMapFilters() updated for ms-wrap")
else:
    print("WARN: getMapFilters not found")

# ══════════════════════════════════════════════════════════════════
# 5. UPDATE applyMapFilters() to handle array values from ms-wrap
# ══════════════════════════════════════════════════════════════════
OLD_MAP_APPLY = """    if (f.round !== 'all' && String(r.round) !== f.round) return false;
    if (f.type  !== 'all' && r.outlet_type   !== f.type)  return false;"""

NEW_MAP_APPLY = """    if (f.round !== 'all' && !(Array.isArray(f.round) ? f.round.includes(String(r.round)) : String(r.round) === f.round)) return false;
    if (f.type  !== 'all' && !(Array.isArray(f.type)  ? f.type.includes(r.outlet_type)       : r.outlet_type   === f.type))  return false;"""

if OLD_MAP_APPLY in html:
    html = html.replace(OLD_MAP_APPLY, NEW_MAP_APPLY, 1)
    fixes += 1
    print("JS: applyMapFilters() updated for array values")
else:
    print("WARN: applyMapFilters conditions not found")

# ══════════════════════════════════════════════════════════════════
# 6. UPDATE msOptChange & msAllToggle to trigger map/quarter rebuild
#    when their ms-wrap IDs change
# ══════════════════════════════════════════════════════════════════
OLD_MS_OPT = """function msOptChange(id) {
  const allCb  = document.querySelector(`#${id} .all-opt input`);
  const anyChecked = [...document.querySelectorAll(`#${id} .ms-opt:not(.all-opt) input:checked`)].length > 0;
  // Uncheck "All" if any specific option is selected
  if (allCb) allCb.checked = !anyChecked;
  updateMSLabel(id);
  render();
}"""

NEW_MS_OPT = """function msOptChange(id) {
  const allCb  = document.querySelector(`#${id} .all-opt input`);
  const anyChecked = [...document.querySelectorAll(`#${id} .ms-opt:not(.all-opt) input:checked`)].length > 0;
  if (allCb) allCb.checked = !anyChecked;
  updateMSLabel(id);
  // Route to correct handler based on which ms-wrap changed
  if (id === 'ms-m-round' || id === 'ms-m-type') {
    updateMap();
  } else if (id === 'ms-quarter') {
    const vals = getMSValues('ms-quarter');
    activeQFilter = vals;
    buildQuarterTab(ALL_DATA, activeQFilter);
    quarterBuilt = true;
  } else {
    render();
  }
}"""

if OLD_MS_OPT in html:
    html = html.replace(OLD_MS_OPT, NEW_MS_OPT, 1)
    fixes += 1
    print("JS: msOptChange() routes to map/quarter/render")
else:
    print("WARN: msOptChange not found")

OLD_MS_ALL = """function msAllToggle(id, cb) {
  if (cb.checked) {
    // Uncheck all individual options
    document.querySelectorAll(`#${id} .ms-opt:not(.all-opt) input`).forEach(c => c.checked = false);
  }
  updateMSLabel(id);
  render();
}"""

NEW_MS_ALL = """function msAllToggle(id, cb) {
  if (cb.checked) {
    document.querySelectorAll(`#${id} .ms-opt:not(.all-opt) input`).forEach(c => c.checked = false);
  }
  updateMSLabel(id);
  if (id === 'ms-m-round' || id === 'ms-m-type') {
    updateMap();
  } else if (id === 'ms-quarter') {
    activeQFilter = 'all';
    buildQuarterTab(ALL_DATA, 'all');
    quarterBuilt = true;
  } else {
    render();
  }
}"""

if OLD_MS_ALL in html:
    html = html.replace(OLD_MS_ALL, NEW_MS_ALL, 1)
    fixes += 1
    print("JS: msAllToggle() routes to map/quarter/render")
else:
    print("WARN: msAllToggle not found")

# ══════════════════════════════════════════════════════════════════
# 7. UPDATE updateMSLabel to recognise new ms IDs
# ══════════════════════════════════════════════════════════════════
OLD_MS_LABEL = """  const defaults = {'ms-round':'All Rounds','ms-type':'All Types','ms-region':'All Regions'};"""
NEW_MS_LABEL = """  const defaults = {
    'ms-round':'All Rounds','ms-type':'All Types','ms-region':'All Regions',
    'ms-m-round':'All Rounds','ms-m-type':'All Types','ms-quarter':'All Quarters'
  };"""

if OLD_MS_LABEL in html:
    html = html.replace(OLD_MS_LABEL, NEW_MS_LABEL, 1)
    fixes += 1
    print("JS: updateMSLabel defaults updated")
else:
    print("WARN: updateMSLabel defaults not found")

# ══════════════════════════════════════════════════════════════════
# 8. UPDATE buildQuarterTab to accept array qFilter
# ══════════════════════════════════════════════════════════════════
OLD_Q_FILTER = """  const filtered = (qFilter === 'all')
    ? data
    : data.filter(r => (MONTH_TO_Q[r.month] || 'Unknown') === qFilter);

  // Update label
  const lbl = document.getElementById('q-filter-label');
  if (lbl) lbl.textContent = qFilter === 'all'
    ? filtered.length.toLocaleString() + ' total audits'
    : filtered.length.toLocaleString() + ' audits in ' + qFilter;"""

NEW_Q_FILTER = """  // Support both string and array qFilter
  const qArr = Array.isArray(qFilter) ? qFilter : (qFilter === 'all' ? [] : [qFilter]);
  const filtered = (qArr.length === 0)
    ? data
    : data.filter(r => qArr.includes(MONTH_TO_Q[r.month] || 'Unknown'));

  // Update label
  const lbl = document.getElementById('q-filter-label');
  if (lbl) lbl.textContent = (qArr.length === 0)
    ? filtered.length.toLocaleString() + ' total audits'
    : filtered.length.toLocaleString() + ' audits in ' + qArr.join(', ');"""

if OLD_Q_FILTER in html:
    html = html.replace(OLD_Q_FILTER, NEW_Q_FILTER, 1)
    fixes += 1
    print("JS: buildQuarterTab handles array qFilter")
else:
    print("WARN: buildQuarterTab filter block not found")

# ══════════════════════════════════════════════════════════════════
# 9. REMOVE old q-select onChange listener (replaced by msOptChange)
# ══════════════════════════════════════════════════════════════════
OLD_Q_LISTENER = """// ── Quarter SELECT inside Quarterly tab ─────────────────────────────────────
document.getElementById('q-select')?.addEventListener('change', function() {
  activeQFilter = this.value;
  buildQuarterTab(ALL_DATA, activeQFilter);
  quarterBuilt = true;
});"""

if OLD_Q_LISTENER in html:
    html = html.replace(OLD_Q_LISTENER, '// Quarter filter handled by ms-wrap msOptChange()', 1)
    fixes += 1
    print("JS: old q-select listener removed")

# Also fix the sync on tab open (was referencing q-select)
OLD_Q_SYNC = """  // Sync select to activeQFilter
  const qs = document.getElementById('q-select');
  if (qs) qs.value = activeQFilter;"""

if OLD_Q_SYNC in html:
    html = html.replace(OLD_Q_SYNC, '', 1)
    print("JS: old q-select sync removed")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes} — Done.")
