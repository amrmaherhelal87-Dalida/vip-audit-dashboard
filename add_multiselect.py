with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════════════════
# 1. ADD CSS for custom multi-select widget
# ══════════════════════════════════════════════════════════════════
MS_CSS = """
/* ── Custom Multi-Select Dropdown ── */
.ms-wrap { position: relative; display: inline-block; }
.ms-display {
  background: var(--surface, #1e293b);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-width: 140px;
  color: #e2e8f0;
  font-size: 14px;
  font-family: inherit;
  transition: border-color .2s;
  user-select: none;
}
.ms-display:hover, .ms-wrap.open .ms-display { border-color: rgba(232,0,28,.5); }
.ms-arrow { font-size: 10px; color: #64748b; transition: transform .2s; flex-shrink:0; }
.ms-wrap.open .ms-arrow { transform: rotate(180deg); }
.ms-panel {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  min-width: 200px;
  background: #1e293b;
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 10px;
  padding: 8px;
  z-index: 9999;
  display: none;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.ms-wrap.open .ms-panel { display: block; }
.ms-opt {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 10px;
  border-radius: 6px;
  cursor: pointer;
  color: #94a3b8;
  font-size: 13px;
  transition: background .15s;
  white-space: nowrap;
}
.ms-opt:hover { background: rgba(255,255,255,0.06); color: #e2e8f0; }
.ms-opt input[type=checkbox] { accent-color: #e8001c; width:14px; height:14px; cursor:pointer; flex-shrink:0; }
.ms-opt.all-opt { border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom:4px; padding-bottom:10px; color:#e2e8f0; font-weight:600; }
.ms-badge {
  background: rgba(232,0,28,.2);
  color: #e8001c;
  border-radius: 10px;
  padding: 1px 7px;
  font-size: 11px;
  font-weight: 700;
}
/* Map search input */
#m-search {
  background: var(--surface, #1e293b);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 8px 12px;
  color: #e2e8f0;
  font-size: 14px;
  font-family: inherit;
  width: 220px;
  outline: none;
  transition: border-color .2s;
}
#m-search:focus { border-color: rgba(232,0,28,.5); }
#m-search::placeholder { color: #4b5563; }
"""

# Insert before .tab-nav {
OLD_CSS_NAV = ".tab-nav {"
html = html.replace(OLD_CSS_NAV, MS_CSS + "\n.tab-nav {", 1)
print("CSS: multi-select styles added")

# ══════════════════════════════════════════════════════════════════
# 2. REPLACE f-round, f-type, f-region selects with ms-wrap widgets
# ══════════════════════════════════════════════════════════════════
OLD_F_ROUND = """    <div class="filter-group">
      <label for="f-round">Round</label>
      <select id="f-round">
        <option value="all">All Rounds</option>
        <option value="79">Round 79 — April</option>
        <option value="80">Round 80 — May</option>
        <option value="81">Round 81 — June</option>
        <option value="82">Round 82 — July</option>
      </select>
    </div>"""

NEW_F_ROUND = """    <div class="filter-group">
      <label>Round</label>
      <div class="ms-wrap" id="ms-round">
        <div class="ms-display" onclick="toggleMS('ms-round')">
          <span class="ms-label" id="ms-round-lbl">All Rounds</span>
          <span class="ms-arrow">&#9660;</span>
        </div>
        <div class="ms-panel">
          <label class="ms-opt all-opt"><input type="checkbox" value="all" checked onchange="msAllToggle('ms-round',this)"> All Rounds</label>
          <label class="ms-opt"><input type="checkbox" value="79" onchange="msOptChange('ms-round')"> Round 79 — April</label>
          <label class="ms-opt"><input type="checkbox" value="80" onchange="msOptChange('ms-round')"> Round 80 — May</label>
          <label class="ms-opt"><input type="checkbox" value="81" onchange="msOptChange('ms-round')"> Round 81 — June</label>
          <label class="ms-opt"><input type="checkbox" value="82" onchange="msOptChange('ms-round')"> Round 82 — July</label>
        </div>
      </div>
    </div>"""

if OLD_F_ROUND in html:
    html = html.replace(OLD_F_ROUND, NEW_F_ROUND, 1)
    print("HTML: f-round → ms-round multi-select")

