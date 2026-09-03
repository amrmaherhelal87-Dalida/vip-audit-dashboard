with open('index.html', encoding='utf-8') as f:
    html = f.read()

fixes = 0

# ══════════════════════════════════════════════════════════════════
# 1. ADD [data-theme="light"] CSS variables + overrides
# ══════════════════════════════════════════════════════════════════
LIGHT_THEME_CSS = """
    /* ════════════════════════════════════════
       RED BULL LIGHT THEME  (redbull.com style)
    ════════════════════════════════════════ */
    [data-theme="light"] {
      --bg:        #f4f6f9;
      --bg2:       #ffffff;
      --surface:   #ffffff;
      --surface2:  #f1f5f9;
      --border:    rgba(0,0,0,0.09);
      --red:       #e8001c;
      --red-glow:  rgba(232,0,28,0.2);
      --gold:      #c8920e;
      --gold-dim:  rgba(200,146,14,0.12);
      --blue:      #2563eb;
      --green:     #059669;
      --purple:    #7c3aed;
      --text:      #111827;
      --muted:     #6b7280;
      --radius:    14px;
    }

    /* Body light bg */
    [data-theme="light"] body {
      background-color: #f4f6f9;
      background-image:
        radial-gradient(ellipse 60% 40% at 8% 0%, rgba(232,0,28,0.05) 0%, transparent 70%),
        radial-gradient(rgba(0,0,0,0.025) 1px, transparent 1px);
      background-size: auto, 28px 28px;
      color: #111827;
    }

    /* Header */
    [data-theme="light"] header {
      background: #ffffff !important;
      border-bottom: 3px solid var(--red) !important;
      box-shadow: 0 2px 16px rgba(0,0,0,0.08) !important;
    }
    [data-theme="light"] .logo-area h1 { color: #111827; }
    [data-theme="light"] .logo-area span { color: #6b7280; }

    /* Tab nav */
    [data-theme="light"] .tab-nav {
      background: #ffffff;
      border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    [data-theme="light"] .tab-btn { color: #6b7280; }
    [data-theme="light"] .tab-btn:hover { color: #111827; }
    [data-theme="light"] .tab-btn.active { color: #111827; font-weight: 700; }

    /* Filter bar */
    [data-theme="light"] .filters-bar {
      background: #ffffff !important;
      border: 1px solid rgba(0,0,0,0.09) !important;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    }
    [data-theme="light"] #tab-map .filters-bar {
      background: rgba(255,255,255,0.97) !important;
      border: 1px solid rgba(0,0,0,0.1) !important;
    }
    [data-theme="light"] .filters-bar label { color: #6b7280; }
    [data-theme="light"] .filters-bar select,
    [data-theme="light"] .ms-display {
      background: #f8fafc !important;
      border: 1px solid rgba(0,0,0,0.12) !important;
      color: #111827 !important;
    }
    [data-theme="light"] .ms-panel {
      background: #ffffff;
      border: 1px solid rgba(0,0,0,0.12);
      box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    }
    [data-theme="light"] .ms-opt { color: #6b7280; }
    [data-theme="light"] .ms-opt:hover { background: rgba(0,0,0,0.04); color: #111827; }
    [data-theme="light"] .ms-opt.all-opt { border-bottom: 1px solid rgba(0,0,0,0.08); }

    /* KPI Cards */
    [data-theme="light"] .kpi-card {
      background: #ffffff;
      border: 1px solid rgba(0,0,0,0.08);
      box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    }
    [data-theme="light"] .kpi-label { color: #6b7280; }
    [data-theme="light"] .kpi-sub   { color: #9ca3af; }
    [data-theme="light"] .kpi-stat-bar-bg { background: rgba(0,0,0,0.06); }

    /* Chart cards */
    [data-theme="light"] .chart-card {
      background: #ffffff;
      border: 1px solid rgba(0,0,0,0.08);
      box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    }
    [data-theme="light"] .chart-card:hover {
      box-shadow: 0 6px 24px rgba(0,0,0,0.12), 0 0 0 1px rgba(232,0,28,0.1);
    }
    [data-theme="light"] .chart-title { color: #111827 !important; }
    [data-theme="light"] .chart-subtitle { color: #6b7280; }

    /* Section labels */
    [data-theme="light"] .section-label {
      background: linear-gradient(90deg, var(--red) 0%, #c8920e 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      border-left: 3px solid var(--red);
    }

    /* Chart tab buttons */
    [data-theme="light"] .chart-tab-btn {
      border: 1px solid rgba(0,0,0,0.12);
      color: #6b7280;
    }
    [data-theme="light"] .chart-tab-btn:hover { color: #111827; }
    [data-theme="light"] .chart-tab-btn.active {
      background: var(--red);
      border-color: var(--red);
      color: #fff;
    }

    /* Table */
    [data-theme="light"] .table-card {
      background: #ffffff;
      border: 1px solid rgba(0,0,0,0.08);
      box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    }
    [data-theme="light"] #data-table thead th {
      background: #e8001c;
      color: #ffffff;
      border-bottom: none;
    }
    [data-theme="light"] #data-table tbody td { color: #374151; }
    [data-theme="light"] #data-table tbody tr { border-bottom: 1px solid rgba(0,0,0,0.05); }
    [data-theme="light"] #data-table tbody tr:hover { background: rgba(232,0,28,0.04); }
    [data-theme="light"] #data-table tbody tr:nth-child(even) { background: #f9fafb; }
    [data-theme="light"] #data-table tbody tr:nth-child(even):hover { background: rgba(232,0,28,0.04); }

    /* Table scroll */
    [data-theme="light"] .table-scroll { border-top: 1px solid rgba(0,0,0,0.08); }

    /* Buttons */
    [data-theme="light"] #btn-reset {
      background: transparent;
      border: 1px solid rgba(232,0,28,0.3);
      color: var(--red);
    }
    [data-theme="light"] #btn-reset:hover {
      background: rgba(232,0,28,0.06);
    }

    /* Badges */
    [data-theme="light"] .badge-red  { background: rgba(232,0,28,.1); }
    [data-theme="light"] .badge-gold { background: rgba(200,146,14,.1); }

    /* Outlet search */
    [data-theme="light"] #outlet-search, [data-theme="light"] #m-search {
      background: #f8fafc;
      border: 1px solid rgba(0,0,0,0.12);
      color: #111827;
    }

    /* Scrollbar */
    [data-theme="light"] ::-webkit-scrollbar-track { background: #f1f5f9; }
    [data-theme="light"] ::-webkit-scrollbar-thumb { background: rgba(232,0,28,0.3); }

    /* Legend & map popups */
    [data-theme="light"] .map-legend {
      background: #ffffff !important;
      border: 1px solid rgba(0,0,0,0.1) !important;
      color: #374151 !important;
    }
    [data-theme="light"] .leaflet-popup-content-wrapper {
      background: #ffffff !important;
      color: #111827 !important;
    }

    /* Theme toggle button */
    #theme-toggle {
      background: transparent;
      border: 1px solid rgba(255,255,255,0.2);
      color: #e2e8f0;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
      transition: all .2s;
      display: flex; align-items: center; gap: 6px;
    }
    #theme-toggle:hover {
      border-color: rgba(232,0,28,.5);
      color: #fff;
      background: rgba(232,0,28,.1);
    }
    [data-theme="light"] #theme-toggle {
      border: 1px solid rgba(0,0,0,0.15);
      color: #374151;
    }
    [data-theme="light"] #theme-toggle:hover {
      border-color: var(--red);
      color: var(--red);
      background: rgba(232,0,28,.05);
    }
"""

