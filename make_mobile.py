import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ══════════════════════════════════════════════════════════════════
# 1. REMOVE light theme CSS block
# ══════════════════════════════════════════════════════════════════
html2 = re.sub(
    r'/\* ════+\s*RED BULL LIGHT THEME.*?(?=\s*/\* ── Theme toggle button)',
    '',
    html, flags=re.DOTALL
)
if html2 != html:
    html = html2; fixes += 1; print("CSS: Light theme block removed")
else:
    print("WARN: Light theme block not found via regex")

# ══════════════════════════════════════════════════════════════════
# 2. REMOVE theme toggle button from header HTML
# ══════════════════════════════════════════════════════════════════
html2 = html.replace(
    """<div class="header-meta">
        <button id="theme-toggle" onclick="toggleTheme()" title="Switch theme">
          <span id="theme-icon">☀️</span>
          <span id="theme-label">Light</span>
        </button>""",
    '<div class="header-meta">'
)
if html2 != html:
    html = html2; fixes += 1; print("HTML: Theme toggle button removed")
else:
    print("WARN: Theme toggle button not found")

# ══════════════════════════════════════════════════════════════════
# 3. REMOVE theme JS block
# ══════════════════════════════════════════════════════════════════
html2 = re.sub(
    r'/\* ── Theme Switcher ─+\s*\*/.*?(?=\n</script>)',
    '',
    html, flags=re.DOTALL
)
if html2 != html:
    html = html2; fixes += 1; print("JS: Theme switcher functions removed")
else:
    print("WARN: Theme switcher JS not found")

# ══════════════════════════════════════════════════════════════════
# 4. REMOVE init() theme patch
# ══════════════════════════════════════════════════════════════════
html2 = html.replace(
    """  // Apply chart theme colors after initial render
  const savedTheme = localStorage.getItem('vip-theme') || 'dark';
  if (savedTheme === 'light') setTimeout(() => updateChartTheme('light'), 100);""",
    ''
)
if html2 != html:
    html = html2; fixes += 1; print("JS: init() theme patch removed")

# ══════════════════════════════════════════════════════════════════
# 5. ADD comprehensive mobile-responsive CSS before </style>
# ══════════════════════════════════════════════════════════════════
MOBILE_CSS = """
    /* ════════════════════════════════════════════════════
       MOBILE RESPONSIVE — Dark Theme
    ════════════════════════════════════════════════════ */

    /* ── Base touch improvements ── */
    * { -webkit-tap-highlight-color: transparent; }
    input, select, button { touch-action: manipulation; }

    /* ── Header mobile ── */
    @media (max-width: 640px) {
      header { padding: 0 16px; }
      .header-inner { height: auto; padding: 10px 0; flex-wrap: wrap; gap: 8px; }
      .rb-logo-img { height: 36px; }
      .logo-area h1 { font-size: 13px; }
      .logo-area span { font-size: 11px; }
      .logo-divider { height: 28px; }
      .adhoc-logo-img { height: 24px; }
      .header-meta { gap: 6px; flex-wrap: wrap; }
      .badge { font-size: 10px; padding: 3px 8px; }
      #last-updated { font-size: 10px; }
    }

    /* ── Tab nav mobile — horizontally scrollable ── */
    @media (max-width: 640px) {
      .tab-nav {
        padding: 0 12px;
        gap: 0;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
        top: 0 !important;   /* below header, header scrolls away on mobile */
        position: sticky;
      }
      .tab-nav::-webkit-scrollbar { display: none; }
      .tab-btn { padding: 12px 14px; font-size: 12px; white-space: nowrap; flex-shrink: 0; }
      .tab-icon { margin-right: 4px; }
    }

    /* ── Main padding ── */
    @media (max-width: 640px) {
      main { padding: 12px 12px 48px; }
    }

    /* ── Sticky filter bar mobile ── */
    @media (max-width: 640px) {
      #tab-overview > .filters-bar,
      #tab-map .filters-bar { top: 46px !important; }
    }

    /* ── Filter bar mobile ── */
    @media (max-width: 768px) {
      .filters-bar { padding: 12px 14px; gap: 8px; }
      .filter-group { width: 100%; }
      .ms-wrap, .ms-display { width: 100%; }
      .filters-bar select { width: 100%; }
      .ms-panel { width: 100%; left: 0; right: 0; }
      #btn-reset, #btn-export { font-size: 12px; padding: 7px 12px; }
      .export-wrap { width: 100%; }
      #btn-export { width: 100%; justify-content: center; }
      .export-menu { width: 100%; right: 0; left: 0; }
    }

    /* ── KPI cards — 2 col on mobile ── */
    @media (max-width: 640px) {
      .kpi-grid {
        grid-template-columns: 1fr 1fr !important;
        gap: 10px;
      }
      .kpi-card { padding: 14px 14px; }
      .kpi-value { font-size: 24px !important; }
      .kpi-icon { width: 34px !important; height: 34px !important; font-size: 15px !important; margin-bottom: 10px; }
      .kpi-label { font-size: 11px; }
      .kpi-sub { font-size: 10px; }
    }

    /* ── Chart grid — 1 col on mobile ── */
    @media (max-width: 768px) {
      .charts-grid { grid-template-columns: 1fr !important; gap: 12px; }
      .chart-wide { grid-column: auto; }
      .chart-card { padding: 14px 14px; }
      .chart-title { font-size: 13px !important; }
      .chart-subtitle { font-size: 11px; }
      .chart-header { flex-wrap: wrap; gap: 8px; }
      .chart-tabs { flex-wrap: wrap; gap: 6px; }
      .chart-tab-btn { font-size: 11px; padding: 5px 10px; }
    }

    /* ── Table mobile — horizontal scroll ── */
    @media (max-width: 768px) {
      .table-card { padding: 14px 0 0; }
      .table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
      #data-table { min-width: 700px; }
      #data-table th, #data-table td { font-size: 11px; padding: 8px 10px; }
      .chart-header { padding: 0 14px 12px; }
      #outlet-search { width: 100% !important; }
    }

    /* ── Section labels mobile ── */
    @media (max-width: 640px) {
      .section-label { font-size: 10px; margin-top: 24px; margin-bottom: 10px; }
    }

    /* ── Contract type tabs mobile ── */
    @media (max-width: 640px) {
      .kpi-contract-tabs { flex-wrap: wrap; gap: 6px; }
      .chart-tab-btn { flex: 1 1 40%; text-align: center; }
    }

    /* ── Map mobile ── */
    @media (max-width: 768px) {
      #map { height: 55vh !important; min-height: 300px; }
      .map-legend { font-size: 11px !important; padding: 8px 10px !important; right: 8px !important; top: 8px !important; }
    }

    /* ── Multi-select panel z-index on mobile ── */
    @media (max-width: 768px) {
      .ms-panel { z-index: 9999 !important; }
    }

    /* ── Export menu mobile ── */
    @media (max-width: 768px) {
      .export-menu { left: auto; right: 0; }
    }

    /* ── KPI deep dive canvas height ── */
    @media (max-width: 640px) {
      .charts-grid canvas { max-height: 260px; }
    }

    /* ── Filter action row wraps on mobile ── */
    @media (max-width: 768px) {
      .filters-bar > div:last-child {
        width: 100%;
        justify-content: space-between;
      }
    }
"""

html = html.replace('</style>', MOBILE_CSS + '\n    </style>', 1)
fixes += 1
print("CSS: Mobile responsive styles added")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes applied: {fixes}")
print("Done.")