OLD_F_TYPE = """    <div class="filter-group">
      <label for="f-type">Outlet Type</label>
      <select id="f-type">
        <option value="all">All Types</option>
        <option value="Impulse &amp; Grocery">Impulse &amp; Grocery</option>
        <option value="Gas Station">Gas Station</option>
        <option value="Supermarket">Supermarket</option>
        <option value="Bazar">Bazar</option>
      </select>
    </div>"""

NEW_F_TYPE = """    <div class="filter-group">
      <label>Outlet Type</label>
      <div class="ms-wrap" id="ms-type">
        <div class="ms-display" onclick="toggleMS('ms-type')">
          <span class="ms-label" id="ms-type-lbl">All Types</span>
          <span class="ms-arrow">&#9660;</span>
        </div>
        <div class="ms-panel">
          <label class="ms-opt all-opt"><input type="checkbox" value="all" checked onchange="msAllToggle('ms-type',this)"> All Types</label>
          <label class="ms-opt"><input type="checkbox" value="Impulse &amp; Grocery" onchange="msOptChange('ms-type')"> Impulse &amp; Grocery</label>
          <label class="ms-opt"><input type="checkbox" value="Gas Station" onchange="msOptChange('ms-type')"> Gas Station</label>
          <label class="ms-opt"><input type="checkbox" value="Supermarket" onchange="msOptChange('ms-type')"> Supermarket</label>
          <label class="ms-opt"><input type="checkbox" value="Bazar" onchange="msOptChange('ms-type')"> Bazar</label>
        </div>
      </div>
    </div>"""

if OLD_F_TYPE in html:
    html = html.replace(OLD_F_TYPE, NEW_F_TYPE, 1)
    print("HTML: f-type → ms-type multi-select")

OLD_F_REGION = """    <div class="filter-group">
      <label for="f-region">Region</label>
      <select id="f-region">
        <option value="all">All Regions</option>
        <option value="Delta">Delta</option>
        <option value="Cairo">Cairo</option>
        <option value="Alexandria">Alexandria</option>
        <option value="Giza">Giza</option>
        <option value="Canal">Canal</option>
        <option value="Sinai">Sinai</option>
        <option value="Red Sea">Red Sea</option>
        <option value="Upper Egypt">Upper Egypt</option>
      </select>
    </div>"""

NEW_F_REGION = """    <div class="filter-group">
      <label>Region</label>
      <div class="ms-wrap" id="ms-region">
        <div class="ms-display" onclick="toggleMS('ms-region')">
          <span class="ms-label" id="ms-region-lbl">All Regions</span>
          <span class="ms-arrow">&#9660;</span>
        </div>
        <div class="ms-panel">
          <label class="ms-opt all-opt"><input type="checkbox" value="all" checked onchange="msAllToggle('ms-region',this)"> All Regions</label>
          <label class="ms-opt"><input type="checkbox" value="Delta" onchange="msOptChange('ms-region')"> Delta</label>
          <label class="ms-opt"><input type="checkbox" value="Cairo" onchange="msOptChange('ms-region')"> Cairo</label>
          <label class="ms-opt"><input type="checkbox" value="Alexandria" onchange="msOptChange('ms-region')"> Alexandria</label>
          <label class="ms-opt"><input type="checkbox" value="Giza" onchange="msOptChange('ms-region')"> Giza</label>
          <label class="ms-opt"><input type="checkbox" value="Canal" onchange="msOptChange('ms-region')"> Canal</label>
          <label class="ms-opt"><input type="checkbox" value="Sinai" onchange="msOptChange('ms-region')"> Sinai</label>
          <label class="ms-opt"><input type="checkbox" value="Red Sea" onchange="msOptChange('ms-region')"> Red Sea</label>
          <label class="ms-opt"><input type="checkbox" value="Upper Egypt" onchange="msOptChange('ms-region')"> Upper Egypt</label>
        </div>
      </div>
    </div>"""

if OLD_F_REGION in html:
    html = html.replace(OLD_F_REGION, NEW_F_REGION, 1)
    print("HTML: f-region → ms-region multi-select")

# ══════════════════════════════════════════════════════════════════
# 3. ADD search box to Map tab filter bar
# ══════════════════════════════════════════════════════════════════
OLD_MAP_FILTERS_END = """      <div class="filter-group">
        <label for="m-compliance">Compliance</label>"""