# Insert before </style>
html = html.replace('</style>', LIGHT_THEME_CSS + '\n    </style>', 1)
fixes += 1
print("CSS: Light theme variables added")

# ══════════════════════════════════════════════════════════════════
# 2. ADD theme toggle button to header
# ══════════════════════════════════════════════════════════════════
OLD_HEADER_META = '<div class="header-meta">'
NEW_HEADER_META = '''<div class="header-meta">
        <button id="theme-toggle" onclick="toggleTheme()" title="Switch theme">
          <span id="theme-icon">☀️</span>
          <span id="theme-label">Light</span>
        </button>'''

if OLD_HEADER_META in html:
    html = html.replace(OLD_HEADER_META, NEW_HEADER_META, 1)
    fixes += 1
    print("HTML: Theme toggle button added to header")
else:
    print("WARN: header-meta not found")

# ══════════════════════════════════════════════════════════════════
# 3. ADD theme JS: toggle + localStorage + chart color updates
# ══════════════════════════════════════════════════════════════════
THEME_JS = """
/* ── Theme Switcher ─────────────────────────────────────────────────────────── */
(function initTheme() {
  const saved = localStorage.getItem('vip-theme') || 'dark';
  applyTheme(saved);
})();

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('vip-theme', theme);
  const icon  = document.getElementById('theme-icon');
  const label = document.getElementById('theme-label');
  if (theme === 'light') {
    if (icon)  icon.textContent  = '🌙';
    if (label) label.textContent = 'Dark';
  } else {
    if (icon)  icon.textContent  = '☀️';
    if (label) label.textContent = 'Light';
  }
  // Update all charts for new theme colors
  updateChartTheme(theme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'dark';
  applyTheme(current === 'dark' ? 'light' : 'dark');
}

function updateChartTheme(theme) {
  const isLight = theme === 'light';
  const textColor  = isLight ? '#374151' : '#94a3b8';
  const gridColor  = isLight ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.05)';
  const legendColor= isLight ? '#374151' : '#94a3b8';

  // Update Chart.js global defaults
  if (typeof Chart !== 'undefined') {
    Chart.defaults.color = textColor;
    Chart.defaults.borderColor = gridColor;

    // Re-apply to all active charts
    Object.values(charts || {}).forEach(ch => {
      if (!ch || !ch.options) return;
      try {
        // Scales
        ['x','y','yLeft','yRight','y2'].forEach(axis => {
          const sc = ch.options.scales?.[axis];
          if (!sc) return;
          if (sc.ticks) sc.ticks.color = textColor;
          if (sc.grid)  sc.grid.color  = gridColor;
          if (sc.title) sc.title.color  = textColor;
        });
        // Legend
        if (ch.options.plugins?.legend?.labels)
          ch.options.plugins.legend.labels.color = legendColor;
        ch.update('none');
      } catch(e) { /* skip */ }
    });
  }
}
"""

html = html.replace('</script>\n</body>', THEME_JS + '\n</script>\n</body>', 1)
fixes += 1
print("JS: Theme switcher functions added")

# ══════════════════════════════════════════════════════════════════
# 4. Also call updateChartTheme after render() so new charts get right colors
# ══════════════════════════════════════════════════════════════════
OLD_RENDER_END = "function render() {"
# Find render function end — add updateChartTheme call after charts are built
# Better approach: wrap the render call
OLD_RENDER_CALL = "render();\n    quarterBuilt = false;"

# Find the init() final render call and patch it
OLD_INIT_RENDER = "  render();\n}"
NEW_INIT_RENDER = """  render();
  // Apply chart theme colors after initial render
  const savedTheme = localStorage.getItem('vip-theme') || 'dark';
  if (savedTheme === 'light') setTimeout(() => updateChartTheme('light'), 100);
}"""

if OLD_INIT_RENDER in html:
    html = html.replace(OLD_INIT_RENDER, NEW_INIT_RENDER, 1)
    fixes += 1
    print("JS: init() patches chart theme on load")
else:
    print("WARN: init render end not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nTotal fixes: {fixes} — Done.")
