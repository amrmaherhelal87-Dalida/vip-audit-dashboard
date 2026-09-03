with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ── 1. ADD Quarter pill tabs to the filter bar (before Reset button) ───────────
OLD_RESET = '    <button id="btn-reset">\u21ba Reset</button>\n  </div>'

NEW_RESET = '''    <div class="filter-group" style="gap:4px;flex-direction:column">
      <label style="font-size:11px;margin-bottom:4px">Quarter</label>
      <div style="display:flex;gap:4px">
        <button class="q-pill active" data-q-filter="all">All</button>
        <button class="q-pill" data-q-filter="Q1">Q1</button>
        <button class="q-pill" data-q-filter="Q2">Q2</button>
        <button class="q-pill" data-q-filter="Q3">Q3</button>
        <button class="q-pill" data-q-filter="Q4">Q4</button>
      </div>
    </div>
    <button id="btn-reset">\u21ba Reset</button>
  </div>'''

if OLD_RESET in html:
    html = html.replace(OLD_RESET, NEW_RESET, 1)
    fixes += 1
    print("HTML: Quarter pills added to filter bar")
else:
    print("WARN: btn-reset target not found")

# ── 2. ADD CSS for q-pill buttons ─────────────────────────────────────────────
OLD_CSS_ANCHOR = '.tab-nav {'
NEW_CSS = '''.q-pill {
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
html = html.replace(OLD_CSS_ANCHOR, NEW_CSS + OLD_CSS_ANCHOR, 1)
fixes += 1
print("CSS: q-pill styles added")

# ── 3. ADD global quarter filter variable ──────────────────────────────────────
# Find applyFilters function and add quarter check
OLD_APPLY = "function applyFilters(data) {"
NEW_APPLY = "let globalQFilter = 'all';\n\nfunction applyFilters(data) {"
if OLD_APPLY in html:
    html = html.replace(OLD_APPLY, NEW_APPLY, 1)
    fixes += 1
    print("JS: globalQFilter var added")
else:
    print("WARN: applyFilters not found")

# ── 4. ADD quarter filter logic inside applyFilters ────────────────────────────
# Find the end of applyFilters - look for its return / filter chain
# Let's find what's inside applyFilters and add quarter filtering
OLD_APPLY_BODY = """function applyFilters(data) {
  const round  = document.getElementById('f-round').value;
  const type   = document.getElementById('f-type').value;
  const region = document.getElementById('f-region').value;
  const gov    = document.getElementById('f-gov').value;
  return data.filter(r => {
    if (round   !== 'all' && String(r.round)       !== round)  return false;
    if (type    !== 'all' && r.outlet_type          !== type)   return false;
    if (region  !== 'all' && r.region               !== region) return false;
    if (gov     !== 'all' && r.governorate          !== gov)    return false;
    return true;
  });
}"""

if OLD_APPLY_BODY in html:
    NEW_APPLY_BODY = """function applyFilters(data) {
  const round  = document.getElementById('f-round').value;
  const type   = document.getElementById('f-type').value;
  const region = document.getElementById('f-region').value;
  const gov    = document.getElementById('f-gov').value;
  return data.filter(r => {
    if (round   !== 'all' && String(r.round)       !== round)  return false;
    if (type    !== 'all' && r.outlet_type          !== type)   return false;
    if (region  !== 'all' && r.region               !== region) return false;
    if (gov     !== 'all' && r.governorate          !== gov)    return false;
    if (globalQFilter !== 'all') {
      const rq = (typeof MONTH_TO_Q !== 'undefined') ? (MONTH_TO_Q[r.month] || 'Unknown') : 'Unknown';
      if (rq !== globalQFilter) return false;
    }
    return true;
  });
}"""
    html = html.replace(OLD_APPLY_BODY, NEW_APPLY_BODY, 1)
    fixes += 1
    print("JS: quarter filter added to applyFilters")
else:
    print("WARN: applyFilters body not found - trying partial match")
    idx = html.find("function applyFilters(data)")
    print(repr(html[idx:idx+400]))

# ── 5. ADD event listeners for q-pill buttons ─────────────────────────────────
# Insert before the closing </script> of the second script block
OLD_SECOND_SCRIPT_END = """document.querySelectorAll('[data-q-tab]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-q-tab]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeQFilter = btn.dataset.qTab;
    buildQuarterTab(ALL_DATA, activeQFilter);
    quarterBuilt = true;
  });
});"""

NEW_SECOND_SCRIPT_END = """document.querySelectorAll('[data-q-tab]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('[data-q-tab]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeQFilter = btn.dataset.qTab;
    buildQuarterTab(ALL_DATA, activeQFilter);
    quarterBuilt = true;
  });
});

// ── Global Quarter pill filter (in main filter bar) ──────────────────────────
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

if OLD_SECOND_SCRIPT_END in html:
    html = html.replace(OLD_SECOND_SCRIPT_END, NEW_SECOND_SCRIPT_END, 1)
    fixes += 1
    print("JS: q-pill event listeners wired")
else:
    print("WARN: q-tab listener block not found")

# ── 6. ALSO reset globalQFilter when Reset button is clicked ──────────────────
OLD_RESET_JS = "['f-round','f-type','f-region','f-gov'].forEach(id => document.getElementById(id).value = 'all');\n  render();"
NEW_RESET_JS = "['f-round','f-type','f-region','f-gov'].forEach(id => document.getElementById(id).value = 'all');\n  globalQFilter = 'all';\n  document.querySelectorAll('[data-q-filter]').forEach(b => b.classList.toggle('active', b.dataset.qFilter === 'all'));\n  render();"
if OLD_RESET_JS in html:
    html = html.replace(OLD_RESET_JS, NEW_RESET_JS, 1)
    fixes += 1
    print("JS: Reset also clears quarter filter")
else:
    print("WARN: Reset JS not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes}  — Done.")