NEW_MAP_FILTERS_END = """      <div class="filter-group" style="flex:1;min-width:200px;max-width:280px">
        <label for="m-search">Search Outlet</label>
        <input type="text" id="m-search" placeholder="🔍 Search by code or name…" oninput="updateMap()">
      </div>
      <div class="filter-group">
        <label for="m-compliance">Compliance</label>"""

if OLD_MAP_FILTERS_END in html:
    html = html.replace(OLD_MAP_FILTERS_END, NEW_MAP_FILTERS_END, 1)
    print("HTML: map search box added")
else:
    print("WARN: map compliance filter anchor not found")

# ══════════════════════════════════════════════════════════════════
# 4. UPDATE getFilters() to read from multi-select widgets
# ══════════════════════════════════════════════════════════════════
OLD_GET_FILTERS = """function getFilters() {
  return {
    round:  document.getElementById('f-round').value,
    type:   document.getElementById('f-type').value,
    region: document.getElementById('f-region').value,
    gov:    document.getElementById('f-gov').value,
  };
}"""

NEW_GET_FILTERS = """function getMSValues(id) {
  const allCb = document.querySelector(`#${id} .all-opt input`);
  if (!allCb || allCb.checked) return 'all';
  const checked = [...document.querySelectorAll(`#${id} .ms-opt:not(.all-opt) input:checked`)].map(c => c.value);
  return checked.length ? checked : 'all';
}

function getFilters() {
  return {
    round:  getMSValues('ms-round'),
    type:   getMSValues('ms-type'),
    region: getMSValues('ms-region'),
    gov:    document.getElementById('f-gov').value,
  };
}"""

if OLD_GET_FILTERS in html:
    html = html.replace(OLD_GET_FILTERS, NEW_GET_FILTERS, 1)
    print("JS: getFilters() updated for multi-select")
else:
    print("WARN: getFilters not found")

# ══════════════════════════════════════════════════════════════════
# 5. UPDATE applyFilters() to handle array values
# ══════════════════════════════════════════════════════════════════
OLD_APPLY = """  return data.filter(r => {
    if (f.round  !== 'all' && String(r.round)       !== f.round)  return false;
    if (f.type   !== 'all' && r.outlet_type          !== f.type)   return false;
    if (f.region !== 'all' && r.region               !== f.region) return false;
    if (f.gov    !== 'all' && r.governorate          !== f.gov)    return false;"""

NEW_APPLY = """  return data.filter(r => {
    if (f.round  !== 'all' && !(Array.isArray(f.round)  ? f.round.includes(String(r.round))   : String(r.round)    === f.round))  return false;
    if (f.type   !== 'all' && !(Array.isArray(f.type)   ? f.type.includes(r.outlet_type)       : r.outlet_type       === f.type))   return false;
    if (f.region !== 'all' && !(Array.isArray(f.region) ? f.region.includes(r.region)          : r.region            === f.region)) return false;
    if (f.gov    !== 'all' && r.governorate          !== f.gov)    return false;"""

if OLD_APPLY in html:
    html = html.replace(OLD_APPLY, NEW_APPLY, 1)
    print("JS: applyFilters() updated for array values")
else:
    print("WARN: applyFilters body not found")

# ══════════════════════════════════════════════════════════════════
# 6. UPDATE Reset button to reset multi-selects
# ══════════════════════════════════════════════════════════════════
OLD_RESET_HANDLER = "['f-round','f-type','f-region','f-gov'].forEach(id => document.getElementById(id).value = 'all');"
NEW_RESET_HANDLER = """['ms-round','ms-type','ms-region'].forEach(msId => {
    document.querySelectorAll(`#${msId} input[type=checkbox]`).forEach(cb => { cb.checked = cb.value === 'all'; });
    updateMSLabel(msId);
  });
  document.getElementById('f-gov').value = 'all';"""

if OLD_RESET_HANDLER in html:
    html = html.replace(OLD_RESET_HANDLER, NEW_RESET_HANDLER, 1)
    print("JS: Reset updated for multi-select")
else:
    print("WARN: Reset handler not found")

