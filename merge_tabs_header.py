with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ══════════════════════════════════════════════════════════════════
# 1. RENAME title
# ══════════════════════════════════════════════════════════════════
html = html.replace(
    '<h1>VIP Audit Dashboard</h1>\n        <span>Red Bull Egypt Field Compliance</span>',
    '<h1>Red Bull Egypt VIP Audit Dashboard</h1>'
)
# Also update browser tab title
html = html.replace(
    '<title>VIP Audit Dashboard — Q2 2026</title>',
    '<title>Red Bull Egypt VIP Audit Dashboard</title>'
)
fixes += 1
print("HTML: Title renamed")

# ══════════════════════════════════════════════════════════════════
# 2. MOVE tab buttons INTO header (between logo-area and header-meta)
#    and REMOVE the separate <nav class="tab-nav">
# ══════════════════════════════════════════════════════════════════

# Insert tab buttons into header before header-meta
OLD_HEADER_META = '    <div class="header-meta">'
NEW_HEADER_META = '''    <!-- Tabs embedded in header -->
    <nav class="header-tabs" id="tab-nav">
      <button class="tab-btn active" data-tab="overview" id="btn-tab-overview">
        <span class="tab-icon">📊</span> Overview
      </button>
      <button class="tab-btn" data-tab="map" id="btn-tab-map">
        <span class="tab-icon">🗺</span> Interactive Map
      </button>
    </nav>
    <div class="header-meta">'''

if OLD_HEADER_META in html:
    html = html.replace(OLD_HEADER_META, NEW_HEADER_META, 1)
    fixes += 1
    print("HTML: Tabs moved into header")

# Remove the old standalone <nav class="tab-nav">
OLD_NAV = '''\n<!-- Tab Navigation -->\n<nav class="tab-nav" id="tab-nav">\n  <button class="tab-btn active" data-tab="overview" id="btn-tab-overview">\n    <span class="tab-icon">📊</span> Overview\n  </button>\n  <button class="tab-btn" data-tab="map" id="btn-tab-map">\n    <span class="tab-icon">🗺</span> Interactive Map\n  </button>\n</nav>'''
if OLD_NAV in html:
    html = html.replace(OLD_NAV, '', 1)
    fixes += 1
    print("HTML: Old standalone nav removed")
else:
    # Try alternate whitespace
    import re
    html2 = re.sub(
        r'\n<!-- Tab Navigation -->\n<nav class="tab-nav"[^>]*>.*?</nav>',
        '', html, flags=re.DOTALL
    )
    if html2 != html:
        html = html2
        fixes += 1
        print("HTML: Old standalone nav removed (regex)")
    else:
        print("WARN: Old nav not found")

# ══════════════════════════════════════════════════════════════════
# 3. UPDATE CSS — replace tab-nav styles with header-tabs styles
#    and fix sticky filter top from 117px → header height (~72px)
# ══════════════════════════════════════════════════════════════════

HEADER_TABS_CSS = """
    /* ── Header tabs (embedded in header bar) ── */
    .header-tabs {
      display: flex;
      align-items: stretch;
      gap: 0;
      margin: 0 auto;
      height: 100%;
    }
    .header-tabs .tab-btn {
      position: relative;
      padding: 0 22px;
      background: none;
      border: none;
      color: rgba(255,255,255,0.55);
      font-size: 13px;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      transition: color .2s;
      display: flex; align-items: center; gap: 6px;
      white-space: nowrap;
      border-bottom: 3px solid transparent;
      letter-spacing: .3px;
    }
    .header-tabs .tab-btn:hover { color: rgba(255,255,255,0.85); }
    .header-tabs .tab-btn.active {
      color: #fff;
      border-bottom-color: var(--red);
    }
    .header-tabs .tab-btn .tab-icon { font-size: 15px; }

    @media (max-width: 640px) {
      .header-tabs { margin: 0; gap: 0; order: 3; width: 100%; border-top: 1px solid rgba(255,255,255,0.06); }
      .header-tabs .tab-btn { padding: 10px 16px; font-size: 12px; flex: 1; justify-content: center; border-bottom: 3px solid transparent; }
      .header-inner { flex-wrap: wrap; height: auto; padding: 10px 0; }
    }
"""

# Replace the old .tab-nav CSS block
import re
html2 = re.sub(
    r'/\* ── Tab nav ──.*?\}\s*(?=\n\s*\.tab-btn\.active)',
    '',
    html, flags=re.DOTALL
)
# More targeted: find and replace .tab-nav { block
html2 = re.sub(
    r'\.tab-nav\s*\{[^}]+\}',
    '.header-tabs { display:flex; align-items:stretch; }',
    html, count=1
)
if html2 != html:
    html = html2
    print("CSS: .tab-nav block replaced")

# Insert our new CSS before </style>
html = html.replace('</style>', HEADER_TABS_CSS + '\n    </style>', 1)
fixes += 1
print("CSS: header-tabs styles added")

# ══════════════════════════════════════════════════════════════════
# 4. FIX sticky filter top — was 117px (header+tab-nav), now 68px (header only)
# ══════════════════════════════════════════════════════════════════
html = html.replace('top: 117px;', 'top: 68px;')
html = html.replace('top: 117px !important;', 'top: 68px !important;')
html = html.replace('top: 46px !important;', 'top: 62px !important;')  # mobile fix
fixes += 1
print("CSS: Sticky filter top updated (117px → 68px)")

# ══════════════════════════════════════════════════════════════════
# 5. FIX header height — make slightly taller to fit tabs inline
# ══════════════════════════════════════════════════════════════════
html = html.replace('height: 68px;', 'height: 68px; min-height: 68px;', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes} — Done.")
print(f"File lines: {len(html.splitlines())}")
