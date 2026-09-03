with open('index.html', encoding='utf-8') as f:
    html = f.read()

import re

fixes = 0

# ── 1. Remove the Quarterly nav button ───────────────────────────────────────
OLD_NAV_BTN = """  <button class="tab-btn" data-tab="quarter" id="btn-tab-quarter">
    <span class="tab-icon">📅</span>Quarterly
  </button>"""
# Try variations
for pat in [
    '  <button class="tab-btn" data-tab="quarter" id="btn-tab-quarter">\n    <span class="tab-icon">📅</span>Quarterly\n  </button>',
    '<button class="tab-btn" data-tab="quarter" id="btn-tab-quarter">',
]:
    if pat in html:
        print(f"Found nav btn pattern")
        break

# Use regex to remove it
html2 = re.sub(
    r'\s*<button[^>]*data-tab="quarter"[^>]*>.*?</button>',
    '',
    html,
    flags=re.DOTALL
)
if html2 != html:
    html = html2
    fixes += 1
    print("HTML: Quarterly nav button removed")
else:
    print("WARN: Quarterly nav button not found via regex")

# ── 2. Remove the entire #tab-quarter panel ───────────────────────────────────
html2 = re.sub(
    r'<div class="tab-panel"[^>]*id="tab-quarter"[^>]*>.*?</div>\s*\n\s*<!-- MAP TAB',
    '\n  <!-- MAP TAB',
    html,
    flags=re.DOTALL
)
if html2 != html:
    html = html2
    fixes += 1
    print("HTML: #tab-quarter panel removed")
else:
    print("WARN: tab-quarter panel not found — trying alternate pattern")
    # Try ending with </div>\n\n  <!-- MAP
    html2 = re.sub(
        r'<div class="tab-panel"[^>]*id="tab-quarter".*?(?=<!-- MAP TAB -->)',
        '',
        html,
        flags=re.DOTALL
    )
    if html2 != html:
        html = html2
        fixes += 1
        print("HTML: #tab-quarter panel removed (alt)")

# ── 3. Remove Quarter tab JS blocks ──────────────────────────────────────────
# MONTH_TO_Q constant
html2 = re.sub(r'const MONTH_TO_Q\s*=\s*\{[^}]+\};', '', html)
if html2 != html:
    html = html2
    fixes += 1
    print("JS: MONTH_TO_Q removed")

# buildQuarterTab function
html2 = re.sub(r'function buildQuarterTab\(.*?\n\}(?=\s*\n)', '', html, flags=re.DOTALL)
if html2 != html:
    html = html2
    fixes += 1
    print("JS: buildQuarterTab() removed")

# quarterBuilt / activeQFilter variables and wiring
html2 = re.sub(
    r'// ── Quarter main tab.*?quarterBuilt = true;\s*\}\);',
    '',
    html,
    flags=re.DOTALL
)
if html2 != html:
    html = html2
    fixes += 1
    print("JS: Quarter tab wiring removed")

# ms-quarter handler in msOptChange
html2 = html.replace(
    """  } else if (id === 'ms-quarter') {
    const vals = getMSValues('ms-quarter');
    activeQFilter = vals;
    buildQuarterTab(ALL_DATA, activeQFilter);
    quarterBuilt = true;
  } else {""",
    "  } else {"
)
if html2 != html:
    html = html2
    fixes += 1
    print("JS: ms-quarter branch in msOptChange removed")

# ms-quarter handler in msAllToggle
html2 = html.replace(
    """  } else if (id === 'ms-quarter') {
    activeQFilter = 'all';
    buildQuarterTab(ALL_DATA, 'all');
    quarterBuilt = true;
  } else {""",
    "  } else {"
)
if html2 != html:
    html = html2
    fixes += 1
    print("JS: ms-quarter branch in msAllToggle removed")

# Remove ms-quarter from updateMSLabel defaults
html2 = html.replace(
    "\n    'ms-m-round':'All Rounds','ms-m-type':'All Types','ms-quarter':'All Quarters'",
    "\n    'ms-m-round':'All Rounds','ms-m-type':'All Types'"
)
if html2 != html:
    html = html2
    fixes += 1
    print("JS: ms-quarter removed from updateMSLabel defaults")

# Remove Quarter tab sticky CSS
html2 = re.sub(
    r',\s*\n\s*#tab-quarter \.filters-bar',
    '',
    html
)
if html2 != html:
    html = html2
    fixes += 1
    print("CSS: #tab-quarter sticky rule removed")

# Remove quarterly tab in sticky rule from visual upgrade CSS
html2 = html.replace(
    "// Quarter filter handled by ms-wrap msOptChange()",
    ""
)
html = html2

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes} — Done.")
