with open('index.html', encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════════════════
# TASK 1: Hide # column
# ══════════════════════════════════════════════════════════════════
# Remove <th> header
html = html.replace(
    "            <th data-col=\"serial\">#</th>\r\n             <th data-col=\"round\">Round</th>",
    "            <th data-col=\"round\">Round</th>"
)
html = html.replace(
    "<th data-col=\"serial\">#</th>\n             <th data-col=\"round\">Round</th>",
    "<th data-col=\"round\">Round</th>"
)
# Use a marker approach for the <td>
idx = html.find("r.serial||'?'")
if idx == -1:
    idx = html.find('r.serial||\'?\'')
if idx != -1:
    # Find the start of the <td> before this
    td_start = html.rfind('<td', 0, idx)
    td_end   = html.find('</td>', idx) + 5
    html = html[:td_start] + html[td_end:]
    print("TASK 1: serial <td> removed")
else:
    # Try: r.serial||'—'
    idx = html.find("r.serial||'\\u2014'")
    if idx == -1:
        idx = html.find("r.serial||'—'")
    if idx != -1:
        td_start = html.rfind('<td', 0, idx)
        td_end   = html.find('</td>', idx) + 5
        html = html[:td_start] + html[td_end:]
        print("TASK 1: serial <td> removed (em-dash variant)")
    else:
        print("WARN: serial td not found")

print("TASK 1: # column removal done")

# ══════════════════════════════════════════════════════════════════
# TASK 2 CSS
# ══════════════════════════════════════════════════════════════════
REFINE_CSS = """
    /* ── Table Refine Panel ── */
    #refine-wrapper { position: relative; }
    #refine-toggle {
      padding: 6px 11px; border-radius: 8px; border: 1px solid var(--border);
      background: var(--surface); color: var(--muted); cursor: pointer;
      font-size: 14px; transition: all .2s; white-space: nowrap;
    }
    #refine-toggle:hover, #refine-toggle.active { border-color: var(--red); color: var(--red); }
    #refine-panel {
      display: none; position: absolute; top: calc(100% + 8px); right: 0; z-index: 600;
      background: var(--surface); border: 1px solid var(--border); border-radius: 12px;
      padding: 16px 18px; min-width: 270px; box-shadow: 0 8px 32px rgba(0,0,0,.6);
    }
    #refine-panel.open { display: block; }
    .rp-title { font-size: 10px; font-weight: 700; letter-spacing: 1px;
      text-transform: uppercase; color: var(--muted); margin-bottom: 8px; }
    .rp-btns  { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
    .rp-btns:last-child { margin-bottom: 0; }
    .rp-btn {
      padding: 4px 12px; border-radius: 20px; border: 1px solid var(--border);
      background: transparent; color: var(--muted); font-size: 11px; font-weight: 600;
      cursor: pointer; font-family: inherit; transition: all .15s;
    }
    .rp-btn:hover  { border-color: var(--red); color: var(--text); }
    .rp-btn.active { background: var(--red); border-color: var(--red); color: #fff; }
"""
html = html.replace('</style>', REFINE_CSS + '\n    </style>', 1)
print("TASK 2: CSS added")

# ══════════════════════════════════════════════════════════════════
# TASK 2 HTML — replace search bar area
# ══════════════════════════════════════════════════════════════════
OLD_SEARCH_DIV = '      <div style="display:flex;align-items:center;gap:8px">'
# Find the full search wrapper block
start = html.find(OLD_SEARCH_DIV)
end   = html.find('</div>', start) + 6  # closing div of the flex wrapper

if start != -1:
    NEW_SEARCH_DIV = """      <div style="display:flex;align-items:center;gap:8px">
        <input type="text" id="outlet-search"
          placeholder="🔍  Search by code or name…"
          oninput="renderTable(applyFilters(ALL_DATA))">
        <button id="outlet-search-clear" title="Clear search"
          style="padding:6px 10px;border-radius:8px;border:1px solid var(--border);
                 background:var(--surface);color:var(--muted);cursor:pointer;font-size:13px">✕</button>
        <div id="refine-wrapper">
          <button id="refine-toggle" title="Refine / advanced filters" onclick="toggleRefinePanel()">🎛</button>
          <div id="refine-panel">
            <div class="rp-title">Score Level</div>
            <div class="rp-btns">
              <button class="rp-btn active" data-rs="all"  onclick="setRP('score',this,'all')">All</button>
              <button class="rp-btn"        data-rs="low"  onclick="setRP('score',this,'low')">🔴 &lt;50%</button>
              <button class="rp-btn"        data-rs="mid"  onclick="setRP('score',this,'mid')">🟡 50–70%</button>
              <button class="rp-btn"        data-rs="high" onclick="setRP('score',this,'high')">🟢 ≥70%</button>
            </div>
            <div class="rp-title">Incentive</div>
            <div class="rp-btns">
              <button class="rp-btn active" data-ri="all" onclick="setRP('inc',this,'all')">All</button>
              <button class="rp-btn"        data-ri="yes" onclick="setRP('inc',this,'yes')">✅ Has Incentive</button>
              <button class="rp-btn"        data-ri="no"  onclick="setRP('inc',this,'no')">✗ No Incentive</button>
            </div>
            <div class="rp-title">Availability</div>
            <div class="rp-btns" style="margin-bottom:0">
              <button class="rp-btn active" data-ra="all"  onclick="setRP('avail',this,'all')">All</button>
              <button class="rp-btn"        data-ra="pass" onclick="setRP('avail',this,'pass')">✓ Compliant</button>
              <button class="rp-btn"        data-ra="fail" onclick="setRP('avail',this,'fail')">✗ Non-Compliant</button>
            </div>
          </div>
        </div>
      </div>"""
    html = html[:start] + NEW_SEARCH_DIV + html[end:]
    print("TASK 2: Refine button+panel HTML inserted")
else:
    print("WARN: search div not found")

# ══════════════════════════════════════════════════════════════════
# TASK 2 JS
# ══════════════════════════════════════════════════════════════════
REFINE_JS = """
/* ═══════════════════════════════════════════════
   TABLE REFINE FILTERS
═══════════════════════════════════════════════ */
let rpScore = 'all', rpInc = 'all', rpAvail = 'all';

function toggleRefinePanel() {
  const panel = document.getElementById('refine-panel');
  const btn   = document.getElementById('refine-toggle');
  panel.classList.toggle('open');
  btn.classList.toggle('active');
}
document.addEventListener('click', function(e) {
  const w = document.getElementById('refine-wrapper');
  if (w && !w.contains(e.target)) {
    document.getElementById('refine-panel')?.classList.remove('open');
    document.getElementById('refine-toggle')?.classList.remove('active');
  }
});
function setRP(type, btn, val) {
  if (type === 'score') {
    rpScore = val;
    document.querySelectorAll('[data-rs]').forEach(b => b.classList.remove('active'));
  } else if (type === 'inc') {
    rpInc = val;
    document.querySelectorAll('[data-ri]').forEach(b => b.classList.remove('active'));
  } else {
    rpAvail = val;
    document.querySelectorAll('[data-ra]').forEach(b => b.classList.remove('active'));
  }
  btn.classList.add('active');
  renderTable(applyFilters(ALL_DATA));
  // Show count badge on toggle button
  const active = [rpScore, rpInc, rpAvail].filter(v => v !== 'all').length;
  const t = document.getElementById('refine-toggle');
  if (t) t.textContent = active > 0 ? '🎛 ' + active : '🎛';
}
function applyRefineFilters(data) {
  let d = data;
  if (rpScore === 'low')  d = d.filter(r => typeof r.overall_score === 'number' && r.overall_score < 0.5);
  if (rpScore === 'mid')  d = d.filter(r => typeof r.overall_score === 'number' && r.overall_score >= 0.5 && r.overall_score < 0.7);
  if (rpScore === 'high') d = d.filter(r => typeof r.overall_score === 'number' && r.overall_score >= 0.7);
  if (rpInc   === 'yes')  d = d.filter(r => typeof r.total_incentive === 'number' && r.total_incentive > 0);
  if (rpInc   === 'no')   d = d.filter(r => !(typeof r.total_incentive === 'number' && r.total_incentive > 0));
  if (rpAvail === 'pass') d = d.filter(r => r.avail_compliance === 1);
  if (rpAvail === 'fail') d = d.filter(r => r.avail_compliance === 0);
  return d;
}
"""

# Insert before last </script>
last_script_end = html.rfind('</script>')
html = html[:last_script_end] + REFINE_JS + '\n' + html[last_script_end:]
print("TASK 2: Refine JS inserted")

# Hook applyRefineFilters into renderTable
HOOK_OLD = "  const searchQ = (document.getElementById('outlet-search')?.value || '').toLowerCase().trim();"
HOOK_NEW = "  if (typeof applyRefineFilters === 'function') data = applyRefineFilters(data);\n  const searchQ = (document.getElementById('outlet-search')?.value || '').toLowerCase().trim();"
if HOOK_OLD in html:
    html = html.replace(HOOK_OLD, HOOK_NEW, 1)
    print("TASK 2: applyRefineFilters hooked into renderTable")
else:
    print("WARN: renderTable hook target not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

import re
has_serial_th = bool(re.search(r'<th[^>]*data-col="serial"', html))
has_serial_td = "r.serial" in html
print(f"\n# column TH still present: {has_serial_th}")
print(f"serial TD still present:   {has_serial_td}")
print(f"Refine panel present:      {'refine-panel' in html}")
print(f"File lines: {len(html.splitlines())}")