# ══════════════════════════════════════════════════════════════════
# 7. REMOVE old select change listeners for f-round/f-type/f-region
# ══════════════════════════════════════════════════════════════════
OLD_CHANGE_LISTENERS = "['f-round','f-type','f-region','f-gov'].forEach(id =>\n  document.getElementById(id).addEventListener('change', render)\n);"
NEW_CHANGE_LISTENERS = """// f-gov still uses native select
document.getElementById('f-gov')?.addEventListener('change', render);"""

if OLD_CHANGE_LISTENERS in html:
    html = html.replace(OLD_CHANGE_LISTENERS, NEW_CHANGE_LISTENERS, 1)
    print("JS: old change listeners replaced")
else:
    print("WARN: change listeners not found")

# ══════════════════════════════════════════════════════════════════
# 8. ADD updateMap search logic - find map filter function and add search
# ══════════════════════════════════════════════════════════════════
OLD_MAP_FILTER = "    if (f.round !== 'all' && String(r.round) !== f.round) return false;\n    if (f.type  !== 'all' && r.outlet_type   !== f.type)  return false;"
NEW_MAP_FILTER = """    if (f.round !== 'all' && String(r.round) !== f.round) return false;
    if (f.type  !== 'all' && r.outlet_type   !== f.type)  return false;
    const mq = (document.getElementById('m-search')?.value||'').toLowerCase().trim();
    if (mq) {
      const code = String(r.outlet_code||r.code||'').toLowerCase();
      const name = String(r.outlet_name||r.name||'').toLowerCase();
      if (!code.includes(mq) && !name.includes(mq)) return false;
    }"""

if OLD_MAP_FILTER in html:
    html = html.replace(OLD_MAP_FILTER, NEW_MAP_FILTER, 1)
    print("JS: map search filter added to updateMap")
else:
    print("WARN: map filter conditions not found")

# ══════════════════════════════════════════════════════════════════
# 9. ADD multi-select JS functions (before closing </script>)
# ══════════════════════════════════════════════════════════════════
MS_JS = """
/* ── Multi-Select widget helpers ─────────────────────────────────────────── */
function toggleMS(id) {
  const wrap = document.getElementById(id);
  const isOpen = wrap.classList.contains('open');
  // Close all other open multi-selects
  document.querySelectorAll('.ms-wrap.open').forEach(w => w.classList.remove('open'));
  if (!isOpen) wrap.classList.add('open');
}

function updateMSLabel(id) {
  const allCb  = document.querySelector(`#${id} .all-opt input`);
  const opts   = [...document.querySelectorAll(`#${id} .ms-opt:not(.all-opt) input:checked`)];
  const lbl    = document.getElementById(`${id}-lbl`);
  const defaults = {'ms-round':'All Rounds','ms-type':'All Types','ms-region':'All Regions'};
  if (!lbl) return;
  if (allCb?.checked || opts.length === 0) {
    lbl.innerHTML = defaults[id] || 'All';
  } else if (opts.length <= 2) {
    lbl.innerHTML = opts.map(c => c.parentElement.textContent.trim()).join(', ');
  } else {
    lbl.innerHTML = `${opts.length} selected <span class="ms-badge">${opts.length}</span>`;
  }
}

function msAllToggle(id, cb) {
  if (cb.checked) {
    // Uncheck all individual options
    document.querySelectorAll(`#${id} .ms-opt:not(.all-opt) input`).forEach(c => c.checked = false);
  }
  updateMSLabel(id);
  render();
}

function msOptChange(id) {
  const allCb  = document.querySelector(`#${id} .all-opt input`);
  const anyChecked = [...document.querySelectorAll(`#${id} .ms-opt:not(.all-opt) input:checked`)].length > 0;
  // Uncheck "All" if any specific option is selected
  if (allCb) allCb.checked = !anyChecked;
  updateMSLabel(id);
  render();
}

// Close multi-selects when clicking outside
document.addEventListener('click', e => {
  if (!e.target.closest('.ms-wrap')) {
    document.querySelectorAll('.ms-wrap.open').forEach(w => w.classList.remove('open'));
  }
});
"""

# Insert before the last </script> tag
html = html.replace('</script>\n</body>', MS_JS + '\n</script>\n</body>', 1)
print("JS: multi-select helper functions added")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\nAll done!")
